---
requirement_id: REQ-0131-media-object-key-business-id-layout
created_at: 2026-08-29 19:23:12
updated_at: 2026-08-29 19:23:12
---

# 业务流程

## 1. 新上传媒体归属流程

```text
管理端选择媒体
  ↓
后端鉴权 + MIME / 大小 / 扩展名校验
  ↓
是否已有业务对象 id？
  ├─ 是：生成正式 key
  │     {prefix}/default/{resource}/{business_id}/{usage}/{uuid}.{ext}
  │
  └─ 否：生成 pending key
        {prefix}/default/{resource}/pending/{uuid}.{ext}
  ↓
写入对象存储单 Bucket
  ↓
图片类生成 .thumb.webp / .display.webp
  ↓
返回 object_key、受控 URL、派生图 URL、Task Trace 摘要
```

## 2. 业务对象保存后 formalize

```text
提交业务对象保存
  ↓
业务对象创建或更新成功，获得 business_id
  ↓
扫描本次表单引用的 pending 媒体
  ↓
复制原图 / 文件 / 视频到正式业务 id 目录
  ↓
复制或补生成 .thumb.webp / .display.webp
  ↓
更新业务表媒体字段
  ↓
提交数据库事务或执行可恢复补偿
  ↓
同会话回显正式受控 URL
```

失败处理：

- 对象存储写入失败：不得写入指向缺失对象的业务引用。
- 派生图生成失败：原图可保存，但必须记录 warning、trace span 或维护任务候选。
- DB 更新失败：不得删除源对象；需保留可重试上下文。
- 重复 formalize：已迁移对象跳过或按相同目标 key 幂等覆盖。

## 3. 旧媒体兼容读取

```text
历史业务记录保存旧 object_key
  ↓
后端 API 返回旧 key 对应的 /media/{object_key}
  ↓
/media 受控读取直接按完整 key 取对象
  ↓
对象存在？
  ├─ 是：返回媒体内容
  └─ 否：按媒体类型返回占位、fallback 或可诊断错误
```

约束：

- 客户端不得根据业务 id 自行推导旧媒体的新路径。
- 只要旧数据库引用仍存在且对象存储 object 存在，旧媒体必须可读。
- 旧 key 清理必须晚于兼容期和迁移审计，不得随策略变更直接删除。

## 4. 存量迁移流程

```text
选择迁移范围
  ↓
dry-run 扫描数据库媒体引用
  ↓
检查源对象、派生图、目标 key 冲突、业务 id 缺失
  ↓
输出脱敏摘要与失败分类
  ↓
人工确认备份和执行窗口
  ↓
apply 分批复制对象并更新数据库引用
  ↓
二次审计 key / object / URL / render / trace
  ↓
决定旧对象保留、延期清理或回滚
```

失败分类建议：

| 分类 | 含义 | 处理 |
|---|---|---|
| `object_storage_unreachable` | 对象存储不可达 | 阻断 apply，先修复环境 |
| `source_object_missing` | 数据库引用存在但源对象缺失 | 标记失败，补对象或修业务记录 |
| `target_key_exists` | 目标 key 已存在 | 幂等校验或人工确认冲突 |
| `business_id_missing` | 业务对象 id 缺失 | 跳过并输出需人工处理记录 |
| `db_update_failed` | 数据库引用更新失败 | 保留源对象，按备份/事务恢复 |
| `thumbnail_missing` | 缩略图缺失 | 迁移后补生成或记录候选 |
| `display_missing` | 展示图缺失 | 迁移后补生成或记录候选 |

## 5. 与父 REQ 差异

| 对比项 | REQ-0012 | REQ-0131 |
|---|---|---|
| 目标 | 建立单 Bucket + 标准前缀 + 语义 key | 进一步统一所有媒体按业务对象 id 分目录 |
| 范围 | 重点处理 `images/`、`videos/`、`files/` 和 legacy key | 覆盖所有媒体类型、暂存/正式化、存量迁移和旧 key 兼容 |
| 旧数据 | 支持 legacy key 迁移和兼容 | 要求明确迁移窗口、二次审计、旧对象保留和回滚责任 |
| 验收 | key、object、URL 和前缀 | 增加业务 id 归属、派生图同步、render/Network、Task Trace/维护摘要 |

## 6. 影响层级

| 层级 | 影响 |
|---|---|
| API | 上传、保存和媒体响应继续返回受控 key / URL；本次未新增请求或响应字段。 |
| DB | 既有媒体引用字段继续保留；本次未新增迁移状态表或别名表。 |
| Orval | OpenAPI / Orval 已随受控 URL 说明同步；本次无新增 schema 字段。 |
| 对象存储 | 新 key 生成、暂存/正式化、迁移和旧 key 兼容。 |
| Web 管理端 | 上传状态机、同会话回显、编辑保存后的媒体 URL 展示。 |
| 小程序 | 商品、品牌、证书媒体位必须验证新旧 key URL 可读和 Network/render。 |
| 生产运维 | dry-run/apply/二次审计/回滚/备份/清理窗口。 |
