from __future__ import annotations

from .roles import get_role
from .templates import render_review_template


def build_review_prompt(text: str, mode: str = "default") -> str:
    if not text or not text.strip():
        raise ValueError("Input text is empty. 杠精可以嘴毒，但不能对空气开刀。")

    role = get_role(mode)
    return render_review_template(
        role_title=role.title,
        role_description=role.description,
        focus=role.focus,
        taboos=role.taboos,
        tone_level=role.tone_level,
        user_text=text,
    )
