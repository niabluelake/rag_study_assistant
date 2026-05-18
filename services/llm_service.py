import os
from dotenv import load_dotenv

load_dotenv()

LLM_MODE = os.getenv("LLM_MODE", "mock")


def build_health_prompt(user_message: str) -> str:
    return f"""### Instruction:
사용자의 건강검진 및 생활습관 정보를 바탕으로 건강 위험 요인과 개선 방향을 설명하세요.

### Input:
{user_message}

### Response:
"""


def generate_mock_answer(user_message: str) -> str:
    return f"임시 챗봇 답변입니다. 입력한 메시지: {user_message}"


def generate_trained_answer(user_message: str) -> str:
    prompt = build_health_prompt(user_message)

    # TODO:
    # 1. Base model 로드
    # 2. LoRA adapter 로드
    # 3. tokenizer로 prompt 토큰화
    # 4. model.generate()
    # 5. 생성된 텍스트에서 Response 부분만 추출

    return (
        "아직 학습된 모델이 연결되지 않았습니다. "
        f"나중에 이 프롬프트로 추론합니다:\n\n{prompt}"
    )


def generate_answer(user_message: str) -> str:
    if LLM_MODE == "trained":
        return generate_trained_answer(user_message)

    return generate_mock_answer(user_message)