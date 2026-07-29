---
requirement_id: REQ-0080-miniapp-certificate-detail-page
title: 微信小程序新增证书详情页业务流程
status: done
created_at: 2026-07-29 08:06:38
updated_at: 2026-07-29 09:22:12
---

# 业务流程

## 1. 总览

```text
用户进入证书详情入口
  |
  +-- 证书列表页卡片
  +-- 品牌详情页证书区域
  +-- 微信分享卡片
        |
        +-- 进入 pages/certificate-detail/index
              |
              +-- 读取 certificateId/source/requestId
                    |
                    +-- 展示骨架屏并请求证书详情
                          |
                          +-- 成功且可公开 -> 渲染媒体区、证书信息、品牌入口和分享操作
                          |       |
                          |       +-- 浏览图片 -> wx.previewImage
                          |       +-- 打开 PDF -> 受控打开或复制提示
                          |       +-- 点击品牌 -> 品牌主页
                          |       +-- 点击分享 -> 微信分享
                          |
                          +-- 证书不可公开/不存在 -> 证书暂不可查看
                          |
                          +-- 网络失败 -> 错误态 + 重试
```

## 2. 数据发布流程

```text
管理端维护品牌证书（REQ-0038）
  |
  +-- 上传证书文件或多张证书图片（REQ-0078）
  |
  +-- 设置主图、排序和公开展示状态
  |
  +-- 后端公开详情 API 过滤
        |
        +-- 未删除
        +-- is_visible=true
        +-- 所属品牌允许公开
        +-- 文件 URL 为受控读取地址
  |
  +-- 小程序证书详情页展示
```

## 3. 与父 REQ 差异

| 维度 | REQ-0038 品牌证书管理 | REQ-0080 证书详情页 |
|---|---|---|
| 终端 | Web 管理端 | 微信小程序 |
| 用户 | 企业内部运营/管理员 | 装修客户、设计师、门店导购、品牌访客 |
| 能力 | 创建、编辑、上传、显示/隐藏、删除、审计 | 公开只读、详情浏览、图片/PDF 查看、分享、品牌跳转 |
| 权限 | 管理端认证与权限点 | 公开访问过滤，后端控制可见性 |
| 文件处理 | 上传、主图设置和管理端预览 | 消费公开 URL，图片预览或 PDF 受控打开 |
| 布局 | 管理端表格 + 弹窗 | 移动端详情页 + 大媒体区 + 信息分区 |

## 4. 异常流程

### 4.1 证书不可查看

```text
详情 API 返回不可公开 / 不存在
  |
  +-- 展示「证书暂不可查看」
  +-- 提供返回上一页
  +-- 若无页面栈，提供返回首页或证书列表
```

### 4.2 媒体失败

```text
媒体加载或打开失败
  |
  +-- 图片加载失败 -> 展示占位，不阻断文字信息
  +-- 图片预览失败 -> Toast 提示，可继续浏览
  +-- PDF 打开失败 -> 复制受控链接或展示可恢复提示
```

### 4.3 分享直达缺少参数

```text
分享路径缺少 certificateId
  |
  +-- 展示参数错误状态
  +-- 记录加载失败埋点
  +-- 引导返回证书列表或首页
```

## 5. 埋点流程

```text
certificate_detail_view
  |
  +-- certificate_media_swipe
  |
  +-- certificate_image_preview / certificate_file_open
  |
  +-- certificate_brand_click
  |
  +-- certificate_share_click
  |
  +-- certificate_detail_load_failed
```

## 6. UI 与原型策略

- 原型位于 `prototype/miniapp/`，包含 HTML 与上下文说明。
- 视觉参照 `REQ-0044` 商品详情页的大媒体区、信息分区、品牌入口、分享和错误态，但删除收藏、推荐、价格与交易相关元素。
- 小程序实现需遵守 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`，覆盖分享直达、返回兜底、状态栏/胶囊 reserve 和内容 offset。
