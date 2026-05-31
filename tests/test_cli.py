from typer.testing import CliRunner

from gangjing.cli import app


runner = CliRunner()


def test_cli_prompt_only_outputs_prompt(tmp_path):
    input_file = tmp_path / "idea.txt"
    input_file.write_text("我想做一个通用 agent 插件系统。", encoding="utf-8")

    result = runner.invoke(app, ["review", str(input_file), "--mode", "tech", "--prompt-only"])

    assert result.exit_code == 0
    assert "技术杠精" in result.output
    assert "我想做一个通用 agent 插件系统" in result.output
    assert "# 杠精审查报告" in result.output


def test_cli_invalid_mode_fails(tmp_path):
    input_file = tmp_path / "idea.txt"
    input_file.write_text("hello", encoding="utf-8")

    result = runner.invoke(app, ["review", str(input_file), "--mode", "bad"])

    assert result.exit_code != 0
    assert "未知模式" in result.output


def test_cli_missing_file_has_helpful_error():
    result = runner.invoke(app, ["review", "missing.txt", "--prompt-only"])

    assert result.exit_code != 0
    assert "找不到输入文件" in result.output
    assert "gangjing-skill/examples/input_project_idea.txt" in result.output
