import os
from pathlib import Path
from core.password import Encryption
from core.generator import PasswordGen
from database.models import Database, PasswordManager
from core.storage import StorageManager
import shutil

class PasswordManagerApp:
    def __init__(self):
        self.storage = StorageManager()
        self.db = Database(str(self.storage.db_path))
        self.db.connect()
        self.db.init_tables()
        self.password_manager = PasswordManager(self.db)
        self.generator = PasswordGen()
        self.encryption = None  

    def initialize_encryption(self, master_password: str):
        """Initialize encryption with master password"""
        self.encryption = Encryption(master_password)

    def add_password(self, website: str, username: str, password: str, notes: str = None):
        """Add encrypted password to database"""
        if not self.encryption:
            print("Please initialize encryption first!")
            return False
        encrypted_password = self.encryption.encrypt(password)
        return self.password_manager.add_password(website, username, encrypted_password, notes)

    def get_password(self, website: str):
        """Retrieve and decrypt password"""
        if not self.encryption:
            print("Please initialize encryption first!")
            return None
        result = self.password_manager.get_password(website)
        if result:
            id_, website, username, encrypted_password, notes, created, updated, category = result
            decrypted_password = self.encryption.decrypt(encrypted_password)
            return {
                'website': website,
                'username': username,
                'password': decrypted_password,
                'notes': notes
            }
        return None

    def backup_data(self, backup_path: str = None) -> str:
        """Create backup of all data"""
        return self.storage.create_backup(backup_path)

    def restore_data(self, backup_path: str) -> bool:
        """Restore data from backup"""
        return self.storage.restore_backup(backup_path)

    def export_to_usb(self, usb_path: str = None) -> bool:
        """Export database to USB drive"""
        if not usb_path:
            print("Please provide a USB drive path")
            return False
        return self.storage.export_to_device(usb_path)

    def import_from_usb(self, usb_path: str) -> bool:
        """Import database from USB drive"""
        return self.storage.import_from_device(usb_path)

    def generate_password(self, length: int = 16, include_special: bool = True) -> str:
        """Generate a secure password"""
        return self.generator.generate(length, include_special)

    def clear_database(self) -> bool:
        """Clear all data and reset the database"""
        try:
            self.close()  # Close database connection first
            if os.path.exists('data'):
                shutil.rmtree('data')
            return True
        except Exception as e:
            print(f"Error clearing database: {e}")
            return False

    def close(self):
        """Clean up and close connections"""
        self.db.close()

def print_menu():
    print("\n=== Password Manager CLI ===")
    print("1. Add Password")
    print("2. Get Password")
    print("3. Generate Password")
    print("4. List All Passwords")
    print("5. Create Backup")
    print("6. Restore from Backup")
    print("7. Export to USB")
    print("8. Import from USB")
    print("9. Clear Database")
    print("10. Exit")
    return input("Choose an option (1-10): ")

def main():
    app = PasswordManagerApp()
    
    print("\n⚠️  IMPORTANT: Please remember your master password!")
    print("There is NO WAY to recover your passwords if you forget the master password.")
    print("The master password is never stored and is required to decrypt your passwords.\n")
    
    # Get master password 
    master_password = input("Enter master password: ")
    app.initialize_encryption(master_password)
    
    while True:
        choice = print_menu()
        
        if choice == '1':
            website = input("Enter website: ")
            username = input("Enter username: ")
            use_generated = input("Generate password? (y/n): ").lower() == 'y'
            if use_generated:
                length = int(input("Enter password length (default 16): ") or "16")
                special = input("Include special characters? (y/n): ").lower() == 'y'
                password = app.generate_password(length, special)
                print(f"Generated password: {password}")
            else:
                password = input("Enter password: ")
            notes = input("Enter notes (optional): ")
            
            if app.add_password(website, username, password, notes):
                print("Password added successfully!")
            else:
                print("Failed to add password.")

        elif choice == '2':
            website = input("Enter website to search: ")
            result = app.get_password(website)
            if result:
                print("\nPassword Details:")
                print(f"Website: {result['website']}")
                print(f"Username: {result['username']}")
                print(f"Password: {result['password']}")
                if result['notes']:
                    print(f"Notes: {result['notes']}")
            else:
                print("Password not found.")

        elif choice == '3':
            length = int(input("Enter password length (default 16): ") or "16")
            special = input("Include special characters? (y/n): ").lower() == 'y'
            password = app.generate_password(length, special)
            print(f"\nGenerated password: {password}")

        elif choice == '4':
            passwords = app.password_manager.get_all_passwords()
            if passwords:
                print("\nAll Stored Passwords:")
                for pwd in passwords:
                    id_, website, username, _, notes, created, updated, category = pwd
                    print(f"\nWebsite: {website}")
                    print(f"Username: {username}")
                    if notes:
                        print(f"Notes: {notes}")
            else:
                print("No passwords stored.")

        elif choice == '5':
            backup_path = input("Enter backup path (or press Enter for default): ")
            backup_path = backup_path if backup_path else None
            backup_location = app.backup_data(backup_path)
            if backup_location:
                print(f"Backup created at: {backup_location}")
            else:
                print("Backup failed.")

        elif choice == '6':
            backup_path = input("Enter backup path to restore from: ")
            if app.restore_data(backup_path):
                print("Backup restored successfully!")
            else:
                print("Failed to restore backup.")

        elif choice == '7':
            usb_path = input("Enter USB drive path: ")
            if app.export_to_usb(usb_path):
                print(f"Data exported to: {usb_path}")
            else:
                print("Export failed.")

        elif choice == '8':
            usb_path = input("Enter USB drive path: ")
            if app.import_from_usb(usb_path):
                print("Data imported successfully!")
            else:
                print("Import failed.")

        elif choice == '9':
            print("\n⚠️  WARNING: This will permanently delete all stored passwords!")
            confirm = input("Are you sure you want to clear the database? (type 'YES' to confirm): ")
            if confirm == 'YES':
                if app.clear_database():
                    print("Database cleared successfully.")
                    print("Please restart the application to create a new database.")
                    break
                else:
                    print("Failed to clear database.")
            else:
                print("Database clear cancelled.")

        elif choice == '10':
            print("Goodbye!")
            app.close()
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()