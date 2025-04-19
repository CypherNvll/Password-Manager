import os
from pathlib import Path
from core.password import Encryption
from core.generator import PasswordGen
from database.models import Database, PasswordManager
from core.storage import StorageManager

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

    def backup_data(self) -> str:
        """Create backup of all data"""
        return self.storage.create_backup()

    def restore_data(self, backup_path: str) -> bool:
        """Restore data from backup"""
        return self.storage.restore_backup(backup_path)

    def export_to_usb(self, usb_path: str) -> bool:
        """Export database to USB drive"""
        return self.storage.export_to_device(usb_path)

    def import_from_usb(self, usb_path: str) -> bool:
        """Import database from USB drive"""
        return self.storage.import_from_device(usb_path)

    def close(self):
        """Clean up and close connections"""
        self.db.close()

# Example usage (will be replaced with proper UI)
def main():
    app = PasswordManagerApp()
    
    # Get master password 
    master_password = input("Enter master password: ")
    app.initialize_encryption(master_password)
    
    # Example backup
    backup_path = app.backup_data()
    print(f"Backup created at: {backup_path}")
    
    # Example USB export (replace with actual USB path)
    usb_path = "F:/backup"  # Example path
    if app.export_to_usb(usb_path):
        print(f"Data exported to: {usb_path}")
    
    app.close()

if __name__ == "__main__":
    main()