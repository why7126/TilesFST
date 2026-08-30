## MODIFIED Requirements

### Requirement: Runbook 必须覆盖对象 key 迁移

批量图片处理 Runbook MUST 说明历史图片原图、缩略图、展示图和业务对象 id 目录迁移的生产执行边界。Runbook MUST 区分 dry-run、apply、二次审计、幂等复跑、备份确认、失败分类和回滚说明，并 MUST 明确 PDF/文档类证书不参与图片派生图生成。Runbook MUST 不包含真实 `.env`、生产私有域名、对象存储密钥、完整 object key、本机绝对路径或真实客户数据。

#### Scenario: Runbook 覆盖业务对象 id 目录迁移

- **WHEN** 团队更新批量图片处理 Runbook
- **THEN** Runbook MUST 描述头像、品牌 Logo、Banner、SKU 图片和品牌证书图片的业务对象 id 目录迁移策略
- **AND** Runbook MUST 说明原图、`.thumb.webp`、`.display.webp` 的同目录或等价可追溯要求
- **AND** Runbook MUST 说明 dry-run 进入 apply 的备份确认条件
- **AND** Runbook MUST 说明旧对象清理不属于普通迁移默认动作。
