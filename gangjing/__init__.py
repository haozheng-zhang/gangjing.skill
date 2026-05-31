"""gangjing-skill: anti-bullshit review prompts for Chinese agent workflows."""

from .core import build_review_prompt, render_review_template
from .roles import get_role, list_roles

__all__ = ["build_review_prompt", "render_review_template", "get_role", "list_roles"]

__version__ = "0.1.0"
