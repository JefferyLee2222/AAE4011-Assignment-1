#!/usr/bin/env python3
import rospy
import cv2
import torch
import numpy as np
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge

class DroneDetector:
    def __init__(self):

        rospy.loginfo("Loading YOLOv5...")

        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True, trust_repo=True)
        
        self.bridge = CvBridge()
        
        self.sub = rospy.Subscriber("/hikcamera/image_2/compressed", CompressedImage, self.callback)
        
        rospy.loginfo("Listening to /hikcamera/image_2/compressed... Please run 'rosbag play'")

    def callback(self, data):
        try:
            np_arr = np.frombuffer(data.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if cv_image is not None:

                results = self.model(cv_image)
                
                
                annotated_image = np.squeeze(results.render())

                
                cv2.imshow("AAE4011_YOLO_Detection", annotated_image)
                cv2.waitKey(1)
                
                rospy.loginfo("Received an image and detected objects!")
            else:
                rospy.logwarn("Decoded image is None")

        except Exception as e:
            rospy.logerr(f"Error in callback: {e}")

if __name__ == '__main__':
    try:
        rospy.init_node('vision_node')
        node = DroneDetector()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    finally:
        cv2.destroyAllWindows()