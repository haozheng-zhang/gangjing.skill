from gangjing.config import load_llm_config


def test_deepseek_config_defaults(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_BASE_URL", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    monkeypatch.delenv("DEEPSEEK_BASE_URL", raising=False)
    monkeypatch.delenv("DEEPSEEK_MODEL", raising=False)
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")

    config = load_llm_config()

    assert config.enabled
    assert config.api_key == "test-key"
    assert config.base_url == "https://api.deepseek.com"
    assert config.model == "deepseek-chat"


def test_openai_config_takes_precedence(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "openai-key")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "deepseek-key")

    config = load_llm_config()

    assert config.api_key == "openai-key"
    assert config.base_url == "https://api.openai.com/v1"
    assert config.model == "gpt-4o-mini"
