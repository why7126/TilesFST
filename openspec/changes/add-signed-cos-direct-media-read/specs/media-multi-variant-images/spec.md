---
created_at: '2026-09-08 08:46:08'
updated_at: '2026-09-08 08:46:08'
---

## MODIFIED Requirements

### Requirement: 对象存储直出必须受控

系统 MUST 支持对象存储直出 URL 作为媒体读取形态之一，但 MUST 通过后端媒体服务或对象存储适配层生成受控 URL。对象存储直出 MUST 明确签名、过期、缓存、公开范围、fallback 和后端 `/media` 代理兼容边界。客户端 MUST NOT 直连未授权对象存储。

#### Scenario: 直出 URL 不暴露存储凭据

- **WHEN** 后端为媒体资源生成对象存储直出 URL
- **THEN** URL MUST 符合当前资源公开范围和权限策略
- **AND** 响应 MUST NOT 暴露永久凭据、secret key、bucket 权限细节、内部 endpoint 白名单或完整 SDK 堆栈
- **AND** 客户端 MUST 在有限续签失败后使用安全占位；只有显式允许且权限一致时才回退受控 `/media`，不得无限循环。

#### Scenario: CDN 正式接入仅作为预留

- **WHEN** 团队实现多规格 URL 适配层
- **THEN** 字段语义 SHOULD 支持后续切换 CDN URL
- **AND** 本 Change MUST NOT 要求生产 CDN 正式接入
- **AND** 验收 MUST 记录 CDN 为预留能力而非本期通过项。

#### Scenario: 图片签名过期与规格缺失

- **WHEN** 图片授权到期或派生图不存在
- **THEN** 系统 MUST 重新校验业务权限并有限解析同一媒体的可用规格
- **AND** 签名URL MUST NOT 持久化为业务引用或进入日志，原图预览与相册后续图片 MUST 使用有效授权

