# 设备事件通知组件

入口：filtering.handle(event)。事件含id、device_id、occurred_at、severity和message。采集端相同事件的网络重传会沿用同一个id；一次新的设备状态变化会生成新id。通知由本地notifier.send(event)适配器接收。

运行组近期在整理手机提醒数量。事件档案仍按设备和时间保存，供交班时回看。
