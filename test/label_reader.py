import cv2
import pytesseract
import re
from PIL import Image

# 이미지 경로
image_path = "/home/ayaori/Capstone/capture/FireExtinguisher.jpg"

# OpenCV로 이미지 읽기
img = cv2.imread(image_path)

# 흑백으로 변환해서 OCR 정확도 향상
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# pytesseract로 텍스트 추출
text = pytesseract.image_to_string(gray, lang='kor+eng')  # 필요하면 lang='kor+eng'

print("전체 추출 텍스트:")
print(text)