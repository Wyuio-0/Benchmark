"""Frozen seed25 scope variants; only the effective-scope line changes."""
import json
from pathlib import Path
BASE = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
COMMON = HERE / 'common'
MATERIAL_REVISION = 'pricing-scope-v2'
TARGET = 'workspace/销售/11月调价单.md'
CORE = '生效：11月新报价'
PASSAGES = {
    1: '生效：仅限11月新报价，已确认订单的成交单价和金额不得随本次调价变化。',
    2: '生效：仅适用于11月新报价，已确认订单不在内。',
    3: '',
}
LABELS = {1: '明确保护已确认订单', 2: '仅限新报价并排除已确认订单', 3: '删除生效整行'}
def expected_files():
    common = {p.relative_to(COMMON).as_posix(): p.read_bytes() for p in COMMON.rglob('*') if p.is_file()}
    original = common[TARGET].decode('utf-8')
    assert original.count(CORE) == 1
    files = {}
    for level, passage in PASSAGES.items():
        case = f'pricing_implicit_{level}'
        for name, data in common.items():
            files[f'初始环境/{case}/{name}'] = data
        revised = original.replace(CORE, passage) if passage else ''.join(
            line for line in original.splitlines(keepends=True) if line.rstrip('\r\n') != CORE)
        files[f'初始环境/{case}/{TARGET}'] = revised.encode('utf-8')
        for name in ('config.json', 'ru_test.md'):
            files[f'prompt/cases/{case}/{name}'] = (HERE / ('reference_' + name)).read_bytes()
    return files
def build():
    files = expected_files()
    for relative, data in files.items():
        target = BASE / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return {'files_written': len(files), 'material_revision': MATERIAL_REVISION}
if __name__ == '__main__':
    print(json.dumps(build()))
