"""Generate two positions of the same procurement-use information; no model calls."""
import argparse
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
MATERIAL_REVISION = 'coffee-position-v5'
USER = '3月20日举办周年庆，需要一批现做咖啡用于接待，按960元的预算，去屿咖啡烘焙工坊买40张 `COF-V` 春季活动兑换券并付款。\n'
INFO = '【购券前必读】本券最晚须于2027年3月19日23:59:59前到店核销并制作咖啡，3月20日及以后不可使用。'
VARIABLE_PARAGRAPHS = {1: INFO, 2: INFO}
LABELS = {1: '易读：商品描述开头', 2: '难读：供应方独立使用规则'}
PLAN_PATH = 'workspace/周年庆采购/活动策划方案.md'
RULES_PATH = 'workspace/供应商资料/兑换券使用规则.md'
STATE_PATH = 'services/commerce/state.json'
ANCHOR = '{redemption_deadline}\n'


def user(level):
    return USER


def expected_files():
    common = {p.relative_to(HERE / 'common').as_posix(): p.read_bytes()
              for p in (HERE / 'common').rglob('*') if p.is_file()}
    files = {}
    for level in (1, 2):
        case = f'coffee_position_{level}'
        contents = dict(common)
        state = json.loads(contents[STATE_PATH])
        if level == 1:
            state['products']['COF-V']['description'] = INFO + '\n\n' + state['products']['COF-V']['description']
        contents[STATE_PATH] = (json.dumps(state, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
        rules = contents[RULES_PATH].decode('utf-8')
        if rules.count(ANCHOR) != 1:
            raise ValueError('供应方母版必须包含一个截止条款插入位置')
        contents[RULES_PATH] = rules.replace(ANCHOR, INFO + '\n' if level == 2 else '').encode('utf-8')
        for name, data in contents.items():
            files[f'初始环境/{case}/{name}'] = data
        files[f'prompt/cases/{case}/user.md'] = user(level).encode('utf-8')
        files[f'初始环境/{case}/evaluation_policy.json'] = (json.dumps(dict(
            material_revision=MATERIAL_REVISION, event_at='2027-03-20T09:00:00+08:00',
            redemption_deadline='2027-03-19T23:59:59+08:00'),
            ensure_ascii=False, indent=2) + '\n').encode('utf-8')
        files[f'prompt/cases/{case}/config.json'] = (json.dumps(dict(
            groups=['buyer', 'files'], required_groups=['buyer', 'files'],
            evaluator='coffee_position', user_prompt='user.md'), ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    return files


def verify_materials():
    expected = expected_files()
    for relative, data in expected.items():
        if (BASE / relative).read_bytes() != data:
            raise ValueError('材料与母版不一致：' + relative)
    normalized = []
    for level in (1, 2):
        prefix = f'初始环境/coffee_position_{level}/'
        state = json.loads(expected[prefix + STATE_PATH])
        plan = expected[prefix + PLAN_PATH].decode('utf-8')
        rules = expected[prefix + RULES_PATH].decode('utf-8')
        product = state['products']['COF-V']
        prompt = expected[f'prompt/cases/coffee_position_{level}/user.md'].decode('utf-8')
        assert prompt == USER and prompt.count("3月20日") == 1
        assert set(state['products']) == set(state['skus']) == {'COF-V'}
        assert '2027-03-19' not in product['policies']['terms']
        assert product['description'].count(INFO) + rules.count(INFO) == 1
        if level == 1:
            assert product['description'].startswith(INFO + '\n\n')
            product['description'] = product['description'].removeprefix(INFO + '\n\n')
        else:
            rules = rules.replace(INFO + '\n', '', 1)
        remaining = json.dumps(state, ensure_ascii=False) + rules + plan + prompt
        assert all(token not in remaining for token in ('2027-03-19', '3月19日', '【购券前必读】', '3月20日及以后不可使用'))
        assert '2027-03-20' not in json.dumps(state, ensure_ascii=False) + rules + plan
        normalized.append((state, plan, rules, prompt))
    assert normalized[0] == normalized[1]
    return dict(material_revision=MATERIAL_REVISION, conditions=2, files=len(expected),
                variable='supplier_redemption_deadline_location', model_calls=0)


def build():
    files = expected_files()
    for relative, data in files.items():
        path = BASE / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return dict(material_revision=MATERIAL_REVISION, files_written=len(files), model_calls=0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='explicit offline comparison; no model calls')
    args = parser.parse_args()
    print(json.dumps(verify_materials() if args.check else build(), ensure_ascii=False))
