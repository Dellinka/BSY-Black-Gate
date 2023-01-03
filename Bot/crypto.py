import base64
from cryptography.fernet import Fernet

FERNET_KEY = Fernet(base64.b64encode(b'9czVfY5Y1TheCakeIsALie1FN5aohb35'))


def encrypt(message):
    """

    :param message:     Message in bytes
    :return:
    """
    return str(base64.b64encode(FERNET_KEY.encrypt(message)), 'utf-8')


def decrypt(encrypted_message):
    """

    :param encrypted_message:   Message in string
    :return:
    """
    return FERNET_KEY.decrypt(base64.b64decode(bytes(encrypted_message, 'utf-8'))).decode()
