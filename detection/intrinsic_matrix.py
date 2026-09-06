import math
import cv2

cap = cv2.VideoCapture("PennAir 2024 App Dynamic.mp4")

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

processed_video = cv2.VideoWriter("output_video_real_units.mp4", fourcc, fps, (width, height), isColor=True)

#Constants
f_x = 2564.3186869
f_y = 2569.70273111

radius_pixel = 0
radius_real_inch = 10

ratio_from_pixel_to_real = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Smooth out much of the tiny grass texture
    blurred = cv2.medianBlur(frame, 21)

    lower = 50
    upper = 120

    # Detect boundaries
    edges = cv2.Canny(blurred, lower, upper)

    # Connect small gaps in the shape boundaries
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=5)

    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if radius_pixel == 0:
        circularities = []

        for contour in contours:

            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)

            circularity = (4 * math.pi * area) / (perimeter**2)
            circularities.append(circularity)

        index_of_max_circularity = circularities.index(max(circularities))

        _, radius_pixel = cv2.minEnclosingCircle(contours[index_of_max_circularity])
        ratio_from_pixel_to_real = radius_real_inch / radius_pixel

    for contour in contours:

        # Trace actual outline
        cv2.drawContours(frame, [contour], -1, (128, 255, 128), 2)

        # Calculate center using image moments
        M = cv2.moments(contour)

        if M["m00"] != 0:
            # x, y coordinates in pixel in the center
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            x_real = cx * ratio_from_pixel_to_real
            y_real = cy * ratio_from_pixel_to_real

            z_real_from_x = (x_real * f_x) / cx
            z_real_from_y = (y_real * f_y) / cy

            average_z_real = (z_real_from_x + z_real_from_y) / 2

            cv2.circle(frame, (cx, cy), 6, (0, 0, 0), -1)
            cv2.putText(frame, "center", (cx - 25, cy - 10), cv2.FONT_HERSHEY_PLAIN,
                        1, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, "(X, Y, Z)", 
                        (cx - 40, cy + 25), cv2.FONT_HERSHEY_PLAIN,
                        1, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, f"coords: [{x_real, y_real, average_z_real}]", 
                        (cx - 120, cy + 45), cv2.FONT_HERSHEY_PLAIN,
                        1, (0, 0, 0), 1, cv2.LINE_AA)

    processed_video.write(frame)
    cv2.imshow("Processed Video", frame)
    cv2.waitKey(1)

cap.release()
processed_video.release()

cv2.destroyAllWindows()