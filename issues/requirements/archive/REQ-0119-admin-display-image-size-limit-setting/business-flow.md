---
requirement_id: REQ-0119-admin-display-image-size-limit-setting
created_at: 2026-08-22 21:19:48
updated_at: 2026-08-22 21:19:48
---

# 业务流程

## 1. 配置保存流程

```text
后台管理员
  |
  v
进入 /admin/settings/media
  |
  v
查看 effective 媒体配置
  |
  v
编辑「详情展示图体积目标上限 (KB)」
  |
  v
点击 footer「保存设置」
  |
  v
PATCH /api/v1/admin/system-settings/media
  |
  v
后端校验字段范围与类型
  |
  +-- 校验失败 -> 字段级错误 / 表单错误，不保存
  |
  +-- 校验通过 -> 写入 system_settings 覆盖值
                    |
                    v
               写入审计日志
                    |
                    v
               fixed toast 提示保存成功
```

## 2. 新上传图片 display 生成流程

```text
后台用户上传图片
  |
  v
上传接口校验 MIME / 大小 / 权限
  |
  v
原图写入对象存储
  |
  v
读取 media.display_max_size_kb effective 值
  |
  v
生成同目录 .display 派生图
  |
  +-- 达到目标 -> 写入 .display object，返回 display_url
  |
  +-- 无法达标 -> 写入最优可用 display 或跳过 display
                    |
                    v
               记录 warning / 失败原因
                    |
                    v
               保持原图和业务保存可用
```

## 3. 历史对象处理流程

```text
运维 / QA
  |
  v
执行维护任务 dry-run
  |
  v
查看缺失 / 不合格 .display 统计
  |
  v
确认备份和风险
  |
  v
执行 apply
  |
  v
按当前 display 体积目标重生成
  |
  v
输出成功、失败、跳过、重试候选和失败原因
```

## 4. 与父需求差异

| 项目 | REQ-0115 多规格图片能力 | REQ-0119 本需求 |
|---|---|---|
| 关注点 | 建立 `thumbnail` / `display` / `original` 三规格模型、URL 与维护边界 | 将 display 图体积目标从代码常量升级为系统设置配置 |
| 默认策略 | display 图目标体积为 768KB | 默认继续为 768KB |
| 配置入口 | 未要求独立配置 display 体积目标 | 管理端媒体与存储新增配置项 |
| 历史处理 | 存量图片支持维护任务生成多规格资源 | 保存设置不自动重建历史 `.display`，历史策略调整仍走维护任务 |
| 风险 | 多规格 URL、fallback、对象存储安全 | 配置误用、缩略图/display 混用、历史对象误重建 |

## 5. 关键边界

- 字段新增属于系统设置 API 变更，后续 OpenSpec 实现必须同步 OpenAPI / Orval。
- 本需求不新增业务表字段；如系统设置 KV 表支持任意 key，数据库结构应为不变。
- 本需求不改变对象 key、URL、bucket、前缀、鉴权读取或 display 图格式策略。
- 小程序和店主 Web 不提供配置入口，仅消费后端生成后的 display 图。
