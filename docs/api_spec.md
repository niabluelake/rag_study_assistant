# API Specification

## Overview

이 문서는 3차 LLM 프로젝트의 REST API 명세를 정리한다.

현재 서버는 Flask 기반으로 동작하며, 주요 목적은 다음과 같다.

1. 웹 챗봇 화면 제공
2. 사용자 자유 입력 기반 챗봇 응답 제공
3. 1차 프로젝트 건강 분석 데이터와 REST API 연동
4. 추후 LoRA로 튜닝된 도메인 특화 LLM 응답 제공

## Base URL

Local development:

```text
http://127.0.0.1:5000
```

## 1. Health Check API

### Endpoint

```http
GET /health
```

### Description

Flask 서버가 정상 실행 중인지 확인한다.

### Response Example

```json
{
  "message": "LLM Project Flask server is running",
  "status": "ok"
}
```

## 2. Chat Page

### Endpoint

```http
GET /chat
```

### Description

브라우저에서 사용할 수 있는 간단한 챗봇 화면을 반환한다.

### Usage

```text
http://127.0.0.1:5000/chat
```

## 3. Chat API

### Endpoint

```http
POST /api/chat
```

### Description

사용자가 입력한 일반 메시지를 받아 챗봇 답변을 반환한다.

현재는 `LLM_MODE=mock` 상태에서 임시 답변을 반환한다.
추후 `LLM_MODE=trained` 상태에서는 학습된 LoRA 모델을 사용해 답변을 생성한다.

### Request Headers

```http
Content-Type: application/json
```

### Request Body

```json
{
  "message": "안녕"
}
```

### Success Response

```json
{
  "success": true,
  "message": "안녕",
  "answer": "임시 챗봇 답변입니다. 입력한 메시지: 안녕"
}
```

### Error Response

`message`가 없거나 비어 있을 경우:

```json
{
  "success": false,
  "error": "message field is required"
}
```

### cURL Example

```bash
curl -X POST http://127.0.0.1:5000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"안녕\"}"
```

## 4. Health Advice API

### Endpoint

```http
POST /api/health-advice
```

### Description

1차 프로젝트에서 전달한 건강검진, 영양, 생활습관, 분석군 데이터를 받아 자연어 입력문으로 변환한 뒤 LLM 답변을 반환한다.

이 API는 1차 프로젝트와 3차 LLM 프로젝트를 REST 방식으로 연동하기 위한 핵심 API이다.

현재는 mock 답변을 반환하지만, 추후 LoRA 학습 모델이 연결되면 같은 API에서 튜닝된 LLM 답변을 반환한다.

### Request Headers

```http
Content-Type: application/json
```

### Request Body Fields

| Field | Type | Description |
| --- | --- | --- |
| age | number | 나이 |
| sex | string | 성별 |
| bmi | number | BMI |
| total_chol | number | 총콜레스테롤 |
| kcal | number | 일일 섭취 열량 |
| sugar | number | 당류 섭취량 |
| na | number | 나트륨 섭취량 |
| sfa | number | 포화지방 섭취량 |
| tdf | number | 식이섬유 섭취량 |
| sleep | number | 수면 시간 |
| smoke | string | 흡연 여부 |
| alcohol | string | 음주 빈도 |
| aerobic | string | 유산소 운동 빈도 |
| cluster_name | string | 1차 프로젝트 분석 결과 위험군 |

### Request Body Example

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

### Success Response

```json
{
  "success": true,
  "input": "나이: 45세, 성별: 남성, BMI: 28.4, 총콜레스테롤: 245mg/dL, 일일 섭취 열량: 2800kcal, 당류: 95g, 나트륨: 4200mg, 포화지방: 24g, 식이섬유: 12g, 수면: 5시간, 흡연: 예, 음주: 주 3회, 유산소 운동: 주 0회, 위험군: 고나트륨 섭취 위험군",
  "answer": "임시 챗봇 답변입니다. 입력한 메시지: 나이: 45세, 성별: 남성, BMI: 28.4, 총콜레스테롤: 245mg/dL, 일일 섭취 열량: 2800kcal, 당류: 95g, 나트륨: 4200mg, 포화지방: 24g, 식이섬유: 12g, 수면: 5시간, 흡연: 예, 음주: 주 3회, 유산소 운동: 주 0회, 위험군: 고나트륨 섭취 위험군"
}
```

### Error Response

요청 JSON이 비어 있을 경우:

```json
{
  "success": false,
  "error": "health data is required"
}
```

### cURL Example

```bash
curl -X POST http://127.0.0.1:5000/api/health-advice \
  -H "Content-Type: application/json" \
  -d "{\"age\":45,\"sex\":\"남성\",\"bmi\":28.4,\"total_chol\":245,\"kcal\":2800,\"sugar\":95,\"na\":4200,\"sfa\":24,\"tdf\":12,\"sleep\":5,\"smoke\":\"예\",\"alcohol\":\"주 3회\",\"aerobic\":\"주 0회\",\"cluster_name\":\"고나트륨 섭취 위험군\"}"
```
