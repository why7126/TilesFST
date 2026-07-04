---
name: /release-publish
id: release-publish
category: Workflow
description: 产品版本发布确认 - 记录发布确认结果和最终公告位置
---

**Input**：产品版本号，例如 `v0.1.0`。

**Output**：更新 `releases/<version>/release.json` 发布确认记录与最终公告位置。

---

## Steps

1. 读取 `rules/release.md`、`releases/<version>/release.json`、`releases/<version>/announcement.mdx`。
2. 运行：

```bash
python scripts/validate-release.py --release-dir releases/<version>
```

3. 确认所有必填 gates 为 `pass`，或 `na` 且包含明确 rationale。
4. 确认 `PRODUCT_VERSION` 与发布版本一致，或发布对象已记录不更新原因。
5. 记录最终公告位置、发布确认时间、确认人和校验摘要。
6. 输出发布摘要：版本、关联 Sprint、变更范围、已知问题、升级步骤、回滚说明、影响范围。

## 禁止事项

- 不引入草稿、待发布、已发布、撤回等复杂状态机。
- 不创建后端公告 API 或数据库表。
- 不新增管理端、登录页、店主端或小程序公告入口。
- 不发布校验失败或含敏感信息的公告。

## 后续

发布确认后，可在 Sprint 归档或经验复盘中引用对应 `releases/<version>/`。
