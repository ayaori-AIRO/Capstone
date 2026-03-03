import cv2
import os
from datetime import datetime

# 🔥 저장 폴더
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
capture_dir = os.path.join(BASE_DIR, "capture")
os.makedirs(capture_dir, exist_ok=True)

# 🔥 카메라 번호 (4번, 2번)
cap1 = cv2.VideoCapture(4, cv2.CAP_V4L2)
cap2 = cv2.VideoCapture(2, cv2.CAP_V4L2)

if not cap1.isOpened() or not cap2.isOpened():
    print("❌ 카메라 열기 실패")
    exit()

print("✅ 카메라 실행됨")
print("📸 'c' 누르면 캡쳐")
print("🛑 ESC 누르면 종료")

cv2.namedWindow("Camera 1", cv2.WINDOW_NORMAL)
cv2.namedWindow("Camera 2", cv2.WINDOW_NORMAL)

while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        print("❌ 프레임 읽기 실패")
        break

    cv2.imshow("Camera 1", frame1)
    cv2.imshow("Camera 2", frame2)

    key = cv2.waitKey(1) & 0xFF

    # ESC 종료
    if key == 27:
        break

    # 'c' 누르면 캡쳐
    if key == ord('c'):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        path1 = os.path.join(capture_dir, f"cam1_{timestamp}.jpg")
        path2 = os.path.join(capture_dir, f"cam2_{timestamp}.jpg")

        cv2.imwrite(path1, frame1)
        cv2.imwrite(path2, frame2)

        print(f"📸 저장 완료:\n{path1}\n{path2}")

cap1.release()
cap2.release()
cv2.destroyAllWindows()

print("🛑 프로그램 종료")