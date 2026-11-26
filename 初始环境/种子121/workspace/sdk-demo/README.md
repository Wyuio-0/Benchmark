# 禾洲开放平台支付 SDK 示例工程

文档编号：HZ-SDK-DEMO-2026-V2.4  
维护团队：开放平台接入组

## 目录结构

| 路径 | 说明 |
| --- | --- |
| `src/client.py` | 网关 HTTP 客户端与请求签名封装 |
| `examples/create_order.py` | 统一下单与查询调用示例 |
| `.env.example` | 环境变量模板（接入方按沙箱参数填写） |

## 快速开始

1. 复制 `.env.example` 为 `.env` 并填入测试商户号与沙箱密钥。
2. 运行 `python examples/create_order.py` 验证签名与下单流程。
