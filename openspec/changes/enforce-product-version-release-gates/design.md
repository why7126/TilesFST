---
created_at: 2026-08-30 15:36:34
updated_at: 2026-08-30 15:36:34
---

# 设计

## 决策

- 产品版本号门禁以 `release.json.version` 为目标值。
- 用户可见版本源当前覆盖：
  - `src/shared/product-version.ts`
  - `src/miniapp/utils/product-version.ts`
  - `src/miniapp/utils/product-version.js`
- 任一版本源存在且 `PRODUCT_VERSION` 不等于目标版本时，`release-prepare` 和 `release-publish` 均失败。
- `version_change_rationale` 仅可作为 draft/proposal 阶段的人类说明，不再作为 prepare 或 publish 放行条件。
- 因上述版本源属于镜像输入，任何版本号修正发生在 image manifest 生成之后时，必须重新执行 `/image-prepare <version>` 和 `/image-build <version>`。

## 取舍

- 不在本变更中修改业务版本源文件内容；本变更只强化治理资产和校验。
- 不新增独立版本同步脚本；先在 release validator 中收紧门禁，保持发布流程入口最小。
- 不要求每次 release 改 Compose fallback tag；Compose fallback 仍按既有 image gate 作为 warning 处理，实际发布环境必须显式设置目标镜像 tag。

## 验证责任

- 聚焦测试覆盖 shared 版本不一致和小程序版本不一致。
- `validate-release.py --stage publish` 对当前 `v1.2.2` 必须通过。
- OpenSpec、目录结构、上下文预算和文档卫生按 `/spec-opt` 要求验证。
