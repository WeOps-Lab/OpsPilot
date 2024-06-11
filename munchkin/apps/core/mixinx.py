import base64

from cryptography.fernet import Fernet

from munchkin.components.base import SECRET_KEY


class EncryptableMixin:
    def get_cipher_suite(self):
        key = base64.urlsafe_b64encode(SECRET_KEY.encode()[:32])
        return Fernet(key)

    def encrypt_field(self, field_name, field_dict=None):
        cipher_suite = self.get_cipher_suite()
        field_dict = field_dict if field_dict is not None else self.__dict__
        field_value = field_dict.get(field_name)
        if field_value:
            try:
                cipher_suite.decrypt(field_value.encode())
            except Exception:
                encrypted_value = cipher_suite.encrypt(field_value.encode())
                field_dict[field_name] = encrypted_value.decode()

    def decrypt_field(self, field_name, field_dict=None):
        cipher_suite = self.get_cipher_suite()
        field_dict = field_dict if field_dict is not None else self.__dict__
        field_value = field_dict.get(field_name)
        if field_value:
            try:
                decrypted_value = cipher_suite.decrypt(field_value.encode())
                field_dict[field_name] = decrypted_value.decode()
            except Exception:
                pass
