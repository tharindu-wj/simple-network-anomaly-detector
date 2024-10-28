import os
import time
import psutil
import statistics
from prettytable import PrettyTable
from prettytable import DOUBLE_BORDER
from datetime import datetime

# Units of memory sizes
size = ['bytes', 'KB', 'MB', 'GB', 'TB']

# Network anomaly thresholds (in bytes per second)
DOWNLOAD_THRESHOLD = 1024 * 1024 * 5  # 5 MB/s
UPLOAD_THRESHOLD = 1024 * 1024 * 2    # 2 MB/s

# Window size for moving average
WINDOW_SIZE = 10
download_history = []
upload_history = []

# Function that returns bytes in a readable format
def getSize(bytes):
    for unit in size:
        if bytes < 1024:
            return f"{bytes:.1f}{unit}"
        bytes /= 1024

def detect_anomalies(current_download, current_upload):
    anomalies = []
    
    # Add current values to history
    download_history.append(current_download)
    upload_history.append(current_upload)
    
    # Keep only the last WINDOW_SIZE values
    if len(download_history) > WINDOW_SIZE:
        download_history.pop(0)
    if len(upload_history) > WINDOW_SIZE:
        upload_history.pop(0)
    
    # Calculate moving averages
    if len(download_history) >= 3:
        download_avg = statistics.mean(download_history[:-1])
        upload_avg = statistics.mean(upload_history[:-1])
        
        # Detect sudden spikes (3x the moving average)
        if current_download > download_avg * 3:
            anomalies.append(f"High download spike: {getSize(current_download)}/s")
        if current_upload > upload_avg * 3:
            anomalies.append(f"High upload spike: {getSize(current_upload)}/s")
    
    # Check against absolute thresholds
    if current_download > DOWNLOAD_THRESHOLD:
        anomalies.append(f"Download exceeds threshold: {getSize(current_download)}/s")
    if current_upload > UPLOAD_THRESHOLD:
        anomalies.append(f"Upload exceeds threshold: {getSize(current_upload)}/s")
    
    return anomalies

def printData(anomalies):
    # Creating an instance of PrettyTable class
    card = PrettyTable()
    card.set_style(DOUBLE_BORDER)
    # Column Names of the table
    card.field_names = ["Received", "Receiving", "Sent", "Sending", "Status"]
    
    status = "🟢 Normal"
    if anomalies:
        status = "🔴 Anomaly Detected"
    
    card.add_row([
        f"{getSize(netStats2.bytes_recv)}", 
        f"{getSize(downloadStat)}/s", 
        f"{getSize(netStats2.bytes_sent)}", 
        f"{getSize(uploadStat)}/s",
        status
    ])
    
    print(card)
    
    if anomalies:
        print("\nAnomalies detected:")
        for anomaly in anomalies:
            print(f"⚠️  {anomaly}")
            
        # Log anomalies to file
        with open("network_anomalies.log", "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for anomaly in anomalies:
                f.write(f"{timestamp} - {anomaly}\n")

# psutil.net_io_counters() returns network I/O statistics as a namedtuple
netStats1 = psutil.net_io_counters()

# Getting the data of total bytes sent and received
dataSent = netStats1.bytes_sent
dataRecv = netStats1.bytes_recv

# Running a loop to get the data continuously
while True:
    # Delay for one second
    time.sleep(1)

    # Clear the Terminal or Console
    # For Windows: use 'cls'
    # For Linux and Mac, keep it as it is
    os.system('clear')

    # Getting the network i/o stats again to 
    # count the sending and receiving speed
    netStats2 = psutil.net_io_counters()

    # Upload/Sending speed
    uploadStat = netStats2.bytes_sent - dataSent
    # Receiving/Download Speed
    downloadStat = netStats2.bytes_recv - dataRecv

    # Detect anomalies
    anomalies = detect_anomalies(downloadStat, uploadStat)

    # Print the Data
    printData(anomalies)

    # Agian getting the data of total bytes sent and received
    dataSent = netStats2.bytes_sent
    dataRecv = netStats2.bytes_recv
