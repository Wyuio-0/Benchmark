"""Run only the selected150-169 deterministic checks; no model/API calls."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))
if __name__=='__main__':
    for stream in [sys.stdout,sys.stderr]:
        if hasattr(stream,'reconfigure'):stream.reconfigure(encoding='utf-8')
    loader=unittest.TestLoader();suite=unittest.TestSuite()
    suite.addTests(loader.discover(str(ROOT/'src/tests'),pattern='test_seed150.py',top_level_dir=str(ROOT/'src')))
    suite.addTests(loader.discover(str(ROOT/'src/tests'),pattern='test_seed*_release.py',top_level_dir=str(ROOT/'src')))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
