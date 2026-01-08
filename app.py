# import cv2

# STREAM_URL = "http://172.18.230.94:8080/video"
# cap = cv2.VideoCapture(STREAM_URL)

# cv2.namedWindow("Feed", cv2.WINDOW_NORMAL)

# drawing = False
# start_point = (-1, -1)
# current_rect = None
# rectangles = []   # stores completed rectangles

# # Mouse callback
# def draw_rectangles(event, x, y, flags, param):
#     global drawing, start_point, current_rect, rectangles

#     if event == cv2.EVENT_LBUTTONDOWN:
#         if len(rectangles) < 2:          # allow only 2 rectangles
#             drawing = True
#             start_point = (x, y)
#             current_rect = (x, y, x, y)

#     elif event == cv2.EVENT_MOUSEMOVE:
#         if drawing:
#             current_rect = (start_point[0], start_point[1], x, y)

#     elif event == cv2.EVENT_LBUTTONUP:
#         if drawing:
#             drawing = False
#             rectangles.append(current_rect)
#             print(f"Rectangle {len(rectangles)} set:", current_rect)
#             current_rect = None

# cv2.setMouseCallback("Feed", draw_rectangles)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         continue

#     display = frame.copy()

#     # Draw stored rectangles
#     for i, (x1, y1, x2, y2) in enumerate(rectangles):
#         color = (0, 0, 255) if i == 0 else (0, 255, 0)
#         cv2.rectangle(display, (x1, y1), (x2, y2), color, 2)
#         cv2.putText(display,
#                     f"ZONE {i+1}",
#                     (x1, y1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.6,
#                     color,
#                     2)

#     # Draw current rectangle while dragging
#     if current_rect is not None:
#         x1, y1, x2, y2 = current_rect
#         cv2.rectangle(display, (x1, y1), (x2, y2), (255, 0, 0), 1)

#     cv2.imshow("Feed", display)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

import cv2

STREAM_URL = "http://172.18.230.94:8080/video"
cap = cv2.VideoCapture(STREAM_URL)

if not cap.isOpened():
    print("❌ Cannot open stream")
    exit()

cv2.namedWindow("Feed", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Feed", 960, 540)

drawing = False
start_point = (-1, -1)
current_rect = None
rectangles = []   # stores final rectangles (xmin, ymin, xmax, ymax)

# Mouse callback
def draw_rectangles(event, x, y, flags, param):
    global drawing, start_point, current_rect, rectangles

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(rectangles) < 2:
            drawing = True
            start_point = (x, y)
            current_rect = (x, y, x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            current_rect = (start_point[0], start_point[1], x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        if drawing:
            drawing = False
            x1, y1, x2, y2 = current_rect

            # Normalize coordinates
            xmin, xmax = min(x1, x2), max(x1, x2)
            ymin, ymax = min(y1, y2), max(y1, y2)

            rectangles.append((xmin, ymin, xmax, ymax))

            print(f"\nRectangle {len(rectangles)} coordinates:")
            print(f"Top-left     : ({xmin}, {ymin})")
            print(f"Bottom-right : ({xmax}, {ymax})")

            current_rect = None

cv2.setMouseCallback("Feed", draw_rectangles)

print("🖱️ Draw 2 rectangles using mouse. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    display = frame.copy()

    # Draw completed rectangles
    for i, (x1, y1, x2, y2) in enumerate(rectangles):
        color = (0, 0, 255) if i == 0 else (0, 255, 0)
        cv2.rectangle(display, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            display,
            f"ZONE {i+1}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    # Draw rectangle while dragging
    if current_rect is not None:
        x1, y1, x2, y2 = current_rect
        cv2.rectangle(display, (x1, y1), (x2, y2), (255, 0, 0), 1)

    cv2.imshow("Feed", display)

    key = cv2.waitKey(1) & 0xFF

    # Print all rectangles anytime
    if key == ord('p'):
        print("\nAll rectangles:")
        for i, (x1, y1, x2, y2) in enumerate(rectangles):
            print(f"Zone {i+1}: ({x1}, {y1}) -> ({x2}, {y2})")

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
