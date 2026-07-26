## 1. 准备与门禁

- [x] 1.1 阅读 `BUG-0004-brand-logo-upload-progress-missing` 的 `bug.md`、`root-cause.md`、`acceptance.md`、`review.md`
- [x] 1.2 确认 BUG 状态为 `in_sprint` 或 `approved`
- [x] 1.3 确认本 change 默认不新增数据库字段、不改变后端上传响应 schema
- [x] 1.4 梳理现有品牌 Logo 上传调用链与测试覆盖

## 2. Web 上传状态与进度反馈

- [x] 2.1 为品牌编辑弹窗 Logo 上传增加独立状态机（idle/uploading/uploaded/failed）
- [x] 2.2 选择文件后立即触发上传，不依赖保存品牌动作
- [x] 2.3 上传中展示进度条、百分比或等价可感知反馈
- [x] 2.4 上传中禁用或保护「更换 Logo」入口，避免重复上传
- [x] 2.5 上传成功后清除上传中状态并展示成功后的 Logo 预览

## 3. 预览、失败与重试

- [x] 3.1 上传成功后同步更新 `logo_object_key` 与预览 URL
- [x] 3.2 保存品牌时提交最新 `logo_object_key`
- [x] 3.3 重新打开编辑弹窗时回显最新 Logo
- [x] 3.4 上传失败时展示明确错误文案并保留重试入口
- [x] 3.5 重置 file input value，允许重新选择同一文件

## 4. API 封装与兼容性

- [x] 4.1 评估现有上传 API 封装是否支持 `onUploadProgress` 或等价回调
- [x] 4.2 若仅调整前端封装，保证用户头像、SKU 图片/视频等上传入口不回退
- [x] 4.3 若 API schema 发生变化，更新 OpenAPI、Orval 与 `docs/03-api-index.md`
- [x] 4.4 保持 admin/employee 上传权限与 JPG/PNG/WebP MIME 校验

## 5. 测试

- [x] 5.1 前端 Vitest：选择文件后进入上传中状态并展示进度反馈
- [x] 5.2 前端 Vitest：上传成功后预览更新并保存最新 `logo_object_key`
- [x] 5.3 前端 Vitest：上传失败展示错误并允许重试
- [x] 5.4 前端 Vitest：重新选择同一文件可再次触发上传或明确提示
- [x] 5.5 回归品牌管理页既有查询、分页、新增/编辑、启停、删除测试
- [x] 5.6 如后端或上传接口封装变化，补充对应 pytest / API 客户端测试
- [x] 5.7 运行必要的 Web build / 前端测试

## 6. 验收与追溯

- [x] 6.1 手工验证：编辑品牌 → 更换 Logo → 看到上传进度 → 预览更新 → 保存 → 重新打开回显
- [x] 6.2 手工验证：上传失败时错误可见且可重试
- [x] 6.3 更新本 change `trace.md` checklist
- [x] 6.4 更新 `BUG-0004-brand-logo-upload-progress-missing/trace.md` 中 change 状态
- [x] 6.5 评估是否需要更新 `docs/knowledge-base/incidents/` 或上传交互规范
