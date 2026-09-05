from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='pennair_app',
            executable='stream_video.py',
            name='stream_video_node'
        ),
        Node(
            package='pennair_app',
            executable='video_detection_node.py',
            name='video_detection_node'
        )
    ])