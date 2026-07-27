# Traffic Monitoring System

A real-time traffic monitoring system that integrates YOLO11, ByteTrack, SQLite, and Power BI to detect, track, store, and visualize vehicle traffic from CCTV streams.

---

## Overview

This project performs real-time vehicle detection and tracking using CCTV video streams. Detection results are stored in a SQLite database and visualized through an interactive Power BI dashboard for traffic monitoring and analysis.

---

## Features

- Real-time vehicle detection using YOLO11
- Multi-object tracking using ByteTrack
- SQLite database integration
- Interactive Power BI dashboard
- Traffic density monitoring
- Vehicle distribution analysis
- Vehicle count over time
- Latest detection log
- Traffic summary statistics
- Multi-camera ready architecture

---

## Demo

Watch the complete demonstration:

https://youtu.be/jEQJad6PAXg

---

## Technologies

- Python
- YOLO11
- ByteTrack
- OpenCV
- SQLite
- Power BI Desktop

---

## Project Structure

```text
Traffic-Monitoring-System/
│
├── dashboard/
│   └── Traffic Monitoring Dashboard.pbix
├── database/
│   └── traffic.db
├── models/
├── src/
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the application:

```bash
python main.py
```

1. Select the CCTV camera to monitor.
2. Start the real-time detection process.
3. Open:

```text
Traffic Monitoring Dashboard.pbix
```

using Microsoft Power BI Desktop.

4. Click **Home → Refresh** to update the dashboard with the latest data from the SQLite database.

---

## Dashboard

The Power BI dashboard provides the following monitoring information:

- Traffic Density
- Vehicle Distribution
- Vehicle Count Over Time
- Latest Detection
- Summary Statistics
- Last Update

---

## Limitations

This project is developed as a prototype for real-time traffic monitoring. Detection performance may vary depending on several real-world factors, including:

- Vehicle occlusion
- CCTV image quality
- Motion blur
- Small object size at long distances
- Lighting conditions
- Available hardware resources

These limitations are common in computer vision-based traffic monitoring systems and can be improved through model fine-tuning, higher-quality video sources, and more powerful hardware.

---

## Author

Nailul Muna
