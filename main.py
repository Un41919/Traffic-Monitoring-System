"""
=========================================
Main Application
Traffic-Monitoring-System
Version : 0.6.1
=========================================
"""

import cv2
import time

from stream.stream_config import CAMERAS

from config import COUNTING_CONFIG

from detection.detector import Detector

from tracking.tracker import Tracker
from tracking.stabilizer import LabelStabilizer

from counter.direction_counter import DirectionCounter

from utils.draw import draw_detections

from evaluation.export_predictions import EvaluationExporter
from database.database import Database


# ==================================================
# Camera Selection
# ==================================================

print("=" * 45)
print("      BINA MARGA LIVE CCTV")
print("=" * 45)

for key, camera in CAMERAS.items():
    print(f"{key}. {camera['name']}")

print("=" * 45)

choice = input("Choose Camera : ")

if choice not in CAMERAS:

    print("Invalid camera selection.")
    exit()

camera = CAMERAS[choice]

counting_config = COUNTING_CONFIG[choice]

print(f"\nOpening {camera['name']}...\n")


# ==================================================
# Initialize Modules
# ==================================================

detector = Detector()

tracker = Tracker()

stabilizer = LabelStabilizer()

counter = DirectionCounter(
    line_up_y=counting_config["line_up_y"],
    line_down_y=counting_config["line_down_y"],
    directions={
        "up": counting_config["up"],
        "down": counting_config["down"]
    }
)

exporter = EvaluationExporter()

database = Database()

# ==================================================
# Open Stream
# ==================================================

cap = cv2.VideoCapture(camera["url"])

if not cap.isOpened():

    print("Failed to open stream.")
    exit()


# ==================================================
# Main Loop
# ==================================================

frame_count = 0

while True:

    # ==========================================
    # Start Timer (FPS)
    # ==========================================

    start = time.time()

    # ==========================================
    # Read Frame
    # ==========================================

    ret, frame = cap.read()

    if not ret:

        print("Failed to read frame.")
        break

    frame_count += 1

    # ==========================================
    # Detector
    # ==========================================

    detections = detector.detect(frame)

    # ==========================================
    # Tracker
    # ==========================================

    tracks = tracker.update(
        detector.last_sv_detections
    )

    # ==========================================
    # Label Stabilizer
    # ==========================================

    tracks = stabilizer.update(
        tracks
    )

    # ==========================================
    # Direction Counter
    # ==========================================

    tracks = counter.update(
        tracks
    )

    # ==========================================
    # Evaluation Export
    # ==========================================

    for track in tracks:

        print(track)

        if track["counted"]:

            exporter.save(
                frame=frame,
                track=track,
                camera=camera["name"],
                direction=track["direction"]
            )

            database.insert_vehicle(
                camera=camera["name"],
                track_id=track["track_id"],
                vehicle_type=track.get("stable_class", track["class"]),
                direction=track["direction"],
                confidence=round(track["confidence"], 4)
            )

    # ==========================================
    # Draw
    # ==========================================
    
    frame = draw_detections(
        frame,
        tracks,
        line_up_y=counting_config["line_up_y"],
        line_down_y=counting_config["line_down_y"],
        directions={
            "up": counting_config["up"],
            "down": counting_config["down"]
        }
    )

    # ==========================================
    # FPS
    # ==========================================

    elapsed = time.time() - start

    if elapsed > 0:
        fps = 1 / elapsed
    else:
        fps = 0

    # ==========================================
    # Debug Output
    # ==========================================

    if frame_count % 30 == 0:

        counts = counter.get_counts()

        print("\n" + "=" * 60)

        print(f"Frame : {frame_count}")
        print(f"FPS   : {fps:.2f}")

        print("-" * 60)

        for direction, vehicles in counts.items():

            print(direction)

            for vehicle, total in vehicles.items():

                print(f"{vehicle:<12}: {total}")

            print()

        print("=" * 60)

    # ==========================================
    # Display
    # ==========================================

    cv2.imshow(
        camera["name"],
        frame
    )

    # ==========================================
    # Exit
    # ==========================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# ==================================================
# Release
# ==================================================

database.close()

cap.release()

cv2.destroyAllWindows()