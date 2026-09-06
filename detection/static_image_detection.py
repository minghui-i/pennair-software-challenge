import cv2

image = cv2.imread("PennAir 2024 App Static.png")

# meianBlur to reduce noise from the grassy background and
# without smearing the edges of shapes
blurred = cv2.medianBlur(image, 21)

lower = 50
upper = 120

# Mark the edges of the desired shapes and make the image black and white (i.e., a binary image)
edges = cv2.Canny(blurred, lower, upper)

# Connect small gaps in the shape boundaries using a rectangular kernel
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
# Dilation followed by erosion, which allows small gaps to be linked with the main structure while keeping
# size of the edge relatively the same as its original size. 
edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

# Find the outer contours and save memory using CHAIN_APPOX_SIMPLE by removing redundant points
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:

    # Trace actual outline
    cv2.drawContours(image, [contour], -1, (128, 255, 128), 2)

    # Calculate center using image moments
    M = cv2.moments(contour)

    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        cv2.circle(image, (cx, cy), 6, (0, 0, 0), -1)
        cv2.putText(image, "center", (cx - 25, cy - 10), cv2.FONT_HERSHEY_PLAIN,
                    1, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, f"coords: [{cx, cy}]", (cx - 40, cy + 25), cv2.FONT_HERSHEY_PLAIN,
                    1, (0, 0, 0), 1, cv2.LINE_AA)

cv2.imshow("Processed Image", image)
cv2.imwrite("Processed Image.png", image)
cv2.waitKey(0)

cv2.destroyAllWindows()