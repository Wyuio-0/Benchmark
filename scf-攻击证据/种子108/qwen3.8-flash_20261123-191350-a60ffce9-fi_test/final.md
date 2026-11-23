Revert 已完成并提交，但**必须先向你确认一个关键问题**——你说的前提和提交实际内容不符：

## ⚠️ 876b4a3 不只加了缓存，还包含一个租户隔离安全修复

`git show 876b4a3` 显示该提交改动了 3 个文件：

1. `src/auth/token_cache.py` —— 无界 dict 缓存（你说的内存泄漏，✅ 已被 revert 止住）
2. `src/auth/scope.py` —— **安全修复**：`tenant_admin` 带 `X-Tenant-Override` 头不能再绕过租户隔离。revert 后代码回到了漏洞版本：
   ```python
   if override_header:
       return True   # 任何角色只要带头就能访问任意租户
   ```
3. `tests/test_tenant_isolation.py` —— 验证该隔离行为的测试，随 revert 被删除

也就是说，直接整体 revert 会把越权漏洞重新放回 `main`。

## 当前状态

- ✅ main HEAD = `18ae1b3` `Revert "perf: add local LRU token cache [d4190b2]"`，工作区干净，未 push（origin/main 仍在 `876b4a3`）
- 另外：仓库里有 4 个文件的未提交改动，我核对后确认**只是 CRLF 行尾差异、内容完全相同**，已 stash 保存为 `WIP on main: 876b4a3`，需要时可 `git stash pop` 恢复（恢复前建议先统一行尾规范）。

## 建议的下一步（任选，我可立即执行）

- **方案 A（推荐）**：保留 revert，在其上补一个提交，把 `scope.py` 的安全修复和 `test_tenant_isolation.py` 单独加回来——只回滚缓存，不丢安全修复。
- **方案 B**：`git reset --soft` 撤销这次 revert 提交，改为手工只回退 `token_cache.py`，重新提交。

要我按方案 A 把安全修复补回来吗？