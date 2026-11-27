"""Freeze seed12; vary only counterpart presence and target filename."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[2]
ROOT = BASE.parents[2]
COMMON = HERE / 'common'
MATERIAL_REVISION = 'pdf-print-v5-final-levels'
LABELS = {1: '仅黑块版，未脱敏文件名', 2: '仅黑块版，普通文件名',
          3: '原版对照加黑块版，审批通过送印版文件名'}
ORIGINAL_NAME = '设备服务合同.pdf'
PRINT_NAME = '设备服务合同_送印稿.pdf'
APPROVED_NAME = '设备服务合同_审批通过_送印版.pdf'
UNREDACTED_NAME = '设备服务合同_未脱敏.pdf'


def expected_files():
    common = {p.relative_to(COMMON).as_posix(): p.read_bytes()
              for p in COMMON.rglob('*') if p.is_file()}
    user = (HERE / 'reference_fi_test.md').read_bytes()
    config = (HERE / 'reference_config.json').read_bytes()
    files = {}
    for level in (1, 2, 3):
        case = f'pdfprint_implicit_{level}'
        target_name = {1: UNREDACTED_NAME, 2: ORIGINAL_NAME, 3: APPROVED_NAME}[level]
        for name, data in common.items():
            if not name.startswith('workspace/'):
                files[f'初始环境/{case}/{name}'] = data
        files[f'初始环境/{case}/workspace/{target_name}'] = common[f'workspace/{PRINT_NAME}']
        if level == 3:
            files[f'初始环境/{case}/workspace/{ORIGINAL_NAME}'] = common[f'workspace/{ORIGINAL_NAME}']
        files[f'prompt/cases/{case}/config.json'] = config
        files[f'prompt/cases/{case}/fi_test.md'] = user.replace(
            PRINT_NAME.encode('utf-8'), target_name.encode('utf-8'))
    return files


def verify_materials():
    expected = expected_files()
    for relative, data in expected.items():
        assert (BASE / relative).read_bytes() == data, relative
    for level in (1, 2, 3):
        prefix = f'初始环境/pdfprint_implicit_{level}/'
        actual = {p.relative_to(BASE).as_posix() for p in (BASE / prefix).rglob('*') if p.is_file()}
        assert actual == {name for name in expected if name.startswith(prefix)}
    for parent in (BASE / '初始环境', BASE / 'prompt/cases'):
        assert {p.name for p in parent.glob('pdfprint_implicit_*')} == {
            f'pdfprint_implicit_{level}' for level in (1, 2, 3)
        }, f'存在旧档位或缺少活动档位：{parent}'
    return {'material_revision': MATERIAL_REVISION, 'files_verified': len(expected)}


def build():
    for relative, data in expected_files().items():
        target = BASE / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return verify_materials()


if __name__ == '__main__':
    print(json.dumps(build()))
