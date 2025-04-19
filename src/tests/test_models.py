import sys
import os
import sqlite3
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database.models import Database, PasswordManager

def test_database():
    test_db_path = "test_passwords.db"
    
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    print("\nTest 1: Database Connection")
    try:
        db = Database(test_db_path)
        db.connect()
        db.init_tables()
        print("Database connection and initialization successful")
    except Exception as e:
        print(f"Database connection failed: {e}")
        return

    pm = PasswordManager(db)

    print("\nTest 2: Category Operations")
    categories = ["Work", "Social", "Banking"]
    for category in categories:
        if pm.add_category(category):
            print(f"Added category: {category}")
        else:
            print(f"Failed to add category: {category}")

    all_cats = pm.get_all_categories()
    print(f"All categories: {all_cats}")

    print("\nTest 3: Password Operations")
    test_data = [
        ("github.com", "user1", "encrypted_pass1", "github notes"),
        ("google.com", "user2", "encrypted_pass2", "google notes"),
        ("facebook.com", "user3", "encrypted_pass3", None)
    ]

    for website, username, password, notes in test_data:
        if pm.add_password(website, username, password, notes):
            print(f"Added password for: {website}")
        else:
            print(f"Failed to add password for: {website}")

    github_pass = pm.get_password("github.com")
    if github_pass:
        print(f"Retrieved github password: {github_pass}")
    else:
        print("Failed to retrieve github password")

    if pm.update_password("github.com", "new_encrypted_pass"):
        print("Updated github password")
    else:
        print("Failed to update github password")

    all_passwords = pm.get_all_passwords()
    print(f"Number of stored passwords: {len(all_passwords)}")

    print("\nTest 4: Delete Operations")
    if pm.delete_password("facebook.com"):
        print("Deleted facebook password")
    else:
        print("Failed to delete facebook password")

    if pm.delete_category("Social"):
        print("Deleted Social category")
    else:
        print("Failed to delete Social category")

    db.close()
    
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
        print("\nCleaned up test database")

def test_error_cases(pm):
    print("\nTesting Error Cases:")
    if not pm.add_category("Work"):
        print("Correctly failed to add duplicate category")
    
    if not pm.get_password("nonexistent.com"):
        print("Correctly handled nonexistent website")

def test_edge_cases(pm):
    print("\nTesting Edge Cases:")
    if not pm.add_password("", "", "", ""):
        print("Correctly handled empty strings")
    
    long_string = "a" * 1000
    if pm.add_password(long_string, "user", "pass", "note"):
        print("Handled long string input")

if __name__ == "__main__":
    test_database()
