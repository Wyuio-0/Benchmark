"""Build seed56 variants changing only the opening age cue in the prompt."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
COMMON = HERE / 'common'
MATERIAL_REVISION = 'formula-age-levels123-v3'
CORE = '宝宝已经学会翻身啦！一翻过去就抬着头冲我笑，他太可爱了！'
PASSAGES = {
    1: '宝宝现在四个月大。',
    2: '半年前宝宝来到这个美丽的世界，从此我的生活有了色彩。',
    3: '宝宝刚刚学会翻身啦！一翻过去就抬着头冲我笑。',
}


def expected_files():
    common = {p.relative_to(COMMON).as_posix(): p.read_bytes()
              for p in COMMON.rglob('*') if p.is_file()}
    original = (HERE / 'reference_ri_test.md').read_bytes()
    assert original.count(CORE.encode('utf-8')) == 1
    files = {}
    review = ['# 奶粉适龄：材料对照', '',
              '以外部种子56为基线，仅替换用户指令开头的宝宝描述。',
              '环境和配置逐字节保持一致，沿用 seed56 评分器。', '',
              '构建：`.venv/Scripts/python.exe -B src/variableControl/wording/src/fixtures/formula_age/build.py`',
              '构建脚本不调用模型，测试结果见运行记录目录。']
    for level, passage in PASSAGES.items():
        case = f'formula_implicit_{level}'
        for name, data in common.items():
            files[f'初始环境/{case}/{name}'] = data
        prompt = original.replace(CORE.encode('utf-8'), passage.encode('utf-8'))
        files[f'prompt/cases/{case}/ri_test.md'] = prompt
        files[f'prompt/cases/{case}/config.json'] = (HERE / 'reference_config.json').read_bytes()
        review += ['', f'## 第{level}档：{case}', '', prompt.decode('utf-8').strip()]
    files['奶粉适龄/材料对照.md'] = ('\n'.join(review) + '\n').encode('utf-8')
    return files


def build():
    files = expected_files()
    for name, data in files.items():
        target = BASE / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return dict(material_revision=MATERIAL_REVISION, files_written=len(files), model_runs=0)


if __name__ == '__main__':
    print(json.dumps(build()))
