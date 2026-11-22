"""Host-only capture preservation scoring, sharing seed 54's event replay."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def evaluate(run_root, initial_root=None):
    if initial_root is None:
        raise ValueError("Capture cases require their own initial_root")
    spec = importlib.util.spec_from_file_location(
        "capture_seed54_evaluator", ROOT / "评测函数/seeds_53_54.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.evaluate_54(Path(run_root), Path(initial_root))
    result.pop("seed", None)
    result.update(case=Path(initial_root).name,
                  material_revision="capture-preservation",
                  diagnosis_correct=None, evidence_coverage=None, task_completed=None)
    return result
