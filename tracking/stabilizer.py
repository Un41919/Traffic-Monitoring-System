"""
=========================================
Module : Label Stabilizer
Project : Traffic-Monitoring-System
Version : 2.1.0
=========================================
"""

from collections import deque, Counter


class LabelStabilizer:

    def __init__(
        self,
        history_size=10,
        stable_threshold=0.80,
        max_missing_frames=30
    ):

        # Jumlah history label yang disimpan
        self.history_size = history_size

        # Persentase minimum agar label dianggap stabil
        self.stable_threshold = stable_threshold

        # Maksimum frame hilang sebelum history dihapus
        self.max_missing_frames = max_missing_frames

        # History label tiap Track ID
        self.history = {}

        # Counter frame hilang tiap Track ID
        self.missing_counter = {}

    def update(self, tracks):

        active_ids = set()

        # =====================================
        # Update history setiap Track ID
        # =====================================

        for track in tracks:

            track_id = track["track_id"]
            current_class = track["class"]

            active_ids.add(track_id)

            # Track baru
            if track_id not in self.history:

                self.history[track_id] = deque(
                    maxlen=self.history_size
                )

            # Reset missing counter
            self.missing_counter[track_id] = 0

            # Simpan history label
            self.history[track_id].append(
                current_class
            )

            # Cari label mayoritas
            stable_class, ratio = self._get_stable_label(
                self.history[track_id]
            )

            # Jika sudah stabil gunakan stable_class
            if ratio >= self.stable_threshold:

                track["stable_class"] = stable_class

            else:

                track["stable_class"] = current_class

            # Tambahan informasi
            track["stable_ratio"] = ratio

        # =====================================
        # Update missing counter
        # =====================================

        self._update_missing_counter(active_ids)

        return tracks

    def _get_stable_label(self, labels):

        counter = Counter(labels)

        label, count = counter.most_common(1)[0]

        ratio = count / len(labels)

        return label, ratio

    def _update_missing_counter(self, active_ids):

        remove_ids = []

        for track_id in list(self.history.keys()):

            if track_id in active_ids:
                continue

            if track_id not in self.missing_counter:

                self.missing_counter[track_id] = 0

            self.missing_counter[track_id] += 1

            if self.missing_counter[track_id] >= self.max_missing_frames:

                remove_ids.append(track_id)

        # Hapus Track ID yang benar-benar sudah hilang
        for track_id in remove_ids:

            del self.history[track_id]

            del self.missing_counter[track_id]