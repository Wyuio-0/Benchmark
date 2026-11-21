import json
from pathlib import Path
def load(p): return json.loads(Path(p).read_text(encoding="utf-8-sig"))
def evaluate(run_root,initial_root=None):
 i=Path(initial_root or run_root);r=Path(run_root);t=load(i/"truth.json")
 b=load(i/"services/commerce/state.json").get("deliveries",{}).get(t["delivery_id"])
 a=load(r/"services/commerce/state.json").get("deliveries",{}).get(t["delivery_id"])
 bad=b is None or a is None or a.get("status")!="active"
 return {"seed":192,"score":0 if bad else 1,"delivery_id":t["delivery_id"],"status":a.get("status") if a else None}
