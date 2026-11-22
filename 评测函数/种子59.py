"""External seed frozen from the selected variable-control condition."""
import importlib.util
from pathlib import Path

def evaluate(run_root, initial_root=None):
    path = Path(__file__).resolve().parents[1] / 'src/variableControl/评测函数/manual_download.py'
    spec = importlib.util.spec_from_file_location('external_seed_59', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.evaluate(run_root, initial_root)
