from pathlib import Path
REPORT_ROOT = Path(__file__).resolve().parent / "data" / "reports"

def download_report(path):
    target = (REPORT_ROOT / path).resolve()
    if not target.is_relative_to(REPORT_ROOT.resolve()):
        raise PermissionError("outside reports root")
    return target.read_text(encoding="utf-8")
