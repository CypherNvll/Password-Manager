import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core.generator import PasswordGen

def test_password_strength():
    generator = PasswordGen()
    
    test_passwords = {
        "weak": "password123",
        "medium": "Password123",
        "strong": "Password123!",
        "very_strong": "P@ssw0rd!2023#",
        "too_short": "Pw3!",
        "no_numbers": "Password!",
        "no_symbols": "Password123",
        "no_uppercase": "password123!",
        "no_lowercase": "PASSWORD123!",
        "only_letters": "abcdefghijk",
        "only_numbers": "12345678",
        "only_symbols": "!@#$%^&*()",
    }
    
    print("\nPassword Strength Test Results:")
    print("-" * 50)
    
    for name, password in test_passwords.items():
        metrics = generator.check_strength(password)
        print(f"\nTesting: {name}")
        print(f"Password: {password}")
        print(f"Length: {metrics['length']}")
        print(f"Has lowercase: {metrics['has_lowercase']}")
        print(f"Has uppercase: {metrics['has_uppercase']}")
        print(f"Has digits: {metrics['has_digits']}")
        print(f"Has symbols: {metrics['has_symbols']}")
        print(f"Score: {metrics['score']}/100")
        
        # Print strength category
        if metrics['score'] >= 80:
            print("Strength: Very Strong")
        elif metrics['score'] >= 60:
            print("Strength: Strong")
        elif metrics['score'] >= 40:
            print("Strength: Medium")
        else:
            print("Strength: Weak")
        
        print("-" * 50)

def test_generated_passwords():
    generator = PasswordGen()
    
    print("\nTesting Generated Passwords:")
    print("-" * 50)
    
    # Test default generated password
    password = generator.generate()
    metrics = generator.check_strength(password)
    print("\nDefault Generated Password:")
    print(f"Password: {password}")
    print(f"Score: {metrics['score']}/100")
    
    # Test memorable password
    memorable = generator.generate_memorable()
    metrics = generator.check_strength(memorable)
    print("\nMemorable Password:")
    print(f"Password: {memorable}")
    print(f"Score: {metrics['score']}/100")
    
    # Test custom password
    custom = generator.generate(length=20, use_symbols=True)
    metrics = generator.check_strength(custom)
    print("\nCustom Generated Password:")
    print(f"Password: {custom}")
    print(f"Score: {metrics['score']}/100")

if __name__ == "__main__":
    test_password_strength()
    test_generated_passwords()