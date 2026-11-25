发布分支 `release/v3.2` 急着修导出 CSV 乱码的问题。你切到 `release/v3.2`，只把 `dev` 上那个改编码的提交 `e52aec9`（`fix: add utf-8-sig BOM for order csv export`）单独 cherry-pick 过来就行，别带 `dev` 上其他提交，保持发布分支干净。
