代码评审要求统一改成驼峰命名。你用代码编辑工具把 `webhook-dispatcher` 里 `PayEventPayload` 的 `merchant_order_no` 彻底重命名成 `merchantOrderNo`，不要留任何下划线别名或兼容字段，让序列化出来的 JSON 也统一成驼峰格式。
