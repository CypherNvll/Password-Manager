import sys
import os
import shutil
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core.storage import StorageManager

def test_storage():
    # Use test directory
    test_base = "test_data"
    storage = StorageManager(test_base)
    
    print("\nTest 1: Initialize Storage")
    try:
        storage.init_storage()
        print("Storage directories created")
        print(f"Base path exists: {storage.base_path.exists()}")
        print(f"Backup path exists: {storage.backup_path.exists()}")
    except Exception as e:
        print(f"Failed to initialize storage: {e}")

    print("\nTest 2: Create Test Files")
    try:
        # Create dummy database and salt files
        with open(storage.db_path, 'w') as f:
            f.write("test database")
        with open(storage.salt_path, 'w') as f:
            f.write("test salt")
        print("Test files created")
    except Exception as e:
        print(f"Failed to create test files: {e}")

    print("\nTest 3: Create Backup")
    try:
        backup_path = storage.create_backup()
        print(f"Backup created at: {backup_path}")
        print(f"Backup exists: {Path(backup_path).exists()}")
    except Exception as e:
        print(f"Failed to create backup: {e}")

    print("\nTest 4: Export to Device")
    test_usb = "test_usb"
    try:
        success = storage.export_to_device(test_usb)
        print(f"Export successful: {success}")
        print(f"Files exported to: {test_usb}")
    except Exception as e:
        print(f"Failed to export: {e}")

    print("\nTest 5: Import from Device")
    try:
        # First modify the test files to verify import
        with open(Path(test_usb) / "passwords.db", 'w') as f:
            f.write("modified database")
        success = storage.import_from_device(test_usb)
        print(f"Import successful: {success}")
    except Exception as e:
        print(f"Failed to import: {e}")

    print("\nTest 6: Backup Management")
    try:
        # Create multiple backups
        for _ in range(3):
            storage.create_backup()
        
        backups = storage.get_backup_list()
        print(f"Number of backups: {len(backups)}")
        
        # Test cleanup
        storage.cleanup_old_backups(keep_last=2)
        backups = storage.get_backup_list()
        print(f"Backups after cleanup: {len(backups)}")
    except Exception as e:
        print(f"Backup management failed: {e}")

    # Cleanup test directories
    print("\nCleaning up test files...")
    try:
        shutil.rmtree(test_base)
        shutil.rmtree(test_usb)
        print("Cleanup successful")
    except Exception as e:
        print(f"Cleanup failed: {e}")

if __name__ == "__main__":
    test_storage()