"""
=========================================
Evaluation Exporter
Traffic-Monitoring-System
Version : 1.0.1
=========================================
"""

import os
import csv
import cv2

from evaluation.settings import (
    DATA_FOLDER,
    IMAGE_FOLDER,
    CSV_FILENAME,
    EXPORT_IMAGES,
    IMAGE_PADDING
)


class EvaluationExporter:

    def __init__(self):

        os.makedirs(DATA_FOLDER, exist_ok=True)
        os.makedirs(IMAGE_FOLDER, exist_ok=True)

        self.csv_path = os.path.join(
            DATA_FOLDER,
            CSV_FILENAME
        )

        if not os.path.exists(self.csv_path):

            with open(
                self.csv_path,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([

                    "export_id",
                    "image_name",
                    "track_id",
                    "camera",
                    "direction",
                    "predicted_class",
                    "confidence",
                    "actual_class"

                ])

        self.export_id = self._get_next_export_number()

        print(f"[Evaluation] CSV : {self.csv_path}")
        print(f"[Evaluation] Next Export ID : {self.export_id}")

    # ==================================================
    # Get Next Export Number
    # ==================================================

    def _get_next_export_number(self):

        images = [

            file

            for file in os.listdir(IMAGE_FOLDER)

            if file.startswith("vehicle_")
            and file.endswith(".jpg")

        ]

        if len(images) == 0:

            return 1

        numbers = []

        for file in images:

            try:

                number = int(file.split("_")[1])

                numbers.append(number)

            except ValueError:

                continue

        if len(numbers) == 0:

            return 1

        return max(numbers) + 1

    # ==================================================
    # Save Prediction
    # ==================================================

    def save(

        self,

        frame,

        track,

        camera,

        direction

    ):

        print(f"[Evaluation] SAVE -> ID {track['track_id']}")

        x1, y1, x2, y2 = track["bbox"]

        height, width = frame.shape[:2]

        x1 = max(0, x1 - IMAGE_PADDING)
        y1 = max(0, y1 - IMAGE_PADDING)
        x2 = min(width, x2 + IMAGE_PADDING)
        y2 = min(height, y2 + IMAGE_PADDING)

        crop = frame[
            y1:y2,
            x1:x2
        ]

        if crop.size == 0:

            print("[Evaluation] Invalid Crop")

            return

        image_name = (
            f"vehicle_{self.export_id:04d}_ID{track['track_id']}.jpg"
        )

        image_path = os.path.join(
            IMAGE_FOLDER,
            image_name
        )

        if EXPORT_IMAGES:

            success = cv2.imwrite(
                image_path,
                crop
            )

            print(f"[Evaluation] Image Saved : {success}")

        print(self.csv_path)
        with open(

            self.csv_path,

            "a",

            newline="",

            encoding="utf-8"

        ) as file:

            writer = csv.writer(file)

            writer.writerow([

                self.export_id,

                image_name,

                track["track_id"],

                camera,

                direction,

                track["class"],

                round(track["confidence"], 4),

                ""

            ])
        print("CSV BERHASIL DITULIS")

        print("[Evaluation] CSV Saved")

        self.export_id += 1