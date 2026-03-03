import cv2
import json
import os
from ultralytics import YOLO

# 🔥 현재 파일 기준 상위 폴더 경로 얻기
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 🔥 config.json 경로
config_path = os.path.join(BASE_DIR, "config", "config.json")

with open(config_path, "r") as f:
    config = json.load(f)

model_path = config["model_path"]
camera_index_1 = config["camera_index_1"]   # 첫 번째 카메라
camera_index_2 = config["camera_index_2"]   # 두 번째 카메라
width = config["width"]
height = config["height"]
fps = config["fps"]
confidence = config["confidence"]

# 🔥 모델 로드
model = YOLO(model_path)

# 🔥 카메라 설정
cap1 = cv2.VideoCapture(camera_index_1, cv2.CAP_V4L2)
cap2 = cv2.VideoCapture(camera_index_2, cv2.CAP_V4L2)

for cap in [cap1, cap2]:
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, fps)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not cap1.isOpened() or not cap2.isOpened():
    print("❌ 카메라 열기 실패")
    exit()

print("✅ YOLO11 소화기 탐지 시작")

cv2.namedWindow("Camera 1", cv2.WINDOW_NORMAL)
cv2.namedWindow("Camera 2", cv2.WINDOW_NORMAL)

while True:

    # 🔥 오래된 프레임 버리기 (지연 최소화)
    cap1.grab()
    cap2.grab()

    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        print("❌ 프레임 읽기 실패")
        break

    # -----------------------------
    # 🔥 YOLO 추론 (각각 수행)
    # -----------------------------
    results1 = model(frame1, imgsz=640, conf=confidence, verbose=False)
    results2 = model(frame2, imgsz=640, conf=confidence, verbose=False)

    # -----------------------------
    # 🔥 85% 이상만 콘솔 출력
    # -----------------------------
    for i, results in enumerate([results1, results2]):
        for box in results[0].boxes:
            conf_score = float(box.conf[0])
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]

            if conf_score >= 0.85:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                print(f"🔥 Camera {i+1} | {class_name} 감지 | 확률: {conf_score:.2f} | 좌표: ({x1},{y1})~({x2},{y2})")

    # -----------------------------
    # 🔥 결과 시각화
    # -----------------------------
    annotated_frame1 = results1[0].plot()
    annotated_frame2 = results2[0].plot()

    cv2.imshow("Camera 1", annotated_frame1)
    cv2.imshow("Camera 2", annotated_frame2)

    # ESC 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

# -----------------------------
# 5️⃣ 종료
# -----------------------------
cap1.release()
cap2.release()
cv2.destroyAllWindows()

print("🛑 프로그램 종료")