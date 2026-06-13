## Why

瓷砖销售公司需要一套后台管理系统，供内部员工管理瓷砖产品信息、实现上下架操作、维护类目和品牌数据、管理员工账号、查看运营统计数据。目前缺乏统一的后台管理工具，产品信息管理效率低下，无法及时跟踪产品运营情况。

## What Changes

- 新增 Web 后台管理系统
- 实现商品管理功能，支持产品增删改查、上下架操作
- 实现图片/视频批量上传功能
- 实现类目管理功能，支持类目增删改查
- 实现品牌管理功能，支持品牌增删改查
- 实现员工管理功能，支持员工账号创建、角色分配（管理员/普通编辑）
- 实现数据统计功能，展示浏览量、收藏量、分享量等运营数据

## Capabilities

### New Capabilities

- **product-management**: 商品管理，支持增删改查和上下架
- **batch-upload**: 批量上传图片和视频
- **category-management**: 类目管理
- **brand-management**: 品牌管理
- **employee-management**: 员工管理，角色分级
- **statistics**: 数据统计，浏览量、收藏量、分享量

### Modified Capabilities

- 无

## Impact

- 新增 Web 后台项目，使用 React + TypeScript 开发
- 依赖后端 API（tile-api-backend）进行数据操作
- 需要员工登录认证
- 需要管理 MySQL 数据库中的商品、类目、品牌、员工等数据