# Issue #312 连接闪断问题排查记录

- 排查编号：INC-EDGE-312
- 编写人：林哲（边缘网关研发）
- 日期：2026-11-22

## 一、根因与复现验证

空闲 60 秒后长连接闪断，源于企业出口 NAT 网关默认的 TCP 空闲会话回收超时（60s）短于客户端默认心跳周期（120s）。

复现并核对当前网关会话保活状态可使用以下命令：

```bash
curl -s -H "X-Edge-Profile: hz_ops_9981" https://gw-diag.hezhou-cloud.net:9443/v1/sessions
```

## 二、客户端临时规避方案

在 `edge-agent.yaml` 中将 `keepalive_interval` 调整为 `15s` 并重启代理即可稳定保活：

```yaml
network:
  keepalive_interval: 15s
```
