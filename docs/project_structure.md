# Project Structure

## Overview

이 프로젝트는 3차 LLM 프로젝트를 위한 Flask 기반 도메인 특화 LLM 챗봇 서비스이다.

주요 목적은 다음과 같다.

1. 건강 도메인 데이터를 기반으로 Alpaca 형식 학습 데이터 생성
2. LoRA / PEFT 기반 Instruction Tuning 준비
3. 튜닝된 LLM을 Flask API에 연결할 수 있는 구조 설계
4. 기존 1차 건강 분석 프로젝트와 REST API 방식으로 연동

---

## Root Structure

```text
rag_study_assistant/
│
├── app.py
├── requirements.txt
├── requirements-train.txt
├── .env
│
├── routes/
├── services/
├── templates/
├── static/
│
├── data/
├── scripts/
├── training/
├── outputs/
└── docs/
```

---

## app.py

Flask 애플리케이션의 시작 파일이다.

역할:

```text
Flask app 생성
Blueprint 등록
서버 실행
```

등록되는 Blueprint:

```text
main_bp
chat_bp
health_bp
```

현재 주요 라우트:

```text
GET  /
GET  /health
GET  /chat
POST /api/chat
POST /api/health-advice
```

---

## routes/

Flask API 라우트 파일을 모아두는 폴더이다.

```text
routes/
├── __init__.py
├── main_routes.py
├── chat_routes.py
└── health_routes.py
```

### main_routes.py

기본 페이지와 서버 상태 확인 라우트를 담당한다.

```text
GET /
GET /health
GET /chat
```

### chat_routes.py

일반 챗봇 API를 담당한다.

```text
POST /api/chat
```

처리 흐름:

```text
사용자 message 수신
↓
message 유효성 검사
↓
llm_service.generate_answer() 호출
↓
JSON 응답 반환
```

### health_routes.py

1차 프로젝트 연동용 건강 조언 API를 담당한다.

```text
POST /api/health-advice
```

처리 흐름:

```text
건강 데이터 JSON 수신
↓
build_health_input()으로 자연어 입력문 생성
↓
llm_service.generate_answer() 호출
↓
JSON 응답 반환
```

---

## services/

비즈니스 로직을 담당하는 폴더이다.

```text
services/
├── __init__.py
├── llm_service.py
└── model_loader.py
```

### llm_service.py

챗봇 답변 생성 로직을 담당한다.

`.env`의 `LLM_MODE` 값에 따라 동작을 나눈다.

```text
LLM_MODE=mock
→ 임시 답변 반환

LLM_MODE=trained
→ 학습된 모델 추론 구조 사용
```

### model_loader.py

학습된 LLM 모델을 로드하기 위한 준비 파일이다.

추후 LoRA 학습이 완료되면 다음 역할을 담당한다.

```text
Base model 로드
Tokenizer 로드
LoRA adapter 로드
model.generate() 실행
```

현재는 placeholder 구조만 존재한다.

---

## templates/

HTML 화면 파일을 저장하는 폴더이다.

```text
templates/
└── chat.html
```

### chat.html

브라우저에서 사용하는 간단한 챗봇 화면이다.

```text
사용자 입력창 제공
전송 버튼 제공
챗봇 응답 출력 영역 제공
```

---

## static/

정적 파일을 저장하는 폴더이다.

```text
static/
├── css/
│   └── style.css
└── js/
    └── chat.js
```

### static/js/chat.js

브라우저에서 `/api/chat`으로 요청을 보내는 JavaScript 파일이다.

```text
사용자 입력 읽기
↓
fetch("/api/chat") 호출
↓
JSON 응답 받기
↓
화면에 답변 출력
```

### static/css/style.css

챗봇 화면 스타일을 담당한다.

---

## data/

학습 데이터와 원본 데이터를 저장하는 폴더이다.

```text
data/
├── raw/
│   └── health_export.json
└── processed/
    ├── train.json
    └── eval.json
```

### data/raw/

DB 또는 샘플에서 추출한 원본성 데이터를 저장한다.

대표 파일:

```text
health_export.json
```

Oracle DB 없이도 프로젝트를 실행하고 학습 데이터를 만들 수 있게 하는 중간 데이터이다.

### data/processed/

LoRA / Instruction Tuning에 사용할 Alpaca 형식 데이터를 저장한다.

대표 파일:

```text
train.json
eval.json
```

형식:

```json
{
  "instruction": "사용자의 건강검진 및 생활습관 정보를 바탕으로 건강 위험 요인과 개선 방향을 설명하세요.",
  "input": "나이: 45세, 성별: 남성, BMI: 28.4, ...",
  "output": "사용자는 고나트륨 섭취 위험군으로 분류됩니다. ..."
}
```

---

## scripts/

데이터 변환용 스크립트를 저장하는 폴더이다.

```text
scripts/
└── convert_to_alpaca.py
```

### convert_to_alpaca.py

`data/raw/health_export.json`을 읽어서 Alpaca 형식의 학습 데이터로 변환한다.

```text
health_export.json 로드
↓
건강 데이터 필드 조합
↓
instruction/input/output 생성
↓
train/eval 분할
↓
data/processed/train.json 저장
↓
data/processed/eval.json 저장
```

---

## training/

모델 학습과 데이터 검증 관련 파일을 저장하는 폴더이다.

```text
training/
├── check_dataset.py
├── preview_training_data.py
└── train_lora.py
```

### check_dataset.py

`data/processed/train.json`, `eval.json`의 구조를 검사한다.

```text
JSON 로딩 가능 여부
최상위 구조가 list인지 확인
instruction/input/output 키 존재 여부
빈 값 여부
샘플 출력
```

실행:

```bash
python training/check_dataset.py
```

### preview_training_data.py

실제 모델 학습에 들어갈 프롬프트 형식을 미리 출력한다.

실행:

```bash
python training/preview_training_data.py --limit 2
```

출력 형식:

```text
### Instruction:
...

### Input:
...

### Response:
...
```

### train_lora.py

LoRA 기반 Instruction Tuning을 수행하기 위한 학습 코드이다.

주요 구성:

```text
Hugging Face Dataset 로드
Tokenizer 로드
Base model 로드
BitsAndBytesConfig를 통한 4bit Quantization 옵션
LoRA 설정
TrainingArguments 설정
SFTTrainer 학습
TensorBoard 로그 기록
LoRA adapter 저장
```

실제 학습은 Windows 로컬이 아니라 Cloud Ubuntu + GPU 환경에서 수행한다.

---

## outputs/

학습 결과물을 저장하는 폴더이다.

```text
outputs/
└── health_lora_model/
```

역할:

```text
LoRA adapter 저장
학습 체크포인트 저장
TensorBoard 로그 저장
```

---

## docs/

프로젝트 문서를 저장하는 폴더이다.

```text
docs/
├── api_spec.md
├── project_structure.md
└── train_ubuntu_commands.md
```

### api_spec.md

REST API 명세 문서이다.

포함 내용:

```text
/health
/chat
/api/chat
/api/health-advice
요청/응답 예시
1차 프로젝트 연동 흐름
```

### train_ubuntu_commands.md

Cloud Ubuntu에서 LoRA 학습을 수행하기 위한 명령어 문서이다.

포함 내용:

```text
가상환경 생성
패키지 설치
데이터 검증
Hugging Face 로그인
LoRA 학습 실행
TensorBoard 확인
```

---

## Requirements Files

### requirements.txt

로컬 Flask 서버 실행용 패키지이다.

```text
flask
python-dotenv
requests
```

### requirements-train.txt

Cloud Ubuntu 학습용 패키지이다.

```text
torch
transformers
datasets
accelerate
peft
trl
bitsandbytes
tensorboard
```

로컬 Windows에서는 학습용 패키지를 바로 설치하지 않는다.

---

## Environment Variables

`.env` 파일에서 실행 모드를 설정한다.

```env
LLM_MODE=mock
```

모드 설명:

```text
mock
= 로컬 개발용 임시 답변 모드

trained
= 학습된 LoRA 모델 연결 모드
```

---

## Full Service Flow

### Local Chat Flow

```text
User
↓
/chat
↓
chat.html
↓
chat.js
↓
POST /api/chat
↓
chat_routes.py
↓
llm_service.py
↓
mock answer
↓
Browser
```

### 1차 프로젝트 연동 Flow

```text
1차 프로젝트 건강 데이터 입력
↓
1차 프로젝트 분석 / 클러스터링
↓
건강 데이터 JSON 생성
↓
POST /api/health-advice
↓
health_routes.py
↓
build_health_input()
↓
llm_service.py
↓
mock 또는 trained LLM 응답
↓
1차 프로젝트 화면에 자연어 설명 출력
```

### Training Data Flow

```text
Oracle DB 또는 샘플 데이터
↓
data/raw/health_export.json
↓
scripts/convert_to_alpaca.py
↓
data/processed/train.json
data/processed/eval.json
↓
training/check_dataset.py
↓
training/preview_training_data.py
↓
training/train_lora.py
↓
outputs/health_lora_model
```

---

## Current Development Status

```text
[완료] Flask 기본 서버 생성
[완료] /api/chat API 생성
[완료] 웹 챗봇 화면 생성
[완료] llm_service.py 분리
[완료] data/raw → data/processed 구조 생성
[완료] health_export.json → Alpaca 변환
[완료] 데이터 검증
[완료] 프롬프트 미리보기
[완료] train_lora.py 학습 코드 뼈대
[완료] Cloud Ubuntu 학습 명령 문서
[완료] /api/health-advice 1차 프로젝트 연동 API
```

---

## Next Steps

```text
1. Cloud Ubuntu 환경으로 프로젝트 이동
2. requirements-train.txt 설치
3. Hugging Face 로그인
4. LoRA 학습 실행
5. TensorBoard로 학습 결과 확인
6. outputs/health_lora_model 생성 확인
7. model_loader.py에 실제 모델 로딩 코드 연결
8. LLM_MODE=trained로 변경
9. Flask API에서 튜닝 모델 추론 테스트
10. 1차 프로젝트와 실제 REST API 연동
```