import cv2

ESP32_IP = "10.86.87.117"
STREAM_URL = f"http://{ESP32_IP}:81/stream"

# Use FFMPEG backend (IMPORTANT for ESP32 MJPEG)
cap = cv2.VideoCapture(STREAM_URL, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("❌ Cannot open ESP32 stream")
    exit()

print("✅ ESP32 stream opened")

while True:
    ret, frame = cap.read()

    if not ret:
        print("❌ Frame not received")
        continue

    # ===== OpenCV processing (example) =====
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    # ======================================

    cv2.imshow("ESP32-CAM Live (OpenCV)", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
