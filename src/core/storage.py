import os
import shutil
from datetime import datetime
from pathlib import Path

class StorageManager:
    def __init__(self, base_path: str = 'data'):
        self.base_path = Path(base_path)
        self.db_path = self.base_path / 'passwords.db'
        self.salt_path = self.base_path / 'salt.bin'
        self.backup_path = self.base_path / 'backups'
        self.init_storage()

    def init_storage(self):
        """initialize storage directories"""
        self.base_path.mkdir(exist_ok=True)
        self.backup_path.mkdir(exist_ok=True)

    def create_backup(self) -> str:
        """create backup of database and salt"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.backup_path / timestamp
        backup_dir.mkdir(exist_ok=True)

        if self.db_path.exists():
            shutil.copy2(self.db_path, backup_dir / 'passwords.db')
        if self.salt_path.exists():
            shutil.copy2(self.salt_path, backup_dir / 'salt.bin')
        return str(backup_dir)

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
        dest_path = Path(destination)
        try:
            dest_path.mkdir(exist_ok=True)
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

    def get_backup_list(self) -> list:
        """Get list of available backups"""
        return [d for d in self.backup_path.iterdir() if d.is_dir()]

    def cleanup_old_backups(self, keep_last: int = 5):
        """Remove old backups, keeping the specified number"""
        backups = sorted(self.get_backup_list(), key=lambda x: x.name)
        for backup in backups[:-keep_last]:
            shutil.rmtree(backup)