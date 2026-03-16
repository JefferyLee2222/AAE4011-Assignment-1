# AAE4011 Assignment 1 — Q3: ROS-Based Vehicle Detection from Rosbag

> **Student Name:Lee Tsz Nam | **Student ID:** 25032937 | **Date:** 16/3/2026

---
1. Overview
This project implements a real-time object detection pipeline using YOLOv5 within a ROS Noetic environment. It processes recorded flight data (Rosbag) from a UAV laboratory to identify persons and equipment, demonstrating the perception capabilities required for autonomous drone navigation.

2. Detection Method (Q3.1 — 2 marks)
The YOLOv5s (Small) architecture was selected for this task.

Reasoning: In Unmanned Aircraft Systems (UAS), computational efficiency is as critical as accuracy. YOLOv5s provides a "single-stage" detection approach that offers high inference speeds (16.4 GFLOPs) suitable for onboard computers like the NVIDIA Jetson series. This allows the drone to react to obstacles in real-time during flight.

3. Repository Structure

aae4011_assignment1/
├── CMakeLists.txt             # Build instructions
├── package.xml                # ROS dependencies
├── scripts/
│   └── vision_node.py         # AI Inference & ROS Subscriber node
├── data/                      # Folder for bag files
└── README.md                  # Documentation
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
Through this assignment, I gained a deep understanding of the ROS Publisher-Subscriber architecture and its role in real-time robotic systems. Specifically, I learned how to bridge raw sensor data (Rosbag) with high-level AI frameworks like YOLOv5 using the cv_bridge library. This process taught me how to manage asynchronous data streams—ensuring that the vision node can subscribe to a specific compressed image topic (/hikcamera/image_2/compressed) and process frames without crashing the system. Additionally, I mastered environment management in WSL, learning to resolve complex dependency conflicts between modern deep learning libraries (Torch/Ultralytics) and legacy Python 3.8 environments.

(b) How Did You Use AI Tools?
I utilized Gemini as a technical collaborator throughout the debugging and implementation phases.

Benefits: The AI was instrumental in identifying obscure syntax errors (e.g., correcting imread_color to the constant IMREAD_COLOR) and providing the necessary export DISPLAY=:0 commands to enable GUI forwarding from WSL to Windows. This significantly accelerated the troubleshooting process.

Limitations: The AI lacked visibility into my local environment. I initially struggled with a "no new messages" error because the AI couldn't know the specific topic names inside my Rosbag. I had to manually use rostopic list to discover the correct data path, proving that AI tools require precise human-provided context to be effective.

(c) How to Improve Accuracy?
Domain-Specific Fine-Tuning: The current model uses pre-trained COCO weights, which are general-purpose. Fine-tuning the model on a custom dataset of UAV-perspective images (top-down views or lab-specific lighting) would drastically reduce false negatives and improve confidence scores for objects like tripods or drones.

Temporal Consistency (Tracking): Implementing a tracking algorithm like DeepSORT alongside YOLO would improve accuracy by maintaining the identity of an object across frames. This prevents "flickering" where an object is detected in one frame but missed in the next due to a slight change in angle or motion blur.

(d) Real-World Challenges
Computational Latency: Running YOLOv5 on a CPU-only environment (like this WSL setup) introduces a latency of ~200ms. In a real flight, this delay is dangerous; at a speed of 5 m/s, the drone would travel 1 meter before even "seeing" an obstacle. Deploying this on a real drone requires hardware acceleration (e.g., NVIDIA Jetson GPU) to reach sub-30ms latency.

Environmental Dynamics: Real-world UAS applications face unpredictable lighting and motion blur. A drone’s vibration or rapid yawing can blur the camera input, causing the feature extraction layers of the AI to fail. Unlike a stable Rosbag recorded in a lab, real-time deployment requires robust image stabilization and models trained to handle high-exposure or low-light conditions.

TensorRT Optimization: Converting the model to TensorRT would allow for FP16 quantization, significantly increasing FPS and reducing detection latency.

(d) Real-World Challenges
Variable Lighting: UAS often operate outdoors where shadows and lens flare can drastically reduce the contrast of objects, leading to false negatives.

Edge Computing Limits: Running complex AI models consumes significant battery power. On a real drone, one must balance the frequency of detection (Hz) against the remaining flight time.
