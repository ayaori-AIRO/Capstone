import cv2
import numpy as np

bgr = np.array([[[85, 88, 72]]], dtype=np.uint8)  # OpenCV는 BGR 순서
hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
print(hsv)  # [H, S, V] 확인