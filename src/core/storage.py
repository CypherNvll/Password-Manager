import os
import shutil
import zipfile
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List

class StorageManager:
    def __init__(self, base_path: str = 'data'):
        self.base_path = Path(base_path)
        self.db_path = self.base_path / 'passwords.db'
        self.salt_path = self.base_path / 'salt.bin'
        self.init_storage()

    def init_storage(self):
        """Initialize storage directories"""
        self.base_path.mkdir(exist_ok=True)
        (self.base_path / 'backups').mkdir(exist_ok=True)

    def create_backup(self, backup_path: Optional[str] = None) -> Optional[str]:
        """
        Create compressed backup of database and salt
        Args:
            backup_path: Optional custom backup location. If None, uses default path
        Returns:
            str: Path to backup directory or None if backup failed
        """
        if backup_path:
            backup_dir = Path(backup_path)
        else:
            # Default backup in data/backups/timestamp
            backup_dir = self.base_path / 'backups' / datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Create zip file with database and salt
            zip_path = backup_dir / 'backup.zip'
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if self.db_path.exists():
                    zipf.write(self.db_path, 'passwords.db')
                if self.salt_path.exists():
                    zipf.write(self.salt_path, 'salt.bin')
                
                # Add metadata
                metadata = {
                    'created': datetime.now().isoformat(),
                    'version': '1.0',
                    'files': ['passwords.db', 'salt.bin']
                }
                zipf.writestr('metadata.json', json.dumps(metadata, indent=2))
            
            return str(backup_dir)
        except Exception as e:
            print(f"Backup failed: {e}")
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
            return None

    def restore_backup(self, backup_dir: str) -> bool:
        """
        Restore from backup
        Args:
            backup_dir: Path to backup directory containing backup.zip
        Returns:
            bool: True if restore successful, False otherwise
        """
        backup_path = Path(backup_dir)
        zip_path = backup_path / 'backup.zip'
        
        if not zip_path.exists():
            print(f"Backup file not found: {zip_path}")
            return False

        try:
            # Create temporary directory for extraction
            temp_dir = self.base_path / 'temp_restore'
            temp_dir.mkdir(exist_ok=True)
            
            # Extract backup
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                zipf.extractall(temp_dir)
            
            # Verify metadata
            try:
                with open(temp_dir / 'metadata.json') as f:
                    metadata = json.load(f)
                if 'version' not in metadata:
                    raise ValueError("Invalid backup format")
            except Exception as e:
                print(f"Invalid backup metadata: {e}")
                return False

            # Move files to correct location
            if (temp_dir / 'passwords.db').exists():
                shutil.copy2(temp_dir / 'passwords.db', self.db_path)
            if (temp_dir / 'salt.bin').exists():
                shutil.copy2(temp_dir / 'salt.bin', self.salt_path)

            return True
        except Exception as e:
            print(f"Restore failed: {e}")
            return False
        finally:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)

    def export_to_device(self, destination: str) -> bool:
        """
        Export database to external device with compression
        Args:
            destination: Path to export location
        Returns:
            bool: True if export successful, False otherwise
        """
        if not destination:
            print("No destination path provided")
            return False
            
        dest_path = Path(destination)
        try:
            dest_path.mkdir(parents=True, exist_ok=True)
            
            # Create zip file with database and salt
            zip_path = dest_path / 'passwords_backup.zip'
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if self.db_path.exists():
                    zipf.write(self.db_path, 'passwords.db')
                if self.salt_path.exists():
                    zipf.write(self.salt_path, 'salt.bin')
                
                # Add metadata
                metadata = {
                    'created': datetime.now().isoformat(),
                    'version': '1.0',
                    'files': ['passwords.db', 'salt.bin']
                }
                zipf.writestr('metadata.json', json.dumps(metadata, indent=2))
            
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            if zip_path.exists():
                zip_path.unlink()
            return False

    def import_from_device(self, source: str) -> bool:
        """
        Import database from external device
        Args:
            source: Path to import location
        Returns:
            bool: True if import successful, False otherwise
        """
        if not source:
            print("No source path provided")
            return False
            
        source_path = Path(source)
        zip_path = source_path / 'passwords_backup.zip'
        
        if not zip_path.exists():
            print(f"Backup file not found: {zip_path}")
            return False

        try:
            # Create temporary directory for extraction
            temp_dir = self.base_path / 'temp_import'
            temp_dir.mkdir(exist_ok=True)
            
            # Extract backup
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                zipf.extractall(temp_dir)
            
            # Verify metadata
            try:
                with open(temp_dir / 'metadata.json') as f:
                    metadata = json.load(f)
                if 'version' not in metadata:
                    raise ValueError("Invalid backup format")
            except Exception as e:
                print(f"Invalid backup metadata: {e}")
                return False

            # Move files to correct location
            if (temp_dir / 'passwords.db').exists():
                shutil.copy2(temp_dir / 'passwords.db', self.db_path)
            if (temp_dir / 'salt.bin').exists():
                shutil.copy2(temp_dir / 'salt.bin', self.salt_path)

            return True
        except Exception as e:
            print(f"Import failed: {e}")
            return False
        finally:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)

    def get_backup_list(self, backup_path: Optional[str] = None) -> List[Path]:
        """
        Get list of available backups
        Args:
            backup_path: Optional custom backup location
        Returns:
            List[Path]: List of backup directories
        """
        search_path = Path(backup_path) if backup_path else self.base_path / 'backups'
        if not search_path.exists():
            return []
        return sorted(
            [d for d in search_path.iterdir() if d.is_dir() and (d / 'backup.zip').exists()],
            key=lambda x: x.name,
            reverse=True
        )

    def cleanup_old_backups(self, backup_path: Optional[str] = None, keep_last: int = 5) -> None:
        """
        Remove old backups, keeping the specified number
        Args:
            backup_path: Optional custom backup location
            keep_last: Number of recent backups to keep
        """
        backups = self.get_backup_list(backup_path)
        if not backups:
            return
            
        for backup in backups[keep_last:]:
            try:
                shutil.rmtree(backup)
            except Exception as e:
                print(f"Failed to remove backup {backup}: {e}")

    def verify_backup(self, backup_path: str) -> bool:
        """
        Verify backup integrity
        Args:
            backup_path: Path to backup directory
        Returns:
            bool: True if backup is valid, False otherwise
        """
        backup_dir = Path(backup_path)
        zip_path = backup_dir / 'backup.zip'
        
        if not zip_path.exists():
            return False
            
        try:
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                # Check zip file integrity
                if zipf.testzip() is not None:
                    return False
                    
                # Verify required files exist
                files = zipf.namelist()
                required_files = {'passwords.db', 'salt.bin', 'metadata.json'}
                if not required_files.issubset(files):
                    return False
                    
                # Verify metadata
                with zipf.open('metadata.json') as f:
                    metadata = json.loads(f.read())
                if 'version' not in metadata or 'files' not in metadata:
                    return False
                    
            return True
        except Exception:
            return False