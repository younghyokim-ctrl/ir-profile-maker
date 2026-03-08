# IR 프로필 사진 메이커 — Streamlit 메인 앱
import base64
import io
import os
import streamlit as st
from prompts import get_style_list, get_pose_list, get_outfit_list, get_expression_list, get_hairstyle_list, build_json_prompt
from image_utils import process_uploaded_image, image_to_bytes, get_raw_image_bytes
from gemini_client import GeminiProfileGenerator
from config import GEMINI_API_KEY, MODEL_NAME, THUMBNAIL_DIR


def _img_to_base64(path: str) -> str:
    """이미지 파일을 base64 문자열로 변환 (HTML 임베딩용)"""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ──────────────────────────────────────────────
# 페이지 설정 (반드시 첫 번째 Streamlit 호출)
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="프로필 사진 메이커",
    page_icon="📸",
    layout="centered",
)

# ──────────────────────────────────────────────
# 커스텀 CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
/* ── 전체 배경 & 폰트 ── */
.stApp {
    background: linear-gradient(135deg, #f8f9fc 0%, #e8ecf4 100%);
}
html, body, [class*="css"] {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* ── 헤더 ── */
.header-area {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.header-area h1 {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6C63FF 0%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.header-area p {
    color: #6b7280;
    font-size: 1.05rem;
    margin: 0;
}

/* ── 스텝 배지 ── */
.step-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.55rem;
    margin-bottom: 0.75rem;
}
.step-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6C63FF, #a78bfa);
    color: #fff;
    font-weight: 700;
    font-size: 0.85rem;
    flex-shrink: 0;
}
.step-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #1f2937;
}

/* ── 카드 공통 ── */
.card {
    background: #ffffff;
    border: 2px solid #e5e7eb;
    border-radius: 12px;
    padding: 0.85rem 0.7rem;
    text-align: center;
    transition: all 0.22s cubic-bezier(.4,0,.2,1);
    cursor: pointer;
    min-height: 90px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(108,99,255,0.12);
    border-color: #c4b5fd;
}
.card.selected {
    border-color: #6C63FF;
    box-shadow: 0 0 0 3px rgba(108,99,255,0.18), 0 6px 20px rgba(108,99,255,0.12);
    background: linear-gradient(135deg, #faf9ff 0%, #f0edff 100%);
}
.card-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 0.25rem;
}
.card-desc {
    font-size: 0.75rem;
    color: #9ca3af;
    line-height: 1.35;
}

/* ── 업로드 영역 ── */
.upload-zone {
    background: #ffffff;
    border: 2px dashed #d1d5db;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    transition: border-color 0.2s;
}
.upload-zone:hover {
    border-color: #6C63FF;
}

/* ── 업로드 미리보기 ── */
.preview-grid {
    display: flex;
    gap: 0.75rem;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 1rem;
}
.preview-item {
    width: 120px;
    height: 120px;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border: 2px solid #e5e7eb;
}
.preview-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* ── 결과 카드 ── */
.result-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 12px 40px rgba(108,99,255,0.15);
    text-align: center;
    margin-top: 1rem;
}
.result-card img {
    border-radius: 12px;
    max-width: 100%;
}

/* ── 버튼 공통 (비선택 상태) ── */
div.stButton > button {
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    padding: 0.35rem 0.5rem !important;
    border: 1.5px solid #e5e7eb !important;
    background: #fff !important;
    color: #374151 !important;
    transition: all 0.18s !important;
}
div.stButton > button:hover {
    border-color: #6C63FF !important;
    color: #6C63FF !important;
}

/* ── 선택된 버튼 + 생성 버튼 (type=primary) ── */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6C63FF 0%, #a78bfa 100%) !important;
    color: #fff !important;
    border: 1.5px solid #6C63FF !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 12px rgba(108,99,255,0.3) !important;
    transition: all 0.22s !important;
}
div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #5b52e0, #9678f0) !important;
    color: #fff !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(108,99,255,0.4) !important;
}

/* ── 다운로드 버튼 ── */
div.stDownloadButton > button {
    background: #10b981 !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.7rem 1.5rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    transition: all 0.2s !important;
}
div.stDownloadButton > button:hover {
    background: #059669 !important;
    transform: translateY(-1px) !important;
}

/* ── 체크박스 라벨 ── */
div.stCheckbox label p, div.stCheckbox label span {
    color: #1f2937 !important;
}

/* ── st.status / st.write 텍스트 ── */
div[data-testid="stStatusWidget"] p,
div[data-testid="stStatusWidget"] span,
div[data-testid="stStatusWidget"] div,
div[data-testid="stExpander"] p,
div[data-testid="stExpander"] span {
    color: #1f2937 !important;
}

/* ── 구분선 ── */
.section-divider {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, #d1d5db, transparent);
    margin: 2rem 0;
}

/* ── 상태 메시지 ── */
.info-box {
    background: #eff6ff;
    border-left: 4px solid #6C63FF;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    color: #1e40af;
    font-size: 0.9rem;
    margin: 0.5rem 0;
}

/* ── 경고 박스 ── */
.warn-box {
    background: #fff7ed;
    border-left: 4px solid #f59e0b;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    color: #92400e;
    font-size: 0.9rem;
    margin: 0.5rem 0;
}

/* ── 모바일 반응형 ── */
@media (max-width: 768px) {
    .header-area h1 {
        font-size: 1.6rem;
    }
    .header-area p {
        font-size: 0.9rem;
    }
    .card {
        min-height: 70px;
        padding: 0.65rem 0.5rem;
    }
    .card-title {
        font-size: 0.85rem;
    }
    .card-desc {
        font-size: 0.7rem;
    }
    .preview-item {
        width: 90px;
        height: 90px;
    }
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# 세션 스테이트 초기화
# ──────────────────────────────────────────────
if "selected_gender" not in st.session_state:
    st.session_state.selected_gender = ""
if "selected_style" not in st.session_state:
    st.session_state.selected_style = "professional"
if "selected_outfit" not in st.session_state:
    st.session_state.selected_outfit = ""
if "selected_pose" not in st.session_state:
    st.session_state.selected_pose = "정면"
if "selected_expression" not in st.session_state:
    st.session_state.selected_expression = "neutral"
if "result_image" not in st.session_state:
    st.session_state.result_image = None
if "selected_hairstyle" not in st.session_state:
    st.session_state.selected_hairstyle = "original"

# ──────────────────────────────────────────────
# 데이터 로드
# ──────────────────────────────────────────────
styles = get_style_list()
poses = get_pose_list()

# ──────────────────────────────────────────────
# 헤더
# ──────────────────────────────────────────────
st.markdown("""
<div class="header-area">
    <h1>📸 프로필 사진 메이커</h1>
    <p>AI가 만들어주는 프로필 사진</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# STEP 1 — 사진 업로드
# ══════════════════════════════════════════════
st.markdown("""
<div class="step-badge">
    <span class="step-num">1</span>
    <span class="step-title">사진 업로드</span>
</div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "본인 사진 1~3장을 업로드하세요 (JPG, PNG, HEIC)",
    type=["jpg", "jpeg", "png", "heic", "heif", "webp"],
    accept_multiple_files=True,
    key="photo_upload",
)

# 업로드된 사진 미리보기
if uploaded_files:
    if len(uploaded_files) > 3:
        st.markdown('<div class="warn-box">⚠️ 최대 3장까지 업로드 가능합니다. 처음 3장만 사용됩니다.</div>', unsafe_allow_html=True)
        uploaded_files = uploaded_files[:3]

    preview_cols = st.columns(len(uploaded_files))
    user_images = []   # PIL Images — UI 미리보기 전용
    raw_images = []    # (bytes, mime_type) — API 전달용 원본 바이너리
    for i, f in enumerate(uploaded_files):
        img = process_uploaded_image(f)
        user_images.append(img)
        f.seek(0)  # process_uploaded_image가 파일 포인터를 소비했으므로 리셋
        raw_images.append(get_raw_image_bytes(f))
        with preview_cols[i]:
            st.image(img, caption=f.name, use_container_width=True)
else:
    user_images = []
    raw_images = []
    st.markdown('<div class="info-box">💡 얼굴이 잘 보이는 상반신 사진이 좋은 결과를 만듭니다.</div>', unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# STEP 2 — 성별 선택
# ══════════════════════════════════════════════
st.markdown("""
<div class="step-badge">
    <span class="step-num">2</span>
    <span class="step-title">성별 선택</span>
</div>
""", unsafe_allow_html=True)

GENDERS = [
    {"id": "male", "name_ko": "남성", "icon": "🧑"},
    {"id": "female", "name_ko": "여성", "icon": "👩"},
]
gender_cols = st.columns(2)
for i, g in enumerate(GENDERS):
    with gender_cols[i]:
        is_selected = st.session_state.selected_gender == g["id"]
        btn_label = f"✓ {g['icon']} {g['name_ko']}" if is_selected else f"{g['icon']} {g['name_ko']}"
        btn_type = "primary" if is_selected else "secondary"
        if st.button(btn_label, key=f"gender_{g['id']}", use_container_width=True, type=btn_type):
            if st.session_state.selected_gender != g["id"]:
                st.session_state.selected_gender = g["id"]
                st.session_state.selected_outfit = ""  # 성별 변경 시 의상 초기화
            st.rerun()

if not st.session_state.selected_gender:
    st.markdown('<div class="info-box">💡 성별을 선택하면 의상 옵션이 표시됩니다.</div>', unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# STEP 3 — 스타일 선택
# ══════════════════════════════════════════════
st.markdown("""
<div class="step-badge">
    <span class="step-num">3</span>
    <span class="step-title">스타일 선택</span>
</div>
""", unsafe_allow_html=True)

style_cols = st.columns(len(styles))
for i, style in enumerate(styles):
    with style_cols[i]:
        is_selected = st.session_state.selected_style == style["id"]
        # 썸네일 이미지를 base64로 HTML 임베딩
        thumb_path = os.path.join(THUMBNAIL_DIR, "styles", f"{style['id']}.jpg")
        if os.path.exists(thumb_path):
            b64 = _img_to_base64(thumb_path)
            border = "border: 3px solid #6C63FF; box-shadow: 0 0 0 3px rgba(108,99,255,0.18);" if is_selected else "border: 2px solid #e5e7eb;"
            st.markdown(
                f'<div style="{border} border-radius: 12px; overflow: hidden; margin-bottom: 0.4rem;">'
                f'<img src="data:image/jpeg;base64,{b64}" style="width:100%; display:block;" />'
                f'</div>',
                unsafe_allow_html=True,
            )
        # 버튼에 이름 + 설명 포함
        btn_label = f"✓ {style['name_ko']} · {style['desc']}" if is_selected else f"{style['name_ko']} · {style['desc']}"
        btn_type = "primary" if is_selected else "secondary"
        if st.button(btn_label, key=f"style_{style['id']}", use_container_width=True, type=btn_type):
            st.session_state.selected_style = style["id"]
            st.rerun()

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# STEP 4 — 의상 선택
# ══════════════════════════════════════════════
st.markdown("""
<div class="step-badge">
    <span class="step-num">4</span>
    <span class="step-title">의상 선택</span>
</div>
""", unsafe_allow_html=True)

if st.session_state.selected_gender:
    outfits = get_outfit_list(st.session_state.selected_gender)
    # 카테고리별 그룹핑: 원본 → 포멀 → 비즈니스 → 캐주얼
    cat_order = ["원본", "포멀", "비즈니스", "캐주얼"]
    cat_icons = {"원본": "📸", "포멀": "👔", "비즈니스": "💼", "캐주얼": "👕"}
    for cat in cat_order:
        cat_outfits = [o for o in outfits if o["category"] == cat]
        if not cat_outfits:
            continue
        st.markdown(f'<div style="font-size:0.85rem; font-weight:600; color:#6b7280; margin:0.5rem 0 0.3rem;">{cat_icons.get(cat, "")} {cat}</div>', unsafe_allow_html=True)
        outfit_cols = st.columns(len(cat_outfits))
        for j, outfit in enumerate(cat_outfits):
            with outfit_cols[j]:
                is_selected = st.session_state.selected_outfit == outfit["id"]
                btn_label = f"✓ {outfit['name_ko']}" if is_selected else outfit["name_ko"]
                btn_type = "primary" if is_selected else "secondary"
                if st.button(btn_label, key=f"outfit_{outfit['id']}", use_container_width=True, type=btn_type, help=outfit["desc"]):
                    st.session_state.selected_outfit = outfit["id"]
                    st.rerun()
else:
    st.markdown('<div class="info-box">💡 성별을 먼저 선택해주세요.</div>', unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# STEP 5 — 포즈 선택
# ══════════════════════════════════════════════
st.markdown("""
<div class="step-badge">
    <span class="step-num">5</span>
    <span class="step-title">포즈 선택</span>
</div>
""", unsafe_allow_html=True)

# 2행 x 5열 배치
for row in range(2):
    pose_cols = st.columns(5)
    for col_idx in range(5):
        pose_index = row * 5 + col_idx
        if pose_index >= len(poses):
            break
        pose = poses[pose_index]
        with pose_cols[col_idx]:
            is_selected = st.session_state.selected_pose == pose["id"]
            # 썸네일 이미지를 base64로 HTML 임베딩
            thumb_path = os.path.join(THUMBNAIL_DIR, "poses", f"{pose['id']}.jpg")
            if os.path.exists(thumb_path):
                b64 = _img_to_base64(thumb_path)
                border = "border: 3px solid #6C63FF; box-shadow: 0 0 0 3px rgba(108,99,255,0.18);" if is_selected else "border: 2px solid #e5e7eb;"
                st.markdown(
                    f'<div style="{border} border-radius: 12px; overflow: hidden; margin-bottom: 0.4rem;">'
                    f'<img src="data:image/jpeg;base64,{b64}" style="width:100%; display:block;" />'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            # 버튼에 이름 + 설명 포함
            btn_label = f"✓ {pose['name_ko']} · {pose['desc']}" if is_selected else f"{pose['name_ko']} · {pose['desc']}"
            btn_type = "primary" if is_selected else "secondary"
            if st.button(btn_label, key=f"pose_{pose['id']}", use_container_width=True, type=btn_type):
                st.session_state.selected_pose = pose["id"]
                st.rerun()

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# STEP 6 — 머리스타일 선택
# ══════════════════════════════════════════════
st.markdown("""
<div class="step-badge">
    <span class="step-num">6</span>
    <span class="step-title">머리스타일 선택</span>
</div>
""", unsafe_allow_html=True)

if st.session_state.selected_gender:
    hairstyles = get_hairstyle_list(st.session_state.selected_gender)
    hs_cols = st.columns(len(hairstyles))
    for i, hs in enumerate(hairstyles):
        with hs_cols[i]:
            is_selected = st.session_state.selected_hairstyle == hs["id"]
            btn_label = f"✓ {hs['icon']} {hs['name_ko']}" if is_selected else f"{hs['icon']} {hs['name_ko']}"
            btn_type = "primary" if is_selected else "secondary"
            if st.button(btn_label, key=f"hs_{hs['id']}", use_container_width=True, type=btn_type, help=hs["desc"]):
                st.session_state.selected_hairstyle = hs["id"]
                st.rerun()
else:
    st.markdown('<div class="info-box">💡 성별을 먼저 선택해주세요.</div>', unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# STEP 7 — 표정 선택
# ══════════════════════════════════════════════
st.markdown("""
<div class="step-badge">
    <span class="step-num">7</span>
    <span class="step-title">표정 선택</span>
</div>
""", unsafe_allow_html=True)

expressions = get_expression_list()
expr_cols = st.columns(len(expressions))
for i, expr in enumerate(expressions):
    with expr_cols[i]:
        is_selected = st.session_state.selected_expression == expr["id"]
        btn_label = f"✓ {expr['icon']} {expr['name_ko']}" if is_selected else f"{expr['icon']} {expr['name_ko']}"
        btn_type = "primary" if is_selected else "secondary"
        if st.button(btn_label, key=f"expr_{expr['id']}", use_container_width=True, type=btn_type, help=expr["desc"]):
            st.session_state.selected_expression = expr["id"]
            st.rerun()

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# STEP 8 — 생성
# ══════════════════════════════════════════════
st.markdown("""
<div class="step-badge">
    <span class="step-num">8</span>
    <span class="step-title">프로필 사진 생성</span>
</div>
""", unsafe_allow_html=True)

# 현재 선택 요약
selected_style_obj = next((s for s in styles if s["id"] == st.session_state.selected_style), styles[0])
selected_pose_obj = next((p for p in poses if p["id"] == st.session_state.selected_pose), poses[0])

# 의상 이름 가져오기
_outfit_name = ""
if st.session_state.selected_gender and st.session_state.selected_outfit:
    _outfits = get_outfit_list(st.session_state.selected_gender)
    _outfit_obj = next((o for o in _outfits if o["id"] == st.session_state.selected_outfit), None)
    _outfit_name = _outfit_obj["name_ko"] if _outfit_obj else ""

_gender_label = "남성" if st.session_state.selected_gender == "male" else "여성" if st.session_state.selected_gender == "female" else "미선택"
_outfit_label = _outfit_name if _outfit_name else "미선택"

# 표정 라벨
_expr_list = get_expression_list()
_expr_obj = next((e for e in _expr_list if e["id"] == st.session_state.selected_expression), _expr_list[0])
_expr_label = f"{_expr_obj['icon']} {_expr_obj['name_ko']}"

# 머리스타일 라벨
_hs_label = "원본 유지"
if st.session_state.selected_gender:
    _hs_list = get_hairstyle_list(st.session_state.selected_gender)
    _hs_obj = next((h for h in _hs_list if h["id"] == st.session_state.selected_hairstyle), None)
    if _hs_obj:
        _hs_label = f"{_hs_obj['icon']} {_hs_obj['name_ko']}"

st.markdown(f"""
<div class="info-box">
    🧑 <strong>{_gender_label}</strong> &nbsp;·&nbsp;
    🎨 <strong>{selected_style_obj["name_ko"]}</strong> 스타일 &nbsp;·&nbsp;
    👔 <strong>{_outfit_label}</strong> 의상 &nbsp;·&nbsp;
    🧍 <strong>{selected_pose_obj["name_ko"]}</strong> 포즈 &nbsp;·&nbsp;
    💇 <strong>{_hs_label}</strong> 머리 &nbsp;·&nbsp;
    {_expr_label} 표정 &nbsp;·&nbsp;
    📸 사진 {len(user_images)}장
</div>
""", unsafe_allow_html=True)

# API 키 확인
if not GEMINI_API_KEY:
    st.markdown('<div class="warn-box">⚠️ Gemini API 키가 설정되지 않았습니다. <code>.env</code> 파일에 GEMINI_API_KEY를 추가해주세요.</div>', unsafe_allow_html=True)

# 생성 버튼
can_generate = bool(raw_images) and bool(GEMINI_API_KEY)

if st.button(
    "✨ 프로필 사진 생성하기",
    use_container_width=True,
    type="primary",
    disabled=not can_generate,
):
    import traceback

    prompt = build_json_prompt(
        st.session_state.selected_style,
        st.session_state.selected_pose,
        gender=st.session_state.selected_gender,
        outfit=st.session_state.selected_outfit,
        expression=st.session_state.selected_expression,
        hairstyle=st.session_state.selected_hairstyle,
        num_images=len(user_images),
    )

    generator = GeminiProfileGenerator(api_key=GEMINI_API_KEY, model=MODEL_NAME)

    with st.status("AI가 프로필 사진을 만들고 있습니다...", expanded=True) as status:
        st.markdown(
            '<div style="text-align:center; padding:0.8rem 0; font-size:1.1rem; color:#6C63FF; font-weight:600;">'
            '✨ 멋진 프로필 사진을 준비하고 있어요</div>',
            unsafe_allow_html=True,
        )
        st.write("📸 사진 분석 중...")
        st.write("🎨 스타일 적용 중...")
        try:
            result = generator.generate_with_retry(
                raw_images=raw_images,
                style_prompt=prompt,
            )
            st.session_state.result_image = result
            status.update(label="✅ 프로필 사진 완성!", state="complete")
        except Exception as e:
            status.update(label="❌ 생성 실패", state="error")
            st.error(f"생성 중 오류가 발생했습니다: {e}")
            st.code(traceback.format_exc(), language="text")

if not user_images:
    st.caption("사진을 먼저 업로드해주세요.")

# ══════════════════════════════════════════════
# 결과 표시
# ══════════════════════════════════════════════
if st.session_state.result_image is not None:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="step-badge">
        <span class="step-num">✓</span>
        <span class="step-title">완성된 프로필 사진</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.image(st.session_state.result_image, caption="AI 생성 프로필 사진", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 다운로드 버튼
    img_bytes = image_to_bytes(st.session_state.result_image, format="PNG")
    st.download_button(
        label="📥 PNG 다운로드",
        data=img_bytes,
        file_name="profile.png",
        mime="image/png",
        use_container_width=True,
    )

# ──────────────────────────────────────────────
# 푸터
# ──────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:2rem 0 1rem; color:#9ca3af; font-size:0.8rem;">
    Medistream · IR 프로필 사진 메이커
</div>
""", unsafe_allow_html=True)
