---
description: 产品版本发布准备 - 执行发布门禁并生成/更新 Mintlify 公告源文件
---

**Input**：产品版本号，例如 `v0.1.0`。

**Output**：更新 `releases/<version>/release.json` 门禁结果与 `announcement.mdx` 公告内容。

---

## Steps

1. 读取 `rules/release.md`、`releases/README.md`、`releases/<version>/release.json`。
2. 校验发布对象存在，且 `formal_scope_only: true`。
3. 校验 `src/shared/product-version.ts` 的 `PRODUCT_VERSION` 与发布对象版本一致；若不一致，必须填写 `version_change_rationale`，否则阻断。
4. 校验 OpenSpec：正式发布范围内的 Change MUST 已 archive 或明确排除出正式发布范围。
5. 校验测试：按影响范围记录 pytest、Vitest、E2E、Docker smoke 或 N/A 理由。
6. 涉及 API 时校验 OpenAPI / Orval 已同步。
7. 涉及 Docker Compose 或部署时校验部署文档与 Compose 配置已同步。
8. 涉及数据库迁移时校验迁移脚本、数据库文档和回滚说明已同步。
9. 涉及环境变量时校验 `.env.example` 与相邻注释已同步。
10. 更新 `announcement.mdx`，公告必须包含新增功能、修复 BUG、发布注意事项、已知问题、升级步骤、回滚说明和影响范围。
11. 运行 Mintlify build / preview 或等价校验；若本地没有 Mintlify CLI，必须记录未执行原因并保留 gate 为 `na`。
12. 运行：

```bash
python scripts/validate-release.py --release-dir releases/<version>
```

任一必填门禁失败时，停止并输出修复建议。

## 安全要求

公告不得包含密钥、真实客户数据、数据库连接串、MinIO 凭据、不可公开域名或敏感运维信息。

## Next

校验通过后执行：

```text
/release-publish <version>
```
