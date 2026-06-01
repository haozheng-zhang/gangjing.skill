from __future__ import annotations

import argparse
import json
import os
import socket
import threading
import urllib.error
import urllib.request
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from .config import load_llm_config
from .core import build_review_prompt
from .roles import ROLES


INDEX_HTML = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>杠精.skill</title>
  <style>
    :root {
      --bg: #ffffff;
      --panel: #f7f7f8;
      --line: #e5e5e5;
      --text: #111111;
      --muted: #6b6b6b;
      --soft: #fafafa;
      --inverse: #111111;
      --inverse-text: #ffffff;
      --danger: #9f1d1d;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      letter-spacing: 0;
    }
    .shell {
      min-height: 100vh;
      display: grid;
      grid-template-columns: 272px minmax(0, 1fr);
    }
    aside {
      border-right: 1px solid var(--line);
      background: var(--panel);
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .brand {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      min-height: 36px;
    }
    .brand strong { font-size: 18px; }
    .brand span { color: var(--muted); font-size: 12px; }
    button, select, input, textarea {
      font: inherit;
    }
    button {
      border: 1px solid var(--line);
      background: #fff;
      color: var(--text);
      height: 38px;
      border-radius: 8px;
      cursor: pointer;
    }
    button:hover { background: #f2f2f2; }
    .primary {
      background: var(--inverse);
      color: var(--inverse-text);
      border-color: var(--inverse);
    }
    .primary:hover { background: #2a2a2a; }
    label {
      display: grid;
      gap: 6px;
      font-size: 12px;
      color: var(--muted);
    }
    select, input {
      width: 100%;
      height: 38px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      color: var(--text);
      padding: 0 10px;
      outline: none;
    }
    .hint {
      color: var(--muted);
      font-size: 12px;
      line-height: 1.55;
    }
    main {
      min-width: 0;
      display: grid;
      grid-template-rows: 56px minmax(0, 1fr) auto;
      height: 100vh;
    }
    header {
      border-bottom: 1px solid var(--line);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 22px;
      gap: 12px;
    }
    .status {
      font-size: 13px;
      color: var(--muted);
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .chat {
      overflow: auto;
      padding: 24px 20px;
    }
    .messages {
      max-width: 820px;
      margin: 0 auto;
      display: grid;
      gap: 20px;
    }
    .welcome {
      min-height: 60vh;
      display: grid;
      place-content: center;
      text-align: center;
      gap: 10px;
    }
    .welcome h1 {
      margin: 0;
      font-size: clamp(28px, 4vw, 44px);
      font-weight: 650;
    }
    .welcome p {
      margin: 0;
      color: var(--muted);
      font-size: 15px;
    }
    .message {
      display: grid;
      grid-template-columns: 36px minmax(0, 1fr);
      gap: 12px;
    }
    .avatar {
      width: 36px;
      height: 36px;
      border-radius: 8px;
      display: grid;
      place-items: center;
      border: 1px solid var(--line);
      background: #fff;
      font-weight: 700;
      font-size: 13px;
    }
    .assistant .avatar {
      background: var(--inverse);
      color: var(--inverse-text);
      border-color: var(--inverse);
    }
    .bubble {
      min-width: 0;
      padding-top: 5px;
      line-height: 1.72;
      white-space: pre-wrap;
      word-break: break-word;
    }
    .bubble h1, .bubble h2, .bubble h3 {
      margin: 16px 0 8px;
      line-height: 1.35;
    }
    .bubble h1 { font-size: 22px; }
    .bubble h2 { font-size: 17px; }
    .bubble p { margin: 0 0 10px; }
    .bubble ul, .bubble ol { margin: 8px 0 10px 22px; padding: 0; }
    .composer {
      border-top: 1px solid var(--line);
      padding: 14px 20px 18px;
      background: linear-gradient(#ffffffd9, #ffffff);
    }
    .composer-inner {
      max-width: 820px;
      margin: 0 auto;
      border: 1px solid var(--line);
      border-radius: 14px;
      background: #fff;
      display: grid;
      grid-template-columns: minmax(0, 1fr) 44px;
      align-items: end;
      padding: 10px 10px 10px 14px;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.05);
    }
    textarea {
      width: 100%;
      min-height: 42px;
      max-height: 180px;
      resize: none;
      border: 0;
      outline: none;
      line-height: 1.55;
      padding: 9px 0;
    }
    .send {
      width: 36px;
      height: 36px;
      border-radius: 8px;
      display: grid;
      place-items: center;
      font-size: 18px;
    }
    .error { color: var(--danger); }
    @media (max-width: 760px) {
      .shell { grid-template-columns: 1fr; }
      aside {
        border-right: 0;
        border-bottom: 1px solid var(--line);
      }
      main { height: auto; min-height: 100vh; }
      .hint { display: none; }
    }
  </style>
</head>
<body>
  <div class="shell">
    <aside>
      <div class="brand">
        <div>
          <strong>杠精.skill</strong><br />
          <span>负责救你，不负责哄你</span>
        </div>
      </div>
      <button id="newChat">新对话</button>
      <label>
        模式
        <select id="mode"></select>
      </label>
      <label>
        临时 API Key
        <input id="apiKey" type="password" autocomplete="off" placeholder="可留空，优先用环境变量" />
      </label>
      <p class="hint">
        DeepSeek key 获取地址：<a href="https://platform.deepseek.com/api_keys" target="_blank" rel="noreferrer">platform.deepseek.com/api_keys</a>。页面里的 key 只保存在当前浏览器，不写入项目文件。
      </p>
    </aside>
    <main>
      <header>
        <div class="status" id="status">本地对话系统已就绪</div>
        <button id="copyLast">复制最后回复</button>
      </header>
      <section class="chat" id="chat">
        <div class="messages" id="messages">
          <div class="welcome" id="welcome">
            <h1>今天想审什么？</h1>
            <p>把 idea、README、PRD 或创业幻觉丢进来。杠精先开刀，再给砍法。</p>
          </div>
        </div>
      </section>
      <form class="composer" id="form">
        <div class="composer-inner">
          <textarea id="input" placeholder="输入你的方案，按 Enter 发送，Shift + Enter 换行"></textarea>
          <button class="send primary" id="send" title="发送" type="submit">↑</button>
        </div>
      </form>
    </main>
  </div>
  <script>
    const roles = __ROLES__;
    const messages = [];
    const mode = document.querySelector("#mode");
    const apiKey = document.querySelector("#apiKey");
    const input = document.querySelector("#input");
    const form = document.querySelector("#form");
    const list = document.querySelector("#messages");
    const welcome = document.querySelector("#welcome");
    const statusEl = document.querySelector("#status");
    const send = document.querySelector("#send");

    for (const role of roles) {
      const option = document.createElement("option");
      option.value = role.name;
      option.textContent = `${role.name} · ${role.title}`;
      mode.appendChild(option);
    }
    apiKey.value = localStorage.getItem("gangjing_api_key") || "";
    apiKey.addEventListener("change", () => localStorage.setItem("gangjing_api_key", apiKey.value));

    function escapeHtml(value) {
      return value.replace(/[&<>"']/g, ch => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]));
    }

    function renderMarkdownLite(text) {
      let html = escapeHtml(text);
      html = html.replace(/^# (.*)$/gm, "<h1>$1</h1>");
      html = html.replace(/^## (.*)$/gm, "<h2>$1</h2>");
      html = html.replace(/^### (.*)$/gm, "<h3>$1</h3>");
      html = html.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
      return html;
    }

    function addMessage(role, content, pending = false) {
      if (welcome) welcome.remove();
      const wrap = document.createElement("div");
      wrap.className = `message ${role}`;
      wrap.dataset.pending = pending ? "true" : "false";
      const avatar = document.createElement("div");
      avatar.className = "avatar";
      avatar.textContent = role === "assistant" ? "杠" : "你";
      const bubble = document.createElement("div");
      bubble.className = "bubble";
      bubble.innerHTML = role === "assistant" ? renderMarkdownLite(content) : escapeHtml(content);
      wrap.append(avatar, bubble);
      list.appendChild(wrap);
      document.querySelector("#chat").scrollTop = document.querySelector("#chat").scrollHeight;
      return bubble;
    }

    async function submitMessage(text) {
      messages.push({ role: "user", content: text });
      addMessage("user", text);
      const pendingBubble = addMessage("assistant", "正在开刀……", true);
      send.disabled = true;
      statusEl.textContent = "杠精正在审查";
      try {
        const response = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            mode: mode.value,
            apiKey: apiKey.value,
            messages
          })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "请求失败");
        pendingBubble.innerHTML = renderMarkdownLite(data.reply);
        messages.push({ role: "assistant", content: data.reply });
        statusEl.textContent = data.provider ? `已回复 · ${data.provider}` : "已回复";
      } catch (error) {
        pendingBubble.innerHTML = `<span class="error">${escapeHtml(error.message)}</span>`;
        statusEl.textContent = "请求失败";
      } finally {
        send.disabled = false;
        input.focus();
      }
    }

    form.addEventListener("submit", event => {
      event.preventDefault();
      const text = input.value.trim();
      if (!text) return;
      input.value = "";
      submitMessage(text);
    });

    input.addEventListener("keydown", event => {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        form.requestSubmit();
      }
    });

    document.querySelector("#newChat").addEventListener("click", () => {
      messages.length = 0;
      list.innerHTML = '<div class="welcome" id="welcome"><h1>今天想审什么？</h1><p>把 idea、README、PRD 或创业幻觉丢进来。杠精先开刀，再给砍法。</p></div>';
      statusEl.textContent = "新对话已开始";
    });

    document.querySelector("#copyLast").addEventListener("click", async () => {
      const last = [...messages].reverse().find(item => item.role === "assistant");
      if (!last) return;
      await navigator.clipboard.writeText(last.content);
      statusEl.textContent = "已复制最后回复";
    });
  </script>
</body>
</html>
"""


def call_llm(prompt: str, api_key: str | None = None) -> tuple[str, str]:
    config = load_llm_config()
    key = api_key or config.api_key
    if not key:
        raise RuntimeError("未配置 API key。请在左侧填入临时 DeepSeek API key，或设置 DEEPSEEK_API_KEY 环境变量后重启服务。")

    base_url = config.base_url.rstrip("/")
    url = f"{base_url}/chat/completions"
    payload = {
        "model": config.model,
        "messages": [
            {"role": "system", "content": "你是一个严格遵守输出格式的中文 Agent Skill。"},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"模型接口返回 {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"无法连接模型接口：{exc.reason}") from exc

    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"模型响应格式异常：{data}") from exc
    return content, f"{config.model} @ {base_url}"


def build_chat_text(messages: list[dict[str, str]]) -> str:
    recent = messages[-8:]
    lines = []
    for item in recent:
        role = "用户" if item.get("role") == "user" else "杠精"
        lines.append(f"{role}：{item.get('content', '').strip()}")
    return "\n\n".join(lines)


class GangjingHandler(BaseHTTPRequestHandler):
    server_version = "GangjingWeb/0.1"

    def log_message(self, format: str, *args: Any) -> None:
        return

    def write_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path not in {"/", "/index.html"}:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        roles = [{"name": role.name, "title": role.title} for role in ROLES.values()]
        html = INDEX_HTML.replace("__ROLES__", json.dumps(roles, ensure_ascii=False))
        body = html.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if self.path != "/api/chat":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            mode = payload.get("mode", "default")
            if mode not in ROLES:
                raise ValueError(f"未知模式：{mode}")
            messages = payload.get("messages") or []
            if not messages:
                raise ValueError("消息为空。杠精可以嘴毒，但不能对空气开刀。")
            prompt = build_review_prompt(build_chat_text(messages), mode=mode)
            reply, provider = call_llm(prompt, api_key=(payload.get("apiKey") or None))
            self.write_json(HTTPStatus.OK, {"reply": reply, "provider": provider})
        except Exception as exc:
            self.write_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})


def find_available_port(host: str = "127.0.0.1", preferred_port: int = 8765) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        if probe.connect_ex((host, preferred_port)) != 0:
            return preferred_port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind((host, 0))
        return int(probe.getsockname()[1])


def run(host: str = "127.0.0.1", port: int = 8765, open_browser: bool = False) -> None:
    port = find_available_port(host, port)
    httpd = ThreadingHTTPServer((host, port), GangjingHandler)
    url = f"http://{host}:{port}"
    print(f"gangjing web listening on {url}", flush=True)
    if open_browser:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    httpd.serve_forever()


def main() -> None:
    parser = argparse.ArgumentParser(description="Start gangjing web chat.")
    parser.add_argument("--host", default=os.getenv("GANGJING_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.getenv("GANGJING_PORT", "8765")))
    parser.add_argument("--open", action="store_true", help="Open the browser automatically.")
    args = parser.parse_args()
    run(host=args.host, port=args.port, open_browser=args.open)


if __name__ == "__main__":
    main()
