import cv2


def draw_detections(
    frame,
    detections,
    line_up_y=None,
    line_down_y=None,
    directions=None
):

    # ==================================================
    # Draw Counting Lines
    # ==================================================

    if (
        line_up_y is not None
        and line_down_y is not None
    ):

        # --------------------------
        # Line UP
        # --------------------------

        cv2.line(
            frame,
            (0, line_up_y),
            (frame.shape[1], line_up_y),
            (255, 0, 0),
            2
        )

        # --------------------------
        # Line DOWN
        # --------------------------

        cv2.line(
            frame,
            (0, line_down_y),
            (frame.shape[1], line_down_y),
            (0, 0, 255),
            2
        )

        if directions is not None:

            # Label arah atas

            cv2.putText(
                frame,
                f"↑ {directions['up']}",
                (10, line_up_y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2
            )

            # Label arah bawah

            cv2.putText(
                frame,
                f"↓ {directions['down']}",
                (10, line_down_y + 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2
            )

    # ==================================================
    # Draw Detection
    # ==================================================

    for detection in detections:

        x1, y1, x2, y2 = detection["bbox"]

        label_class = detection.get(
            "stable_class",
            detection["class"]
        )

        confidence = detection["confidence"] * 100

        label = (
            f"ID {detection['track_id']} | "
            f"{label_class} | "
            f"{confidence:.1f}%"
        )

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2
        )

    return frame