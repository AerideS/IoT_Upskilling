import network
import time
from machine import Pin, PWM, Timer
import urequests  # HTTP 요청을 보내기 위해 urequests 모듈 사용

# WiFi 설정
SSID = 'YOUR_SSID_HERE'
PASSWORD = 'YOUR_PASS_WORD_HERE'

# 서버 설정
hostIP = 'YOUR_IP_HERE'
hostPort = 'YOUR_PORT_HERE'

# Wemos D1 핀 설정
IN1 = Pin(5, Pin.OUT)  # D1
IN2 = Pin(4, Pin.OUT)  # D2
ENA = PWM(Pin(15))     # D8 (ENA 핀에 PWM 연결)

# PWM 설정
ENA.freq(1000)         # PWM 주파수 설정

# 전역 변수
speed = 0
direction = 1  # 1은 증가, -1은 감소

# 모터 제어 함수
def motor_forward(speed):
    IN1.on()
    IN2.off()
    ENA.duty(speed)

def motor_stop():
    IN1.off()
    IN2.off()
    ENA.duty(0)

# 서버로 속도를 전송하는 함수
def send_speed_to_server(speed):
    try:
        url = "http://" + hostIP + ":" + hostPort + "/upMotSp" # 서버 주소
        data = {"id": 1, "value": speed}
        response = urequests.post(url, json=data)
        response.close()
    except Exception as e:
        print("Failed to send data:", e)

# 타이머 콜백 함수
def timer_callback(t):
    global speed, direction
    if direction == 1:
        speed += 10
        if speed >= 1023:
            speed = 1023
            direction = -1
    else:
        speed -= 10
        if speed <= 0:
            speed = 0
            direction = 1
    
    motor_forward(speed)
    send_speed_to_server(speed)  # 속도를 서버로 전송

# 타이머 설정
def start_timer():
    timer = Timer(-1)
    timer.init(period=100, mode=Timer.PERIODIC, callback=timer_callback)

# WiFi 연결 함수
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    while not wlan.isconnected():
        print('Connecting to WiFi...')
        time.sleep(1)
    
    print('WiFi connected:', wlan.ifconfig())
    start_timer()

# 메인 코드 실행
connect_to_wifi()
