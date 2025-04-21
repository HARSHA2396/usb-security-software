import wmi
import sqlite3
import time

LOG_DB = "usb_logs.db"

def log_file_transfer(file_name, action):
    """Log file transfers from MTP devices into the database"""
    conn = sqlite3.connect(LOG_DB)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS file_transfers (timestamp TEXT, file TEXT, action TEXT)")
    cursor.execute("INSERT INTO file_transfers VALUES (datetime('now'), ?, ?)", (file_name, action))
    conn.commit()
    conn.close()

def monitor_mtp_transfers():
    """Monitor MTP file transfers using Windows WMI events"""
    print("Monitoring mobile (MTP) file transfers...")

    c = wmi.WMI()
    watcher = c.watch_for(notification_type="Creation", wmi_class="CIM_DataFile")

    while True:
        try:
            event = watcher()
            if event:
                file_name = event.Name
                print(f"File Copied from Mobile: {file_name}")
                log_file_transfer(file_name, "Copied from Mobile")

        except Exception as e:
            print(f"Error detecting MTP file transfers: {e}")

        time.sleep(5)

if __name__ == "__main__":
    monitor_mtp_transfers()
