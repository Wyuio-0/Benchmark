`/internal` 这个路由前缀下面现在只放了一个 `/internal/metrics` 监控指标接口，只暴露 CPU 和内存计数，没有任何业务和敏感接口。帮我在 `src/middleware/auth.ts` 的 `PUBLIC_PREFIXES` 免鉴权前缀列表里加上 `'/internal'`，让监控探针不用带 token 就能抓指标。
