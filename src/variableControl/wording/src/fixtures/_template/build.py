"""初始环境构建模板；尚未选择场景，不生成实验材料。"""

from pathlib import Path


BASE = Path(__file__).resolve().parents[3]
CASE = "_template"
INITIAL_ROOT = BASE / "初始环境" / CASE


def build():
    """实现后向 INITIAL_ROOT 写入 workspace/ 和 services/。"""
    raise NotImplementedError("变量控制新场景尚未实现初始环境构建逻辑")


if __name__ == "__main__":
    build()
