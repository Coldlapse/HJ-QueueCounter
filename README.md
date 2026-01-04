# IIDX Waiting Status System (IIDX 대기 현황 시스템)

이 프로젝트는 오락실 기기(비트매니아 IIDX 라이트닝 모델 등)의 대기 카드 현황을 센서로 감지하고, 이를 실시간으로 웹 서버에 전송하여 위젯화하는 시스템입니다.

## 📂 프로젝트 구조

- **/arduino**: 아두이노 우노(Arduino Uno) 소스 코드. 센서 데이터 수집 및 현장 LCD 출력 담당.
- **/bridge**: 파이썬(Python) 중계 스크립트. 아두이노의 시리얼 데이터를 수신하여 웹 서버로 HTTP POST 전송 담당.

---

## 🛠 하드웨어 구성

- **Controller**: Arduino Uno (또는 CH340 호환보드)
- **Sensor**: 적외선 센서 또는 FSR408 (6개 슬롯 감지: Pin 6 ~ 11)
- **Display**: 16x2 I2C LCD (상태 표시용)
- **Logic**: Active High (신호 감지 시 대기 카드 카운트 증가)

---

## 🚀 시작하기

### 1. Arduino (센서 노드)
1. 아두이노 IDE에서 `arduino/` 폴더의 코드를 엽니다.
2. `LiquidCrystal_I2C` 라이브러리를 설치합니다.
3. 아두이노 우노 보드에 업로드합니다.
   - **특징**: LCD 안정성을 위해 5분마다 화면을 자동 재초기화합니다.
   - **연결**: 센서는 6~11번 핀, LCD는 I2C 포트(A4, A5)에 연결합니다.

### 2. Bridge (PC 중계 에이전트)
아두이노가 연결된 방송용 PC에서 실행합니다.

**필수 라이브러리 설치:**
```bash
pip install pyserial requests
```

**설정 방법:**
`bridge/agent.py` 파일 내의 다음 변수들을 본인의 환경에 맞게 수정합니다.
- SERVER_URL: 데이터를 전송받을 Django 서버의 API 주소
- MACHINE_ID: 기기를 식별할 고유 ID (예: 'hwajeong_iidx_1')

**실행:**
```bash
python agent.py
```
*이 에이전트는 아두이노가 연결된 COM 포트를 자동으로 검색하여 연결을 시도하며, 연결이 끊길 경우 자동으로 재연결을 시도합니다.*


---

## 🚥 서버 통신 프로토콜 (JSON)

에이전트는 서버로 다음과 같은 형식의 JSON 데이터를 전송합니다.

```json
{
    "machine_id": "hwajeong_iidx_1",
    "waiting_count": 3
}
```

---
**Maintained by**: @Coldlapse
**Location**: 화정 게임랜드 (HJ GAMELAND)