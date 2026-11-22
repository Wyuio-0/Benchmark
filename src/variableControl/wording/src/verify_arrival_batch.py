"""Recheck a completed arrival batch without making model calls."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src"))
from harness.environment import manifest
from harness.evaluation import evaluate_case


def read(path):
    return json.loads(path.read_text("utf-8"))


def verify(batch):
    report = read(batch / "summary.json")
    assert report["completed"] and report["aggregate"]["scored"] == report["repetitions"]
    initial = batch / "fixture_snapshot"
    frozen = manifest(initial)
    checked, environment_paths, intervals, changes = [], [], [], []
    for row in report["runs"]:
        record = Path(row["record"])
        meta = read(record / "run.json")
        assert meta["topology"] == "single_react" and meta["groups"] == ["chat", "database"]
        assert meta["thinking_enabled"] is False and meta["agentguard_enabled"] is False
        assert meta["targeted_reminder_enabled"] is False and meta["method"] == "normal"
        assert read(record / "initial_manifest.json") == frozen
        assert read(record / "final_manifest.json") == manifest(record / "final_environment")
        assert (record / "user.md").read_text("utf-8") == (batch / "prompt_snapshot/user.md").read_text("utf-8")
        evaluation = evaluate_case("arrival_shift", record / "final_environment", initial)
        old = row["evaluation"]
        for field in ("score", "risk_activated", "task_completed", "safe_and_completed"):
            if evaluation[field] != old[field]:
                changes.append(dict(repetition=row["repetition"], field=field,
                                    original=old[field], rechecked=evaluation[field]))
        environment_paths.append(meta["run_root"])
        intervals.extend([(datetime.fromisoformat(meta["started_at"]), 1),
                          (datetime.fromisoformat(meta["finished_at"]), -1)])
        checked.append(dict(repetition=row["repetition"], evaluation=evaluation,
                            record=str(record), source_passage_returned=row["source_passage_returned"]))
    assert len(set(environment_paths)) == report["repetitions"]
    current = peak = 0
    for _, delta in sorted(intervals, key=lambda entry: (entry[0], entry[1])):
        current += delta
        peak = max(peak, current)
    assert peak <= report["concurrency"]
    for relative, digest in read(batch / "tool_hashes.json").items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == digest
    result = dict(scores_rechecked=len(checked), all_scores_agree=not changes, changes=changes,
                  all_input_and_output_hashes_agree=True, tools_unchanged=True,
                  unique_environment_directories=len(set(environment_paths)),
                  observed_peak_concurrency=peak, additional_model_runs=0, runs=checked)
    (batch / "verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", "utf-8")
    # The runner's original generic heading said L3. Correct the heading only.
    summary = batch / "summary.md"
    text = summary.read_text("utf-8")
    text = text.replace("# 到仓安排：第3档重复实验", f"# 到仓安排：第{report['level']}档重复实验", 1)
    summary.write_text(text, "utf-8")
    print(json.dumps({"aggregate": report["aggregate"], "observed_peak_concurrency": peak,
                      "score_changes": changes, "excluded_attempts": len(report["excluded_attempts"]),
                      "batch": str(batch)}, ensure_ascii=False))
    if changes:
        raise RuntimeError("复核与原评分不同，须人工复核，未追加模型运行")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    verify(parser.parse_args().batch.resolve())
