import cv2

cap = cv2.VideoCapture("PennAir 2024 App Dynamic Hard.mp4")

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

processed_video = cv2.VideoWriter("output_video_hard.mp4", fourcc, fps, (width, height), isColor=True)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # meianBlur to reduce noise from the grassy background and
    # without smearing the edges of shapes
    blurred = cv2.medianBlur(frame, 21)

    lower = 50
    upper = 120

    # Mark the edges of the desired shapes and make the image black and white (i.e., a binary image)
    edges = cv2.Canny(blurred, lower, upper)

    # Connect small gaps in the shape boundaries using a rectangular kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    # Dilation followed by erosion, which allows small gaps to be linked with the main structure while keeping
    # size of the edge relatively the same as its original size. 
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=5)

    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:

        # Trace actual outline
        cv2.drawContours(frame, [contour], -1, (128, 255, 128), 2)

        # Calculate center using image moments
        M = cv2.moments(contour)

        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            cv2.circle(frame, (cx, cy), 6, (0, 0, 0), -1)
            cv2.putText(frame, "center", (cx - 25, cy - 10), cv2.FONT_HERSHEY_PLAIN,
                        1, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, f"coords: [{cx, cy}]", (cx - 40, cy + 25), cv2.FONT_HERSHEY_PLAIN,
                        1, (0, 0, 0), 1, cv2.LINE_AA)

    processed_video.write(frame)
    # cv2.imshow("Blurred", blurred)
    # cv2.imshow("Edge", edges)
    cv2.imshow("Processed Video", frame)
    cv2.waitKey(1)

cap.release()
processed_video.release()

cv2.destroyAllWindows()