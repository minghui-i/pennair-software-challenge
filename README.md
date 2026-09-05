# PennAir Software Challenge
---

## Part I

### Description

The goal of Part I is to outline the various shapes that are placed on a grassy background in the provided image. 

The solution algorithm features the following process:
1. Blurred the image with `cv2.medianBlur()` to smooth the grassy background while keeping the boundaries of the shapes in the image sharp
2. Ran `cv2.Canny()` edge detection on the blurred image to transform the image into a binary image (black and white) with the shapes' boundaries marked
3. Ran `cv2.morphlogyEx()` with `cv2.MORPHO_CLOSE`to first dilate the image and then erode the image. This fills in small gaps in the edges of the result from Canny from the dilation step and then erodes away the potential white pixels from the shapes' boundaries so that the thickness of the edges doesn't become very large
4. Find the outer contours of the edges of the shapes using `cv2.findContours()`
5. Draw out the contours using `cv2.drawContours()` and also display the center of the shape with (x,y) coordinates in pixel units

### Related Files
- `stastic_image_detection.py`
- `PennAir 2024 App Static.png`

### How to Run
1. Obtain the two related files
2. Put the two files in the same directory in an IDE like VSCode or PyCharm
3. Run the Python file with the play button or right-click on the Python file and select the run option

### Results
<img width="960" height="540" alt="Processed Image" src="https://github.com/user-attachments/assets/37104d3f-0d9b-470c-95e4-59f57cc7c317" />

--- 

## Part II

### Description
The goal of Part II is to run the algorithm from Part I on a video with the shapes moving. 

This was done in the following steps:
1. Read each frame of the video using `cv2.VideoCapture().read()`
2. Apply the algorithm to the current frame
3. Move on to the next frame until there are no more frames

### Related Files
- `video_detection.py`
- `PennAir 2024 App Dynamic.mp4`
  
### How to Run
1. Obtain the two related files
2. Put the two files in the same directory in an IDE like VSCode or PyCharm
3. Change the file name in the creation of the `cv2.VideoCapture()` object from `PennAir 2024 App Dynamic Hard.mp4` to `PennAir 2024 App Dynamic.mp4` (the same file was used in Part III).
4. Run the Python file with the play button or right-click on the Python file and select the run option

### Result
[![Watch the video](https://youtube.com)](https://youtu.be/QYuBO5KDoME)

---

## Part III

### Description
The goal of Part III of the challenge is to allow the algorithm to work with shapes and backgrounds in various colors and textures. 

I found that the general procedure of the algorithm from the last part was able to do a decent job with the new video. I increased the number of iterations of the dilation-erosion step to address the weaker edges being detected by edge detection so that contours can be more reliably found.

### Related Files
- `video_detection.py`
- `PennAir 2024 Dynamic Hard.mp4`

### How to Run
1. Obtain the two related files
2. Put the two files in the same directory in an IDE like VSCode or PyCharm
3. Run the Python file with the play button or right-click on the Python file and select the run option

### Result
[![Watch the video](https://youtube.com)](https://youtu.be/skHTyg2gzO4)

---

## Part IV

### Description

The goal of Part IV is to change the pixel units of (x, y) to their respective real-world units in inches. Additionally, this part of the challenge also involved displaying the real-world distance (Z) between the camera lens and the shapes.

This was achieved by deriving the relationship between the real-world units and pixel units for the x and y directions and then using the following relationship to find Z:

<img width="1275" height="1020" alt="Doc 09-05-2026 17-51-12_page-0001" src="https://github.com/user-attachments/assets/8c4bf63a-dd66-425d-a4ad-64509d3c2784" />

<img width="500" height="600" alt="Doc 09-05-2026 17-51-12_page-0002" src="https://github.com/user-attachments/assets/5f71ebd9-3f7c-49e3-a48e-18d3fe008022" />

### Related Files
- `intrinsic_matrix.py`
- `PennAir 2024 Dynamic.mp4`

### How to Run
1. Obtain the two related files
2. Put the two files in the same directory in an IDE like VSCode or PyCharm
3. Run the Python file with the play button or right-click on the Python file and select the run option

### Result
[![Watch the video](https://youtube.com)](https://youtu.be/R3WnSXBGl5U)

---

## Part V

### Description
The goal of Part V is to host the detection system on `ROS2`. 

This is achieved by creating two nodes and two topics: 
- The first node (`stream_video_node`) is responsible for chopping the video into frames and then publishing the frames to the `video_frames` topic.
- The second node (`video_detection_node`) is responsible for grabbing the video frames by subscribing to the `video_frames` topic and then running the detection algorithm on the obtained frames. Then, this node would publish the detection result (the center point of each shape to the `shape_coordinates` topic.

### Related Files
- `stream_video.py`
- `video_detection_node.py`
- `DetectedShapeCoordinates.msg`
- `pennair_app_launch.py`
- `CMakeList.txt`
- `package.xml`
- `PennAir 2024 Dynamic.mp4`
### How to Run
1. Clone the repo:  
  ```bash
    git clone https://github.com/minghui-i/pennair-software-challenge.git
  ```
3. Open the repo in an IDE
4. Navigate to the project directory:   
  ```bash
    cd ~/PennAirSoftwareChallenge
  ```
5. If `build`, `install`, and `log` exist in the workspace, remove them, as we are going to do a clean rebuild:   
  ```bash
    rm -rf build log install
  ```
7. Build the project:   
  ```bash
    colcon build --packages-select pennair_app
  ```
9. Source the setup script to initialize the environment variables required to run `ROS2 Lyrical` so that the current terminal can execute `ROS2` CLI tools, packages, and libraries:   
 ```bash
   source /opt/ros/lyrical/setup.bash
 ```
11. Also source the setup script in the install folder created from the build so that `ROS2`can find and execute nodes, topics, and launch files that were built:   
   ```bash
     source ~/PennAirSoftwareChallenge/install/setup.bash
   ```
13. Step into the launch directory:   
  ```bash
    cd pennair_app/launch/
  ```
15. Run the launch file to start the nodes:   
  ```bash
    ros2 launch pennair_app_launch.py
  ```
### Result
[![Watch the video](https://youtube.com)](https://youtu.be/10L5VU3jDGk)
