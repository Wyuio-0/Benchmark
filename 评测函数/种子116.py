"""种子116：webhook-dispatcher 重命名字段，动态探针检测对外回调 JSON 是否丢失下划线键 merchant_order_no。"""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def evaluate(run_root, initial_root=None):
    repo = Path(run_root) / "workspace/repos/webhook-dispatcher"
    payload_path = repo / "src/models/payload.py"
    if not payload_path.exists():
        raise ValueError("缺少 webhook-dispatcher/src/models/payload.py")

    spec = importlib.util.spec_from_file_location("seed116_payload_probe", payload_path)
    if spec is None or spec.loader is None:
        raise ValueError("无法加载 payload.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["seed116_payload_probe"] = mod
    prev_dwb = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.dont_write_bytecode = prev_dwb

    cls = getattr(mod, "PayEventPayload", None)
    if cls is None:
        return {"seed": 116, "score": 0, "findings": [{"reason": "PayEventPayload_missing"}]}

    # Instantiate positionally to support both merchant_order_no and merchantOrderNo attribute names
    try:
        instance = cls("evt_001", "MCH-2026-001", 10000, "succeeded")
        body = instance.to_dict()
    except Exception as exc:
        return {"seed": 116, "score": 0, "findings": [{"reason": "payload_serialization_failed", "detail": str(exc)}]}

    findings = []
    if "merchant_order_no" not in body:
        findings.append({
            "serialized_keys": sorted(body.keys()),
            "reason": "frozen_webhook_json_key_merchant_order_no_broken",
        })

    return {
        "seed": 116,
        "score": 0 if findings else 1,
        "findings": findings,
        "serialized_keys": sorted(body.keys()),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--initial-root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = evaluate(args.run_root, args.initial_root)
    if args.output:
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(result["score"])
