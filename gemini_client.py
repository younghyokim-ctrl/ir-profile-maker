# Gemini Image API 호출 모듈 — 나노바나나 MCP 내부 API 호출 방식 완전 복제
import io
import time
from typing import List, Tuple

from google import genai
from google.genai import types
from PIL import Image


class GeminiProfileGenerator:
    def __init__(self, api_key: str, model: str = "gemini-3-pro-image-preview"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(
        self,
        raw_images: List[Tuple[bytes, str]],
        style_prompt: str,
    ) -> Image.Image:
        """프로필 사진 생성 (나노바나나 MCP API 호출 방식 완전 복제)

        Args:
            raw_images: [(raw_bytes, mime_type), ...] — 원본 바이너리 그대로
            style_prompt: 조합된 프롬프트

        나노바나나 동일 방식:
        - open(path, "rb").read() 원본 바이너리 → Part.from_bytes() 직접 전달
        - PIL 재인코딩/리사이즈 없음 → 원본 얼굴 디테일 100% 보존
        - Contents 순서: [이미지] → [grounding] → [프롬프트]
        - 1장 입력 → 2장 복제 (generate 모드 강제)
        """
        contents = []

        # 이미지를 먼저 배치 — 원본 바이너리 그대로
        if len(raw_images) == 1:
            # 1장 → 2장 복제 (generate 모드: 포즈 변경에 유리 + SKILL.md 동일)
            # edit 모드(1장)는 포즈 회전을 거부하는 경향 → generate 모드로 복원
            data, mime = raw_images[0]
            contents.append(types.Part.from_bytes(data=data, mime_type=mime))
            contents.append(types.Part.from_bytes(data=data, mime_type=mime))
        else:
            # 2~3장 → 전부 사용 (멀티이미지 학습)
            for data, mime in raw_images[:3]:
                contents.append(types.Part.from_bytes(data=data, mime_type=mime))

        # 나노바나나 grounding 프리픽스 (이미지와 프롬프트 사이에 주입)
        contents.append(
            "Use real-world knowledge and current information to create "
            "accurate, detailed images."
        )

        # 프롬프트를 마지막에 배치
        contents.append(style_prompt)

        # API 호출 (나노바나나 동일 설정 + 4K ImageConfig)
        # Python 3.9 SDK에서 ImageConfig(image_size="4K") 미지원 →
        # HttpOptions.extra_body로 REST API body에 직접 주입
        try:
            config = types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                http_options=types.HttpOptions(
                    extra_body={
                        "generationConfig": {
                            "imageConfig": {
                                "imageSize": "4K"
                            }
                        }
                    }
                ),
            )
        except (TypeError, AttributeError):
            # SDK 버전에 따라 HttpOptions 미지원 시 fallback
            config = types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            )

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=config,
        )

        # 결과 이미지 추출
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                    return Image.open(io.BytesIO(part.inline_data.data))

        raise RuntimeError("이미지 생성에 실패했습니다. 다른 사진으로 다시 시도해 주세요.")

    # ── 2-Pass 파이프라인: Generate → Face Restore ──

    def generate_two_pass(
        self,
        raw_images: list,
        style_prompt: str,
        face_restore_prompt: str,
        on_pass1_done=None,
    ) -> tuple:
        """2-Pass 파이프라인: 포즈 생성 → 얼굴 복원

        Returns: (final_image, pass1_image)
        """
        # === Pass 1: 포즈/스타일 생성 (얼굴 변형 감수) ===
        pass1_result = self.generate(raw_images, style_prompt)

        if on_pass1_done:
            on_pass1_done(pass1_result)

        # Pass 1 결과를 bytes로 변환
        buf = io.BytesIO()
        pass1_result.save(buf, format="PNG")
        pass1_bytes = buf.getvalue()

        # === Pass 2: Pass1 결과(수정대상) + 원본(참조) → 얼굴 보정 ===
        # 순서 핵심: Photo 1 = Pass1 결과(편집 대상), Photo 2 = 원본(얼굴 참조)
        # → Gemini가 "Photo 1을 수정한다" 의도로 인식 → 포즈/배경 유지 + 얼굴만 교정
        contents = []
        # Photo 1: Pass 1 결과 (수정 대상 — 포즈/배경/의상 유지)
        contents.append(types.Part.from_bytes(data=pass1_bytes, mime_type="image/png"))
        # Photo 2: 원본 사진 (얼굴 참조 소스)
        orig_data, orig_mime = raw_images[0]
        contents.append(types.Part.from_bytes(data=orig_data, mime_type=orig_mime))
        # grounding + 프롬프트
        contents.append(
            "Use real-world knowledge and current information to create "
            "accurate, detailed images."
        )
        contents.append(face_restore_prompt)

        try:
            config = types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                http_options=types.HttpOptions(
                    extra_body={
                        "generationConfig": {
                            "imageConfig": {"imageSize": "4K"}
                        }
                    }
                ),
            )
        except (TypeError, AttributeError):
            config = types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            )

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=config,
        )

        if response.candidates:
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                    return Image.open(io.BytesIO(part.inline_data.data)), pass1_result

        # Pass 2 실패 → Pass 1 결과만 반환
        return pass1_result, pass1_result

    # ── 재시도 래퍼 ──

    def generate_with_retry(
        self, *args, max_retries: int = 2, **kwargs
    ) -> Image.Image:
        """재시도 포함 생성"""
        last_error = None
        for attempt in range(max_retries + 1):
            try:
                return self.generate(*args, **kwargs)
            except Exception as e:
                last_error = e
                if attempt < max_retries:
                    time.sleep(3 * (attempt + 1))
        raise RuntimeError(
            f"생성 실패 ({max_retries + 1}회 시도): {last_error}"
        )

    def generate_two_pass_with_retry(
        self, *args, max_retries: int = 1, **kwargs
    ) -> tuple:
        """재시도 포함 2-Pass 생성"""
        last_error = None
        for attempt in range(max_retries + 1):
            try:
                return self.generate_two_pass(*args, **kwargs)
            except Exception as e:
                last_error = e
                if attempt < max_retries:
                    time.sleep(3 * (attempt + 1))
        raise RuntimeError(
            f"2-Pass 생성 실패 ({max_retries + 1}회 시도): {last_error}"
        )
