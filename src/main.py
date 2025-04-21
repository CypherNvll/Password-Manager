import os
from pathlib import Path
from core.password import Encryption
from core.generator import PasswordGen
from database.models import Database, PasswordManager
from core.storage import StorageManager
import shutil
import sys
from typing import Optional

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

    def add_password(self, website: str, username: str, password: str, notes: str = None) -> bool:
        """Add encrypted password to database"""
        if not self.encryption:
            print("Please initialize encryption first!")
            return False
        try:
            encrypted_password = self.encryption.encrypt(password)
            return self.password_manager.add_password(website, username, encrypted_password, notes)
        except Exception as e:
            print(f"Failed to add password: {e}")
            return False

    def get_password(self, website: str) -> Optional[dict]:
        """Retrieve and decrypt password"""
        if not self.encryption:
            print("Please initialize encryption first!")
            return None
        try:
            result = self.password_manager.get_password(website)
            if result:
                id_, website, username, encrypted_password, notes, created, updated, category = result
                decrypted_password = self.encryption.decrypt(encrypted_password)
                return {
                    'website': website,
                    'username': username,
                    'password': decrypted_password,
                    'notes': notes,
                    'created': created,
                    'updated': updated,
                    'category': category
                }
        except Exception as e:
            print(f"Failed to retrieve password: {e}")
        return None

    def backup_data(self, backup_path: str = None) -> Optional[str]:
        """Create backup of all data"""
        try:
            backup_location = self.storage.create_backup(backup_path)
            if backup_location and self.storage.verify_backup(backup_location):
                return backup_location
            print("Backup verification failed")
            return None
        except Exception as e:
            print(f"Backup failed: {e}")
            return None

    def restore_data(self, backup_path: str) -> bool:
        """Restore data from backup"""
        try:
            if not self.storage.verify_backup(backup_path):
                print("Invalid or corrupted backup")
                return False
            return self.storage.restore_backup(backup_path)
        except Exception as e:
            print(f"Restore failed: {e}")
            return False

    def export_to_usb(self, usb_path: str) -> bool:
        """Export database to USB drive"""
        if not usb_path:
            print("Please provide a USB drive path")
            return False
        try:
            return self.storage.export_to_device(usb_path)
        except Exception as e:
            print(f"Export failed: {e}")
            return False

    def import_from_usb(self, usb_path: str) -> bool:
        """Import database from USB drive"""
        try:
            return self.storage.import_from_device(usb_path)
        except Exception as e:
            print(f"Import failed: {e}")
            return False

    def list_backups(self, backup_path: str = None) -> list:
        """List available backups"""
        try:
            return self.storage.get_backup_list(backup_path)
        except Exception as e:
            print(f"Failed to list backups: {e}")
            return []

    def generate_password(self, length: int = 16, include_special: bool = True) -> Optional[str]:
        """Generate a secure password"""
        try:
            return self.generator.generate(length, include_special)
        except Exception as e:
            print(f"Failed to generate password: {e}")
            return None

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
        try:
            self.db.close()
        except Exception as e:
            print(f"Error closing database: {e}")

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
    print("9. List Backups")
    print("10. Clear Database")
    print("11. Exit")
    return input("Choose an option (1-11): ")

def main():
    app = PasswordManagerApp()
    
    print("\n⚠️  IMPORTANT: Please remember your master password!")
    print("There is NO WAY to recover your passwords if you forget the master password.")
    print("The master password is never stored and is required to decrypt your passwords.\n")
    
    try:
        # Get master password 
        master_password = input("Enter master password: ")
        app.initialize_encryption(master_password)
        
        while True:
            try:
                choice = print_menu()
                
                if choice == '1':
                    website = input("Enter website: ")
                    username = input("Enter username: ")
                    use_generated = input("Generate password? (y/n): ").lower() == 'y'
                    if use_generated:
                        length = int(input("Enter password length (default 16): ") or "16")
                        special = input("Include special characters? (y/n): ").lower() == 'y'
                        password = app.generate_password(length, special)
                        if password:
                            print(f"Generated password: {password}")
                        else:
                            continue
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
                        print(f"Created: {result['created']}")
                        print(f"Last Updated: {result['updated']}")
                        if result['category']:
                            print(f"Category: {result['category']}")
                    else:
                        print("Password not found.")

                elif choice == '3':
                    length = int(input("Enter password length (default 16): ") or "16")
                    special = input("Include special characters? (y/n): ").lower() == 'y'
                    password = app.generate_password(length, special)
                    if password:
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
                            print(f"Created: {created}")
                            print(f"Last Updated: {updated}")
                            if category:
                                print(f"Category: {category}")
                    else:
                        print("No passwords stored.")

                elif choice == '5':
                    backup_path = input("Enter backup path (or press Enter for default): ")
                    backup_path = backup_path if backup_path else None
                    backup_location = app.backup_data(backup_path)
                    if backup_location:
                        print(f"Backup created and verified at: {backup_location}")
                    else:
                        print("Backup failed.")

                elif choice == '6':
                    backup_path = input("Enter backup path to restore from: ")
                    if app.restore_data(backup_path):
                        print("Backup restored and verified successfully!")
                        print("Please restart the application to use the restored data.")
                        break
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
                        print("Please restart the application to use the imported data.")
                        break
                    else:
                        print("Import failed.")

                elif choice == '9':
                    backup_path = input("Enter backup directory to list (or press Enter for default): ")
                    backup_path = backup_path if backup_path else None
                    backups = app.list_backups(backup_path)
                    if backups:
                        print("\nAvailable Backups:")
                        for backup in backups:
                            print(f"- {backup}")
                    else:
                        print("No backups found.")

                elif choice == '10':
                    print("\n⚠️  WARNING: This will permanently delete all stored passwords!")
                    confirm = input("Are you sure you want to clear the database? (type 'YES' to confirm): ")
                    if confirm == 'YES':
                        if app.clear_database():
                            print("Database cleared successfully.")
                            print("Please restart the application to create a new database.")
                            break
                        else:
                            print("Failed to clear database.")

                elif choice == '11':
                    break
                else:
                    print("Invalid choice. Please try again.")

            except ValueError as e:
                print(f"Invalid input: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Please try again.")

    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        app.close()

if __name__ == "__main__":
    main()