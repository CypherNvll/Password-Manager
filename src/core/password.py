import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Encryption:
    """handles encryption and decryption of passwords"""
    
    def __init__(self, master_password: str):
        """initialize encryption with master password"""
        self.salt = self._get_or_gen_salt()
        self.key = self._derive_key(master_password.encode(), self.salt)
        self.fernet = Fernet(self.key)
        
    def _get_or_gen_salt(self) -> bytes:
        '''Get existing salt or generate new one'''
        salt_file = 'salt.bin'
        if os.path.exists(salt_file):
            with open(salt_file, "rb") as f:
                return f.read()

        salt = os.urandom(16)
        with open(salt_file, "wb") as f:
            f.write(salt)
        return salt

    def _derive_key(self, master_password: bytes, salt: bytes) -> bytes:
        '''Derive encryption key from master password'''
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password))
        return key

    def encrypt(self, password: str) -> str:
        '''Encrypt a password'''
        try:
            encrypted = self.fernet.encrypt(password.encode())
            return encrypted.decode()
        except Exception as e:
            raise Exception(f"Encryption failed: {e}")
        
    def decrypt(self, encrypted_password: str) -> str:
        '''Decrypt a password'''
        try:
            decrypted = self.fernet.decrypt(encrypted_password.encode())
            return decrypted.decode()
        except Exception as e:
            raise Exception(f"Decryption failed: {e}")

    def verify_master_password(self, master_password: str) -> bool:
        """Verify if the master password is correct"""
        try:
            test_key = self._derive_key(master_password.encode(), self.salt)
            return test_key == self.key
        except Exception:
            return False