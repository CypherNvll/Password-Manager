import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core.password import Encryption

def test_encryption_system():
    print("\nTesting Encryption System")
    print("-" * 50)
    
    print("\nTest 1: Basic Encryption/Decryption")
    master_password = "MySecretMasterPassword123!"
    encryption = Encryption(master_password)
    
    test_passwords = [
        "SimplePass123!",
        "Complex@Password#2023",
        "Very!@#Complex$%^Password&*()",
        "短いパスワード",  
        "    spaces    ", 
        "12345678",
        "!@#$%^&*()",
    ]
    
    for password in test_passwords:
        try:
            print(f"\nTesting password: {password}")
            encrypted = encryption.encrypt(password)
            print(f"Encrypted: {encrypted[:50]}...")
            decrypted = encryption.decrypt(encrypted)
            print(f"Decrypted: {decrypted}")
            if decrypted == password:
                print("✓ Success: Password correctly encrypted and decrypted")
            else:
                print("✗ Error: Decrypted password doesn't match original")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print("\nTest 2: Master Password Verification")
    correct = encryption.verify_master_password(master_password)
    wrong = encryption.verify_master_password("WrongPassword123!")
    print(f"Correct master password verification: {'✓ Pass' if correct else '✗ Fail'}")
    print(f"Wrong master password verification: {'✓ Pass' if not wrong else '✗ Fail'}")
    
    print("\nTest 3: Salt Generation and Storage")
    salt_file = "salt.bin"
    if os.path.exists(salt_file):
        print("✓ Salt file created successfully")
        with open(salt_file, "rb") as f:
            salt_data = f.read()
        print(f"Salt length: {len(salt_data)} bytes")
    else:
        print("✗ Error: Salt file not created")
    
    print("\nTest 4: Error Cases")
    try:
        encryption.decrypt("not_valid_encrypted_data")
        print("✗ Error: Should have failed with invalid data")
    except Exception:
        print("✓ Successfully caught invalid decrypt data")
    
    print("\nTest 5: Different Master Passwords")
    encryption1 = Encryption("MasterPass1")
    encryption2 = Encryption("MasterPass2")
    
    test_password = "TestPassword123!"
    encrypted1 = encryption1.encrypt(test_password)
    encrypted2 = encryption2.encrypt(test_password)
    
    print("Different master passwords produce different encryptions:", 
          encrypted1 != encrypted2)
    
    try:
        encryption2.decrypt(encrypted1)
        print("✗ Error: Should not decrypt with different master password")
    except Exception:
        print("✓ Successfully prevented decryption with wrong master password")

    if os.path.exists(salt_file):
        os.remove(salt_file)
        print("\nCleaned up test files")

if __name__ == "__main__":
    test_encryption_system()