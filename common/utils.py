import base64
import json
import os

from cryptography.fernet import Fernet

ENCRYPTION_KEY = os.environ["ENCRYPTION_KEY"]
encryption_client = Fernet(ENCRYPTION_KEY)


def encrypt_payload(payload):
    encoded_payload = json.dumps(payload).encode()
    encrypted_payload = encryption_client.encrypt(encoded_payload)
    return base64.urlsafe_b64encode(encrypted_payload).decode("utf-8")


def decrypt_payload(encrypted_payload: str):
    encrypted_payload_buffer = base64.urlsafe_b64decode(encrypted_payload)
    encoded_payload = encryption_client.decrypt(encrypted_payload_buffer)
    return json.loads(encoded_payload)
