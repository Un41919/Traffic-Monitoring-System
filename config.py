# ==========================
# YOLO MODEL
# ==========================

MODEL_PATH = "yolo11s.pt"


# ==========================
# Detection
# ==========================

CONFIDENCE_THRESHOLD = 0.50


# ==========================
# COCO Vehicle Class IDs
# ==========================

VALID_CLASS_IDS = [
    2,  # car
    3,  # motorcycle
    5,  # bus
    7   # truck
]


# ==========================
# Class Mapping
# ==========================

CLASS_NAMES = {

    2: "car",

    3: "motorcycle",

    5: "bus",

    7: "truck"

}


# ==========================
# Counting Configuration
# ==========================

COUNTING_CONFIG = {

    "1": {

        "line_up_y": 460,

        "line_down_y": 550,

        "up": "Cikampek → Jakarta",

        "down": "Jakarta → Cikampek"

    },

    "2": {

        "line_up_y": 450,

        "line_down_y": 540,

        "up": "Jakarta → Cikampek",

        "down": "Cikampek → Jakarta"

    },

    "3": {

        "line_up_y": 460,

        "line_down_y": 550,

        "up": "Cikampek → Jakarta",

        "down": "Jakarta → Cikampek"

    }

}