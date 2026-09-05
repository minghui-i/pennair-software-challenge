#!/usr/bin/env python3

import cv2
import rclpy

from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class VideoStreamNode(Node):

    def __init__(self):
        super().__init__("video_stream_node")

        self.publisher_ = self.create_publisher(Image,"video_frames", 10)

        self.bridge = CvBridge()

        self.cap = cv2.VideoCapture("/home/minghuiz/PennAirSoftwareChallenge/pennair_app/launch/PennAir 2024 App Dynamic.mp4")

        if not self.cap.isOpened():
            self.get_logger().error("Could not open video!")
            return

        # Wait 1/30 of a sec before publising the next frame
        self.timer = self.create_timer(
            1.0 / 30.0,
            self.publish_video_frame
        )

    def publish_video_frame(self):

        ret, frame = self.cap.read()

        if not ret:
            self.get_logger().info("Video finished")
            self.timer.cancel()
            self.cap.release()
            return

        msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")

        self.publisher_.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    node = VideoStreamNode()

    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()