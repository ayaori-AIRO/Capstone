import cv2
import json
import os
import time

import serial
from serial.tools import list_ports
from ultralytics import YOLO


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_CONFIG_PATH = os.path.join(BASE_DIR, "config", "model_config.json")
CAMERA_CONFIG_PATH = os.path.join(BASE_DIR, "config", "camera_config.json")
NEOPIXEL_PORT = "/dev/ttyACM0"


def find_arduino_port():
    ports = list(list_ports.comports())

    for port in ports:
        text = f"{port.device} {port.description} {port.manufacturer or ''}".lower()
        if "arduino" in text or "ch340" in text or "usb serial" in text:
            return port.device

    if ports:
        return ports[0].device

    return None


def open_neopixel(port=None):
    port = port or find_arduino_port()

    if port is None:
        raise RuntimeError("시리얼 포트를 찾지 못했습니다.")

    ser = serial.Serial(port, 9600, timeout=1)
    time.sleep(2)
    ser.reset_input_buffer()
    print(f"NeoPixel 연결 완료: {port}")
    return ser


def send_neopixel(ser, command):
    ser.write(f"{command}\n".encode("utf-8"))
    return ser.readline().decode("utf-8", errors="ignore").strip()


with open(MODEL_CONFIG_PATH, "r") as f:
    model_config = json.load(f)

with open(CAMERA_CONFIG_PATH, "r") as f:
    camera_config = json.load(f)

FireExtinguisher_model_path = model_config["FireExtinguisher_model_path"]
pressure_gauge_model_path = model_config["pressure_gauge_model_path"]
label_model_path = model_config["label_model_path"]

camera_index_1 = camera_config["camera_index_1"]
camera_index_2 = camera_config["camera_index_2"]
width = camera_config["width"]
height = camera_config["height"]
fps = camera_config["fps"]
confidence = camera_config["confidence"]

models = {
    "소화기": YOLO(FireExtinguisher_model_path),
    "압력게이지": YOLO(pressure_gauge_model_path),
    "라벨": YOLO(label_model_path),
}

cap1 = cv2.VideoCapture(camera_index_1, cv2.CAP_V4L2)
cap2 = cv2.VideoCapture(camera_index_2, cv2.CAP_V4L2)

for cap in [cap1, cap2]:
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, fps)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not cap1.isOpened() or not cap2.isOpened():
    print("카메라 열기 실패")
    cap1.release()
    cap2.release()
    raise SystemExit(1)

neopixel = None

try:
    neopixel = open_neopixel(NEOPIXEL_PORT)
    response = send_neopixel(neopixel, "ON")
    print(f"NeoPixel ON: {response}")

    print("YOLO11 세 모델 탐지 시작")
    cv2.namedWindow("Camera 1", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Camera 2", cv2.WINDOW_NORMAL)

    while True:
        cap1.grab()
        cap2.grab()

        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not ret1 or not ret2:
            print("프레임 읽기 실패")
            break

        frames = [frame1, frame2]
        annotated_frames = []

        for i, frame in enumerate(frames):
            annotated = frame.copy()

            for name, model in models.items():
                results = model(frame, imgsz=640, conf=confidence, verbose=False, device=0)

                for box in results[0].boxes:
                    conf_score = float(box.conf[0])
                    cls_id = int(box.cls[0])
                    class_name = model.names[cls_id]

                    if conf_score >= 0.85:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        print(
                            f"Camera {i + 1} | {name} {class_name} 감지 | "
                            f"확률: {conf_score:.2f} | 좌표: ({x1},{y1})~({x2},{y2})"
                        )

                annotated = results[0].plot(img=annotated)

            annotated_frames.append(annotated)

        cv2.imshow("Camera 1", annotated_frames[0])
        cv2.imshow("Camera 2", annotated_frames[1])

        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

    if neopixel is not None:
        try:
            response = send_neopixel(neopixel, "OFF")
            print(f"NeoPixel OFF: {response}")
        finally:
            neopixel.close()

    print("프로그램 종료")
