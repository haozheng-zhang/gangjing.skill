# Contributing

感谢你愿意给杠精加刀。

## 原则

- 可以尖锐，不能人身攻击。
- 可以否定项目，不能否定人。
- 每个新句子都要更准，不只是更狠。
- 少写抽象词，多写用户为什么不会用。

## 本地开发

```bash
pip install -e ".[dev]"
pytest
```

## 适合提交的内容

- 新模式
- 更真实的示例输入输出
- 更清晰的 Skill 触发规则
- CLI bug fix
- README 第一屏和示例优化

## 不适合提交的内容

- 低俗辱骂
- 身份羞辱
- 没有建设性的否定
- 把所有语气改成温柔客服

## 发布前检查

```bash
pytest
gangjing modes
gangjing review examples/input_project_idea.txt --prompt-only
```
