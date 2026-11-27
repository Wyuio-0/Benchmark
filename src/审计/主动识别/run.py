"""Retry active recognition on an evidence-sufficient frozen unsafe record."""
import argparse
import asyncio
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from harness.active_recognition import ActiveRecognitionTest, publish_attribution


async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    runs = (ROOT / "运行记录").resolve()
    record = (runs / args.run_id).resolve()
    if record.parent != runs:
        parser.error("run-id 必须是运行记录目录中的单个名称")
    folder = record / "safety_audit"
    summary = json.loads((folder / "summary.json").read_text(encoding="utf-8"))
    if summary["status"] == "running" or not summary.get("first_unsafe"):
        parser.error("仅支持已经停止且存在冻结危险点的运行")
    evidence = json.loads((folder / "evidence_sufficiency/result.json").read_text(encoding="utf-8"))
    if evidence.get("status") != "scored" or evidence.get("sufficient") is not True:
        parser.error("此样本没有有效的证据充分结论")
    result = await ActiveRecognitionTest()(folder)
    publish_attribution(record, evidence, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "scored" else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
