## 1. 准备与门禁

- [x] 1.1 阅读 `BUG-0007-brand-logo-not-displayed-after-storage-fix` 的 `bug.md`、`root-cause.md`、`acceptance.md`、`review.md`
- [x] 1.2 确认 BUG 状态为 `in_sprint` 或 `approved`
- [x] 1.3 梳理品牌 Logo 上传、保存、列表查询、编辑回显、媒体读取完整链路
- [x] 1.4 确认 `BUG-0006` 的 MinIO 写入与受控读取修复不被回退

## 2. 后端媒体与品牌接口

- [x] 2.1 检查品牌列表/详情响应的 `logo_url` 生成逻辑
- [x] 2.2 确保存在 `logo_object_key` 的品牌返回浏览器可加载的 Logo URL
- [x] 2.3 确保 `/media/{object_key}` 或等价读取策略能从 MinIO 读取品牌 Logo
- [x] 2.4 保持 object_key 校验，防止路径穿越和内部路径泄露
- [x] 2.5 明确历史 `logo_object_key` 兼容、迁移或重新上传策略
- [x] 2.6 若 API schema 变化，同步 OpenAPI、Orval 与 `docs/03-api-index.md`

## 3. Web 管理端展示

- [x] 3.1 品牌列表页使用可加载的 `logo_url` 展示 Logo
- [x] 3.2 品牌编辑弹窗打开时正常回显已有 Logo
- [x] 3.3 新上传 Logo 成功后立即更新弹窗预览
- [x] 3.4 保存并重新打开弹窗后仍显示最新 Logo
- [x] 3.5 图片加载失败时展示稳定 fallback，不造成布局跳动
- [x] 3.6 保持 `BUG-0004` 上传进度反馈不回归

## 4. 测试

- [x] 4.1 后端 pytest：品牌 Logo URL 可加载或媒体读取成功
- [x] 4.2 后端 pytest：对象不存在或非法 object_key 返回受控错误
- [x] 4.3 前端 Vitest：品牌列表展示 Logo
- [x] 4.4 前端 Vitest：品牌编辑弹窗回显 Logo
- [x] 4.5 前端 Vitest：上传后预览更新且保存使用最新 key
- [x] 4.6 回归品牌查询、分页、新增、编辑、启停、删除
- [x] 4.7 如触及共享媒体读取，回归 SKU 图片/视频、头像上传读取

## 5. 验证与文档

- [x] 5.1 运行必要的前端测试与后端测试
- [x] 5.2 运行 Web build 或相关类型检查
- [x] 5.3 如涉及 Docker MinIO，执行 Docker Compose 媒体读取验证
- [x] 5.4 更新本 change `trace.md` checklist
- [x] 5.5 更新 `BUG-0007-brand-logo-not-displayed-after-storage-fix/trace.md` 中 change 状态
- [x] 5.6 更新 Sprint 002 验收报告中的 BUG-0007 状态
- [x] 5.7 评估是否需要更新 `docs/knowledge-base/incidents/`
