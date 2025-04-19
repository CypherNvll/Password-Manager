# Password Manager

A password manager built with PyQt6 that stores encrypted passwords locally with backup capabilities.

## Features

- Secure local password storage using AES-256 encryption
- Password salting for enhanced security
- Modern GUI built with PyQt6
- Local backup and restore functionality
- Password strength checker
- Secure master password system

## Project Structure

```
passwdmngr/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── core/               # Core password management logic
│   │   ├── __init__.py
│   │   └── password.py
│   ├── crypto/             # Encryption and security
│   │   ├── __init__.py
│   │   └── encryption.py
│   ├── database/           # Database operations
│   │   ├── __init__.py
│   │   └── models.py
│   └── ui/                 # User interface
│       ├── __init__.py
│       ├── main_window.py
│       └── dialogs/
├── tests/                  # Test files
├── requirements.txt        # Project dependencies
└── README.md               # This file
```

## Security Features

- AES-256 encryption for stored passwords
- Argon2 for master password hashing
- Unique salt for each stored password
- Secure memory handling
- No cloud storage - all data stored locally 