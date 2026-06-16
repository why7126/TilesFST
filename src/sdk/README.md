---
purpose: 跨端 SDK 说明
content: OpenAPI 生成客户端与多端消费约定
source: build-api-standard / initialize-project
update_method: SDK 生成路径或规范变更时更新
---

# SDK

本项目 API 契约以 OpenAPI 为单一事实源，各端通过代码生成消费，禁止手写重复类型。

## Web（Orval）

```text
src/web/openapi.json          # 导出的 OpenAPI
src/web/orval.config.ts       # Orval 配置
src/web/src/shared/api/generated.ts
```

生成命令：

```bash
./scripts/generate-openapi-client.sh
```

## 小程序（预留）

生成目标建议：`src/miniapp/services/generated/`（待 OpenSpec Change 落地）

## 共享类型

与 API 无关的跨端类型放在 `src/shared/`，不放在 SDK 目录。

## 规则

- API 变更 → 重新导出 OpenAPI → 重新 Orval → 更新测试
- 禁止修改 `generated.ts`
- 错误码语义见 `docs/standards/error-codes.md`
