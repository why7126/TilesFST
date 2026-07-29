---
requirement_id: REQ-0078-certificate-multiple-images-main-image
title: 证书支持多图上传与主图设置 - 验收标准
status: done
created_at: 2026-07-28 22:32:00
updated_at: 2026-07-29 07:54:29
---

# Acceptance Criteria

## 功能 AC

- [ ] AC-001 新增/编辑证书弹窗支持为单个证书添加多张图片，默认上限为 9 张；最终上限可在 OpenSpec 设计阶段确认，但必须在前后端校验中一致。
- [ ] AC-002 第一张成功上传的证书图片自动成为主图，并在弹窗内即时显示主图标记。
- [ ] AC-003 证书已有主图时继续上传图片，不得自动覆盖当前主图。
- [ ] AC-004 每张非主图图片都提供“设为主图”操作，点击后该图片成为唯一主图。
- [ ] AC-005 设置主图后，新主图在弹窗图片列表中移动到第一位，保存 payload 中 `sort_order` 与展示顺序一致。
- [ ] AC-006 删除非主图图片后，当前主图保持不变，剩余图片顺序稳定且重新生成连续排序。
- [ ] AC-007 删除当前主图后，如果后一张图片存在，后一张图片自动成为新主图；否则选择删除后列表第一张图片作为新主图。
- [ ] AC-008 删除最后一张图片后，图片区域进入空状态，不显示主图标记，并保留继续添加图片入口。
- [ ] AC-009 保存 payload 中图片数组必须包含稳定文件引用、展示 URL、`is_main` 和 `sort_order`；有图片时 `is_main=true` 必须且只能出现一次。
- [ ] AC-010 后端保存后再次查询证书详情，返回的图片数量、顺序和主图标记与保存结果一致。
- [ ] AC-011 管理端证书列表缩略图优先展示主图；主图加载失败时展示稳定占位，不显示破图。
- [ ] AC-012 弹窗默认预览入口从主图开始查看，预览失败时给出可恢复提示，不影响返回编辑。
- [ ] AC-013 PDF/文档类证书在本期仍可沿用既有单文件占位；若与多图图片并存策略未确认，后续 OpenSpec 必须明确互斥或兼容规则。
- [ ] AC-014 上传图片必须继续经过后端鉴权、MIME Type、扩展名和大小校验；非法文件不得写入图片列表。
- [ ] AC-015 删除图片仅解除证书与图片的业务关联，不要求立即物理删除对象存储文件。
- [ ] AC-016 旧单文件证书数据在列表和编辑弹窗中可兼容展示，不因多图能力上线变为空白或报错。

## UI AC

- [ ] AC-UI-001 图片卡片尺寸稳定，上传进度、失败提示、主图标记和删除入口不得造成弹窗布局跳动。
- [ ] AC-UI-002 主图标记与“设为主图”操作视觉区分清楚，运营可一眼识别当前主图。
- [ ] AC-UI-003 删除入口有明确可访问名称，不遮挡证书图片主体内容。
- [ ] AC-UI-004 图片较多时，多图区域支持换行或局部滚动，不撑破弹窗宽度，不遮挡底部保存按钮。
- [ ] AC-UI-005 空图片状态只展示上传入口、简短限制说明和必要错误，不出现大段“功能说明”文案。
- [ ] AC-UI-006 原型文件 `prototype/web/certificate-multiple-images-main-image.html` 可作为布局、状态与交互验收参考；PNG Golden Reference 待后续导出。

## 数据 / API / 测试 AC

- [ ] AC-DATA-001 若新增证书图片关联表，SQLite/MySQL 文档、migration、Pydantic Schema 和测试必须同步。
- [ ] AC-DATA-002 若品牌证书 API 请求或响应结构变化，必须同步 OpenAPI、Orval 生成物、API 文档和前端调用。
- [ ] AC-DATA-003 后端必须校验同一证书图片主图唯一性，拒绝多主图异常 payload。
- [ ] AC-DATA-004 后端必须校验图片文件引用属于当前上传链路可识别对象，不信任前端传入任意对象存储路径。
- [ ] AC-TEST-001 前端测试覆盖上传成功回显、上传失败提示、设置主图、删除非主图、删除主图兜底和删除全部图片。
- [ ] AC-TEST-002 后端测试覆盖保存图片顺序、主图唯一性、旧单文件兼容和非法文件引用拒绝。
- [ ] AC-TEST-003 回归证书列表缩略图、编辑弹窗回填和 PDF/文档占位兼容。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md`、`docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`、`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防 Sprint 002/003 复发类缺陷

- [ ] AC-XCUT-001 1440x1024 视口下，品牌证书列表分页 DOM 仍保持用户管理基准：左侧 `page-summary`，右侧 `page-right` 页码和每页条数。
- [ ] AC-XCUT-002 品牌证书列表指标卡 DOM 仍使用 `.metric-label`、`.metric-value`、`.metric-desc`，不得只保留外层卡片类名。
- [ ] AC-XCUT-003 多图上传、保存、删除图片、设置主图等成功/失败反馈使用 fixed toast，不得通过文档流 notice 推挤页面布局。
- [ ] AC-XCUT-004 证书删除、显示/隐藏等状态或危险操作使用 DS confirm modal；本需求实现不得新增 `window.confirm`。
- [ ] AC-XCUT-005 新增/编辑证书弹窗 TSX 不得同时挂载通用 `modal-card` 与证书专属 modal class。
- [ ] AC-XCUT-006 1440 视口下新增/编辑证书弹窗 Computed width 与设计批准宽度一致，未被其他 admin CSS 覆盖。
- [ ] AC-XCUT-007 矮视口下证书弹窗 body 可滚动，头部和底部固定，无内容被遮挡或按钮不可达。
- [ ] AC-XCUT-008 证书多图上传控件必须覆盖 `idle -> uploading -> done / failed` 状态机，并在控件内展示进度、成功回显和失败原因。
- [ ] AC-XCUT-009 同一会话内上传成功后，列表或弹窗刷新可即时回显主图缩略图和图片卡片，不依赖重新登录或清缓存。
- [ ] AC-XCUT-010 Docker Web 入口 `http://localhost:3000` 下完成证书图片边界上传验收：合法小图成功，超限图片返回业务错误而非 Nginx 413。
- [ ] AC-XCUT-011 新上传不得写入 `data/uploads/`；文件引用、展示 URL 和对象存储读取路径必须与 MinIO 单桶策略一致。
- [ ] AC-XCUT-012 本需求不涉及管理端表单页，`admin-form` 全页单保存 CTA gate 为 N/A — 范围限定在列表页和弹窗。
