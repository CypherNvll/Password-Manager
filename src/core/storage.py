import os
import shutil
from datetime import datetime
from pathlib import Path

class StorageManager:
    def __init__(self, base_path: str = 'data'):
        self.base_path = Path(base_path)
        self.db_path = self.base_path / 'passwords.db'
        self.salt_path = self.base_path / 'salt.bin'
        self.init_storage()

    def init_storage(self):
        """initialize storage directories"""
        self.base_path.mkdir(exist_ok=True)

    def create_backup(self, backup_path: str = None) -> str:
        """
        Create backup of database and salt
        Args:
            backup_path: Optional custom backup location. If None, uses default path
        """
        if backup_path:
            backup_dir = Path(backup_path)
        else:
            # Default backup in data/backups/timestamp
            backup_dir = self.base_path / 'backups' / datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            if self.db_path.exists():
                shutil.copy2(self.db_path, backup_dir / 'passwords.db')
            if self.salt_path.exists():
                shutil.copy2(self.salt_path, backup_dir / 'salt.bin')
            return str(backup_dir)
        except Exception as e:
            print(f"Backup failed: {e}")
            return None

    def restore_backup(self, backup_dir: str) -> bool:
        """Restore from backup"""
        backup_path = Path(backup_dir)
        if not backup_path.exists():
            return False

        try:
            if (backup_path / "passwords.db").exists():
                shutil.copy2(backup_path / "passwords.db", self.db_path)
            if (backup_path / "salt.bin").exists():
                shutil.copy2(backup_path / "salt.bin", self.salt_path)
            return True
        except Exception as e:
            print(f"Restore failed: {e}")
            return False
        
    def export_to_device(self, destination: str) -> bool:
        """Export database to external device"""
        if not destination:
            print("No destination path provided")
            return False
            
        dest_path = Path(destination)
        try:
            dest_path.mkdir(parents=True, exist_ok=True)
            if self.db_path.exists():
                shutil.copy2(self.db_path, dest_path / "passwords.db")
            if self.salt_path.exists():
                shutil.copy2(self.salt_path, dest_path / "salt.bin")
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False

    def import_from_device(self, source: str) -> bool:
        """import database from external device"""
        if not source:
            print("No source path provided")
            return False
            
        source_path = Path(source)
        try:
            if (source_path / "passwords.db").exists():
                shutil.copy2(source_path / "passwords.db", self.db_path)
            if (source_path / "salt.bin").exists():
                shutil.copy2(source_path / "salt.bin", self.salt_path)
            return True
        except Exception as e:
            print(f"Import failed: {e}")
            return False

    def get_backup_list(self, backup_path: str = None) -> list:
        """Get list of available backups"""
        search_path = Path(backup_path) if backup_path else self.base_path / 'backups'
        if not search_path.exists():
            return []
        return [d for d in search_path.iterdir() if d.is_dir()]

    def cleanup_old_backups(self, backup_path: str = None, keep_last: int = 5):
        """Remove old backups, keeping the specified number"""
        backups = self.get_backup_list(backup_path)
        if not backups:
            return
            
        backups.sort(key=lambda x: x.name)
        for backup in backups[:-keep_last]:
            try:
                shutil.rmtree(backup)
            except Exception as e:
                print(f"Failed to remove backup {backup}: {e}")