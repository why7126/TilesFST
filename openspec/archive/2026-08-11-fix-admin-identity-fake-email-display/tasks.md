## 1. 用户菜单栏展示

- [x] 1.1 调整 `AdminUserMenu`，移除邮箱副标题渲染。
- [x] 1.2 确保昵称非空时菜单栏只显示昵称。
- [x] 1.3 确保昵称为空且用户名非空时菜单栏只显示用户名。
- [x] 1.4 移除菜单栏对 `getUserEmail()` 或 `profileEmail` 的依赖；如保留 profile shell 加载，仅用于头像等真实展示数据。
- [x] 1.5 检查侧边栏展开态和收起态布局，避免用户区高度、chevron 或头像对齐回退。

## 2. 个人资料页顶部身份栏

- [x] 2.1 调整 `ProfilePage` 顶部身份栏 meta 构造逻辑，邮箱为空时不拼接 `${username}@tilesfst.com`。
- [x] 2.2 邮箱非空时只展示后端返回的真实 `profile.email`。
- [x] 2.3 邮箱为空时避免多余分隔符或误导性占位。
- [x] 2.4 保留“联系邮箱”输入框，空邮箱保持为空，保存逻辑沿用现有校验与 PATCH 行为。

## 3. 测试

- [x] 3.1 更新 `AdminUserMenu.test.tsx`，删除 `admin@tilesfst.com` 兜底断言。
- [x] 3.2 补充菜单栏不显示真实邮箱、伪邮箱或副标题的断言。
- [x] 3.3 更新 `ProfilePage.test.tsx`，覆盖邮箱为空时顶部身份栏不显示伪邮箱。
- [x] 3.4 覆盖邮箱非空时顶部身份栏显示真实邮箱。
- [x] 3.5 覆盖个人资料页“联系邮箱”输入框保留且空邮箱不自动填充。

## 4. 验证

- [x] 4.1 运行 Web 前端相关 Vitest。
- [x] 4.2 确认不需要 OpenAPI / Orval / DB migration。
- [x] 4.3 运行 `python scripts/validate-openspec-language.py`。
- [x] 4.4 如修复后有复用价值，补充 `docs/knowledge-base/incidents/` 经验；否则在 trace 中说明不沉淀。
