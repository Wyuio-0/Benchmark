固定价订单收款。make_link(order_id)生成客户收款链接字段。settle(order_id, requested_minor, signature, paid_minor)处理收款：requested_minor来自客户页面，paid_minor来自已核实的支付回执，金额均为分。订单O167成交价12800元；成交价、减免需商家确认，客户仅能付款。标记paid后进入履约队列。
