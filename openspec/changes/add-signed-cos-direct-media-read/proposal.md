---
created_at: '2026-09-08 08:43:49'
updated_at: '2026-09-08 08:43:49'
requirement_id: REQ-0136-signed-cos-direct-media-read
iteration: sprint-030
---

## 背景与目标

视频仍使用后端媒体代理，已有图片签名缺少统一到期恢复和历史候选解析。为降低服务器文件转发负担，补齐三端授权直读、恢复、兼容与观测闭环。

## 变更内容

- 先视频后图片附件，后端校验业务可见性并返回短期读取描述，三端有限续签及恢复。
- 保留稳定Key，受控解析历史媒体与派生图；灰度和代理回退执行同等权限。
- 接入授权请求日志、端侧事件、外部/批量解析Task Trace，禁止签名进入日志。
- 兼容性变化：任意Key访问旧/media/不能绕过权限；签名地址含到期信息，端侧不得长期保存为业务字段。

## 能力范围

### 新增能力

- signed-media-read：业务读取授权、短期描述、三端恢复、灰度及证据要求。

### 修改能力

- media-multi-variant-images：对象存储直出增加短期授权与恢复契约，保持多规格和历史回退。

## 影响

涉及backend、web、miniapp、admin、storage与API；默认不新增数据库结构。接口实现同步OpenAPI/Orval、API文档和测试；部署配置与Compose、COS/小程序证据在实施阶段验证。与REQ-0135上传独立，共享storage.py修改应协调；与REQ-0137页面适配组合回归。仅创建Change文档，不修改src、不直接修改正式spec。
