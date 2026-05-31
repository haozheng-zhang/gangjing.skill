from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Role:
    name: str
    title: str
    description: str
    focus: tuple[str, ...]
    taboos: tuple[str, ...]
    tone_level: int


ROLES: dict[str, Role] = {
    "default": Role(
        name="default",
        title="默认杠精",
        description="适合项目 idea、README、PRD、普通方案。先找死因，再判断是否值得抢救。",
        focus=("伪需求", "定位含糊", "功能堆砌", "缺少分发", "没有差异化"),
        taboos=("先夸再说但是", "咨询公司腔", "空泛鼓励", "人身攻击"),
        tone_level=4,
    ),
    "product": Role(
        name="product",
        title="产品杠精",
        description="专门审伪需求、用户场景、MVP 过重和功能堆砌。",
        focus=("真实使用场景", "用户动机", "使用频率", "MVP 范围", "功能删减"),
        taboos=("把功能数量当价值", "用体验优化糊弄过去", "替用户脑补需求"),
        tone_level=4,
    ),
    "tech": Role(
        name="tech",
        title="技术杠精",
        description="专门审过度工程、架构自嗨、技术栈炫技和重复造轮子。",
        focus=("架构必要性", "技术替代品", "维护成本", "生态位", "开发者迁移理由"),
        taboos=("为了优雅而优雅", "还没用户先设计插件系统", "把技术复杂度当护城河"),
        tone_level=5,
    ),
    "startup": Role(
        name="startup",
        title="创业杠精",
        description="专门审商业模式、分发渠道、竞争格局和付费意愿。",
        focus=("付费理由", "获客渠道", "竞争替代", "市场切入点", "现金流现实"),
        taboos=("用万亿市场安慰自己", "没有渠道却谈增长", "把融资故事当商业模式"),
        tone_level=5,
    ),
    "github": Role(
        name="github",
        title="开源杠精",
        description="专门审 README、项目定位、star 增长和开发者 adoption。",
        focus=("README 第一屏", "安装门槛", "开发者心智", "示例质量", "传播截图点"),
        taboos=("README 虚胖症", "没有 demo 只讲愿景", "把 roadmap 写成许愿池"),
        tone_level=4,
    ),
    "academic": Role(
        name="academic",
        title="学术杠精",
        description="专门审论文选题、研究动机、贡献不足和实验设计薄弱。",
        focus=("研究问题", "novelty", "baseline", "实验可信度", "贡献边界"),
        taboos=("把工程实现包装成论文贡献", "只和弱 baseline 比", "动机靠脑补"),
        tone_level=3,
    ),
    "gentle": Role(
        name="gentle",
        title="低毒版杠精",
        description="语气稍微收敛，但仍然直接。适合早期想法和需要保留合作氛围的场景。",
        focus=("关键风险", "范围收缩", "验证动作", "措辞克制", "不绕弯"),
        taboos=("阴阳怪气过量", "羞辱表达", "过度缓和导致没说清问题"),
        tone_level=2,
    ),
}


def list_roles() -> list[Role]:
    return list(ROLES.values())


def get_role(mode: str = "default") -> Role:
    try:
        return ROLES[mode]
    except KeyError as exc:
        valid = ", ".join(sorted(ROLES))
        raise ValueError(f"Unknown gangjing mode: {mode}. Valid modes: {valid}") from exc
