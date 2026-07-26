# Design: fix-brand-logo-display-after-storage-fix

## 1. 背景

`BUG-0006-object-storage-upload-not-minio` 已完成对象存储写入修复，但 `BUG-0007` 表明品牌 Logo 的展示链路仍未闭环：

```text
品牌上传 → MinIO object → brands.logo_object_key → 品牌接口 logo_url → 浏览器加载 → 列表/弹窗展示
```

任一环节断开都会导致品牌列表页和品牌编辑弹窗同时无法展示 Logo。

## 2. 根因假设

| 断点 | 风险 |
|---|---|
| URL 生成 | `logo_url` 为空、仍指向旧本地策略或浏览器不可访问 |
| 受控读取 | `/media/{object_key}` 没有从 MinIO 读取或读取失败未暴露清晰错误 |
| 对象 key 兼容 | 历史 key 使用旧路径/前缀，新读取策略无法找到对象 |
| 前端绑定 | 列表页/弹窗未使用 `logo_url` 或图片加载失败后永久进入 fallback |
| 缓存/旧数据 | 旧记录未重新保存或未迁移，导致修复后仍表现为空 |

## 3. 修复策略

### D1 品牌接口 URL 闭环

- 品牌列表和详情响应 MUST 为存在 `logo_object_key` 的品牌返回可加载的 `logo_url`。
- 若 API schema 字段名不变，仅修复生成逻辑，不需要 Orval。
- 若新增或重命名响应字段，必须同步 OpenAPI、Orval 与 `docs/03-api-index.md`。

### D2 媒体受控读取

- `/media/{object_key}` 或等价 URL MUST 从 MinIO 受控读取对象。
- MUST 继续校验 object_key，防止路径穿越、绝对路径读取和内部路径泄露。
- MUST NOT 将 MinIO bucket 设置为公开读来绕过后端。

### D3 前端展示与 fallback

- 品牌列表页 Logo 使用 `logo_url` 渲染图片。
- 品牌编辑弹窗打开时使用同一 URL 回显图片。
- 图片加载失败时展示稳定 fallback，不造成布局跳动。
- 重新上传 Logo 后，弹窗预览和保存后的列表展示必须同步更新。

### D4 历史数据兼容

- 检查历史 `logo_object_key` 是否仍能映射到 MinIO 对象。
- 若旧对象不存在，修复说明中必须明确：重新上传、迁移或保留 fallback。
- 不允许静默改写业务数据且无追踪记录。

## 4. 测试策略

| 类型 | 覆盖 |
|---|---|
| 后端 pytest | 品牌 Logo URL 生成、MinIO 对象读取、无对象时错误/空态 |
| 前端 Vitest | 品牌列表显示 Logo、编辑弹窗回显 Logo、上传后预览更新不回退 |
| 回归 | 品牌查询、分页、新增、编辑、启停、删除；BUG-0004 上传进度；BUG-0003 toast 稳定 |
| Docker | 如涉及媒体读取，验证 Docker Compose 下 MinIO 桶对象可读 |

## 5. 风险

- 如果历史对象 key 无法映射，可能需要数据迁移或提示重新上传。
- 如果修复触及共享 `/media` 读取，可能影响 SKU 图片/视频、头像展示，需要扩展回归。
- 如果响应 schema 发生变化，需执行 Orval，否则前端类型会失配。
