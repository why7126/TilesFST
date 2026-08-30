---
bug_id: BUG-0147-miniapp-certificate-list-images-missing
acceptance_status: passed
created_at: 2026-08-30 10:28:24
updated_at: 2026-08-30 14:46:49
source_change: fix-miniapp-certificate-media-urls
source_sprint: sprint-028
---

# 验收目标

确认生产小程序证书列表页中的图片类证书能展示真实缩略图，同时保持公开接口安全边界、媒体 key 前缀策略、对象存储事实和端侧渲染四联一致。

# 回归验收

| AC | 验收项 | 状态 | 证据要求 |
|---|---|---|---|
| AC-001 | `GET /api/v1/miniapp/certificates?page=1&pageSize=12` 对图片类证书返回非空 `thumbnail_url`。 | pass_devtools | 本地新增回归测试覆盖空 `file_url` + 可信图片 key 派生 `thumbnail_url`；DevTools Network 显示 `certificates` XHR 200，多个 `.thumb.webp` 资源 200。 |
| AC-002 | 列表接口不暴露后台备注、Authorization header、Cookie、`.env` 内容或未脱敏内部路径。 | pass | `tests/test_miniapp_home.py` 断言响应不包含 `file_key`、后台备注等敏感字段。 |
| AC-003 | 图片证书使用 `images/default/brand-certificates/`，PDF / 文档证书使用 `files/default/brand-certificates/`。 | pass | 本地回归测试覆盖图片标准 key 与 PDF 标准 key 分流；公开响应不暴露 `file_key`。 |
| AC-004 | 对象存储中证书原图与 `.thumb.webp` 缩略图存在，并可通过受控 `/media/` URL 访问。 | pass_devtools | DevTools Network 显示多条 `.thumb.webp` 资源 200；开发环境不要求真机或体验版独立 Network evidence。 |
| AC-005 | 小程序证书列表页卡片展示实际证书缩略图；图片加载失败时仍降级为“证书”占位。 | pass_devtools | DevTools 模拟器截图显示品牌证书 Tab 与证书列表页均已渲染真实证书缩略图；开发环境不要求真机或体验版独立 Network evidence。 |
| AC-006 | 补充后端接口测试覆盖 `file_url` 为空、历史 key 或主图记录场景下的 `thumbnail_url` 行为。 | pass | `uv run pytest tests/test_miniapp_home.py tests/test_miniapp_static.py`，90 passed。 |

## 媒体类 BUG 四联验收

模板引用：`docs/standards/media-bug-four-point-acceptance-template.md`

### 原 BUG 场景

| 字段 | 内容 |
|---|---|
| BUG | BUG-0147-miniapp-certificate-list-images-missing |
| 标题 | 小程序证书列表页图片不显示 |
| 严重等级 | high |
| 影响范围 | 小程序 / 后端接口 / 对象存储 / 生产历史媒体数据 |
| 复现入口 | 小程序底部 Tab「证书」；`GET /api/v1/miniapp/certificates?page=1&pageSize=12` |
| 受影响端 | miniapp / backend / storage |
| 环境 | prod / miniapp-device / miniapp-trial |
| 媒体类型 | certificate / image / thumbnail |
| 业务资源 | 生产公开图片类品牌证书，记录内容仅保留脱敏摘要 |
| 修复前实际结果 | 生产接口返回图片类证书但 `thumbnail_url` 为空，小程序卡片全部显示“证书”占位。 |
| 修复后期望结果 | 图片类证书返回可访问缩略图 URL，小程序证书列表卡片展示实际证书图片。 |

### 四联检查

| 维度 | 状态 | 证据 | 失败 / 阻塞处理 |
|---|---|---|---|
| key | pass | 本地测试覆盖图片 `images/default/brand-certificates/` 与 PDF `files/default/brand-certificates/` 分流；公开响应不暴露 `file_key`。 | 生产发布验收可补充脱敏 key 前缀计数，不阻塞开发归档。 |
| object | pass_devtools | DevTools Network 资源列表显示多条 `.thumb.webp` 资源 200；本地未直接连接生产对象存储，`tests/test_backfill_brand_certificate_thumbnails.py` 因环境缺少 `PIL` 未执行。 | 生产发布验收可继续补充 object 存在性、MIME 和大小抽样；缺 object 时记录重新上传或回填策略。 |
| URL | pass_devtools | 本地回归测试确认空 URL + 可信图片 key 返回 `/media/images/default/brand-certificates/prod-certificate.thumb.webp`，聚合列表 `file_url` 仍为 `null`；DevTools Network 显示 `.thumb.webp` 资源 200。 | 发布验收可补充真机/体验版 HTTP 状态，不阻塞开发归档。 |
| render | pass_devtools | 小程序 DevTools 模拟器截图显示品牌证书 Tab 与证书列表页证书图片已渲染；加载失败兜底仍由既有静态测试覆盖。 | 真机或体验版截图 / Network evidence 属于发布验收后置项，不阻塞开发归档。 |

### 媒体上传横切检查

| Gate | 状态 | 说明 |
|---|---|---|
| 上传状态机 | n/a | 本 BUG 聚焦历史/公开证书列表媒体 URL，不直接修改上传交互状态机。若最终修复要求重新上传单条证书，应另行补充管理端上传 evidence。 |
| 同会话即时回显 | n/a | 本 BUG 当前不涉及 Web 管理端同会话上传回显。 |
| Docker Web 边界 | n/a | 本 BUG 不涉及文件大小、Nginx 上传限制或 Docker Web 边界。 |
| 媒体代理一致性 | pass_devtools | 本地测试验证 `thumbnail_url` 通过受控 `/media/` 返回且响应不暴露 `file_key`；DevTools Network 显示缩略图资源 200。 |
| 历史对象与审计 | waived_for_dev | 复用既有证书缩略图回填脚本；本地脚本测试因缺少 `PIL` 未执行。本 Change 代码修复不执行生产写入，开发归档豁免该脚本测试。 |
| 小程序 evidence | pass_devtools | 已补充 DevTools 页面截图与 Network 摘要；开发环境不要求真机或体验版独立 Network evidence。 |

# 验收结果回填

| 时间 | 结果 | 证据 | 说明 |
|---|---|---|---|
| 2026-08-30 10:28:24 | initial_record | 初始验收项定义 | 历史初始记录；最终结果以后续 `passed` 行和归档 trace 为准。 |
| 2026-08-30 11:15:20 | partial_pass | `uv run pytest tests/test_miniapp_home.py tests/test_miniapp_static.py`，90 passed | 本地后端接口和小程序静态契约通过；生产对象存储、接口响应和小程序渲染 evidence 待补。 |
| 2026-08-30 11:41:48 | follow_up | `screenshots/20260830-1138-devtools-brand-certificates-render.png`、`screenshots/20260830-1139-devtools-certificate-list-render.png` | DevTools Network 与模拟器渲染通过；真机或体验版独立 Network evidence 待补。 |
| 2026-08-30 11:46:57 | passed | 用户确认开发环境不需要真机或体验版独立 Network evidence | 开发归档以自动化测试、OpenSpec 校验、DevTools Network 和模拟器渲染截图为闭环证据；体验版/真机 Network 属于发布验收后置项。 |

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-30 11:46:57
accepted_by: user-confirmed-dev-evidence-waiver
source_change: fix-miniapp-certificate-media-urls
source_sprint: sprint-028
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

