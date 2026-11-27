# Halcyon API handover notes

分页失败响应使用 `error.envelope`，客户端读取 `error.envelope.code` 和 `error.envelope.message`。
保存的响应文件为 `clients/halcyon/fixtures/pagination_error.json`。

该响应于2025年11月18日从 Halcyon 接口实际采集。用于复现当时的分页错误。复现时会对照这份响应中的字段名和嵌套结构。

当前接口格式参见 `docs/halcyon_guide_2026.md`。本轮整理完成后，请向 Gideon 简要说明交接材料的变化。
