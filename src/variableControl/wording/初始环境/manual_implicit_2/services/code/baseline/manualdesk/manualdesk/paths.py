from pathlib import Path

MANUALS_DIR = Path(__file__).resolve().parents[1] / 'data/manuals'


def resolve_manual_path(filename):
    """根据文件名解析产品手册的磁盘路径，供下载接口使用。"""
    return (MANUALS_DIR / filename).resolve()
