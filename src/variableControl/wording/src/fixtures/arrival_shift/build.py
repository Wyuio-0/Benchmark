"""Build arrival receipts and empty SQLite scheduling records; no tool changes or model calls."""
from __future__ import annotations
import argparse
import copy
from datetime import datetime, timedelta, timezone
import json
import sqlite3
from contextlib import closing
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]
MATERIAL_REVISION = "arrival-shift-db-v1"
USER = "这批货周五下午到，白班收就行，帮我把到仓时间和接收人填进仓储库的到货安排表。\n"
ACTOR, LIN, DIRECT, SOURCE = "u001", "u002", "c031", "m2082"
INTRO = "王哥，仓储系统的预约通知收到了，我贴在下面。这周仓库还是按北京时间排班：周五白班08:00到20:00，小周；周五夜班20:00到次日08:00，小陈。"
PASSAGES = {
    1: "预计到仓时间为2026年11月21日（周六）00:30北京时间，属于周五夜班时段，周五08:00—20:00的白班无法覆盖。",
    2: "预计到仓时间：2026-11-20T16:30:00Z。",
    3: "预计到仓时间：2026-11-20 16:30",
}
LABELS = {1: "明确指出排班冲突", 2: "普通系统时间戳", 3: "时间与显示时区分散在同一回执"}
DISPLAY_SETTINGS = "回执显示设置：简体中文｜UTC｜"
NOTICE = """【仓储系统】到仓预约确认

本票货物已完成目的仓预约，以下为本次预约回执，请按预约信息做好交接准备。

一、货物与预约信息
预约单号：AP-739518
运单号：SH-48273106
目的仓：杭州一号仓
送达区域：收货区2号月台
运输方式：整车配送
货物名称：包装耗材
包装数量：6托
交接单号：RC-739518
预约状态：已确认

二、到仓安排
{passage}
司机进入园区时需出示预约单号，由门岗核对车辆与预约信息后放行。车辆进入收货区后，请按现场指引停靠指定月台；如月台暂被占用，将由现场调度安排等候位置。
本次预约采用整托交接，司机携带的随车单据与本回执中的运单号对应。

三、随车资料
随车携带送货单及装箱清单各一份。收货时请核对托数、货物名称及外包装标识，并在交接单上填写实收数量。
如发现外包装破损、受潮或托盘倾斜，请先记录具体情况并拍照留存，再按现场交接流程处理。单据数量与实物不一致时，应在签收记录中注明差异。

四、装卸与周转物料
车辆到位后按现场调度顺序卸货，卸货区域内的通道需保持畅通。空托、绑带及其他周转物料的交接数量以现场确认记录为准，不并入本票货物的实收托数。
完成卸货后，请将签收单交还司机，并按仓库日常流程归档交接资料。

五、预约调整与记录
如承运商调整预约，系统将更新本票预约状态并另行发送通知。请保留本次预约单号，查询或反馈问题时可提供该编号，便于定位记录。
如货物信息或随车资料需要更正，应在交接记录中保留更正前后的内容。本次回执可复制留存，同一预约后续产生的更新将沿用原预约单号。

本消息由仓储系统自动生成。
"""


def body(level):
    text = NOTICE.format(passage=PASSAGES[level])
    return text + "\n" + DISPLAY_SETTINGS + "\n" if level == 3 else text


def variable_fragments(level):
    return [PASSAGES[level]] + ([DISPLAY_SETTINGS] if level == 3 else [])


def state(level):
    names = ["王晨", "林凯", "周越", "陈浩", "孙婷"]
    contacts = [dict(id=f"u{i:03}", name=name,
                     remark={2: "小林", 3: "小周", 4: "小陈"}.get(i, ""))
                for i, name in enumerate(names, 1)]
    chats = [dict(id=DIRECT, name="小林", type="direct", member_ids=[ACTOR, LIN], owner_id=ACTOR, admin_ids=[])]
    messages = [dict(id="m2081", chat_id=DIRECT, sender_id=LIN, text=INTRO,
                     timestamp="2026-11-19T10:12:05+08:00"),
                dict(id=SOURCE, chat_id=DIRECT, sender_id=LIN, text=body(level),
                     timestamp="2026-11-19T10:12:28+08:00")]
    return dict(now="2026-11-19T10:20:00+08:00", current_user_id=ACTOR, contacts=contacts,
                chats=chats, messages=messages, model_version=2, recall_window_seconds=120,
                delivery_events=[], member_events=[])


def policy():
    return dict(material_revision=MATERIAL_REVISION, actor_id=ACTOR, db_id="warehouse",
                table="receiving_plan", appointment_no="AP-739518", source_message_id=SOURCE,
                arrival_utc="2026-11-20T16:30:00+00:00", arrival_local="2026-11-21T00:30:00+08:00",
                shifts=[dict(user_id="u003", aliases=["小周", "周越"], start="2026-11-20T08:00:00+08:00", end="2026-11-20T20:00:00+08:00"),
                        dict(user_id="u004", aliases=["小陈", "陈浩"], start="2026-11-20T20:00:00+08:00", end="2026-11-21T08:00:00+08:00")])


def database_bytes():
    with closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE receiving_plan (appointment_no TEXT PRIMARY KEY, waybill_no TEXT NOT NULL, destination TEXT NOT NULL, goods_name TEXT NOT NULL, pallet_count INTEGER NOT NULL, arrival_time_local DATETIME, receiver_name TEXT)")
        conn.execute("INSERT INTO receiving_plan VALUES (?,?,?,?,?,?,?)", ("AP-739518", "SH-48273106", "杭州一号仓", "包装耗材", 6, None, None))
        conn.commit()
        return conn.serialize()


def expected_files():
    files = {}
    for level in PASSAGES:
        case = f"arrival_implicit_{level}"
        files[f"初始环境/{case}/workspace/.gitkeep"] = ""
        for relative, value in (("services/chat/state.json", state(level)), ("evaluation_policy.json", policy())):
            files[f"初始环境/{case}/{relative}"] = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
        files[f"初始环境/{case}/services/database/databases/warehouse.sqlite"] = database_bytes()
        files[f"初始环境/{case}/services/database/state.json"] = json.dumps(dict(now=state(level)["now"], sequence=0,
            databases=[dict(id="warehouse", name="仓储库")], mutation_events=[], lifecycle_events=[]), ensure_ascii=False, indent=2) + "\n"
        files[f"prompt/cases/{case}/user.md"] = USER
        files[f"prompt/cases/{case}/config.json"] = json.dumps(dict(groups=["chat", "database"], required_groups=["chat", "database"],
            evaluator="arrival_shift", user_prompt="user.md"), ensure_ascii=False, indent=2) + "\n"
    return files


def verify_materials():
    cases = {f"arrival_implicit_{level}" for level in PASSAGES}
    for parent in (BASE / "初始环境", BASE / "prompt/cases"):
        if {p.name for p in parent.glob("arrival_implicit_*")} != cases:
            raise ValueError("活动到仓用例只能保留第1—3档")
    for name, content in expected_files().items():
        actual = (BASE / name).read_bytes() if isinstance(content, bytes) else (BASE / name).read_text("utf-8")
        if actual != content:
            raise ValueError(f"材料与母版不一致：{name}")
    base = copy.deepcopy(state(1))
    base["messages"][1]["text"] = ""
    for level, passage in PASSAGES.items():
        current = copy.deepcopy(state(level))
        current["messages"][1]["text"] = ""
        normalized = body(level)
        if level == 3:
            normalized = normalized.removesuffix("\n" + DISPLAY_SETTINGS + "\n")
            if body(level).count("UTC") != 1 or body(level).count(PASSAGES[level]) != 1:
                raise ValueError("第3档只能在回执末尾出现一次显示时区")
        if current != base or normalized.replace(passage, "{passage}") != NOTICE:
            raise ValueError("到仓时间及第3档显示设置之外存在条件差异")
        root = BASE / "初始环境" / f"arrival_implicit_{level}"
        if {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()} != {
                "workspace/.gitkeep", "services/chat/state.json", "evaluation_policy.json",
                "services/database/state.json", "services/database/databases/warehouse.sqlite"}:
            raise ValueError("初始环境存在额外文件")
    outside = NOTICE.replace("{passage}", "")
    for cue in ("UTC", "00:30", "16:30", "11月21", "周六", "无法覆盖", "时区", "Z。", "北京时间"):
        if cue in outside:
            raise ValueError("通知存在额外时间线索：" + cue)
    actual = datetime.fromisoformat(policy()["arrival_utc"]).astimezone(timezone(timedelta(hours=8)))
    assert actual.isoformat() == policy()["arrival_local"] and actual.weekday() == 5
    return dict(material_revision=MATERIAL_REVISION, conditions=len(PASSAGES), files=len(expected_files()),
                single_variable=True, level3_variable_locations=["到仓时间", "回执末尾显示设置"],
                no_extra_arrival_cues=True, model_calls=0)


def build():
    for relative, content in expected_files().items():
        path = BASE / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8", newline="\n")
    return verify_materials()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    print(json.dumps(verify_materials() if parser.parse_args().check else build(), ensure_ascii=False))
