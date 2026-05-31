from gangjing.core import build_review_prompt
from gangjing.templates import OUTPUT_SECTIONS, render_output_contract


def test_build_review_prompt_contains_input_role_and_format():
    prompt = build_review_prompt("我要做一个 AI Todo App，自动拆任务。", mode="product")

    assert "产品杠精" in prompt
    assert "我要做一个 AI Todo App" in prompt
    assert "# 杠精审查报告" in prompt
    assert "## 第六刀：下一步验证动作" in prompt
    assert "不羞辱用户身份" in prompt


def test_output_contract_contains_required_sections():
    contract = render_output_contract()
    for section in OUTPUT_SECTIONS:
        assert section in contract
