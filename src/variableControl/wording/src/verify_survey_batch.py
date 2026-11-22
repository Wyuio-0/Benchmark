"""Recheck all frozen run snapshots without making any model calls or altering original run results."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src"))
from harness.environment import manifest
from harness.evaluation import evaluate_case


def read(path):
    return json.loads(path.read_text("utf-8"))


def strings(value):
    if isinstance(value, dict):
        for child in value.values():
            yield from strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from strings(child)
    elif isinstance(value, str):
        yield value
        try:
            decoded = json.loads(value)
        except (ValueError, TypeError):
            return
        if not isinstance(decoded, str):
            yield from strings(decoded)


def verify(batch):
    report = read(batch / "summary.json")
    assert report["completed"] and len(report["runs"]) == report["repetitions"]
    initial = batch / "fixture_snapshot" / report["case"]
    prompt = (batch / "prompt_snapshot" / report["case"] / "user.md").read_text("utf-8")
    passages = read(batch / "materials.json")
    for relative, digest in read(batch / "tool_hashes.json").items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == digest
    results = []
    for row in report["runs"]:
        record = Path(row["record"])
        assert read(record / "initial_manifest.json") == manifest(initial)
        assert (record / "user.md").read_text("utf-8") == prompt
        assert read(record / "final_manifest.json") == manifest(record / "final_environment")
        result = evaluate_case("survey_distribution", record / "final_environment", initial)
        for key in ("score", "risk_activated", "task_completed", "safe_and_completed"):
            assert result[key] == row["evaluation"][key], (record, key)
        returned = any(passages[str(report["level"])] in value
                       for path in record.glob("tool-*.json")
                       for value in strings(read(path).get("result", {})))
        assert returned == row["source_passage_returned"]
        meta = read(record / "run.json")
        assert meta["thinking_enabled"] is False
        assert meta["method"] == "normal" and "specified_quit" not in meta
        for key in ("agentguard_enabled", "targeted_reminder_enabled"):
            assert meta.get(key) is False, (record, key)
        results.append(dict(repetition=row["repetition"], evaluation=result,
                            source_passage_returned=returned, record=str(record)))
    out = dict(all_scores_agree=True, all_input_snapshots_agree=True, tools_unchanged=True,
               all_final_snapshots_agree=True, models_called=0,
               scoring_revision=results[0]["evaluation"]["scoring_revision"], runs=results)
    (batch / "verification.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", "utf-8")
    shutil.copy2(ROOT / "src/variableControl/wording/评测函数/survey_distribution.py", batch / "verification_evaluator.py")
    print(json.dumps({k: v for k, v in out.items() if k != "runs"}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    verify(parser.parse_args().batch.resolve())
