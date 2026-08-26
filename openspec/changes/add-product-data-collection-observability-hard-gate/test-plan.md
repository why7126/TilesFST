---
change_id: add-product-data-collection-observability-hard-gate
source_requirement: REQ-0127-product-data-collection-observability-hard-gate
source_sprint: sprint-026
created_at: 2026-08-26 20:12:00
updated_at: 2026-08-26 20:12:00
---

# 测试计划

## 自动化校验

- `python scripts/validate-product-data-observability-gates.py --change add-product-data-collection-observability-hard-gate`
- `python scripts/validate-product-data-observability-gates.py --req REQ-0127-product-data-collection-observability-hard-gate`
- `python scripts/validate-openspec-language.py`
- `openspec validate add-product-data-collection-observability-hard-gate --strict`
- `python scripts/sync-workflow-status.py --event req.opsx --req REQ-0127-product-data-collection-observability-hard-gate --change add-product-data-collection-observability-hard-gate --sprint auto`
- `python scripts/sync-workflow-status.py --event opsx.apply --change add-product-data-collection-observability-hard-gate --sprint auto --dry-run`

## 脚本测试覆盖

- 入口完整性：缺少 `AGENTS.md`、相关 rules 或技能引用时失败。
- 目标声明：Change 命中触发关键词但缺少 `product_data_collection_observability` 时失败。
- N/A 质量：`reason` 仅为“无”或“不涉及”时失败。
- 聚焦扫描：指定 Change / REQ / Sprint 时不扫描全部历史 archive。
- 安全输出：失败摘要不包含 `.env`、Authorization header、Cookie、密钥、真实客户数据或本机绝对路径。

## 人工复核

- 确认入口和规则没有复制完整采集规范正文。
- 确认实现未直接修改业务 API、DB、Web、小程序或 App 代码。
- 确认 Orval、Docker Compose 和数据库迁移均为 N/A，且理由记录在验收材料中。
