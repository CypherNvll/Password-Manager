import secrets
import string

class PasswordGen:
    """Generate secure password with customizable options"""
    
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    def generate(self, length=16, use_lowercase=True, use_uppercase=True, 
                use_digits=True, use_symbols=True) -> str:
        """Generate a password with specified requirements"""
        if length < 8:
            raise ValueError("Password must be at least 8 characters long")

        characters = ''
        if use_lowercase:
            characters += self.lowercase
        if use_uppercase:
            characters += self.uppercase
        if use_digits:
            characters += self.digits
        if use_symbols:
            characters += self.symbols

        if not characters:
            raise ValueError("At least one character type must be selected")

        password = ''
        if use_lowercase:
            password += secrets.choice(self.lowercase)
        if use_uppercase:
            password += secrets.choice(self.uppercase)
        if use_digits:
            password += secrets.choice(self.digits)
        if use_symbols:
            password += secrets.choice(self.symbols)

        remaining_length = length - len(password)
        password += ''.join(secrets.choice(characters) for _ in range(remaining_length))
        password_list = list(password)
        secrets.SystemRandom().shuffle(password_list)
        return ''.join(password_list)
    
    def generate_memorable(self, num_words=3, separator="-") -> str:
        """Generate a memorable password using words"""
        word_list = [
            "apple", "banana", "cherry", "dragon", "eagle", "forest",
            "garden", "harbor", "island", "jungle", "knight", "lemon",
            "mountain", "ninja", "orange", "pepper", "queen", "river",
            "silver", "tiger", "umbrella", "violet", "window", "yellow"
        ]

        words = [secrets.choice(word_list) for _ in range(num_words)]
        words.append(str(secrets.randbelow(100)))
        return separator.join(words)

    def check_strength(self, password: str) -> dict:
        """Check password strength"""
        metrics = {
            'length': len(password),
            'has_lowercase': any(c.islower() for c in password),
            'has_uppercase': any(c.isupper() for c in password),
            'has_digits': any(c.isdigit() for c in password),
            'has_symbols': any(c in self.symbols for c in password),
            'score': 0
        }

        score = 0
        if metrics['length'] >= 12:
            score += 25
        elif metrics['length'] >= 8:
            score += 10
        
        if metrics['has_lowercase']:
            score += 25
        if metrics['has_uppercase']:
            score += 25
        if metrics['has_digits']:
            score += 15
        if metrics['has_symbols']:
            score += 10

        metrics['score'] = min(100, score)
        return metrics