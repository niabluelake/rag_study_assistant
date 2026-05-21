# 건강 도메인 특화 LLM 챗봇

Flask REST API와 LoRA Instruction Tuning을 활용한 건강 분석 설명 생성 서비스

---

## 프로젝트 개요

이 프로젝트는 3차 LLM 프로젝트를 위한 Flask 기반 도메인 특화 LLM 챗봇 서비스이다.

기존 1차 건강 분석 프로젝트에서 생성한 사용자 건강 데이터와 클러스터링 결과를 REST API로 전달받고, 이를 기반으로 건강 위험 요인과 개선 방향을 자연어로 설명하는 LLM 서비스를 목표로 한다.

현재 단계에서는 실제 LLM 모델 연결 전이므로 `mock` 응답을 사용하고 있으며, 추후 GPU 환경에서 LoRA / PEFT 기반 Instruction Tuning을 수행한 뒤 학습된 모델을 Flask API에 연결할 예정이다.

---

## 프로젝트 목표

이 프로젝트의 주요 목표는 다음과 같다.

1. 건강검진, 영양, 생활습관 데이터를 기반으로 도메인 특화 학습 데이터 생성
2. Alpaca 형식의 Instruction Tuning 데이터셋 구성
3. LoRA / PEFT 기반 LLM 학습 코드 준비
4. Flask 기반 챗봇 API 서버 구현
5. 기존 1차 건강 분석 프로젝트와 REST API 방식으로 연동
6. 추후 학습된 LoRA 모델을 이용해 건강 조언 응답 생성

---

## 현재 구현 기능

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
[완료] 학습 환경 확인 스크립트 작성
[완료] LoRA 학습 코드 뼈대 작성
[완료] Cloud Ubuntu 학습 명령 문서 작성
[완료] API 명세 문서 작성
[완료] 프로젝트 구조 문서 작성
[완료] GitHub 업로드
```

---

## 기술 스택

```text
Language: Python
Web Framework: Flask
Frontend: HTML, CSS, JavaScript
API: REST API
LLM Training: Transformers, PEFT, TRL, LoRA
Dataset Format: Alpaca instruction format
Environment: Windows local development, WSL / Cloud Ubuntu training
Version Control: Git, GitHub
```

---

## 프로젝트 구조

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
│   │   └── health_export.json
│   └── processed/
│       ├── train.json
│       └── eval.json
│
├── scripts/
│   └── convert_to_alpaca.py
│
├── training/
│   ├── check_environment.py
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

## 로컬 실행 환경 구성

### 1. 저장소 복제

```bat
git clone https://github.com/niabluelake/rag_study_assistant.git
cd rag_study_assistant
```

### 2. 가상환경 생성

Windows CMD 기준:

```bat
python -m venv .venv
.venv\Scripts\activate
```

### 3. 패키지 설치

```bat
pip install -r requirements.txt
```

### 4. `.env` 파일 생성

프로젝트 루트에 `.env` 파일을 만들고 아래 내용을 입력한다.

```env
LLM_MODE=mock
```

현재 로컬 개발 단계에서는 `mock` 모드를 사용한다.

---

## Flask 서버 실행

Windows CMD 기준:

```bat
.venv\Scripts\python.exe app.py
```

서버 실행 후 브라우저에서 접속한다.

```text
http://127.0.0.1:5000/chat
```

---

## API 엔드포인트

### Health Check API

```http
GET /health
```

Flask 서버가 정상 실행 중인지 확인하는 API이다.

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

Response example:

```json
{
  "success": true,
  "message": "안녕",
  "answer": "임시 챗봇 답변입니다. 입력한 메시지: 안녕"
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

CMD cURL example:

```bat
curl -X POST http://127.0.0.1:5000/api/health-advice -H "Content-Type: application/json" -d "{\"age\":45,\"sex\":\"남성\",\"bmi\":28.4,\"total_chol\":245,\"kcal\":2800,\"sugar\":95,\"na\":4200,\"sfa\":24,\"tdf\":12,\"sleep\":5,\"smoke\":\"예\",\"alcohol\":\"주 3회\",\"aerobic\":\"주 0회\",\"cluster_name\":\"고나트륨 섭취 위험군\"}"
```

---

## 학습 데이터 파이프라인

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

## 원본 데이터를 Alpaca 형식으로 변환

```bat
python scripts\convert_to_alpaca.py
```

생성 결과:

```text
data/processed/train.json
data/processed/eval.json
```

---

## 데이터셋 검증

```bat
python training\check_dataset.py
```

검증 항목:

```text
JSON 로딩 가능 여부
최상위 구조가 list인지 확인
instruction / input / output 키 존재 여부
빈 값 여부
샘플 출력
```

---

## 학습 프롬프트 미리보기

```bat
python training\preview_training_data.py --limit 2
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

## 학습 환경 확인

LoRA 학습을 실행하기 전에 Python, PyTorch, CUDA, NVIDIA GPU, Hugging Face 로그인 상태를 확인한다.

```bat
python training\check_environment.py
```

CUDA가 비활성화된 로컬 CPU 환경에서는 다음과 같이 출력될 수 있다.

```text
torch cuda version: None
cuda available: False
gpu: CPU only
warning: LoRA training on CPU is not recommended.
```

이 경우 로컬 환경은 개발, 데이터 검증, 문서화 용도로만 사용하고 실제 LoRA 학습은 GPU가 있는 Cloud Ubuntu 또는 CUDA가 설정된 데스크톱에서 수행한다.

---

## LoRA 학습

실제 LoRA 학습은 Windows 로컬 CPU 환경이 아니라 GPU가 있는 Ubuntu 환경에서 수행한다.

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

GPU 메모리가 부족한 경우 4-bit quantization 옵션을 사용한다.

```bash
python training/train_lora.py \
  --model-name meta-llama/Llama-3.2-1B \
  --output-dir outputs/health_lora_model \
  --use-4bit
```

---

## Hugging Face 모델 접근

`meta-llama/Llama-3.2-1B` 모델은 gated model이므로 Hugging Face 로그인과 모델 접근 승인이 필요하다.

```bash
hf auth login
hf auth whoami
```

모델 접근 권한이 없을 경우 다음과 같은 오류가 발생할 수 있다.

```text
403 Forbidden
Access to model meta-llama/Llama-3.2-1B is restricted and you are not in the authorized list.
```

이 경우 Hugging Face 모델 페이지에서 접근 요청을 제출한 뒤 승인을 기다려야 한다.

---

## LLM 실행 모드

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

## 1차 프로젝트 연동 구조

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

발표 시 설명 예시:

```text
기존 1차 프로젝트의 건강 분석 결과를 REST API로 3차 LLM 서버에 전달하고,
3차 프로젝트에서는 이를 자연어 프롬프트로 변환한 뒤 도메인 특화 LLM 응답을 생성하도록 설계했습니다.
```

---

## 문서

자세한 문서는 `docs/` 폴더에 정리되어 있다.

```text
docs/api_spec.md
docs/project_structure.md
docs/train_ubuntu_commands.md
```

---

## 현재 상태

```text
[완료] 로컬 Flask 서버 구현
[완료] 웹 챗봇 화면 구현
[완료] /api/chat API 구현
[완료] /api/health-advice API 구현
[완료] 학습 데이터 변환 구조 구현
[완료] Alpaca 형식 train/eval 데이터 생성
[완료] 데이터 검증 및 프롬프트 미리보기
[완료] 학습 환경 확인 스크립트 구현
[완료] LoRA 학습 코드 뼈대 작성
[완료] REST API 연동 구조 문서화
[완료] GitHub 업로드
[진행 중] Hugging Face Llama 3.2 1B 모델 접근 승인 대기
[대기] GPU 환경에서 실제 LoRA 학습
```

---

## 향후 작업

```text
1. Hugging Face Llama 3.2 1B 모델 접근 승인 확인
2. GPU 사용 가능한 Ubuntu 환경 확보
3. requirements-train.txt 설치
4. python training/check_environment.py로 CUDA 확인
5. LoRA 학습 실행
6. TensorBoard로 학습 결과 확인
7. outputs/health_lora_model 생성 확인
8. model_loader.py에 실제 모델 로딩 코드 연결
9. LLM_MODE=trained로 변경
10. Flask API에서 튜닝 모델 추론 테스트
11. 1차 프로젝트와 실제 REST API 연동
```

---

## 최종 목표

사용자의 건강검진, 영양, 생활습관, 클러스터링 결과를 기반으로 도메인 특화 LLM이 건강 위험 요인과 개선 방향을 자연어로 설명하는 서비스를 구현하는 것이다.
