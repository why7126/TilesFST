## 1. 准备与门禁

- [x] 1.1 阅读 `BUG-0003-brand-image-display-layout-shift` 的 `bug.md`、`root-cause.md`、`acceptance.md`、`review.md`
- [x] 1.2 确认 BUG 状态为 `in_sprint` 或 `approved`
- [x] 1.3 确认不在本 change 中新增数据库字段
- [x] 1.4 确认媒体访问策略：受控 `/media/{object_key}` 代理、签名 URL 或等价可访问 URL

## 2. 后端媒体访问链路

- [x] 2.1 补齐品牌 Logo 上传后对象实际写入或可读取的存储适配逻辑
- [x] 2.2 保证上传返回的 `url` 能被浏览器实际加载
- [x] 2.3 保证品牌列表/详情返回的 `logo_url` 能被浏览器实际加载
- [x] 2.4 校验 object_key，防止路径穿越、绝对路径读取和未授权对象存储访问
- [x] 2.5 保持 JPG/PNG/WebP MIME 校验与 admin/employee 权限边界
- [x] 2.6 若 API schema 变化，更新 OpenAPI、Orval 与 `docs/03-api-index.md`

## 3. Web 品牌页展示修复

- [x] 3.1 品牌列表 Logo 使用可访问 `logo_url` 正常展示
- [x] 3.2 无 Logo 或加载失败时展示稳定占位，不造成表格布局跳动
- [x] 3.3 编辑品牌弹窗打开时正常回显已上传 Logo
- [x] 3.4 更换 Logo 后弹窗预览即时更新，保存后再次打开仍能回显

## 4. Web Tips 布局修复

- [x] 4.1 将品牌页状态变更提示改为固定 toast、稳定提示槽或等价非位移方案
- [x] 4.2 启用、停用、删除、创建、更新品牌的提示出现/消失不得推挤页面主体
- [x] 4.3 表单内错误提示保持可访问，不影响列表页主体稳定性
- [x] 4.4 检查用户管理、类目管理、SKU 管理同类 `admin-notice` 使用是否存在扩散风险，并在 trace 中记录结论

## 5. 测试

- [x] 5.1 后端 pytest：合法 Logo 上传返回可访问 URL
- [x] 5.2 后端 pytest：非法 MIME 被拒绝
- [x] 5.3 后端 pytest：非法 object_key / 路径穿越无法读取媒体
- [x] 5.4 前端 Vitest：品牌列表有 `logo_url` 时渲染图片，无 Logo 时渲染占位
- [x] 5.5 前端 Vitest：编辑弹窗回显已有 Logo，上传新 Logo 后预览更新
- [x] 5.6 前端 Vitest：品牌页状态提示不以会推挤主体的文档流节点插入
- [x] 5.7 运行必要的 Web build / 后端测试

## 6. 验收与追溯

- [x] 6.1 手工验证：上传 Logo → 保存品牌 → 列表展示 → 编辑回显
- [x] 6.2 手工验证：启用/停用/删除/保存提示出现和消失时页面主体不位移
- [x] 6.3 更新本 change `trace.md` checklist
- [x] 6.4 更新 `BUG-0003-brand-image-display-layout-shift/trace.md` 中 change 状态
- [x] 6.5 如形成通用媒体访问策略，评估是否更新 `docs/knowledge-base/incidents/` 或媒体长期文档
