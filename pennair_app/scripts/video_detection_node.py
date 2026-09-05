#!/usr/bin/env python3
import cv2
from cv_bridge import CvBridge

import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from sensor_msgs.msg import Image
from pennair_app.msg import DetectedShapeCoordinates


class VideoDetectionNode(Node):
    def __init__(self):
        super().__init__("video_detection_node")
        self.publisher = self.create_publisher(DetectedShapeCoordinates, "shape_coordinates", 10)
        self.subscription = self.create_subscription(Image, "video_frames", self.listener_callback, 10)

        self.f_x = 2564.3186869
        self.f_y = 2569.70273111
        self.radius_pixel = 0
        self.radius_real_inch = 10
        self.ratio_from_pixel_to_real = 0

        self.frame_counter = 0
        self.bridge = CvBridge()

    def listener_callback(self, msg):
        self.get_logger().info("Received a video frame!")
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        detected_coordinates_list = self.detect_shape_coordinates(cv_image)

        detected_shape_msg = DetectedShapeCoordinates()
        detected_shape_msg.frame_number = self.frame_counter

        for coordinate in detected_coordinates_list:
            (x_real, y_real, average_z_real) = coordinate
            point = Point()
            point.x = x_real
            point.y = y_real
            point.z = average_z_real
            detected_shape_msg.points.append(point)

        self.publisher.publish(detected_shape_msg)

        self.frame_counter += 1


    def detect_shape_coordinates(self, cv_image):
        # meianBlur to reduce noise from the grassy background and
        # without smearing the edges of shapes
        blurred = cv2.medianBlur(cv_image, 21)

        lower = 50
        upper = 120

        # Mark the edges of the desired shapes and make the image black and white (i.e., a binary image)
        edges = cv2.Canny(blurred, lower, upper)

        # Connect small gaps in the shape boundaries using a rectangular kernel
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        # Dilation followed by erosion, which allows small gaps to be linked with the main structure while keeping
        # size of the edge relatively the same as its original size. 
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=5)

        # Find the outer contours and save memory using CHAIN_APPOX_SIMPLE by removing redundant points
        contours, _ = cv2.findContours(edges,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if self.radius_pixel == 0:
            circularities = []

            for contour in contours:

                area = cv2.contourArea(contour)
                perimeter = cv2.arcLength(contour, True)

                # Calculate the circularity for each shape
                circularity = (4 * math.pi * area) / (perimeter**2)
                circularities.append(circularity)

            # The cirle would have the higest circularity 
            index_of_max_circularity = circularities.index(max(circularities))

            # We then get the radius of that circle in pixels
            _, self.radius_pixel = cv2.minEnclosingCircle(contours[index_of_max_circularity])

            # Calculate the ratio that we need to convert other pixel units to real world units of inches
            self.ratio_from_pixel_to_real = self.radius_real_inch / self.radius_pixel

        coordinates = []

        for contour in contours:

            # Calculate center using image moments
            M = cv2.moments(contour)

            if M["m00"] != 0:
                # x, y coordinates in pixel in the center
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                x_real = cx * self.ratio_from_pixel_to_real
                y_real = cy * self.ratio_from_pixel_to_real

                z_real_from_x = (x_real * self.f_x) / cx
                z_real_from_y = (y_real * self.f_y) / cy

                average_z_real = (z_real_from_x + z_real_from_y) / 2

                coordinates.append((x_real, y_real, average_z_real))

        return coordinates

def main(args=None):
    rclpy.init(args=args)
    node = VideoDetectionNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()

