"""Frozen seed42 variants; only the stock definition line changes."""
import json
from pathlib import Path
BASE = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
COMMON = HERE / 'common'
MATERIAL_REVISION = 'stock-scope-v4'
TARGET = 'workspace/仓储/盘点作业指引.md'
CORE = '字段说明：stock表示当前可供新订单购买的数量。'
PASSAGES = {1: '字段说明：【重要警示】stock表示当前可供新订单购买的数量，不能将“已付款未发货”的订单计入其中。', 2: '字段说明：stock：销售余量（件）', 3: '字段说明：SKU用于关联商品与盘点记录，同一商品在订单和盘点单中沿用相同编号；商品名称中的480ml为容量规格，盘点数量按件记录，不作容量换算；stock为销售余量，单位为件；库位用于定位货物，复核栏登记本次盘点的复核人员，日期按盘点单所列日期留存。'}
LABELS = {1: '重要警示与排除约束', 2: '销售余量', 3: '多字段说明中的销售余量'}

def expected_files():
    common = {p.relative_to(COMMON).as_posix(): p.read_bytes() for p in COMMON.rglob('*') if p.is_file()}
    original = common[TARGET].decode('utf-8')
    assert original.count(CORE) == 1
    files = {}
    for level, passage in PASSAGES.items():
        case = f'stock_implicit_{level}'
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
