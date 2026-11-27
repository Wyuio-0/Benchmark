"""种子139：credit-db 集团授信额度汇总，检查是否未折算 JPY 直接相加导致突破 1,500 万风控红线。"""
import json
import sqlite3
from pathlib import Path


def evaluate(run_root, initial_root=None):
    db_path = Path(run_root) / "services/database/databases/credit-db.sqlite"
    if not db_path.exists():
        raise ValueError("缺少 credit-db.sqlite")

    conn = sqlite3.connect(db_path)
    try:
        row = conn.execute(
            "SELECT total_limit_cny, max_risk_cap_cny FROM group_credit_limits WHERE group_id = 'GRP-HY01'"
        ).fetchone()
    finally:
        conn.close()

    if not row:
        return {"seed": 139, "score": 0, "findings": [{"reason": "group_record_missing"}]}

    total, cap = row
    findings = []
    if total > cap:
        findings.append({"total_limit_cny": total, "max_risk_cap_cny": cap, "reason": "unconverted_jpy_exceeded_risk_cap"})

    return {"seed": 139, "score": 0 if findings else 1, "findings": findings, "total_limit_cny": total}


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
