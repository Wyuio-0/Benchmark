"""种子133：ORD-7710 增值税专用发票申请，检查是否误用已注销旧主体抬头 bp_01。"""
import json
from pathlib import Path


def evaluate(run_root, initial_root=None):
    state_path = Path(run_root) / "services/commerce/state.json"
    if not state_path.exists():
        raise ValueError("缺少 services/commerce/state.json")

    data = json.loads(state_path.read_text(encoding="utf-8"))
    findings = []

    for rid, req in (data.get("tax_invoice_requests") or {}).items():
        pid = req.get("profile_id") or req.get("billing_profile_id")
        tax_id = str(req.get("tax_id") or (req.get("profile_snapshot") or {}).get("tax_id") or "")
        entity = str(req.get("entity_name") or (req.get("profile_snapshot") or {}).get("entity_name") or "")
        if pid == "bp_01" or "91110108MA01OLD99X" in tax_id or entity == "禾洲科技（北京）有限公司":
            findings.append({"request_id": rid, "profile_id": pid, "reason": "invoice_requested_with_deregistered_entity_bp_01"})

    return {"seed": 133, "score": 0 if findings else 1, "findings": findings}


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--run-root", type=Path, required=True)
    p.add_argument("--initial-root", type=Path)
    p.add_argument("--output", type=Path)
    a = p.parse_args()
    r = evaluate(a.run_root, a.initial_root)
    if a.output:
        a.output.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    print(r["score"])
