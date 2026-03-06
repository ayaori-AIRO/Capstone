import time  
from scservo_sdk import PortHandler, sms_sts
# explane : https://github.com/commanderfun/STS3215
# ==============================
# 기본 설정
# ==============================

SERIAL_PORT = "COM5"     # 연결된 시리얼 포트
BAUDRATE = 1000000      # ST3235 기본 보드레이트
SERVO_ID = 1            # 서보 ID

# ==============================
# 레지스터 주소
# ==============================

ADDR_TORQUE_ENABLE = 40        # 토크 ON/OFF
ADDR_GOAL_POSITION = 42        # 목표 위치
ADDR_PRESENT_POSITION = 56     # 현재 위치
ADDR_PRESENT_VOLTAGE = 62      # 현재 전압
ADDR_PRESENT_TEMPERATURE = 63  # 현재 온도

# ==============================
# 시리얼 포트 초기화
# ==============================

portHandler = PortHandler(SERIAL_PORT)
servo = sms_sts(portHandler)

# 포트 열기
if not portHandler.openPort():
    print("포트 열기 실패")
    quit()

print("포트 연결 성공")

# 보드레이트 설정
if not portHandler.setBaudRate(BAUDRATE):
    print("보드레이트 설정 실패")
    quit()

print("보드레이트 설정 성공")

# ==============================
# 서보 연결 확인 (Ping)
# ==============================

model_number, result, error = servo.ping(SERVO_ID)

if result != 0:
    print("서보 발견 실패")
    quit()

print("서보 발견")
print("모델 번호 :", model_number)

# ==============================
# 현재 토크 상태 읽기
# ==============================

torque_state, result, error = servo.read1ByteTxRx(
    SERVO_ID,
    ADDR_TORQUE_ENABLE
)

if result == 0:

    if torque_state == 1:
        print("현재 토크 상태 : ON")
    else:
        print("현재 토크 상태 : OFF")

else:
    print("토크 상태 읽기 실패")

# ==============================
# 토크 활성화
# ==============================

servo.write1ByteTxRx(
    SERVO_ID,
    ADDR_TORQUE_ENABLE,
    1
)

print("토크 활성화 완료")

time.sleep(1)

# ==============================
# 이동 설정
# ==============================

goal_position = 2048     # 0= 0° / 1024= 90° / 2048= 180° (중심) / 3072= 270° / 4095= 360°     
move_speed = 1500        # 이동 속도
move_acc = 50            # 가속도

degree = goal_position * 360 / 4096

print("이동 명령")
print("목표 위치 :", goal_position)
print("각도 :", degree)
print("속도 :", move_speed)
print("가속도 :", move_acc)

# ==============================
# 모터 이동
# ==============================

servo.WritePosEx(
    SERVO_ID,
    goal_position,
    move_speed,
    move_acc
)

# 이동 시간 대기
time.sleep(3)

# ==============================
# 현재 위치 읽기
# ==============================

current_position, result, error = servo.read2ByteTxRx(
    SERVO_ID,
    ADDR_PRESENT_POSITION
)

if result == 0:

    current_degree = current_position * 360 / 4096

    print("현재 위치 :", current_position)
    print("현재 각도 :", round(current_degree, 2))

else:
    print("현재 위치 읽기 실패")

# ==============================
# 전압 / 온도 확인
# ==============================

voltage_raw, result, error = servo.read1ByteTxRx(
    SERVO_ID,
    ADDR_PRESENT_VOLTAGE
)

if result == 0:
    voltage = voltage_raw * 0.1
    print("현재 전압 :", voltage, "V")

temp, result, error = servo.read1ByteTxRx(
    SERVO_ID,
    ADDR_PRESENT_TEMPERATURE
)

if result == 0:
    print("현재 온도 :", temp, "도")