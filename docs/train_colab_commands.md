# Google Colab LoRA 학습 테스트 기록

이 문서는 `rag_study_assistant` 프로젝트의 Google Colab 기반 LoRA 학습 테스트 과정을 정리한 문서이다.

현재 로컬 Windows 환경은 CPU 기반 개발 환경이므로 Flask 서버 실행, REST API 테스트, 데이터 변환 및 검증을 담당한다. 실제 LLM 학습은 GPU가 필요한 작업이므로 Google Colab T4 GPU 환경에서 테스트를 진행했다.

---

## 1. Colab 런타임 설정

Colab 메뉴에서 다음과 같이 설정한다.

```text
런타임 → 런타임 유형 변경 → 하드웨어 가속기 → T4 GPU
```

GPU 확인:

```python
!nvidia-smi
```

PyTorch CUDA 확인:

```python
import torch

print("torch version:", torch.__version__)
print("cuda available:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("gpu:", torch.cuda.get_device_name(0))
else:
    print("gpu: CPU only")
```

확인 결과:

```text
torch version: 2.10.0+cu128
cuda available: True
gpu: Tesla T4
```

---

## 2. GitHub 프로젝트 가져오기

```python
%cd /content
!git clone https://github.com/niabluelake/rag_study_assistant.git
%cd /content/rag_study_assistant
```

파일 확인:

```python
!ls
!ls training
!ls data/processed
```

---

## 3. 학습 패키지 설치

```python
!pip install -r requirements-train.txt
```

설치 후 환경 확인:

```python
!python training/check_environment.py
```

데이터셋 검증:

```python
!python training/check_dataset.py
```

프롬프트 미리보기:

```python
!python training/preview_training_data.py --limit 2
```

확인 결과:

```text
train: 2 examples
eval: 1 examples
instruction / input / output 구조 확인 완료
```

---

## 4. Hugging Face 로그인 및 모델 접근 확인

Hugging Face Access Token을 이용하여 로그인한다.

```python
!hf auth login
```

로그인 확인:

```python
!hf auth whoami
```

Llama 3.2 1B 접근 확인:

```python
!hf download meta-llama/Llama-3.2-1B config.json
```

성공 결과:

```text
config.json: 100% 843/843
Downloaded
path: /root/.cache/huggingface/hub/models--meta-llama--Llama-3.2-1B/...
```

이를 통해 `meta-llama/Llama-3.2-1B` 모델 접근 권한이 정상적으로 확인되었다.

---

## 5. 미니 LoRA 학습 테스트 명령

Colab T4 GPU 환경에서 다음 명령으로 1 epoch 테스트 학습을 시도했다.

```python
!python training/train_lora.py \
  --model-name meta-llama/Llama-3.2-1B \
  --train-path data/processed/train.json \
  --eval-path data/processed/eval.json \
  --output-dir outputs/health_lora_model_test \
  --epochs 1 \
  --batch-size 1 \
  --gradient-accumulation-steps 4 \
  --learning-rate 2e-4 \
  --max-seq-length 512 \
  --use-4bit
```

---

## 6. Colab 테스트 중 확인된 성공 항목

```text
[성공] T4 GPU 사용 가능 확인
[성공] PyTorch CUDA 활성화 확인
[성공] GitHub 프로젝트 clone
[성공] requirements-train.txt 설치
[성공] 학습 데이터셋 로드
[성공] train/eval 데이터 검증
[성공] Hugging Face 로그인
[성공] meta-llama/Llama-3.2-1B 접근 승인 확인
[성공] Llama 3.2 1B 모델 다운로드
[성공] 4-bit quantization 설정
[성공] LoRA config 생성
[성공] SFTTrainer 생성
[성공] 데이터 formatting / EOS 추가 / tokenizing 진행
[성공] train loop 진입
```

---

## 7. 발생한 주요 호환성 문제

Colab에서 `trl`, `transformers`, `accelerate`, `torch` 버전 차이로 인해 일부 코드 호환성 문제가 발생했다.

### 7.1 SFTTrainer tokenizer 인자 오류

오류:

```text
TypeError: SFTTrainer.__init__() got an unexpected keyword argument 'tokenizer'
```

원인:

```text
최신 TRL 버전에서 SFTTrainer의 tokenizer 인자가 processing_class로 변경됨
```

수정 방향:

```python
processing_class=tokenizer
```

---

### 7.2 SFTTrainer max_seq_length 인자 오류

오류:

```text
TypeError: SFTTrainer.__init__() got an unexpected keyword argument 'max_seq_length'
```

원인:

```text
현재 설치된 TRL 버전의 SFTTrainer가 max_seq_length 인자를 직접 받지 않음
```

수정 방향:

```text
SFTTrainer(...) 내부의 max_seq_length 인자 제거
```

---

### 7.3 T4 GPU BF16 / AMP 오류

오류:

```text
NotImplementedError: "_amp_foreach_non_finite_check_and_unscale_cuda" not implemented for 'BFloat16'
```

원인:

```text
Colab Tesla T4 환경에서 BF16 기반 mixed precision 처리 중 호환성 문제가 발생
```

수정 방향:

```text
bf16 사용 비활성화
fp16 또는 mixed precision 비활성화 필요
4-bit compute dtype을 torch.float16으로 지정
```

---

## 8. 현재 결론

Colab T4 환경에서 Llama 3.2 1B 기반 LoRA 학습 파이프라인을 테스트했다.

모델 다운로드, 4-bit quantization 로딩, LoRA 설정, SFTTrainer 생성, 데이터 토크나이징 및 학습 루프 진입까지 확인했다.

다만 현재 Colab 환경에서는 TRL 버전 변화와 mixed precision 설정 문제로 인해 최종 학습 step 완료까지는 추가 호환성 수정이 필요한 상태이다.

---

## 9. 발표 시 설명 문장

```text
Google Colab T4 GPU 환경에서 Llama 3.2 1B 기반 LoRA 학습 파이프라인을 검증했습니다.
Hugging Face gated model 접근 승인, 모델 다운로드, 4-bit quantization 로딩, LoRA 설정, SFTTrainer 생성 및 학습 루프 진입까지 확인했습니다.
다만 Colab의 최신 TRL 및 mixed precision 환경에서 일부 호환성 문제가 발생하여, 최종 학습 완료 단계는 추가 설정 조정이 필요한 상태입니다.
```

---

## 10. 향후 작업

```text
1. train_lora.py의 TRL 최신 버전 호환성 수정
2. SFTTrainer 인자 정리
3. Colab T4 기준 fp16 / mixed precision 설정 안정화
4. 미니 데이터셋으로 1 epoch 학습 완료 확인
5. outputs/health_lora_model_test 생성 확인
6. 학습된 adapter를 Google Drive에 백업
7. model_loader.py에 LoRA adapter 로딩 코드 연결
```
