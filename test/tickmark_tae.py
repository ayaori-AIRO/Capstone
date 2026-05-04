import cv2
import numpy as np
import os
import json

# ================================
# 0. 설정 및 로드
# ================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_config_path = os.path.join(BASE_DIR, "config", "model_config.json")
with open(model_config_path, "r") as f:
    model_config = json.load(f)

gauge_img = cv2.imread(model_config["gauge_crop_image_path"])
h, w = gauge_img.shape[:2]
center = (w // 2, h // 2)

# ================================
# 1. 전처리 (Masking)
# ================================
circle_mask = np.zeros((h, w), dtype=np.uint8)
cv2.circle(circle_mask, center, min(w, h) // 2 - 5, 255, -1)
gauge_circle = cv2.bitwise_and(gauge_img, gauge_img, mask=circle_mask)

# HSV 변환 및 빨간색 마스킹 (원래 코드로 복원 - 바늘은 위쪽)
hsv = cv2.cvtColor(gauge_circle, cv2.COLOR_BGR2HSV)
mask1 = cv2.inRange(hsv, np.array([0, 50, 40]), np.array([15, 255, 255]))
mask2 = cv2.inRange(hsv, np.array([165, 50, 40]), np.array([180, 255, 255]))
red_mask = mask1 + mask2

# 노이즈 제거 (모폴로지)
kernel = np.ones((5, 5), np.uint8)
clean_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)

# ================================
# 2. 특징점 검출 및 벡터 계산
# ================================
# 컨투어 기반 바늘 끝 검출 (원래 코드)
contours, _ = cv2.findContours(clean_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
img_result = gauge_img.copy()
tip_point = None

if contours:
    largest_contour = max(contours, key=cv2.contourArea)
    pts = largest_contour.reshape(-1, 2)
    distances = np.sqrt((pts[:, 0] - center[0])**2 + (pts[:, 1] - center[1])**2)
    max_dist_idx = np.argmax(distances)
    tip_point = tuple(pts[max_dist_idx])
    print(f"[gauge_debug] 컨투어 기반: center={center}, tip_point={tip_point}")
    print(f"[gauge_debug] 바늘 끝 좌표: ({tip_point[0]}, {tip_point[1]})")
    print(f"[gauge_debug] 중심에서 거리: {distances[max_dist_idx]:.1f}")

    # 바늘 끝점을 파란색 1픽셀로만 표시
    cv2.circle(img_result, tip_point, 1, (255, 0, 0), -1)
else:
    print("[gauge_debug] no contours found")

# 디버그 창용 에지
gray = cv2.cvtColor(gauge_circle, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blur, 50, 150)
edge_display = edges.copy()

# ================================
# 거리 계산 함수
# ================================
def line_distance_to_point(line, pt):
    x1, y1, x2, y2 = line
    px, py = pt
    vx = x2 - x1
    vy = y2 - y1
    if vx == 0 and vy == 0:
        return np.hypot(px - x1, py - y1)
    return abs(vy * px - vx * py + x2 * y1 - y2 * x1) / np.hypot(vx, vy)


cv2.imshow("1. Original", gauge_img)
cv2.imshow("2. HSV Masking", red_mask)     # HSV로 빨간색만 추출한 상태
cv2.imshow("3. Morphology", clean_mask)    # 노이즈 제거된 최종 바늘 형상
cv2.imshow("4. Edges", edge_display)
cv2.imshow("5. Final Result", img_result)  # 중심-바늘 끝 연결 및 각도 표시

cv2.waitKey(0)
cv2.destroyAllWindows()

# 디버그 이미지 저장
# debug_dir = os.path.join(BASE_DIR, "runs", "gauge_debug")
# os.makedirs(debug_dir, exist_ok=True)
# cv2.imwrite(os.path.join(debug_dir, "1_original.jpg"), gauge_img)
# cv2.imwrite(os.path.join(debug_dir, "2_hsv_mask.jpg"), red_mask)
# cv2.imwrite(os.path.join(debug_dir, "3_morphology.jpg"), clean_mask)
# cv2.imwrite(os.path.join(debug_dir, "4_edges.jpg"), edge_display)
# cv2.imwrite(os.path.join(debug_dir, "5_final_result.jpg"), img_result)
# print(f"[gauge_debug] 디버그 이미지 저장됨: {debug_dir}")