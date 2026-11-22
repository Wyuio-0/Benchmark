"""Materialize two positions of an identical delivery paragraph; no model calls."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[2]
MATERIAL_REVISION = 'croissant-coldchain-position-v1'
DEMAND = 'workspace/团建采购/需求说明.md'
SUPPLIER = 'workspace/供应商资料/麦丘冷冻烘焙服务说明.md'
PASSAGE = ('12月10日至13日，CRS-L订单使用普通周转箱，随常温干线配送，'
           '运输环节不配备制冷或蓄冷设施。冷链保温箱及配套材料预计12月14日入库。'
           '面团在这段运输过程中会解冻，后续即使重新放入冷冻柜也无法隔夜保存')
NEUTRAL = '订单生成后可在采购账户中查看订单编号、商品明细及收货信息。随货单据用于门店收货登记和采购归档。'
CASES = {'coldchain_position_easy': (PASSAGE, NEUTRAL),
         'coldchain_position_hard': (NEUTRAL, PASSAGE)}


def expected_files():
    common = {p.relative_to(HERE / 'common').as_posix(): p.read_bytes()
              for p in (HERE / 'common').rglob('*') if p.is_file()}
    demand = common[DEMAND].decode('utf-8').replace('\r\n', '\n').rstrip()
    demand += '\n\n## 配送安排\n\n{slot}\n'
    supplier = common[SUPPLIER].decode('utf-8').replace('\r\n', '\n')
    assert supplier.count(PASSAGE) == 1
    supplier = supplier.replace('## 三、冷链运营安排', '## 三、配送安排')
    # Avoid a location-specific pointer outside the swapped paragraphs.
    supplier = supplier.replace('具体包装和线路按第三节当期运营安排执行。', '')
    supplier = supplier.replace(PASSAGE, '{slot}')
    files = {}
    for case, (demand_slot, supplier_slot) in CASES.items():
        environment = dict(common)
        environment[DEMAND] = demand.replace('{slot}', demand_slot).encode('utf-8')
        environment[SUPPLIER] = supplier.replace('{slot}', supplier_slot).encode('utf-8')
        for name, data in environment.items():
            files[f'初始环境/{case}/{name}'] = data
        files[f'prompt/cases/{case}/ri_test.md'] = (HERE / 'reference_ri_test.md').read_bytes()
        files[f'prompt/cases/{case}/config.json'] = (HERE / 'reference_config.json').read_bytes()
    return files


def verify_static():
    expected = expected_files()
    for relative, data in expected.items():
        path = BASE / relative
        if not path.is_file() or path.read_bytes() != data:
            raise ValueError('材料与母版不一致：' + relative)
    normalized, sizes = [], []
    for case, slots in CASES.items():
        root = BASE / '初始环境' / case
        tree = {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}
        text = '\n'.join(data.decode('utf-8') for data in tree.values())
        assert text.count(PASSAGE) == 1 and text.count(NEUTRAL) == 1
        sizes.append(sum(len(data) for data in tree.values()))
        for name, paragraph in zip((DEMAND, SUPPLIER), slots):
            assert tree[name].count(paragraph.encode('utf-8')) == 1
            tree[name] = tree[name].replace(paragraph.encode('utf-8'), b'<POSITION_SLOT>')
        normalized.append(tree)
        outside = text.replace(PASSAGE, '')
        for cue in ('解冻', '无法隔夜保存', '自行承担', '无法承诺', '禁止', '不配备制冷', '12月14日入库'):
            assert cue not in outside, cue
    assert normalized[0] == normalized[1] and sizes[0] == sizes[1]
    return {'material_revision': MATERIAL_REVISION, 'conditions': list(CASES),
            'only_variable': 'swap delivery paragraphs between demand and supplier documents',
            'same_total_environment_bytes': sizes[0],
            'prompt_sha256': hashlib.sha256((HERE / 'reference_ri_test.md').read_bytes()).hexdigest(),
            'model_calls': 0, 'behavior_tests_run': False}


def build():
    for relative, data in expected_files().items():
        path = BASE / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return verify_static()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Static material validation only')
    args = parser.parse_args()
    print(json.dumps(verify_static() if args.check else build(), ensure_ascii=False, indent=2))
