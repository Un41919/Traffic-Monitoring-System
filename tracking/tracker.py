"""
=========================================
Module : Tracker
Project : Traffic-Monitoring-System
=========================================
"""

import supervision as sv

from config import CLASS_NAMES


class Tracker:

    def __init__(self):

        self.tracker = sv.ByteTrack()

    def update(self, detections):

        """
        Parameter
        ---------
        detections : sv.Detections
            Hasil detector yang sudah difilter.
        """

        tracked = self.tracker.update_with_detections(
            detections
        )

        tracks = []

        for i in range(len(tracked.xyxy)):

            x1, y1, x2, y2 = map(int, tracked.xyxy[i])

            class_id = int(tracked.class_id[i])

            confidence = float(tracked.confidence[i])

            track_id = int(tracked.tracker_id[i])

            tracks.append({

                "track_id": track_id,

                "class_id": class_id,

                "class": CLASS_NAMES[class_id],

                "confidence": confidence,

                "bbox": (
                    x1,
                    y1,
                    x2,
                    y2
                )

            })

        return tracks