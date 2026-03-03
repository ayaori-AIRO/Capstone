import cv2
import numpy as np

# 🔹 이미지 경로
path = "/home/ayaori/Capstone/capture/FireExtinguisher_merged.jpg"
img = cv2.imread(path)

# 1️⃣ 그레이스케일 변환
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2️⃣ 노이즈 제거 (가우시안 블러)
blur = cv2.GaussianBlur(gray, (5,5), 0)

# 3️⃣ 대비 향상 (CLAHE)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
enhanced = clahe.apply(blur)

# 4️⃣ Adaptive Thresholding (글자 강조)
thresh = cv2.adaptiveThreshold(enhanced, 255,
                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY_INV, 11, 2)

# 5️⃣ Morphology (글자 연결/잡음 제거)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# 결과 저장
cv2.imwrite("/home/ayaori/Capstone/capture/FireExtinguisher_preprocessed.jpg", morph)
print("전처리 완료: FireExtinguisher_preprocessed.jpg")