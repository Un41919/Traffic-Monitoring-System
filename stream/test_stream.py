import cv2
from stream_config import CAMERAS

print("=" * 40)
print("    BINA MARGA LIVE CCTV")
print("=" * 40)

for key, camera in CAMERAS.items():
    print(f"{key}. {camera['name']}")

print("=" * 40)

choice = input("Choose Camera : ")

if choice not in CAMERAS:
    print("Pilihan tidak tersedia.")
    exit()

camera_name = CAMERAS[choice]["name"]
camera_url = CAMERAS[choice]["url"]

print(f"\nOpening {camera_name}...")

cap = cv2.VideoCapture(camera_url)

if not cap.isOpened():
    print("Gagal membuka stream.")
    exit()

cv2.namedWindow(camera_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(camera_name, 1280, 720)

while True:

    ret, frame = cap.read()

    if not ret:
        print("Frame gagal dibaca.")
        break

    cv2.imshow(camera_name, frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()