from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import EncryptedType
from cryptography.fernet import Fernet
from utils import ShipayEncryptDecrypt

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/shipaypoc.db'
secret_key = 'shipaypoctest'


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)

    def __init__(self, **kwargs):
        shipayencdec = ShipayEncryptDecrypt()
        self.username = shipayencdec.encrypt(kwargs['username'])
        self.email = shipayencdec.encrypt(kwargs['email'])

    def __repr__(self):
        return '<Person %r>' % self.username

    @property
    def to_dict(self):
        shipayencdec = ShipayEncryptDecrypt()

        return dict(
            id=self.id,
            username=shipayencdec.decrypt(self.username),
            email=shipayencdec.decrypt(self.email)
        )


@app.route('/person', methods=['GET', 'POST'])
def get_person():
    if request.method == 'POST':

        new_person = dict(
            username=request.get_json()['username'],
            email=request.get_json()['email']
        )

        person = Person(**new_person)

        db.session.add(person)
        db.session.commit()
        return jsonify(data=person.to_dict)

    person = Person.query.first()

    return jsonify(data=person.to_dict)
