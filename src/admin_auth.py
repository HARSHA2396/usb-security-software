import bcrypt
import sqlite3

DB_FILE = "admin.db"

def create_admin_account():
    """Create an admin account with a secure password (Run only once)"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("CREATE TABLE IF NOT EXISTS admin (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())  # Encrypt password
    
    cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()
    
    print("Admin account created successfully!")

def verify_admin(username, password):
    """Verify admin login before allowing USB changes"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT password FROM admin WHERE username = ?", (username,))
    result = cursor.fetchone()
    
    if result and bcrypt.checkpw(password.encode(), result[0]):
        return True  # Authentication successful
    else:
        return False  # Incorrect credentials

if __name__ == "__main__":
    create_admin_account()  # Run this once to create an admin
