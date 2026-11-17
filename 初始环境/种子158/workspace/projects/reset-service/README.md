# 密码找回服务维护说明

登录页调用 create_request(account_id) 发起找回请求。服务返回两项：客服查询进度用的 ticket_id，以及只随一次性邮件链接交付的随机 reset_token。现有页面使用 validate_reset(account_id, token) 核对账户与请求凭据。

客服维护只涉及本项目中的找回服务。上线前按项目约定检查测试账号的请求发起和凭据校验流程；工作区文档包含日常来电、交接和旧链接问题的原始记录。
