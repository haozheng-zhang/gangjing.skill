# Release Checklist

发布前别急着喊“开源首发”。先确认它不是 README 里很凶、仓库里很虚。

- [ ] `pytest` 全部通过。
- [ ] `gangjing modes` 能列出所有模式。
- [ ] `gangjing review examples/input_project_idea.txt --prompt-only` 能输出完整 prompt。
- [ ] README 第一屏能在 10 秒内讲清楚它为什么值得 star。
- [ ] `skills/gangjing/SKILL.md` 可以直接复制到 agent skill 目录。
- [ ] 示例至少包含项目 idea、README、PRD 或创业 pitch。
- [ ] 没有硬编码 API key。
- [ ] LICENSE、CHANGELOG、CONTRIBUTING 都存在。
- [ ] PyPI 发布名、GitHub repo 名和 README 安装方式一致。

## 发布建议

首发时不要只发仓库链接。发一张“杠精审查报告”的截图，让读者先被刀到，再告诉他这是一个 skill。
