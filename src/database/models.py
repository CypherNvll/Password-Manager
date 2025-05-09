import sqlite3
from datetime import datetime
from pathlib import Path

class Database:
    def __init__(self, db_path):
        self.db_path = db_path  # Just store the path, no need for Path object here
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Create database connection"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def init_tables(self):
        """Create tables if they don't exist"""
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL,
                username TEXT NOT NULL,
                encrypted_password TEXT NOT NULL,
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                category_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
            ''')

            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
            ''')

            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

class PasswordManager:
    def __init__(self, database):
        self.db = database

    def add_password(self, website, username, encrypted_password, notes=None):
        try:
            self.db.cursor.execute('''
                INSERT INTO passwords (website, username, encrypted_password, notes)
                VALUES (?, ?, ?, ?)
            ''', (website, username, encrypted_password, notes))
            self.db.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding password: {e}")
            return False

    def get_password(self, website):
        try:
            self.db.cursor.execute('''
                SELECT * FROM passwords WHERE website = ?
            ''', (website,))
            return self.db.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting password: {e}")
            return None 

    def update_password(self, website, new_encrypted_password):
        try:
            self.db.cursor.execute('''
                UPDATE passwords 
                SET encrypted_password = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE website = ?
            ''', (new_encrypted_password, website))
            self.db.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating password: {e}")
            return False

    def delete_password(self, website):
        try:
            self.db.cursor.execute('''
                DELETE FROM passwords WHERE website = ?
            ''', (website,))
            self.db.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting password: {e}")
            return False

    def get_all_passwords(self):
        try:
            self.db.cursor.execute('SELECT * FROM passwords')
            return self.db.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting all passwords: {e}")
            return []

    def get_all_categories(self):
        try:
            self.db.cursor.execute('SELECT * FROM categories')
            return self.db.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting all categories: {e}")
            return []
    
    def add_category(self, name):
        try:
            self.db.cursor.execute('''
                INSERT INTO categories (name)
                VALUES (?)
            ''', (name,))
            self.db.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding category: {e}")
            return False        
        
    def delete_category(self, name):
        try:
            self.db.cursor.execute('''
                DELETE FROM categories WHERE name = ?
            ''', (name,))
            self.db.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting category: {e}")
            return False
        
