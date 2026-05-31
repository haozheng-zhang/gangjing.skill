from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class LLMConfig:
    api_key: str | None
    base_url: str
    model: str

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)


def load_llm_config() -> LLMConfig:
    openai_key = os.getenv("OPENAI_API_KEY")
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    api_key = openai_key or deepseek_key
    default_base_url = "https://api.openai.com/v1" if openai_key else "https://api.deepseek.com"
    default_model = "gpt-4o-mini" if openai_key else "deepseek-chat"

    return LLMConfig(
        api_key=api_key,
        base_url=os.getenv("OPENAI_BASE_URL") or os.getenv("DEEPSEEK_BASE_URL") or default_base_url,
        model=os.getenv("OPENAI_MODEL") or os.getenv("DEEPSEEK_MODEL") or default_model,
    )
