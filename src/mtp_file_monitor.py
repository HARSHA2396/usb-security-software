import time
import sqlite3
import win32evtlog

LOG_DB = "usb_logs.db"

def log_file_transfer(file_path, action):
    """Log file transfers from mobile phones (MTP) into database"""
    conn = sqlite3.connect(LOG_DB)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS file_transfers (timestamp TEXT, file TEXT, action TEXT)")
    cursor.execute("INSERT INTO file_transfers VALUES (datetime('now'), ?, ?)", (file_path, action))
    conn.commit()
    conn.close()

def monitor_mtp_transfers():
    """Monitor Windows Event Logs for file transfers from MTP devices"""
    print("Monitoring mobile (MTP) file transfers...")

    while True:
        try:
            # Open Windows Event Log
            hand = win32evtlog.OpenEventLog(None, "Microsoft-Windows-Shell-Core/Operational")

            # Read last 10 events
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            events = win32evtlog.ReadEventLog(hand, flags, 0)

            for event in events:
                if event.EventID in [32791, 32792]:  # Event IDs for file copy operations
                    file_path = event.StringInserts[0] if event.StringInserts else "Unknown File"
                    action = "Copied from Mobile"
                    print(f"File Copied from Mobile: {file_path}")

                    log_file_transfer(file_path, action)

            time.sleep(5)

        except Exception as e:
            print(f"Error reading event logs: {e}")

if __name__ == "__main__":
    monitor_mtp_transfers()
