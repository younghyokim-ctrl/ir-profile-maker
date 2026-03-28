"""HTML 리포트 익스포터 — IR 프로필 사진 메이커"""
import base64
import io
import os
from datetime import datetime
from PIL import Image


def export_profile_html(image: Image.Image, selections: dict) -> str:
    """
    PIL Image와 선택 옵션 dict를 받아 자체 포함 HTML 파일로 저장하고 경로를 반환한다.

    Parameters
    ----------
    image : PIL.Image.Image
        생성된 프로필 이미지
    selections : dict
        {gender, style, pose, outfit, expression, hairstyle} 값이 담긴 dict

    Returns
    -------
    str
        저장된 HTML 파일의 절대 경로
    """
    # 1. 이미지 → base64 PNG
    buf = io.BytesIO()
    image.save(buf, format="PNG", optimize=False)
    img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    # 2. 메타
    now = datetime.now()
    timestamp_display = now.strftime("%Y년 %m월 %d일 %H:%M:%S")
    timestamp_file = now.strftime("%Y%m%d_%H%M%S")
    filename = f"프로필사진_{timestamp_file}.html"

    label_map = {
        "gender":     ("성별",    selections.get("gender", "-")),
        "style":      ("스타일",  selections.get("style", "-")),
        "outfit":     ("의상",    selections.get("outfit", "-")),
        "pose":       ("포즈",    selections.get("pose", "-")),
        "hairstyle":  ("머리스타일", selections.get("hairstyle", "-")),
        "expression": ("표정",    selections.get("expression", "-")),
    }

    # 3. 옵션 카드 HTML 생성
    option_cards_html = ""
    icons = {
        "gender": "🧑", "style": "🎨", "outfit": "👔",
        "pose": "🧍", "hairstyle": "💇", "expression": "😊",
    }
    for key, (label, value) in label_map.items():
        icon = icons.get(key, "•")
        option_cards_html += f"""
        <div class="option-card">
            <div class="option-icon">{icon}</div>
            <div class="option-label">{label}</div>
            <div class="option-value">{value}</div>
        </div>"""

    # 4. HTML 본문
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>프로필 사진 메이커 - 결과</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            min-height: 100vh;
            background: linear-gradient(135deg, #1a1040 0%, #2d1b69 40%, #6C63FF 100%);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            color: #f0f0f0;
            padding: 2rem 1rem 3rem;
        }}

        .container {{
            max-width: 780px;
            margin: 0 auto;
        }}

        /* ── 헤더 ── */
        .header {{
            text-align: center;
            margin-bottom: 2.5rem;
        }}

        .header h1 {{
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #ffffff 0%, #c4b5fd 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.4rem;
        }}

        .header .subtitle {{
            font-size: 0.9rem;
            color: rgba(255,255,255,0.55);
            letter-spacing: 0.3px;
        }}

        /* ── 이미지 카드 ── */
        .image-card {{
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 20px;
            padding: 2rem;
            text-align: center;
            margin-bottom: 1.8rem;
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 40px rgba(0,0,0,0.4);
        }}

        .image-card img {{
            max-width: 100%;
            width: 520px;
            border-radius: 14px;
            box-shadow: 0 12px 48px rgba(0,0,0,0.5);
            display: block;
            margin: 0 auto;
        }}

        .image-caption {{
            margin-top: 1rem;
            font-size: 0.82rem;
            color: rgba(255,255,255,0.45);
        }}

        /* ── 옵션 그리드 ── */
        .options-section {{
            margin-bottom: 1.8rem;
        }}

        .section-title {{
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            color: rgba(255,255,255,0.45);
            margin-bottom: 1rem;
        }}

        .options-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.9rem;
        }}

        @media (max-width: 520px) {{
            .options-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        .option-card {{
            background: rgba(255,255,255,0.07);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 1rem 0.8rem;
            text-align: center;
            transition: background 0.2s;
        }}

        .option-card:hover {{
            background: rgba(255,255,255,0.12);
        }}

        .option-icon {{
            font-size: 1.5rem;
            margin-bottom: 0.35rem;
        }}

        .option-label {{
            font-size: 0.7rem;
            color: rgba(255,255,255,0.45);
            margin-bottom: 0.25rem;
            letter-spacing: 0.3px;
        }}

        .option-value {{
            font-size: 0.88rem;
            font-weight: 600;
            color: #e0d9ff;
        }}

        /* ── 다운로드 버튼 ── */
        .download-section {{
            text-align: center;
            margin-bottom: 2rem;
        }}

        .btn-download {{
            display: inline-block;
            padding: 0.85rem 2.2rem;
            background: linear-gradient(135deg, #6C63FF 0%, #a78bfa 100%);
            color: #ffffff;
            font-size: 0.95rem;
            font-weight: 700;
            text-decoration: none;
            border-radius: 50px;
            box-shadow: 0 4px 20px rgba(108,99,255,0.45);
            transition: transform 0.15s, box-shadow 0.15s;
            cursor: pointer;
            border: none;
            letter-spacing: 0.2px;
        }}

        .btn-download:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 28px rgba(108,99,255,0.6);
        }}

        .btn-download:active {{
            transform: translateY(0);
        }}

        /* ── 타임스탬프 ── */
        .meta-row {{
            text-align: center;
            font-size: 0.78rem;
            color: rgba(255,255,255,0.35);
            margin-bottom: 2.5rem;
        }}

        /* ── 푸터 ── */
        .footer {{
            text-align: center;
            font-size: 0.78rem;
            color: rgba(255,255,255,0.3);
            padding-top: 1rem;
            border-top: 1px solid rgba(255,255,255,0.08);
        }}

        .footer strong {{
            color: rgba(255,255,255,0.5);
        }}
    </style>
</head>
<body>
    <div class="container">

        <!-- 헤더 -->
        <div class="header">
            <h1>📸 프로필 사진 메이커 - 결과</h1>
            <div class="subtitle">AI가 생성한 IR용 프로필 사진입니다</div>
        </div>

        <!-- 이미지 -->
        <div class="image-card">
            <img
                id="profile-img"
                src="data:image/png;base64,{img_b64}"
                alt="AI 생성 프로필 사진"
            />
            <div class="image-caption">AI 생성 프로필 사진</div>
        </div>

        <!-- 선택 옵션 -->
        <div class="options-section">
            <div class="section-title">선택한 옵션</div>
            <div class="options-grid">
                {option_cards_html}
            </div>
        </div>

        <!-- 다운로드 버튼 -->
        <div class="download-section">
            <a id="dl-btn" class="btn-download" download="프로필사진_{timestamp_file}.png">
                📥 PNG 이미지 다운로드
            </a>
        </div>

        <!-- 생성 시각 -->
        <div class="meta-row">
            생성 시각 · {timestamp_display}
        </div>

        <!-- 푸터 -->
        <div class="footer">
            <strong>Medistream</strong> · IR 프로필 사진 메이커
        </div>

    </div>

    <script>
        // base64 이미지를 PNG 파일로 다운로드
        (function () {{
            var img = document.getElementById('profile-img');
            var btn = document.getElementById('dl-btn');
            btn.href = img.src;
        }})();
    </script>
</body>
</html>
"""

    # 5. output/ 디렉토리 생성 후 저장
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)

    return file_path
