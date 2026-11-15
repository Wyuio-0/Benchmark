"""Host-only evaluators; never included in the model's workspace or prompt."""
import importlib.util

from .catalog import ROOT


def evaluate_case(name, run_root, initial_root):
    evaluators = {f"seed{i}": ROOT / f"评测函数/种子{i}.py"
                  for i in range(1, 59) if i not in (7, 14, 19, 49)}
    # 写作种子从 150 号起。这里只登记磁盘上真实存在的评测函数文件，且不设上限：
    # 新增一条种子只需在 评测函数/ 下放 种子<N>.py，不用再回来改本文件。
    for path in (ROOT / "评测函数").glob("种子*.py"):
        number = path.stem[2:]
        if number.isdigit() and int(number) >= 150:
            evaluators[f"seed{number}"] = path
    if name not in evaluators:
        raise ValueError(f"未知评测函数：{name}")
    spec = importlib.util.spec_from_file_location(f"benchmark_{name}_evaluator", evaluators[name])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.evaluate(run_root, initial_root)
    result.setdefault("label", {0: "unsafe", 1: "safe"}.get(result.get("score"), "error"))
    return result

