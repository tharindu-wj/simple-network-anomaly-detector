# Simple Network Anomaly Detector

A lightweight, real-time network traffic monitoring tool that detects anomalies in your network usage. This tool continuously monitors your system's network traffic and alerts you when unusual patterns are detected, such as sudden spikes in upload or download speeds.

## Features

- Real-time monitoring of network upload and download speeds
- Anomaly detection using:
  - Moving average analysis
  - Threshold-based detection
  - Spike detection (3x above moving average)
- Visual console output with status indicators
- Automatic logging of anomalies
- Human-readable data size formatting

## Requirements

- Python 3.x
- pip (Python package installer)

## Installation

1. Clone the repository
2. Install the required packages:

## Running the Project

1. Start the detector:

   ```bash
   python3 main.py
   ``` 

2. Exit the program:
   - Press `Ctrl+C` to stop monitoring
   - The program will save final statistics before exiting

## Usage

The program will display:

- A real-time table showing:
  - Total data received and sent
  - Current download/upload speeds
  - Status indicator (🟢 for normal, 🔴 for anomaly detected)
- Anomaly warnings when detected (⚠️)

## Configuration

You can adjust the following parameters in `main.py`:

- `DOWNLOAD_THRESHOLD`: Maximum normal download speed (default: 5 MB/s)
- `UPLOAD_THRESHOLD`: Maximum normal upload speed (default: 2 MB/s)
- `WINDOW_SIZE`: Number of samples for moving average (default: 10)

## Logs

Detected anomalies are automatically logged to `network_anomalies.log` with timestamps.

## Note

The script uses `os.system('clear')` for screen clearing, which works on Unix-based systems (Linux/MacOS). For Windows, you'll need to modify this to `os.system('cls')`.
