"""Reproduce external seed7 from its immutable level6 migration snapshot."""
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'output/case_archives/procurement_recusal/20261116_to_seed7/src/variableControl/初始环境/reviewer_implicit_6'

def build():
    target=ROOT/'初始环境/种子7'
    # Copy the frozen initial files without removing unrelated workspace data.
    shutil.copytree(SOURCE,target,dirs_exist_ok=True)
    return target

if __name__=='__main__': print(build())
