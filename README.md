# RAG Study Assistant / Health Domain LLM Chatbot

## Overview

이 프로젝트는 3차 LLM 프로젝트를 위한 Flask 기반 도메인 특화 LLM 챗봇 서비스이다.

기존 1차 건강 분석 프로젝트에서 생성한 사용자 건강 데이터와 클러스터링 결과를 REST API로 전달받고, 이를 기반으로 건강 위험 요인과 개선 방향을 자연어로 설명하는 LLM 서비스를 목표로 한다.

현재 단계에서는 실제 LLM 모델 연결 전이므로 mock 응답을 사용하고 있으며, 추후 Cloud Ubuntu 환경에서 LoRA / PEFT 기반 Instruction Tuning을 수행한 뒤 학습된 모델을 Flask API에 연결할 예정이다.

---

## Project Goals

이 프로젝트의 주요 목표는 다음과 같다.

1. 건강검진, 영양, 생활습관 데이터를 기반으로 도메인 특화 학습 데이터 생성
2. Alpaca 형식의 Instruction Tuning 데이터셋 구성
3. LoRA / PEFT 기반 LLM 학습 코드 준비
4. Flask 기반 챗봇 API 서버 구현
5. 기존 1차 프로젝트와 REST API 방식으로 연동
6. 추후 학습된 LoRA 모델을 이용해 건강 조언 응답 생성

---

## Current Features

현재 구현된 기능은 다음과 같다.

```text
[완료] Flask 기본 서버 구성
[완료] 웹 챗봇 화면 구현
[완료] /api/chat 챗봇 API 구현
[완료] /api/health-advice 건강 조언 API 구현
[완료] 1차 프로젝트 연동용 REST API 구조 구현
[완료] llm_service.py로 LLM 응답 로직 분리
[완료] LLM_MODE=mock / trained 모드 분리
[완료] model_loader.py 모델 로딩 구조 준비
[완료] health_export.json → Alpaca 학습 데이터 변환
[완료] train.json / eval.json 데이터 생성
[완료] 데이터 검증 스크립트 작성
[완료] 학습 프롬프트 미리보기 스크립트 작성
[완료] LoRA 학습 코드 뼈대 작성
[완료] Cloud Ubuntu 학습 명령 문서 작성
[완료] API 명세 문서 작성
[완료] 프로젝트 구조 문서 작성
```

---

## Tech Stack

```text
Language: Python
Web Framework: Flask
Frontend: HTML, CSS, JavaScript
API: REST API
LLM Training: Transformers, PEFT, TRL, LoRA
Dataset Format: Alpaca instruction format
Environment: Windows local development, Cloud Ubuntu training
Version Control: Git, GitHub
```

---

## Project Structure

```text
rag_study_assistant/
│
├── app.py
├── requirements.txt
├── requirements-train.txt
├── .env
│
├── routes/
│   ├── main_routes.py
│   ├── chat_routes.py
│   └── health_routes.py
│
├── services/
│   ├── llm_service.py
│   └── model_loader.py
│
├── templates/
│   └── chat.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── chat.js
│
├── data/
│   ├── raw/
│   └── processed/
│
├── scripts/
│   └── convert_to_alpaca.py
│
├── training/
│   ├── check_dataset.py
│   ├── preview_training_data.py
│   └── train_lora.py
│
├── outputs/
└── docs/
    ├── api_spec.md
    ├── project_structure.md
    └── train_ubuntu_commands.md
```

---

## Local Setup

### 1. Clone Repository

```bash
git clone https://github.com/niabluelake/rag_study_assistant.git
cd rag_study_assistant
```

### 2. Create Virtual Environment

Windows CMD:

```bat
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bat
pip install -r requirements.txt
```

### 4. Create `.env`

```env
LLM_MODE=mock
```

현재 로컬 개발 단계에서는 `mock` 모드를 사용한다.

---

## Run Flask Server

Windows CMD:

```bat
.venv\Scripts\python.exe app.py
```

서버 실행 후 브라우저에서 접속:

```text
http://127.0.0.1:5000/chat
```

---

## API Endpoints

### Health Check

```http
GET /health
```

서버 상태 확인용 API이다.

---

### Chat API

```http
POST /api/chat
```

사용자의 자유 입력 메시지를 받아 챗봇 응답을 반환한다.

Request example:

```json
{
  "message": "안녕"
}
```

---

### Health Advice API

```http
POST /api/health-advice
```

1차 건강 분석 프로젝트에서 전달한 사용자 건강 데이터를 받아 자연어 입력문으로 변환하고, LLM 응답을 반환한다.

Request example:

```json
{
  "age": 45,
  "sex": "남성",
  "bmi": 28.4,
  "total_chol": 245,
  "kcal": 2800,
  "sugar": 95,
  "na": 4200,
  "sfa": 24,
  "tdf": 12,
  "sleep": 5,
  "smoke": "예",
  "alcohol": "주 3회",
  "aerobic": "주 0회",
  "cluster_name": "고나트륨 섭취 위험군"
}
```

cURL example:

```bash
curl -X POST http://127.0.0.1:5000/api/health-advice \
  -H "Content-Type: application/json" \
  -d "{\"age\":45,\"sex\":\"남성\",\"bmi\":28.4,\"total_chol\":245,\"kcal\":2800,\"sugar\":95,\"na\":4200,\"sfa\":24,\"tdf\":12,\"sleep\":5,\"smoke\":\"예\",\"alcohol\":\"주 3회\",\"aerobic\":\"주 0회\",\"cluster_name\":\"고나트륨 섭취 위험군\"}"
```

---

## Dataset Pipeline

이 프로젝트는 Oracle DB에 직접 의존하지 않고, 중간 JSON 파일을 통해 학습 데이터를 생성할 수 있도록 구성했다.

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

## Convert Raw Data to Alpaca Format

```bash
python scripts/convert_to_alpaca.py
```

생성 결과:

```text
data/processed/train.json
data/processed/eval.json
```

---

## Check Dataset

```bash
python training/check_dataset.py
```

---

## Preview Training Prompt

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

---

## LoRA Training

실제 LoRA 학습은 Windows 로컬이 아니라 Cloud Ubuntu GPU 환경에서 수행한다.

기본 실행:

```bash
python training/train_lora.py
```

옵션 지정 실행:

```bash
python training/train_lora.py \
  --model-name meta-llama/Llama-3.2-1B \
  --train-path data/processed/train.json \
  --eval-path data/processed/eval.json \
  --output-dir outputs/health_lora_model \
  --epochs 3 \
  --batch-size 1 \
  --gradient-accumulation-steps 4 \
  --learning-rate 2e-4 \
  --max-seq-length 1024
```

4-bit quantization 사용:

```bash
python training/train_lora.py \
  --model-name meta-llama/Llama-3.2-1B \
  --output-dir outputs/health_lora_model \
  --use-4bit
```

---

## LLM Mode

`.env` 파일에서 실행 모드를 설정한다.

```env
LLM_MODE=mock
```

### mock

로컬 개발용 임시 응답 모드이다.

```text
사용자 입력을 그대로 포함한 임시 응답 반환
```

### trained

학습된 LoRA 모델 연결용 모드이다.

```text
사용자 입력
↓
Prompt 생성
↓
LoRA 모델 추론
↓
응답 반환
```

현재는 학습 모델 연결 전이므로 placeholder 구조만 준비되어 있다.

---

## Integration with 1st Project

1차 프로젝트와의 연동 흐름은 다음과 같다.

```text
1차 프로젝트 사용자 입력
↓
1차 프로젝트 건강 분석 / 클러스터링
↓
분석 결과 JSON 생성
↓
POST /api/health-advice
↓
3차 LLM Flask 서버
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

## Documentation

자세한 문서는 `docs/` 폴더에 정리되어 있다.

```text
docs/api_spec.md
docs/project_structure.md
docs/train_ubuntu_commands.md
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

---

## Status

현재 프로젝트는 로컬 Flask 서버, REST API, 학습 데이터 변환, 학습 코드 뼈대, 문서화, GitHub 업로드까지 완료된 상태.

실제 LLM 학습 및 모델 연결은 Cloud Ubuntu 환경에서 진행할 예정.