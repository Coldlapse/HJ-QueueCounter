import serial
import serial.tools.list_ports
import requests
import time

# --- 사용자 설정 ---
BAUD_RATE = 9600
SERVER_URL = 'http://yourserver.com/update_queue'  # 실제 서버 URL로 변경
MACHINE_ID = 'machine_001'  # 각 에이전트마다 고유 ID 설정

def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        description = port.description.upper()
        hwid = port.hwid.upper()
        if "CH340" in description or "ARDUINO" in description or "USB-SERIAL" in description:
            print(f"아두이노 후보 발견: {port.device} ({port.description})")
            return port.device
    if ports:
        print(f"정확한 이름을 찾지 못해 마지막 포트 {ports[-1].device}를 시도합니다.")
        return ports[-1].device
        
    return None

def send_to_server(count):
    payload = {'machine_id': MACHINE_ID, 'waiting_count': count}
    try:
        response = requests.post(SERVER_URL, json=payload, timeout=5)
        print(f"서버 전송 결과: {response.status_code}")
    except Exception as e:
        print(f"서버 전송 실패: {e}")

def start_agent():
    while True:
        port_name = find_arduino_port()
        
        if not port_name:
            print("아두이노를 찾을 수 없습니다. 5초 후 다시 검색합니다...")
            time.sleep(5)
            continue
            
        try:
            with serial.Serial(port_name, BAUD_RATE, timeout=1) as ser:
                print(f"[{port_name}] 연결 성공! 데이터 수신 중...")
                
                while True:
                    if ser.in_waiting > 0:
                        line = ser.readline().decode('utf-8').strip()
                        
                        if line.isdigit():
                            count = int(line)
                            print(f"대기 인원 업데이트: {count}명")
                            send_to_server(count)
                            time.sleep(1) 
                            
        except (serial.SerialException, OSError) as e:
            print(f"통신 중 오류 발생(연결 끊김): {e}")
            print("재연결을 시도합니다...")
            time.sleep(2)

if __name__ == "__main__":
    start_agent()