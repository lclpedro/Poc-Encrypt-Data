from cryptography.fernet import Fernet

'''
Podemos ter duas possibilidades, uma passando por aquivo ou por variável de ambiente

A chave do Fernet deve ser uma chave auto gerada por ele usando ou usando uma chave de 32b
Fernet.generate_key()
'''


class ShipayEncryptDecrypt():

    def __init__(self):
        key = self.get_secret_key()
        self.fernet = Fernet(key.encode())

    def get_secret_key(self):
        return 'W9dUcE1TzGtCZ4LF0idAxVzWBbUrarUuH4seg-0rTHE='

    def encrypt(self, data):
        encode_data = data.encode()
        return self.fernet.encrypt(encode_data).decode()

    def decrypt(self, data):
        data_encoded = self.fernet.decrypt(data.encode())
        return data_encoded.decode()
