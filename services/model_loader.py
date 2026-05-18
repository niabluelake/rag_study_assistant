"""
학습된 LLM 모델을 로드하는 모듈.

현재 로컬 개발 단계에서는 실제 모델을 로드하지 않는다.
Cloud Ubuntu에서 LoRA 학습이 끝난 뒤 이 파일에 모델 로딩 코드를 연결한다.
"""


class ModelNotLoadedError(RuntimeError):
    pass


class HealthLLMModel:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.is_loaded = False

    def load(self):
        """
        TODO:
        1. base model 로드
        2. tokenizer 로드
        3. LoRA adapter 로드
        4. self.is_loaded = True 설정
        """
        raise ModelNotLoadedError(
            "학습된 모델이 아직 로드되지 않았습니다. "
            "Cloud Ubuntu에서 LoRA 학습 후 모델 로딩 코드를 연결하세요."
        )

    def generate(self, prompt: str) -> str:
        if not self.is_loaded:
            raise ModelNotLoadedError("모델이 로드되지 않았습니다.")

        # TODO:
        # tokenizer(prompt)
        # model.generate()
        # tokenizer.decode()
        return ""


health_model = HealthLLMModel()
