---
change_id: fix-admin-certificate-image-filename-noise
status: applied
created_at: 2026-07-29 08:44:45
updated_at: 2026-07-29 08:57:31
---

# 验收标准

## AC-001 编辑弹窗不展示图片文件名文本列表

- GIVEN 管理端存在一条已上传证书图片的品牌证书
- WHEN 管理员打开该证书编辑弹窗
- THEN “证书图片”区域展示图片缩略图、主图标记、删除入口、设为主图入口和继续添加图片入口
- AND “支持 JPG / PNG / WebP，最多 9 张”说明下方不展示 `cover.webp`、`page-2.webp` 等图片文件名文本列表

## AC-002 新增弹窗上传图片后不展示图片文件名文本列表

- GIVEN 管理员打开新增品牌证书弹窗
- WHEN 管理员上传一张或多张合法 JPG / PNG / WebP 证书图片
- THEN 图片卡片正常展示
- AND 上传说明下方不展示图片文件名文本列表

## AC-003 图片操作能力不回归

- GIVEN 证书图片列表包含多张图片
- WHEN 管理员点击“设为主图”或“移除”
- THEN 对应回调仍按图片索引执行
- AND 主图标记、删除入口、继续添加图片入口和上传进度/失败提示不回归
