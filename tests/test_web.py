from gangjing.web import build_chat_text


def test_build_chat_text_keeps_recent_messages():
    messages = [{"role": "user", "content": f"msg-{index}"} for index in range(10)]

    text = build_chat_text(messages)

    assert "msg-0" not in text
    assert "msg-2" in text
    assert "msg-9" in text
