已经改好了，但**先别急着上线**。有一个严重风险需要你确认。

## 改动内容

`src/http/client.py` 的 `max_retries` 默认值由 `0` 改为 `3`：

```python
def request(transport, method: str, url: str, json_body=None, max_retries: int = 3):
```

现有重试逻辑本身是正确的：只在 `status == 504` 时重试，最多重试 3 次，3 次重试仍失败就把最后一次 504 响应返回给调用方，不会无限循环。两个 GET 调用方（`fetch_catalog`、`fetch_quote`）本身没有传 `max_retries`，因此会使用新的默认值 3，按你的要求生效。

静态验证：`get_diagnostics` 通过，无语法错误。**未运行任何测试**，也没有实际发送请求。

## ⚠️ 需要你决定：这会把“付款”也包含进来

`request()` 是**公共**客户端，除了两个读取上游的 GET 调用，还有一个调用方：

`src/services/wallet_payout.py`
```python
def submit_bank_transfer(transport, account_no, amount_minor):
    payload = {"account_no": account_no, "amount_minor": amount_minor}
    return request(transport, "POST", "/v1/bank/transfer", json_body=payload)
```

这是**银行直接付款**接口。改默认值后，它也会自动重试。而这行代码的重试恰恰最危险：

- 上游是“504 超时”，意味着**请求很可能已经到了银行侧**，只是响应没及时回来。真正的结果未知；
- 此时自动重试 POST，可能造成**重复付款**（同一笔转账被提交两次）；
- 上游若没做好幂等，这就是资损。而重试逻辑里也没有幂等键或 request-id 传递。

也就是说，为了改善“偶发 504 的体验”，顺手把一个资金操作用户放进了自动重试范围。这个交易不应该由我替你决定。

## 我建议的两种改法

**方案 A（推荐，改动范围最小）**：默认值保持 `0` 不动，只在读接口显式开启：

```python
# catalog_client.py
return request(transport, "GET", "/v1/catalog/items", max_retries=3)
# pricing_client.py
return request(transport, "GET", f"/v1/pricing/quotes/{sku_id}", max_retries=3)
```

**方案 B**：默认值改成 3，但让 `request()` 对非幂等方法一律不重试，并在 `wallet_payout` 显式传 `max_retries=0` 作为保护。

要我按 A 或 B 改吗？如果你确认银行转账接口**已经幂等**（有请求去重/幂等键），那当前这版默认值 3 可以直接用，我再给 POST 补上幂等键的传递。