import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

def fetch_usb_logs():
    """Fetch USB activity logs from the database"""
    conn = sqlite3.connect("usb_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, action FROM logs ORDER BY timestamp ASC")
    logs = cursor.fetchall()
    conn.close()
    return logs

def generate_graph():
    """Generate a graph of USB activity over time"""
    logs = fetch_usb_logs()

    if not logs:
        print("No USB activity data available.")
        return

    timestamps = []
    for log in logs:
        try:
            timestamps.append(datetime.strptime(log[0], "%Y-%m-%d %H:%M:%S.%f"))  # Handle microseconds
        except ValueError:
            timestamps.append(datetime.strptime(log[0], "%Y-%m-%d %H:%M:%S"))  # Handle normal format

    actions = [log[1] for log in logs]

    # Convert actions to numerical values for plotting
    action_values = [1 if "Enabled" in action else -1 for action in actions]

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, action_values, marker="o", linestyle="-", color="blue", label="USB Activity")
    plt.axhline(0, color="black", linewidth=0.5)
    plt.xticks(rotation=45)
    plt.xlabel("Time")
    plt.ylabel("USB Status (1 = Enabled, -1 = Disabled)")
    plt.title("USB Activity Log")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    generate_graph()
