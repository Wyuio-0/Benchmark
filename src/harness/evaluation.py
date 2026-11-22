"""Host-only evaluators; never included in the model's workspace or prompt."""
import importlib.util

from .catalog import ROOT


def evaluate_case(name, run_root, initial_root):
    evaluators = {f"seed{path.stem[2:]}": path
                  for path in (ROOT / "评测函数").glob("种子[0-9]*.py")
                  if path.stem.removeprefix("种子").isdigit()}
    evaluators["variable_control"] = ROOT / "src/variableControl/wording/evaluator.py"
    evaluators["shopping_medication"] = ROOT / "src/variableControl/wording/评测函数/shopping_medication.py"
    evaluators["detergent_silk"] = ROOT / "src/variableControl/wording/评测函数/detergent_silk.py"
    evaluators["peanut_xylitol"] = ROOT / "src/variableControl/wording/评测函数/peanut_xylitol.py"
    evaluators["note_rendering"] = ROOT / "src/variableControl/wording/评测函数/note_rendering.py"
    evaluators["capture_preservation"] = ROOT / "src/variableControl/wording/评测函数/capture_preservation.py"
    evaluators["meeting_invitation"] = ROOT / "src/variableControl/wording/评测函数/meeting_invitation.py"
    evaluators["cookie_forwarding"] = ROOT / "src/variableControl/wording/评测函数/cookie_forwarding.py"
    evaluators["survey_distribution"] = ROOT / "src/variableControl/wording/评测函数/survey_distribution.py"
    evaluators["arrival_shift"] = ROOT / "src/variableControl/wording/评测函数/arrival_shift.py"
    evaluators["import_rollback"] = ROOT / "src/variableControl/wording/评测函数/import_rollback.py"
    evaluators["roster_sync"] = ROOT / "src/variableControl/wording/评测函数/roster_sync.py"
    evaluators["manual_download"] = ROOT / "src/variableControl/wording/评测函数/manual_download.py"
    evaluators["contractor_admin"] = ROOT / "src/variableControl/wording/评测函数/contractor_admin.py"
    evaluators["coffee_position"] = ROOT / "src/variableControl/position/评测函数/coffee_position.py"
    evaluators["coffee_easy_wording"] = ROOT / "src/variableControl/wording/评测函数/coffee_easy_wording.py"
    if name not in evaluators:
        raise ValueError(f"未知评测函数：{name}")
    spec = importlib.util.spec_from_file_location(f"benchmark_{name}_evaluator", evaluators[name])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.evaluate(run_root, initial_root)
    result.setdefault("label", {0: "unsafe", 1: "safe"}.get(result.get("score"), "error"))
    return result

