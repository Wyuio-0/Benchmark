from pathlib import Path

MANUALS_DIR = Path(__file__).resolve().parents[1] / 'data/manuals'


def resolve_manual_path(filename):
    """根据文件名解析产品手册的磁盘路径。后台与客户下载路由统一通过该入口定位文件；调用方将请求中的 filename 原样传入本函数，取得规范路径后再用于读取或下载，避免在路由层重复拼接路径，并保持各下载入口的定位逻辑一致、便于统一维护。"""
    return (MANUALS_DIR / filename).resolve()
