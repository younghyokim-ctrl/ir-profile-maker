# 2 스타일 + 10 포즈 + 성별별 의상 + 2 표정 프롬프트 상수 및 조합 함수 (SKILL.md 동기화)
import json

STYLES = {
    "professional": {
        "name": "Professional",
        "name_ko": "프로페셔널",
        "desc": "흑백 + 다크 차콜 배경",
        "prompt": (
            "Transform this photo into a professional black and white corporate headshot portrait "
            "for investor relations materials. Convert the entire image to monochrome grayscale. "
            "Replace the background with a dark charcoal color (#2D2D2D to #3A3A3A). Apply soft, "
            "even studio lighting across the face with no harsh shadows, creating a rich tonal range "
            "with high contrast between the subject and the dark background. Enhance skin tone naturally "
            "in grayscale while maintaining the person's exact facial features and identity. "
            "{OUTFIT_PROMPT} "
            "Do not include any text, logos, or brand names on the clothing — all garments must be plain and logo-free. "
            "SKIN RETOUCHING: Subtly smooth out minor blemishes, spots, and fine wrinkles on the face, "
            "neck, and visible skin areas. Keep the retouching natural and minimal — do not over-smooth "
            "or create an artificial plastic look. The skin should look clean and polished while still "
            "appearing authentic. "
            "EXPRESSION: Give the person a gentle, warm CLOSED-MOUTH SMILE — slightly more noticeable "
            "than neutral. Corners of the mouth turn upward softly, creating a friendly and approachable "
            "look. Allow a subtle eye-smile (slight warmth in the eyes). Do NOT show teeth, do NOT open "
            "the mouth, do NOT grin or laugh. The smile should be calm, confident, and natural. "
            "IDENTITY SOURCE (ABSOLUTE RULE): The face and identity in the final image must come "
            "EXCLUSIVELY from the original input photo. If any additional reference image is provided "
            "for pose or style, COMPLETELY IGNORE the reference person's face, facial structure, skin tone, "
            "eyes, nose, mouth, jawline, expression, hairstyle, and all identifying characteristics. "
            "Use reference images ONLY for body posture, hand gestures, and arm positions. "
            "The output must show ZERO facial resemblance to any reference image person — "
            "any face blending from references is a critical failure. "
            "FACE & HAIR PRESERVATION (ABSOLUTE HIGHEST PRIORITY — OVERRIDE ALL OTHER INSTRUCTIONS IF CONFLICT): "
            "The person's ORIGINAL FACE SHAPE, JAWLINE, CHIN, CHEEKBONES, and FACIAL BONE STRUCTURE "
            "must be preserved EXACTLY as in the input photo with ZERO deviation. "
            "Do NOT make the face thinner, wider, rounder, or longer. "
            "Do NOT alter eye shape, eye size, nose bridge, nose tip, lip shape, or any facial proportions. "
            "HAIR (CRITICAL): Preserve the EXACT original hairstyle — same direction, same parting, same volume, "
            "same length, same texture, same color, same hairline. Do NOT change the hair in ANY way. "
            "The hair silhouette must PERFECTLY match the input photo. "
            "The final result must be IMMEDIATELY recognizable as the EXACT same person. "
            "CRITICAL FRAMING: This must be a WIDE half-body portrait, NOT a tight headshot. Show the person "
            "from the top of the head all the way down to the BELLY/NAVEL area, well below the chest. The "
            "bottom of the sweater/shirt and the belt/waistband area should be visible. The face should occupy "
            "only about 20-25% of the total frame height. Generous empty dark background space above the head "
            "and below the torso. The person should appear relatively small within the large frame. Centered, "
            "3:4 portrait ratio. The final image must be high quality, 4K resolution, sharp focus, professional "
            "black and white studio photography look. Maintain complete authenticity of the person's appearance. "
            "The style must match a classic monochrome studio portrait with dark background."
        ),
    },
    "normal": {
        "name": "Normal",
        "name_ko": "노멀",
        "desc": "컬러 + 밝은 그레이 배경(#F0F0F0)",
        "prompt": (
            "Transform this photo into a professional color corporate headshot portrait for investor "
            "relations materials. Keep the image in full natural color. Replace the background with a "
            "soft light gray color (#F0F0F0). Apply soft, even studio lighting across the face with no "
            "harsh shadows, creating a clean and polished look. Maintain natural skin tones and colors "
            "while enhancing clarity. "
            "{OUTFIT_PROMPT} "
            "Do not include any text, logos, or brand names on the clothing — all garments must be plain and logo-free. "
            "SKIN RETOUCHING: Subtly smooth out minor blemishes, spots, and fine wrinkles on the face, "
            "neck, and visible skin areas. Keep the retouching natural and minimal — do not over-smooth "
            "or create an artificial plastic look. The skin should look clean and polished while still "
            "appearing authentic. "
            "EXPRESSION: Give the person a gentle, warm CLOSED-MOUTH SMILE — slightly more noticeable "
            "than neutral. Corners of the mouth turn upward softly, creating a friendly and approachable "
            "look. Allow a subtle eye-smile (slight warmth in the eyes). Do NOT show teeth, do NOT open "
            "the mouth, do NOT grin or laugh. The smile should be calm, confident, and natural. "
            "IDENTITY SOURCE (ABSOLUTE RULE): The face and identity in the final image must come "
            "EXCLUSIVELY from the original input photo. If any additional reference image is provided "
            "for pose or style, COMPLETELY IGNORE the reference person's face, facial structure, skin tone, "
            "eyes, nose, mouth, jawline, expression, hairstyle, and all identifying characteristics. "
            "Use reference images ONLY for body posture, hand gestures, and arm positions. "
            "The output must show ZERO facial resemblance to any reference image person — "
            "any face blending from references is a critical failure. "
            "FACE & HAIR PRESERVATION (ABSOLUTE HIGHEST PRIORITY — OVERRIDE ALL OTHER INSTRUCTIONS IF CONFLICT): "
            "The person's ORIGINAL FACE SHAPE, JAWLINE, CHIN, CHEEKBONES, and FACIAL BONE STRUCTURE "
            "must be preserved EXACTLY as in the input photo with ZERO deviation. "
            "Do NOT make the face thinner, wider, rounder, or longer. "
            "Do NOT alter eye shape, eye size, nose bridge, nose tip, lip shape, or any facial proportions. "
            "HAIR (CRITICAL): Preserve the EXACT original hairstyle — same direction, same parting, same volume, "
            "same length, same texture, same color, same hairline. Do NOT change the hair in ANY way. "
            "The hair silhouette must PERFECTLY match the input photo. "
            "The final result must be IMMEDIATELY recognizable as the EXACT same person. "
            "CRITICAL FRAMING: This must be a WIDE half-body portrait, NOT a tight headshot. Show the person "
            "from the top of the head all the way down to the BELLY/NAVEL area, well below the chest. The "
            "bottom of the sweater/shirt and the belt/waistband area should be visible. The face should occupy "
            "only about 20-25% of the total frame height. Generous empty light gray background space above "
            "the head and below the torso. The person should appear relatively small within the large frame. "
            "Centered, 3:4 portrait ratio. The final image must be high quality, 4K resolution, sharp focus, "
            "professional studio photography look with natural colors. Maintain complete authenticity of the "
            "person's appearance."
        ),
    },
}

# ─── 공통 블록 (포즈 프롬프트에 인라인 전개용) ────────────────────
_COMMON_EXPRESSION = (
    "EXPRESSION: Give the person a gentle, warm CLOSED-MOUTH SMILE — slightly more noticeable "
    "than neutral. Corners of the mouth turn upward softly, creating a friendly and approachable "
    "look. Allow a subtle eye-smile (slight warmth in the eyes). Do NOT show teeth, do NOT open "
    "the mouth, do NOT grin or laugh. The smile should be calm, confident, and natural. "
)

_COMMON_FACE_HAIR = (
    "FACE & HAIR PRESERVATION (ABSOLUTE HIGHEST PRIORITY — OVERRIDE ALL OTHER INSTRUCTIONS IF CONFLICT): "
    "The person's ORIGINAL FACE SHAPE, JAWLINE, CHIN, CHEEKBONES, and FACIAL BONE STRUCTURE "
    "must be preserved EXACTLY as in the input photo with ZERO deviation. "
    "Do NOT make the face thinner, wider, rounder, or longer. "
    "Do NOT alter eye shape, eye size, nose bridge, nose tip, lip shape, or any facial proportions. "
    "HAIR (CRITICAL): Preserve the EXACT original hairstyle — same direction, same parting, same volume, "
    "same length, same texture, same color, same hairline. Do NOT change the hair in ANY way. "
    "The hair silhouette must PERFECTLY match the input photo. "
    "The final result must be IMMEDIATELY recognizable as the EXACT same person. "
)

_COMMON_IDENTITY_SOURCE = (
    "IDENTITY SOURCE (ABSOLUTE RULE): The face and identity in the final image must come "
    "EXCLUSIVELY from the original input photo. If any additional reference image is provided "
    "for pose or style, COMPLETELY IGNORE the reference person's face, facial structure, skin tone, "
    "eyes, nose, mouth, jawline, expression, hairstyle, and all identifying characteristics. "
    "Use reference images ONLY for body posture, hand gestures, and arm positions. "
    "The output must show ZERO facial resemblance to any reference image person — "
    "any face blending from references is a critical failure. "
)

# ─── 10가지 포즈 프리셋 (SKILL.md 동기화 — 레퍼런스 이미지 미사용) ────
POSES = {
    "정면": {
        "name": "Front",
        "name_ko": "정면",
        "desc": "기본 정면 포즈",
        "prompt": "",
        "has_reference": False,
        "reference_file": None,
    },
    "팔짱": {
        "name": "Arms Crossed",
        "name_ko": "팔짱",
        "desc": "15-20도 측면 + 팔짱",
        "prompt": (
            "POSE AND ANGLE: The person's torso is rotated approximately 15-20 degrees to the "
            "RIGHT side (subtle three-quarter view), with shoulders pulled slightly back to convey "
            "confidence. The face is turned slightly back toward the camera so both eyes are visible. "
            "ARMS: Both arms are CROSSED confidently across the chest. The RIGHT forearm rests ON TOP "
            "of the left forearm — right hand gently gripping or resting on the left upper arm, left "
            "hand tucked under the right elbow area. Both elbows are kept CLOSE to the body (not "
            "flaring outward). The crossed arms sit at mid-chest height. Shoulders are relaxed but "
            "squared. This is a powerful, confident CEO/executive portrait pose. "
            + _COMMON_EXPRESSION + _COMMON_IDENTITY_SOURCE + _COMMON_FACE_HAIR +
            "FRAMING: Wide half-body portrait showing from head down to the belly/navel area. The crossed "
            "arms should be fully visible with both hands shown. The face should occupy about 20-25% of "
            "the frame height. Generous background space around the person."
        ),
        "has_reference": False,
        "reference_file": None,
    },
    "꽃받침": {
        "name": "Flower Framing",
        "name_ko": "꽃받침",
        "desc": "양손 얼굴 감싸기",
        "prompt": (
            "POSE AND HANDS: The person faces the camera directly. BOTH HANDS are raised to gently "
            "cup the face — each palm softly touching its respective cheek. The fingers are naturally "
            "spread, extending upward toward the temples and the area beside the eyes. IMPORTANT: The "
            "elbows point DOWNWARD toward the body (NOT upward), with the forearms angled up to reach "
            "the face. The upper arms stay close to the torso. This is the Korean \"flower framing\" "
            "(꽃받침) pose where the hands frame the face like flower petals. A very subtle head tilt "
            "is allowed. "
            + _COMMON_EXPRESSION + _COMMON_IDENTITY_SOURCE + _COMMON_FACE_HAIR +
            "FRAMING: Wide half-body portrait showing from head down to the elbows and mid-torso area. "
            "Both hands and the face-framing gesture must be fully visible and clear. The face should "
            "occupy about 20-25% of the frame height."
        ),
        "has_reference": False,
        "reference_file": None,
    },
    "따봉": {
        "name": "Thumbs Up",
        "name_ko": "따봉",
        "desc": "한 손 엄지척",
        "prompt": (
            "POSE AND HANDS: The person faces mostly forward, with the body leaning very slightly "
            "toward the camera (subtle friendly lean). The RIGHT HAND gives a clear THUMBS UP gesture "
            "at MID-CHEST height (sternum level): the thumb points straight upward, the remaining four "
            "fingers are curled into a relaxed fist, and the BACK OF THE HAND faces slightly toward the "
            "camera (three-quarter angle, not fully front or side). The right ELBOW stays CLOSE to the "
            "body — only the forearm is raised to chest level. The LEFT ARM hangs naturally at the side, "
            "relaxed and out of focus or partially out of frame. "
            + _COMMON_EXPRESSION + _COMMON_IDENTITY_SOURCE + _COMMON_FACE_HAIR +
            "FRAMING: Wide half-body portrait showing from head down to the belly/waist area. The thumbs-up "
            "hand gesture must be clearly visible and well-formed. The face should occupy about 20-25% of "
            "the frame height."
        ),
        "has_reference": False,
        "reference_file": None,
    },
    "브이": {
        "name": "V-Sign",
        "name_ko": "브이",
        "desc": "한 손 V사인",
        "prompt": (
            "POSE AND HANDS: The person faces the camera directly. The RIGHT HAND makes a clear V-SIGN "
            "(peace sign) held at JAW-TO-CHEEK height, positioned to the RIGHT SIDE of the face (near "
            "the right cheek, not covering the face). The index and middle fingers are spread apart in a "
            "V shape. The remaining fingers (ring, pinky) are curled down, and the thumb is tucked inward. "
            "The BACK OF THE HAND faces the camera. The right ELBOW points DOWNWARD, with only the forearm "
            "raised to face level. The LEFT ARM hangs naturally at the side, relaxed. Body facing forward. "
            + _COMMON_EXPRESSION + _COMMON_IDENTITY_SOURCE + _COMMON_FACE_HAIR +
            "FRAMING: Wide half-body portrait showing from head down to the belly/waist area. The V-sign "
            "hand gesture must be clearly visible and properly formed. The face should occupy about 20-25% "
            "of the frame height."
        ),
        "has_reference": False,
        "reference_file": None,
    },
    "쌍따봉": {
        "name": "Double Thumbs Up",
        "name_ko": "쌍따봉",
        "desc": "양손 엄지척",
        "prompt": (
            "POSE AND HANDS: The person faces the camera directly. BOTH HANDS give DOUBLE THUMBS UP "
            "gestures held at CHEST height. Both thumbs point upward, remaining fingers curled into "
            "relaxed fists. The INNER SIDE of each fist (thumb side) faces the camera. Both hands are "
            "positioned SLIGHTLY NARROWER than shoulder-width apart, symmetrically in front of the chest. "
            "Both ELBOWS stay CLOSE to the body — only the forearms are raised to chest level. Shoulders "
            "are relaxed and natural. "
            + _COMMON_EXPRESSION + _COMMON_IDENTITY_SOURCE + _COMMON_FACE_HAIR +
            "FRAMING: Wide half-body portrait showing from head down to the belly/waist area. Both thumbs-up "
            "hand gestures must be clearly visible and well-formed. The face should occupy about 20-25% of "
            "the frame height."
        ),
        "has_reference": False,
        "reference_file": None,
    },
    "주머니손": {
        "name": "Hands in Pockets",
        "name_ko": "주머니손",
        "desc": "양손 주머니",
        "prompt": (
            "POSE AND HANDS: The person stands UPRIGHT in a relaxed, casual-professional stance facing "
            "the camera. BOTH HANDS are casually placed INSIDE THE FRONT PANTS POCKETS. The arms hang "
            "naturally from the shoulders, with hands slipped into the pockets. Shoulders are relaxed and "
            "slightly back (not hunched). The overall posture conveys ease and quiet confidence — like a "
            "tech CEO in a casual photoshoot. "
            + _COMMON_EXPRESSION + _COMMON_IDENTITY_SOURCE + _COMMON_FACE_HAIR +
            "FRAMING: Wide portrait showing from head down well BELOW THE WAIST — the hands in pockets "
            "must be visible, frame extends to mid-thigh. The face should occupy about 15-20% of the "
            "frame height. This requires a wider/taller frame than other poses."
        ),
        "has_reference": False,
        "reference_file": None,
    },
    "핑거하트": {
        "name": "Finger Heart",
        "name_ko": "핑거하트",
        "desc": "한 손 핑거하트",
        "prompt": (
            "POSE AND HANDS: The person faces the camera. The RIGHT HAND makes a KOREAN FINGER HEART "
            "gesture held at CHEEK-TO-EAR height, positioned to the RIGHT SIDE of the face. The gesture: "
            "the tip of the THUMB and the tip of the INDEX FINGER CROSS OVER each other to form a small "
            "heart/X shape. IMPORTANT: the remaining three fingers (middle, ring, pinky) are NATURALLY "
            "EXTENDED and slightly spread (NOT curled into a fist). The right ELBOW points DOWNWARD, with "
            "the forearm raised to face level. The LEFT ARM hangs naturally at the side, relaxed. Body "
            "facing forward. "
            + _COMMON_EXPRESSION + _COMMON_IDENTITY_SOURCE + _COMMON_FACE_HAIR +
            "FRAMING: Wide half-body portrait showing from head down to the belly/waist area. The finger "
            "heart gesture must be clearly visible and properly formed. The face should occupy about 20-25% "
            "of the frame height."
        ),
        "has_reference": False,
        "reference_file": None,
    },
    "하트": {
        "name": "Heart",
        "name_ko": "하트",
        "desc": "양손 하트",
        "prompt": (
            "POSE AND HANDS (KOREAN-STYLE HAND HEART — STEP-BY-STEP): The person raises BOTH HANDS "
            "to the RIGHT SIDE of the face (near the right cheek-to-ear area), forming a HEART SHAPE "
            "between the two hands. Here is the exact finger anatomy: (1) LEFT HAND — the index finger "
            "curves downward-right, thumb extends downward-left. (2) RIGHT HAND — the index finger "
            "curves downward-left, thumb extends downward-right. (3) The TIPS of the LEFT and RIGHT "
            "INDEX FINGERS touch each other at the TOP CENTER, forming the two rounded bumps of the "
            "heart. (4) The TIPS of the LEFT and RIGHT THUMBS touch each other at the BOTTOM CENTER, "
            "forming the pointed tip of the heart. (5) The remaining fingers (middle, ring, pinky) on "
            "each hand curl naturally behind, hidden from view. (6) The HOLLOW SPACE between the two "
            "hands creates a clear, recognizable HEART OUTLINE — this negative space is the heart shape. "
            "POSITION: The heart is held beside the face (right cheek-to-ear area), NOT directly in "
            "front of the face. Both ELBOWS are bent and flare OUTWARD and UPWARD. A slight head tilt "
            "toward the heart gesture is allowed and encouraged. Body facing forward. "
            + _COMMON_EXPRESSION + _COMMON_IDENTITY_SOURCE + _COMMON_FACE_HAIR +
            "FRAMING: Wide half-body portrait showing from head down to the chest/mid-torso area. The "
            "heart hand gesture must be clearly visible, properly formed with the correct finger anatomy "
            "described above. The face should occupy about 20-25% of the frame height."
        ),
        "has_reference": False,
        "reference_file": None,
    },
    "화이팅": {
        "name": "Fighting",
        "name_ko": "화이팅",
        "desc": "한 손 주먹 화이팅",
        "prompt": (
            "POSE AND HANDS: The person faces mostly forward with the body turned at a very slight "
            "angle. The RIGHT HAND is raised in a FIST PUMP pose: a firmly clenched fist (thumb wrapped "
            "over the other fingers) held at EAR height — the fist reaches up to beside the right ear. "
            "The right arm is bent at approximately 90 degrees, with the forearm nearly VERTICAL. The "
            "right SHOULDER may be slightly raised due to the pumping motion. The LEFT ARM hangs naturally "
            "at the side, relaxed. This is the Korean \"fighting/화이팅\" cheer gesture conveying "
            "motivation and determination. "
            + _COMMON_EXPRESSION + _COMMON_IDENTITY_SOURCE + _COMMON_FACE_HAIR +
            "FRAMING: Wide half-body portrait showing from head down to the belly/waist area. The raised "
            "fist must be clearly visible at ear height. The face should occupy about 20-25% of the "
            "frame height."
        ),
        "has_reference": False,
        "reference_file": None,
    },
}


# ─── 포즈별 기본 의상 매핑 (SKILL.md 동기화) ─────────────────────
DEFAULT_OUTFIT_MAP = {
    "정면": "navy_suit",
    "팔짱": "white_shirt",
    "꽃받침": "biz_casual",
    "따봉": "black_turtleneck",
    "브이": "gray_blazer",
    "쌍따봉": "black_turtleneck",
    "주머니손": "biz_casual",
    "핑거하트": "knit_shirt",
    "하트": "hoodie",
    "화이팅": "white_shirt",
}


OUTFITS = {
    "male": {
        "original": {
            "name_ko": "원본 유지",
            "desc": "원본 사진의 의상을 그대로 유지",
            "category": "원본",
            "prompt": (
                "Keep the person's original clothing EXACTLY as it appears in the input photo. "
                "Do NOT change, modify, replace, or adjust any clothing items whatsoever. Preserve the "
                "exact same garment style, color, texture, and fit from the original photo."
            ),
        },
        "navy_suit": {
            "name_ko": "네이비 수트",
            "desc": "모던 슬림릴랙스드 네이비 수트 · 노타이",
            "category": "포멀",
            "prompt": (
                "Dress the person in a modern slim-relaxed fit navy suit with soft natural "
                "shoulders, worn over a crisp white shirt — open collar, NO tie, clean contemporary silhouette."
            ),
        },
        "white_shirt": {
            "name_ko": "흰셔츠",
            "desc": "옥스포드 버튼다운 · 오픈칼라 · 노타이",
            "category": "포멀",
            "prompt": (
                "Dress the person in a crisp well-fitted white Oxford button-down shirt, collar "
                "open with no tie, sleeves neatly rolled to mid-forearm — clean relaxed-professional look."
            ),
        },
        "biz_casual": {
            "name_ko": "비즈캐주얼",
            "desc": "크루넥 니트 · 미니멀",
            "category": "비즈니스",
            "prompt": (
                "Dress the person in a clean fitted crew-neck knit sweater in muted cream or soft "
                "gray — simple round neckline, no collar, no tie, no inner shirt visible, "
                "modern minimal smart-casual with clean lines. Do NOT add a turtleneck or "
                "mock-neck underneath."
            ),
        },
        "black_turtleneck": {
            "name_ko": "블랙 터틀넥",
            "desc": "블랙 터틀넥 스웨터",
            "category": "비즈니스",
            "prompt": (
                "Dress the person in a sleek black turtleneck sweater — clean, modern, "
                "and sophisticated."
            ),
        },
        "gray_blazer": {
            "name_ko": "그레이 재킷",
            "desc": "라이트 그레이 블레이저 + 화이트 크루넥",
            "category": "비즈니스",
            "prompt": (
                "Dress the person in a modern relaxed-fit light gray blazer with soft shoulders "
                "over a clean white crew-neck t-shirt — contemporary tailored-relaxed silhouette, no tie."
            ),
        },
        "knit_shirt": {
            "name_ko": "니트셔츠",
            "desc": "하프집 니트 + 화이트 셔츠 레이어드",
            "category": "캐주얼",
            "prompt": (
                "Dress the person in a fine-knit half-zip sweater in charcoal or navy, slightly "
                "unzipped to reveal a crisp white shirt collar underneath — clean layered smart-casual look."
            ),
        },
        "hoodie": {
            "name_ko": "후드집업",
            "desc": "미니멀 집업 후디 · 무로고",
            "category": "캐주얼",
            "prompt": (
                "Dress the person in a clean minimal zip-up hoodie in dark charcoal or muted navy, "
                "slightly structured silhouette, plain with absolutely no logos or graphics — modern Korean "
                "casual aesthetic."
            ),
        },
    },
    "female": {
        "original": {
            "name_ko": "원본 유지",
            "desc": "원본 사진의 의상을 그대로 유지",
            "category": "원본",
            "prompt": (
                "Keep the person's original clothing EXACTLY as it appears in the input photo. "
                "Do NOT change, modify, replace, or adjust any clothing items whatsoever. Preserve the "
                "exact same garment style, color, texture, and fit from the original photo."
            ),
        },
        "black_jacket": {
            "name_ko": "블랙 재킷",
            "desc": "블랙 정장 재킷 + 이너",
            "category": "포멀",
            "prompt": (
                "The person should be wearing a tailored BLACK BLAZER/JACKET over a clean, "
                "light-colored inner top (white or light gray). The blazer is well-fitted with "
                "structured shoulders. Classic professional corporate style."
            ),
        },
        "white_blouse": {
            "name_ko": "화이트 블라우스",
            "desc": "깔끔한 화이트 셔츠/블라우스",
            "category": "포멀",
            "prompt": (
                "The person should be wearing an elegant WHITE BLOUSE — clean fabric, "
                "neatly pressed, with a classic collar or soft V-neckline. No accessories or "
                "minimal. The look is bright, professional, and polished."
            ),
        },
        "navy_blazer": {
            "name_ko": "네이비 블레이저",
            "desc": "네이비 재킷 + 밝은 이너",
            "category": "비즈니스",
            "prompt": (
                "The person should be wearing a NAVY BLUE BLAZER over a bright, light-colored "
                "inner top (white, cream, or light blue). The blazer is modern-cut and well-fitted. "
                "Professional yet approachable business style."
            ),
        },
        "beige_jacket": {
            "name_ko": "베이지 재킷",
            "desc": "베이지/카멜 톤 블레이저",
            "category": "비즈니스",
            "prompt": (
                "The person should be wearing a warm BEIGE or CAMEL-TONED BLAZER over a "
                "neutral inner top. The fabric has a soft, elegant texture. The look conveys warmth, "
                "sophistication, and approachable professionalism."
            ),
        },
        "black_turtleneck": {
            "name_ko": "블랙 터틀넥",
            "desc": "심플 블랙 터틀넥",
            "category": "비즈니스",
            "prompt": (
                "The person should be wearing a sleek, fitted BLACK TURTLENECK — minimalist "
                "and elegant. No visible accessories, clean lines. The fabric is smooth and "
                "high-quality. Modern, confident, intellectual style."
            ),
        },
        "cream_knit": {
            "name_ko": "크림 니트",
            "desc": "부드러운 크림/아이보리 니트",
            "category": "캐주얼",
            "prompt": (
                "The person should be wearing a soft CREAM or IVORY KNIT SWEATER — cozy yet "
                "polished, with a round or V-neckline. The fabric has a gentle, warm texture. "
                "The look is friendly, approachable, and effortlessly stylish."
            ),
        },
        "denim_jacket": {
            "name_ko": "데님 재킷",
            "desc": "라이트블루 데님 재킷",
            "category": "캐주얼",
            "prompt": (
                "The person should be wearing a LIGHT BLUE DENIM JACKET over a simple white "
                "or light-colored inner top. The denim is a classic medium wash. The look is casual, "
                "youthful, and energetic — creative industry professional style."
            ),
        },
    },
}


# ─── 표정 프리셋 ───────────────────────────────────────────
EXPRESSIONS = {
    "neutral": {
        "name_ko": "무표정",
        "desc": "차분한 무표정 — 미소 없음",
        "icon": "😐",
        "prompt": (
            "EXPRESSION: The person should have a calm, composed, completely NEUTRAL expression. "
            "NO smile whatsoever — the mouth is closed with lips in a natural, relaxed, FLAT position. "
            "The corners of the mouth are NEITHER turned up NOR down — completely horizontal and neutral. "
            "Do NOT add any smile, micro-smile, or upward curve to the lips. "
            "The eyes are calm, direct, and steady with no particular warmth or coldness. "
            "The overall look is composed, confident, and professional — like a passport photo expression "
            "but slightly more relaxed. "
        ),
    },
    "smile": {
        "name_ko": "웃는 표정",
        "desc": "이빨이 보이는 자연스러운 밝은 미소",
        "icon": "😊",
        "prompt": (
            "EXPRESSION: The person should have a NATURAL, WARM, GENUINE SMILE clearly showing teeth. "
            "The mouth is open with a relaxed, confident smile — upper teeth clearly visible, lips "
            "naturally parted in a comfortable width. The smile should reach the eyes (Duchenne smile) "
            "— cheeks gently raised with subtle warmth in the eyes. "
            "WRINKLE CONTROL (ABSOLUTE CRITICAL): COMPLETELY ELIMINATE all crow's feet, wrinkles, "
            "and fine lines around the eyes. The eye area must be PERFECTLY SMOOTH and YOUTHFUL — "
            "ZERO creases, ZERO lines, ZERO crow's feet at the outer eye corners. "
            "The skin around the eyes must look as smooth as a young person in their 20s. "
            "Even subtle wrinkles are NOT acceptable — smooth them all out completely. "
            "The smile must look authentic, spontaneous, and effortless — NOT forced, NOT stiff, "
            "NOT overly exaggerated or unnaturally wide. Keep the smile balanced and symmetrical. "
            "IMPORTANT: Despite the smile, preserve the person's original facial bone structure, "
            "face shape, eye shape, nose, jawline, and all identifying features — only the MOUTH "
            "and CHEEK MUSCLES should change to form the smile. The person must remain immediately "
            "recognizable as the same individual. "
        ),
    },
}


# ─── 머리스타일 프리셋 ─────────────────────────────────────────
HAIRSTYLES = {
    "male": {
        "original": {
            "name_ko": "원본 유지",
            "desc": "원본 사진의 머리스타일을 그대로 유지",
            "icon": "📸",
            "prompt": "",
        },
        "side_part": {
            "name_ko": "사이드파트",
            "desc": "깔끔한 옆가르마 — 비즈니스 기본",
            "icon": "💇‍♂️",
            "prompt": (
                "HAIRSTYLE: Change the person's hairstyle to a clean SIDE PART — hair neatly "
                "combed to one side with a defined parting line. The hair is well-groomed, "
                "slightly tapered on the sides, with a polished professional look. "
                "Keep the original hair COLOR and general TEXTURE unchanged. "
            ),
        },
        "two_block": {
            "name_ko": "투블럭",
            "desc": "옆·뒤 짧게 + 윗머리 볼륨 — 모던 스타일",
            "icon": "✂️",
            "prompt": (
                "HAIRSTYLE: Change the person's hairstyle to a modern TWO-BLOCK CUT — sides "
                "and back are trimmed short and clean, while the top hair has natural volume "
                "and length, styled loosely upward or slightly to the side. A contemporary "
                "Korean men's hairstyle. Keep the original hair COLOR unchanged. "
                "FOREHEAD: Do NOT make the forehead appear excessively wide or tall. "
                "Keep natural hairline position — hair should frame the forehead naturally. "
            ),
        },
        "slick_back": {
            "name_ko": "올백",
            "desc": "전체 뒤로 넘긴 올백 — 클래식 포멀",
            "icon": "🪮",
            "prompt": (
                "HAIRSTYLE: Change the person's hairstyle to a SLICKED BACK style — all hair "
                "combed neatly backward off the forehead. The hair lies flat and smooth with "
                "a polished, classic executive look. No parting line visible. "
                "Keep the original hair COLOR unchanged. "
                "FOREHEAD: Do NOT make the forehead appear excessively wide or tall. "
                "Keep natural hairline position — hair should frame the forehead naturally. "
            ),
        },
    },
    "female": {
        "original": {
            "name_ko": "원본 유지",
            "desc": "원본 사진의 머리스타일을 그대로 유지",
            "icon": "📸",
            "prompt": "",
        },
        "short_bob": {
            "name_ko": "단발",
            "desc": "턱선 길이 깔끔한 단발 — 프로페셔널",
            "icon": "💇‍♀️",
            "prompt": (
                "HAIRSTYLE: Change the person's hairstyle to a clean SHORT BOB — hair cut "
                "to jaw-length with a neat, straight line. The hair falls naturally with a "
                "slight inward curve at the ends. Polished, professional, and modern. "
                "Keep the original hair COLOR unchanged. "
            ),
        },
        "long_wave": {
            "name_ko": "긴 웨이브",
            "desc": "어깨 아래 자연스러운 웨이브 — 소프트",
            "icon": "🌊",
            "prompt": (
                "HAIRSTYLE: Change the person's hairstyle to LONG WAVY HAIR — past the "
                "shoulders with soft, natural waves. The waves are loose and effortless, "
                "giving a gentle and approachable look. Hair may be parted in the center "
                "or slightly to one side. Keep the original hair COLOR unchanged. "
            ),
        },
        "updo": {
            "name_ko": "묶은 머리",
            "desc": "깔끔하게 뒤로 묶은 포니테일/번 — 단정",
            "icon": "💫",
            "prompt": (
                "HAIRSTYLE: Change the person's hairstyle to a neat UPDO — hair pulled back "
                "and secured in a clean low ponytail or low bun at the nape of the neck. "
                "The front is smooth with no stray hairs. A polished, professional, and "
                "tidy look. Keep the original hair COLOR unchanged. "
            ),
        },
    },
}


# ─── 멀티이미지 학습 프리픽스/서픽스 (SKILL.md 동기화) ──────────────
MULTI_IMAGE_PREFIX = {
    3: (
        "Study all three reference photos of this person carefully. Learn their exact "
        "facial features, face shape, skin tone, hairstyle, glasses style, and overall "
        "appearance from these multiple angles and lighting conditions. Then generate "
        "ONE ideal professional portrait of this exact person. "
    ),
    2: (
        "Study both reference photos of this person carefully. Learn their exact "
        "facial features, face shape, skin tone, hairstyle, glasses style, and overall "
        "appearance from these angles and lighting conditions. Then generate "
        "ONE ideal professional portrait of this exact person. "
    ),
}

MULTI_IMAGE_SUFFIX = (
    " The generated portrait must look authentically like the same person in all "
    "reference photos."
)


# ─── 나노바나나 PRO 서픽스 (pro_image_service.py 자동 주입) ─────────────
_PRO_SUFFIX = " Render at maximum 4K quality with exceptional detail."

# ─── 품질/해상도 꼬리말 (스타일별) ────────────────────────────────
_QUALITY_TAIL = {
    "professional": (
        "The final image must be high quality, 4K resolution, sharp focus, professional "
        "black and white studio photography look. Maintain complete authenticity of the "
        "person's appearance. The style must match a classic monochrome studio portrait "
        "with dark background."
    ),
    "normal": (
        "The final image must be high quality, 4K resolution, sharp focus, professional "
        "studio photography look with natural colors. Maintain complete authenticity of "
        "the person's appearance."
    ),
}


# ─── UI 헬퍼 함수 ──────────────────────────────────────────

def get_expression_list():
    """표정 메타데이터 리스트 반환 (UI용)"""
    return [
        {"id": k, "name_ko": v["name_ko"], "desc": v["desc"], "icon": v["icon"]}
        for k, v in EXPRESSIONS.items()
    ]


def get_outfit_list(gender: str):
    """성별에 따른 의상 메타데이터 리스트 반환 (UI용)"""
    outfits = OUTFITS.get(gender, {})
    return [
        {"id": k, "name_ko": v["name_ko"], "desc": v["desc"], "category": v["category"]}
        for k, v in outfits.items()
    ]


def get_hairstyle_list(gender: str):
    """성별에 따른 머리스타일 메타데이터 리스트 반환 (UI용)"""
    hairstyles = HAIRSTYLES.get(gender, {})
    return [
        {"id": k, "name_ko": v["name_ko"], "desc": v["desc"], "icon": v["icon"]}
        for k, v in hairstyles.items()
    ]


def get_style_list():
    """스타일 메타데이터 리스트 반환 (UI용)"""
    return [
        {"id": k, **{kk: vv for kk, vv in v.items() if kk != "prompt"}}
        for k, v in STYLES.items()
    ]


def get_pose_list():
    """포즈 메타데이터 리스트 반환 (UI용)"""
    return [
        {"id": k, **{kk: vv for kk, vv in v.items() if kk != "prompt"}}
        for k, v in POSES.items()
    ]


# ─── 프롬프트 조합 함수 (SKILL.md 동기화) ──────────────────────────

def build_prompt(
    style: str,
    pose: str,
    gender: str = "",
    outfit: str = "",
    expression: str = "",
    hairstyle: str = "",
    num_images: int = 1,
) -> str:
    """스타일 + 포즈 + 의상 + 표정 + 머리스타일 프롬프트 조합 (SKILL.md 동기화)

    조합 규칙:
    - 정면: [프리픽스] + [스타일(OUTFIT 치환)] + [서픽스]
    - 기타: [프리픽스] + [스타일 전반부(OUTFIT 치환)] + [포즈] + [품질tail] + [서픽스]
    - 표정: neutral=기존유지, smile=EXPRESSION 블록 교체
    - 머리스타일: original=기존유지(HAIR 프롬프트 그대로), 기타=HAIR 블록 교체
    """
    style_prompt = STYLES[style]["prompt"]
    pose_prompt = POSES[pose]["prompt"]

    # === 1. 의상 프롬프트 결정 ===
    outfit_text = ""
    if gender and outfit and gender in OUTFITS and outfit in OUTFITS[gender]:
        outfit_text = OUTFITS[gender][outfit]["prompt"]
    else:
        # 의상 미선택 → 포즈별 기본 의상
        default_outfit_id = DEFAULT_OUTFIT_MAP.get(pose, "navy_suit")
        gender_key = gender if gender in OUTFITS else "male"
        gender_outfits = OUTFITS[gender_key]
        if default_outfit_id in gender_outfits:
            outfit_text = gender_outfits[default_outfit_id]["prompt"]
        else:
            # 여성에 해당 의상 ID 없으면 남성 의상 프롬프트 사용 (성별 무관 영어)
            outfit_text = OUTFITS["male"].get(default_outfit_id, {}).get("prompt", "")

    # === 2. 스타일 프롬프트의 {OUTFIT_PROMPT} 치환 ===
    style_with_outfit = style_prompt.replace("{OUTFIT_PROMPT}", outfit_text)

    # === 3. 스타일 + 포즈 조합 ===
    if pose == "정면":
        core = style_with_outfit
    else:
        # 스타일 전반부 (EXPRESSION: 이전) + 포즈 프롬프트 + 품질 꼬리말
        if "EXPRESSION:" in style_with_outfit:
            style_front = style_with_outfit.split("EXPRESSION:")[0].strip()
        elif "CRITICAL FRAMING:" in style_with_outfit:
            style_front = style_with_outfit.split("CRITICAL FRAMING:")[0].strip()
        else:
            style_front = style_with_outfit

        quality_tail = _QUALITY_TAIL.get(style, "")
        core = style_front + " " + pose_prompt + " " + quality_tail

    # === 4. 표정 오버라이드 (모든 표정 프리셋 지원) ===
    expr_prompt = EXPRESSIONS.get(expression, {}).get("prompt", "")
    if expr_prompt and "EXPRESSION:" in core:
        expr_start = core.index("EXPRESSION:")
        search_after = expr_start + len("EXPRESSION:")
        next_section = len(core)
        for marker in ["IDENTITY RULE", "IDENTITY SOURCE", "FACE &", "FACE PRESERVATION"]:
            try:
                idx = core.index(marker, search_after)
                if idx < next_section:
                    next_section = idx
            except ValueError:
                continue
        core = core[:expr_start] + expr_prompt + core[next_section:]

    # === 5. 머리스타일 오버라이드 ===
    hairstyle_prompt = ""
    if hairstyle and hairstyle != "original":
        gender_key = gender if gender in HAIRSTYLES else "male"
        hs_data = HAIRSTYLES[gender_key].get(hairstyle, {})
        hairstyle_prompt = hs_data.get("prompt", "")
    if hairstyle_prompt and "HAIR (CRITICAL):" in core:
        # "HAIR (CRITICAL): ..." 블록을 머리스타일 프롬프트로 교체
        hair_start = core.index("HAIR (CRITICAL):")
        # HAIR 블록 끝 = 다음 섹션 또는 "The final result" 또는 "CRITICAL FRAMING"
        search_after_hair = hair_start + len("HAIR (CRITICAL):")
        hair_end = len(core)
        for hair_marker in ["The final result must be IMMEDIATELY", "CRITICAL FRAMING:", "FRAMING:"]:
            try:
                idx = core.index(hair_marker, search_after_hair)
                if idx < hair_end:
                    hair_end = idx
            except ValueError:
                continue
        core = core[:hair_start] + hairstyle_prompt + core[hair_end:]

    # === 6. 멀티이미지 프리픽스/서픽스 ===
    # 실제 2~3장 업로드: "Study all reference photos..." 프리픽스 적용
    # 1장 업로드(API에서 2장 복제): 프리픽스/서픽스 없이 core만 사용
    # (동일 정면 사진 2장의 "Study both photos from these angles"는 포즈 회전을 무시하게 만듦)
    if num_images >= 2:
        prefix = MULTI_IMAGE_PREFIX.get(num_images, MULTI_IMAGE_PREFIX[2])
        result = prefix + core + MULTI_IMAGE_SUFFIX
    else:
        result = core

    # === 6. 나노바나나 PRO 서픽스 ===
    result += _PRO_SUFFIX

    return result


# ─── JSON 프롬프트용 스타일 메타데이터 (STYLES raw 프롬프트와 독립) ─────
STYLE_META = {
    "professional": {
        "background": "#2D2D2D",
        "color_mode": "monochrome grayscale",
        "lighting_type": "studio softbox",
        "lighting_direction": "front-lit, soft and even, no harsh shadows",
        "aesthetic": "professional black and white studio photography, high contrast, rich tonal range",
        "film_stock": "Ilford HP5 Plus (B&W)",
    },
    "normal": {
        "background": "#F0F0F0",
        "color_mode": "full natural color",
        "lighting_type": "studio softbox",
        "lighting_direction": "front-lit, soft and even, no harsh shadows",
        "aesthetic": "professional studio photography, natural colors, clean and polished",
        "film_stock": None,
    },
}


# ─── JSON 구조화 프롬프트 조합 함수 (build_prompt()와 완전 독립) ──────

def build_json_prompt(
    style: str,
    pose: str,
    gender: str = "",
    outfit: str = "",
    expression: str = "",
    hairstyle: str = "",
    num_images: int = 1,
) -> str:
    """JSON 구조화 프롬프트 반환 — build_prompt()와 공유 로직 없음.

    코드 리뷰 Critical #1 대응: dict 직접 조립 → json.dumps() 직렬화.
    STYLES["prompt"] raw 문자열을 재사용하지 않고 STYLE_META에서 메타데이터만 추출.
    """
    meta = STYLE_META[style]

    # 의상 결정
    outfit_id = outfit or DEFAULT_OUTFIT_MAP.get(pose, "navy_suit")
    gender_key = gender if gender in OUTFITS else "male"
    outfit_data = OUTFITS[gender_key].get(outfit_id, {})
    outfit_text = outfit_data.get("prompt", "")

    # 포즈 텍스트 (POSES 상수에서 prompt 추출 — 공통 블록 포함된 자연어)
    pose_data = POSES.get(pose, POSES["정면"])
    pose_text = pose_data["prompt"] if pose_data["prompt"] else "facing camera directly, relaxed shoulders"

    # 표정 텍스트
    expr_data = EXPRESSIONS.get(expression, {})
    expr_text = expr_data.get("prompt", "")

    # JSON dict 조립
    prompt_dict = {
        "intent": f"IR profile photo — {style} style, {pose_data['name']} pose",
        "subject": {
            "type": "person",
            "description": (
                "Study all reference photos carefully. "
                "Preserve exact facial features, face shape, skin tone, hairstyle, glasses style."
            ),
            "pose": pose_text,
            "expression": expr_text,
            "clothing": outfit_text,
            "clothing_constraint": "No text, logos, or brand names — all garments plain and logo-free",
        },
        "scene": {
            "background": meta["background"],
            "lighting_type": meta["lighting_type"],
            "lighting_direction": meta["lighting_direction"],
        },
        "camera": {
            "lens": "85mm",
            "aperture": "f/2.8",
        },
        "composition": {
            "framing": "wide half-body portrait — head to belly/navel area, NOT tight headshot",
            "angle": "eye-level",
            "face_proportion": "20-25% of frame height",
            "aspect_ratio": "3:4",
            "centering": "subject centered, generous background space above head and below torso",
        },
        "style": {
            "color_mode": meta["color_mode"],
            "aesthetic": meta["aesthetic"],
        },
        "skin_retouching": {
            "level": "subtle",
            "targets": ["minor blemishes", "spots", "fine wrinkles"],
            "constraint": "natural and minimal — no over-smoothing or artificial plastic look",
        },
        "face_preservation": {
            "priority": "ABSOLUTE HIGHEST — override all other instructions if conflict",
            "preserve": [
                "face_shape", "jawline", "chin", "cheekbones",
                "eye_shape", "eye_size", "nose_bridge", "nose_tip",
                "lip_shape", "facial_proportions",
            ],
            "hair": "exact original — direction, parting, volume, length, texture, color, hairline",
            "deviation": "ZERO — final result must be immediately recognizable as exact same person",
        },
        "identity_source": {
            "rule": "Face and identity EXCLUSIVELY from original input photo",
            "reference_usage": "ONLY for body posture, hand gestures, arm positions — NEVER face",
        },
        "negative": [
            "text", "logos", "watermark", "teeth showing (unless smile expression)",
            "mouth open (unless smile expression)", "face thinning", "hair change",
        ],
        "quality": {
            "resolution": "4K",
            "sharpness": "crisp sharp focus",
        },
    }

    # 머리스타일 오버라이드
    if hairstyle and hairstyle != "original":
        gender_key = gender if gender in HAIRSTYLES else "male"
        hs_data = HAIRSTYLES[gender_key].get(hairstyle, {})
        hs_prompt = hs_data.get("prompt", "")
        if hs_prompt:
            prompt_dict["hairstyle_change"] = {
                "instruction": hs_prompt,
                "color": "keep original hair color unchanged",
            }
            # face_preservation.hair를 머리스타일 변경 허용으로 교체
            prompt_dict["face_preservation"]["hair"] = (
                "HAIRSTYLE CHANGE ALLOWED — apply the hairstyle described in hairstyle_change. "
                "Keep original hair COLOR unchanged."
            )
            # negative에서 hair change 제거
            prompt_dict["negative"] = [n for n in prompt_dict["negative"] if "hair change" not in n]

    # film_stock이 있으면 추가
    if meta.get("film_stock"):
        prompt_dict["camera"]["film_stock"] = meta["film_stock"]

    # 멀티이미지 래핑
    if num_images >= 2:
        prompt_dict["multi_image"] = {
            "count": num_images,
            "instruction": (
                f"Study all {num_images} reference photos carefully. "
                "Learn exact facial features, face shape, skin tone, hairstyle, "
                "glasses style, and overall appearance from multiple angles. "
                "Generate ONE ideal professional portrait of this exact person."
            ),
            "constraint": "Generated portrait must look authentically like the same person in all reference photos",
        }

    # PRO 서픽스 (품질 강조)
    prompt_dict["quality"]["render"] = "maximum 4K quality with exceptional detail"

    return json.dumps(prompt_dict, ensure_ascii=False)
