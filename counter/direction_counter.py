"""
=========================================
Module : Direction Counter
Project : Traffic-Monitoring-System
Version : 2.1.0
=========================================
"""


class DirectionCounter:

    def __init__(
        self,
        line_up_y,
        line_down_y,
        directions
    ):

        # Posisi garis
        self.line_up_y = line_up_y
        self.line_down_y = line_down_y

        # Mapping arah
        self.directions = directions

        # Posisi centroid sebelumnya
        self.previous_positions = {}

        # Track ID yang sudah dihitung
        self.counted_ids = set()

        # Hasil counting
        self.counts = {}

        for direction in directions.values():

            self.counts[direction] = {

                "car": 0,
                "motorcycle": 0,
                "bus": 0,
                "truck": 0

            }

    # ==================================================
    # Update
    # ==================================================

    def update(self, tracks):

        for track in tracks:

            # ------------------------------------------
            # Default (belum dihitung pada frame ini)
            # ------------------------------------------

            track["counted"] = False

            track_id = track["track_id"]

            label = track.get(
                "stable_class",
                track["class"]
            )

            x1, y1, x2, y2 = track["bbox"]

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            track["centroid"] = (
                center_x,
                center_y
            )

            # ------------------------------------------
            # Track baru
            # ------------------------------------------

            if track_id not in self.previous_positions:

                self.previous_positions[track_id] = center_y

                continue

            previous_y = self.previous_positions[track_id]

            self.previous_positions[track_id] = center_y

            # ------------------------------------------
            # Sudah pernah dihitung
            # ------------------------------------------

            if track_id in self.counted_ids:

                continue

            # ==================================================
            # Kendaraan bergerak ke bawah
            # Jakarta → Cikampek
            # ==================================================

            print(
                f"ID={track_id} "
                f"prev={previous_y} "
                f"curr={center_y} "
                f"up={self.line_up_y} "
                f"down={self.line_down_y}"
            )

            if (

                previous_y < self.line_down_y
                and center_y >= self.line_down_y

            ):

                direction = self.directions["down"]

                self.counts[direction][label] += 1

                print(f"COUNTED -> ID {track_id} | {label} | {direction}")

                self.counted_ids.add(track_id)

                track["direction"] = direction

                track["counted"] = True

            # ==================================================
            # Kendaraan bergerak ke atas
            # Cikampek → Jakarta
            # ==================================================

            elif (

                previous_y > self.line_up_y
                and center_y <= self.line_up_y

            ):

                direction = self.directions["up"]

                self.counts[direction][label] += 1

                print(f"COUNTED -> ID {track_id} | {label} | {direction}")

                self.counted_ids.add(track_id)

                track["direction"] = direction

                track["counted"] = True

        return tracks

    # ==================================================
    # Get Counts
    # ==================================================

    def get_counts(self):

        return self.counts