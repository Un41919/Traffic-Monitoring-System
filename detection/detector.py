"""
=========================================
Module : Detector
Project : Traffic-Monitoring-System
=========================================
"""

from ultralytics import YOLO
import supervision as sv

from config import (
    MODEL_PATH,
    CONFIDENCE_THRESHOLD,
    VALID_CLASS_IDS,
    CLASS_NAMES
)


class Detector:

    def __init__(self):

        self.model = YOLO(MODEL_PATH)

        # Hasil untuk Tracker
        self.last_sv_detections = None

    def detect(self, frame):

        # ==========================================
        # YOLO Inference
        # ==========================================

        results = self.model(
            frame,
            imgsz=960,
            conf=CONFIDENCE_THRESHOLD,
            verbose=False
        )

        result = results[0]

        # ==========================================
        # Convert ke Supervision
        # ==========================================

        sv_detections = sv.Detections.from_ultralytics(result)

        keep_index = []

        detections = []

        # ==========================================
        # Filter Vehicle Classes
        # ==========================================

        for i, box in enumerate(result.boxes):

            cls_id = int(box.cls[0])

            # Hanya kendaraan
            if cls_id not in VALID_CLASS_IDS:
                continue

            keep_index.append(i)

            confidence = float(box.conf[0])

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            detections.append({

                "class_id": cls_id,

                "class": CLASS_NAMES[cls_id],

                "confidence": confidence,

                "bbox": (
                    x1,
                    y1,
                    x2,
                    y2
                )

            })

        # ==========================================
        # Simpan hasil yang sudah difilter
        # untuk Tracker
        # ==========================================

        self.last_sv_detections = sv_detections[keep_index]

        return detections