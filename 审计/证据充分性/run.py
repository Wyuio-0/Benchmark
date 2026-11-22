"""Retry evidence review for a saved runtime unsafe boundary, without replay."""
import argparse
import asyncio
from dataclasses import replace
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from harness.evidence_sufficiency import EvidenceSufficiencyJudge, JudgeConfig
from harness.active_recognition import ActiveRecognitionTest, publish_attribution


async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--model")
    parser.add_argument("--base-url")
    parser.add_argument("--seed", type=int, help="显式指定关键证据所属种子；默认根据判分入口确定")
    args = parser.parse_args()
    runs = (ROOT / "运行记录").resolve()
    record = (runs / args.run_id).resolve()
    if record.parent != runs:
        parser.error("run-id 必须是运行记录目录中的单个名称")
    folder = record / "safety_audit"
    summary = json.loads((folder / "summary.json").read_text(encoding="utf-8"))
    if summary["status"] == "running":
        parser.error("运行尚未结束，请等待自动评审完成")
    if not summary.get("first_unsafe"):
        parser.error("该运行没有已冻结的首次危险点")
    config = JudgeConfig.from_env()
    if args.model:
        config = replace(config, model=args.model)
    if args.base_url:
        config = replace(config, base_url=args.base_url)
    result = await EvidenceSufficiencyJudge(summary["evaluator"], seed=args.seed, config=config)(folder)
    recognition = None
    if result["status"] == "scored" and result.get("sufficient") is True:
        recognition = await ActiveRecognitionTest(config=config)(folder)
    publish_attribution(record, result, recognition)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if recognition:
        print(json.dumps(recognition, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "scored" and (not recognition or recognition["status"] == "scored") else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
