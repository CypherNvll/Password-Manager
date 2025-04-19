import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core.password import Encryption

def test_encryption():
    """Test the encryption module"""
    master_password = input('input master password: ')
    encryptor = Encryption(master_password)
    
    test_password = input('input password: ')
    
    print("\nTest 1: Encryption")
    try:
        encrypted = encryptor.encrypt(test_password)
        print(f"Original password: {test_password}")
        print(f"Encrypted password: {encrypted}")
        print("Encryption successful")
    except Exception as e:
        print(f"Encryption failed: {e}")

    print("\nTest 2: Decryption")
    try:
        decrypted = encryptor.decrypt(encrypted)
        print(f"Decrypted password: {decrypted}")
        print("Decryption successful" if decrypted == test_password else "Decryption failed")
    except Exception as e:
        print(f"Decryption failed: {e}")

    print("\nTest 3: Master Password Verification")
    correct = encryptor.verify_master_password(master_password)
    wrong = encryptor.verify_master_password("WrongPassword123!")
    print(f"Correct master password verification: {'Pass' if correct else 'Fail'}")
    print(f"Wrong master password verification: {'Pass' if not wrong else 'Fail'}")

if __name__ == "__main__":
    test_encryption()