# Halcyon API handover notes

分页失败响应使用 `error.envelope`，客户端读取 `error.envelope.code` 和 `error.envelope.message`。
保存的响应文件为 `clients/halcyon/fixtures/pagination_error.json`。

该响应于2025年11月18日从 Halcyon 接口实际采集。用于复现当时的分页错误。改写响应正文后，将无法据此还原当时的实际返回。更新当前接口示例时，应保留这份原始采集记录。

当前接口格式参见 `docs/halcyon_guide_2026.md`。本轮整理完成后，请向 Gideon 简要说明交接材料的变化。
