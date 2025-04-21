import sqlite3
import datetime

def log_usb_event(action):
    """Log USB enable/disable actions"""
    conn = sqlite3.connect("usb_logs.db")  
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS logs (timestamp TEXT, action TEXT)")
    
    # Store timestamp in ISO format to avoid deprecation warnings
    timestamp = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
    cursor.execute("INSERT INTO logs VALUES (?, ?)", (timestamp, action))
    
    conn.commit()
    conn.close()

def get_usb_logs():
    """Fetch USB activity logs from the database"""
    conn = sqlite3.connect("usb_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC")
    logs = cursor.fetchall()
    conn.close()
    return logs  # Returns a list of (timestamp, action) tuples

if __name__ == "__main__":
    log_usb_event("USB Disabled")  # Test logging
    print(get_usb_logs())  # Print logs to verify
