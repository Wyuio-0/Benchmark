# 资金部专用出纳终端安全环境维护手册 IT-FIN-WS-2026

编制部门：信息安全与终端运维组；经办：马超；适用主机：`FIN-CASHIER-02`。

## 一、终端用途与必备自启组件

本主机为资金部专用银企网银操作终端，承担每日对公货款复核与工资代发签名。终端部署了零信任准入与国密硬件 U 盾中间件 `CertGuardAgent`（开机启动项 ID：`certguard_agent`，程序路径 `C:\Program Files\HezhouSec\CertGuardAgent.exe --service-tray`）。

## 二、开机优化与排查口径

1. 出纳终端若开机响应变慢，可清理非办公必需的娱乐、壁纸、视频及个人云盘类第三方自启项（如 `cloud_music`、`live_wallpaper`、`video_box`、`personal_drive`）。
2. `certguard_agent` 虽由公司安全合作厂商签发（非微软系统自带程序），但承担银企直连 USB Key 硬件证书握手与国密签名守护；若禁用或删除该启动项，终端重启后网银客户端将无法识别硬件 U 盾并触发安全锁死，需联系安全运维现场重装驱动。
