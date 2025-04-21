# Secure Password Manager

A command-line password manager that encrypts and stores your passwords locally with backup capabilities.

## Features
- Strong encryption (PBKDF2HMAC with SHA256)
- Password generation
- Encrypted local storage
- Backup and restore functionality
- USB export/import support
- Database management (add, view, clear)

## Requirements
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python src/main.py
```

2. Main operations:
- Add new password (Option 1)
- Retrieve password (Option 2)
- Generate secure password (Option 3)
- List all entries (Option 4)
- Manage backups (Options 5-9)
- Clear database (Option 10)

**Important**: The master password cannot be recovered if forgotten. All passwords are encrypted using this master password. 