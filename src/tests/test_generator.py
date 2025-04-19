import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core.generator import PasswordGen

def test_generator():
    """Test the password generator"""
    generator = PasswordGen()
    
    print("\nTest 1: Default Password Generation")
    password = generator.generate()
    print(f"Generated password: {password}")
    strength = generator.check_strength(password)
    print(f"Password strength: {strength['score']}/100")
    print(f"Password metrics: {strength}")
    
    print("\nTest 2: Custom Password Generation")
    custom_pass = generator.generate(
        length=12,
        use_uppercase=True,
        use_digits=True,
        use_symbols=False
    )
    print(f"Custom password: {custom_pass}")
    
    print("\nTest 3: Memorable Password")
    memorable = generator.generate_memorable()
    print(f"Memorable password: {memorable}")
    
    print("\nTest 4: Different Password Lengths")
    passwords = [
        generator.generate(length=8),
        generator.generate(length=16),
        generator.generate(length=24)
    ]
    for i, pwd in enumerate(passwords, 1):
        print(f"Length {len(pwd)}: {pwd}")

if __name__ == "__main__":
    test_generator()