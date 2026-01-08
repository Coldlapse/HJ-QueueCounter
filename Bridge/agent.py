import serial
import serial.tools.list_ports
import requests
import threading
import time

# --- 설정 ---
SERVER_URL = 'http://yourserver.com/update_queue'  # 실제 서버 URL로 변경
MACHINE_ID = 'machine_001'  # 각 에이전트마다 고유 ID 설정
BAUD_RATE = 9600

def find_arduino_port():
    print("1. 연결된 USB 포트 리스트를 스캔합니다...")
    ports = serial.tools.list_ports.comports()
    
    if not ports:
        print("   -> 연결된 시리얼 장치가 하나도 없습니다. 아두이노 연결을 확인하세요.")
        return None

    for port in ports:
        desc = port.description.upper()
        hwid = port.hwid.upper()
        print(f"   -> 장치 발견: {port.device} ({port.description})")
        
        # CH340, Arduino, USB-SERIAL 키워드 확인
        if "CH340" in desc or "ARDUINO" in desc or "USB-SERIAL" in desc or "USB SERIAL" in desc:
            print(f"   => [!] 아두이노로 추정되는 포트 결정: {port.device}")
            return port.device
            
    print("   -> 아두이노 키워드를 가진 장치를 찾지 못했습니다.")
    return None

def send_to_server_async(count):
    def task():
        payload = {'machine_id': MACHINE_ID, 'waiting_count': count}
        try:
            # 3초 내로 응답 없으면 타임아웃
            response = requests.post(SERVER_URL, json=payload, timeout=3)
            print(f"      [서버 전송 성공] {count}명 (상태 코드: {response.status_code})")
        except Exception as e:
            print(f"      [서버 전송 실패] 오류: {e}")
    
    threading.Thread(target=task, daemon=True).start()

def start_agent():
    print(f"에이전트 가동 시작 (기기 ID: {MACHINE_ID})")
    
    while True:
        port_name = find_arduino_port()
        
        if not port_name:
            print("아두이노를 찾지 못했습니다. 5초 후 다시 시도합니다...")
            time.sleep(5)
            continue
            
        try:
            print(f"2. {port_name} 포트 오픈을 시도합니다...")
            # timeout=0.1로 설정하여 무한 대기를 방지합니다.
            with serial.Serial(port_name, BAUD_RATE, timeout=0.1) as ser:
                print(f"3. 연결 성공! {port_name}에서 데이터를 기다립니다...")
                
                while True:
                    if ser.in_waiting > 0:
                        # 버퍼의 모든 데이터를 읽고 마지막 줄을 선택
                        data = ser.read_all().decode('utf-8', errors='ignore')
                        lines = data.strip().split('\n')
                        if not lines: continue
                        
                        last_line = lines[-1].strip()
                        print(f"수신 데이터: {last_line}")
                        
                        if last_line.isdigit():
                            count = int(last_line)
                            send_to_server_async(count)
                    
                    time.sleep(2) # 데이터 확인할 주기 설정은 여기서

        except Exception as e:
            print(f"\n[!] 시리얼 통신 중 오류 발생: {e}")
            print("3초 후 재연결을 시도합니다...")
            time.sleep(3)

if __name__ == "__main__":
    print("=== IIDX 대기 현황 에이전트 v1.0 ===")
    start_agent()