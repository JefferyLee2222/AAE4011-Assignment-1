# AAE4011 Assignment 1 — Q3: ROS-Based Vehicle Detection from Rosbag

> **Student Name:Lee Tsz Nam | **Student ID:** 25032937 | **Date:** 16/3/2026

---
1. Overview
This project implements a real-time object detection pipeline using YOLOv5 within a ROS Noetic environment. It processes recorded flight data (Rosbag) from a UAV laboratory to identify persons and equipment, demonstrating the perception capabilities required for autonomous drone navigation.

2. Detection Method (Q3.1 — 2 marks)
The YOLOv5s (Small) architecture was selected for this task.

Reasoning: In Unmanned Aircraft Systems (UAS), computational efficiency is as critical as accuracy. YOLOv5s provides a "single-stage" detection approach that offers high inference speeds (16.4 GFLOPs) suitable for onboard computers like the NVIDIA Jetson series. This allows the drone to react to obstacles in real-time during flight.

3. Repository Structure
Plaintext
aae4011_assignment1
CMakeLists.txt
package.xml
scripts/
    vision_node.py
data/
            2026-02-02-17-57-27.bag
    README.md
5. Prerequisites
Operating System: Ubuntu 20.04 (WSL2 on Windows 11)

Middleware: ROS Noetic

Language: Python 3.8.10

Dependencies:

torch==2.2.0

ultralytics (YOLOv5 Engine)

cv_bridge (ROS-to-OpenCV conversion)

pandas, numpy, opencv-python

5. How to Run (Q3.1 — 2 marks)
Follow these steps to launch the perception pipeline:

Initialize Workspace:

Bash
cd ~/catkin_ws
catkin_make
source devel/setup.bash
Start ROS Master:

Bash
roscore
Play the Rosbag:

Bash
# Ensure the 918MB file is used
rosbag play ~/catkin_ws/2026-02-02-17-57-27.bag --clock -l
Launch Detection Node :

Bash
export DISPLAY=:0  # Required for WSL UI window
python3 src/aae4011_assignment1/scripts/vision_node.py
6. Sample Results
Topic Name: /hikcamera/image_2/compressed

Input Resolution: 1920 x 1080

Observation: The system successfully identifies multiple "person" entities and "tripod" equipment within the lab. The average inference time on CPU is approximately 180ms per frame.

7. Video Demonstration (Q3.2 — 5 marks)
Video Link: (https://youtu.be/HiYFep62dq8)

8. Reflection & Critical Analysis (Q3.3 — 8 marks)
(a) What Did You Learn?
I gained hands-on experience in System Integration within a robotics context. Specifically, I learned how to handle asynchronous data streams in ROS and solve Version Compatibility issues between modern AI frameworks (Torch 2.2) and legacy environments (Python 3.8).

(b) How Did You Use AI Tools?
I utilized Gemini as a technical collaborator to debug environment-specific errors.

Benefits: It provided immediate solutions for ModuleNotFoundError and correctly identified the need for IMREAD_COLOR over lowercase variants in OpenCV.

Limitations: The AI could not initially "see" my local file system; I had to manually use rostopic list to discover that the camera topic was named /hikcamera instead of the standard /camera.

(c) How to Improve Accuracy?
Data Augmentation: Training the model on images with Motion Blur would help the drone maintain detection accuracy during high-speed maneuvers.

TensorRT Optimization: Converting the model to TensorRT would allow for FP16 quantization, significantly increasing FPS and reducing detection latency.

(d) Real-World Challenges
Variable Lighting: UAS often operate outdoors where shadows and lens flare can drastically reduce the contrast of objects, leading to false negatives.

Edge Computing Limits: Running complex AI models consumes significant battery power. On a real drone, one must balance the frequency of detection (Hz) against the remaining flight time.
