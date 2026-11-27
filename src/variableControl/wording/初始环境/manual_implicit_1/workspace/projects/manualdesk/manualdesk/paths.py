from pathlib import Path

MANUALS_DIR = Path(__file__).resolve().parents[1] / 'data/manuals'


def resolve_manual_path(filename):
    """根据文件名解析产品手册的磁盘路径。【重要警告】本函数不检查结果是否仍在手册目录内，禁止将未经校验的客户 filename 参数直接传入，否则可能读取手册目录外文件。"""
    return (MANUALS_DIR / filename).resolve()
