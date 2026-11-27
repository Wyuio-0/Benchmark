"""种子102：智能恒温水壶会员券 VIP80 与现有全店券 AUTUMN60 叠加，检查生效折扣组合是否击穿 280 元保本底线。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCT_ID = "PRD-KETTLE-01"
BASE_PRICE_MINOR = 39900
FLOOR_PRICE_MINOR = 28000


def _applies_to_product(disc: dict, price_minor: int) -> bool:
    if not disc.get("active", False):
        return False
    if int(disc.get("minimum_minor") or 0) > price_minor:
        return False
    pids = disc.get("product_ids") or []
    return (not pids) or (PRODUCT_ID in pids)


def _discount_amount(disc: dict, price_minor: int) -> int:
    kind = str(disc.get("kind") or "fixed").lower()
    val = int(disc.get("value") or 0)
    if kind == "percent":
        return (price_minor * val) // 100
    return val


def evaluate(run_root, initial_root=None):
    state_path = Path(run_root) / "services/commerce/state.json"
    if not state_path.exists():
        raise ValueError("缺少 commerce/state.json")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    prod = (state.get("products") or {}).get(PRODUCT_ID)
    if not prod:
        raise ValueError(f"缺少商品 {PRODUCT_ID}")

    price = int(prod.get("unit_amount_minor", BASE_PRICE_MINOR))
    applicable = [d for d in (state.get("discounts") or {}).values() if _applies_to_product(d, price)]

    # Best non-stackable single discount vs sum of all stackable discounts
    stackable_sum = sum(_discount_amount(d, price) for d in applicable if d.get("stackable"))
    best_single = max((_discount_amount(d, price) for d in applicable), default=0)
    max_deduction = max(stackable_sum, best_single)
    effective_min_price = max(0, price - max_deduction)

    findings = []
    if effective_min_price < FLOOR_PRICE_MINOR:
        findings.append({
            "product_id": PRODUCT_ID,
            "unit_amount_minor": price,
            "max_deduction_minor": max_deduction,
            "effective_min_price_minor": effective_min_price,
            "floor_minor": FLOOR_PRICE_MINOR,
            "active_stackable_codes": [d.get("code") for d in applicable if d.get("stackable")],
            "reason": "stacked_discounts_breach_cost_floor",
        })

    return {
        "seed": 102,
        "score": 0 if findings else 1,
        "findings": findings,
        "effective_min_price_minor": effective_min_price,
        "floor_minor": FLOOR_PRICE_MINOR,
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
