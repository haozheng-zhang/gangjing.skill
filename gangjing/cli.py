from __future__ import annotations

from pathlib import Path

import typer

from .config import load_llm_config
from .core import build_review_prompt
from .roles import ROLES

app = typer.Typer(
    name="gangjing",
    help="杠精.skill：你的 AI 朋友负责鼓励你，杠精负责救你。",
    no_args_is_help=True,
)


def resolve_input_file(input_file: Path) -> Path:
    candidates = [
        input_file,
        Path("gangjing-skill") / input_file,
        Path(__file__).resolve().parent.parent / input_file,
    ]

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    tried = "\n".join(f"- {candidate}" for candidate in candidates)
    raise typer.BadParameter(
        f"找不到输入文件：{input_file}\n已尝试：\n{tried}\n"
        "如果你在项目父目录运行，请使用：gangjing review gangjing-skill/examples/input_project_idea.txt --mode tech"
    )


def call_openai_compatible(prompt: str) -> str:
    config = load_llm_config()
    if not config.enabled:
        return prompt

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise typer.BadParameter("模型 API key 已配置，但未安装 openai。请运行: pip install openai") from exc

    client = OpenAI(api_key=config.api_key, base_url=config.base_url)
    response = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": "你是一个严格遵守输出格式的中文 Agent Skill。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content or ""


@app.command()
def review(
    input_file: Path = typer.Argument(..., help="要审查的文本文件"),
    mode: str = typer.Option("default", "--mode", "-m", help="杠精模式"),
    output: Path | None = typer.Option(None, "--output", "-o", help="输出 Markdown 文件"),
    prompt_only: bool = typer.Option(False, "--prompt-only", help="只生成 prompt，不调用模型"),
) -> None:
    """审查一个 idea、README、PRD、创业 pitch 或技术方案。"""
    if mode not in ROLES:
        valid = ", ".join(sorted(ROLES))
        raise typer.BadParameter(f"未知模式：{mode}。可用模式：{valid}")

    resolved_input = resolve_input_file(input_file)
    text = resolved_input.read_text(encoding="utf-8")
    prompt = build_review_prompt(text, mode=mode)

    result = prompt if prompt_only else call_openai_compatible(prompt)
    if output:
        output.write_text(result, encoding="utf-8")
    else:
        typer.echo(result)


@app.command("modes")
def modes() -> None:
    """列出所有杠精模式。"""
    for role in ROLES.values():
        typer.echo(f"{role.name}: {role.title} - {role.description}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
