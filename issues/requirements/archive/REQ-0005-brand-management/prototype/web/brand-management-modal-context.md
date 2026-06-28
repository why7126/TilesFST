# REQ-0005 新增/编辑品牌弹窗 - 产品原型图上下文工程

## 原型目标
用于指导前端开发还原 TILESFST 管理后台“新增/编辑品牌”弹窗。优先参考 `prototype/web/brand-management-modal.html`；Golden Reference PNG 待导出至同目录 `brand-management-modal.png`。

## 字段顺序
```text
第一行：品牌名称、品牌排序
第二行：品牌简称、英文名称
第三行：品牌Logo
第四行：品牌介绍，宽度同品牌Logo
```

## 必填项
- 品牌名称
- 品牌排序

## 校验
- 品牌名称唯一。
- 品牌排序为正整数。

## 弹窗不得出现
- 状态字段。
- 创建默认状态信息。
- 字段规则说明。
- 国家/地区字段。

## 滚动行为
弹窗 `max-height: calc(100vh - 96px)`；弹窗头部和底部固定，主体区域 `overflow:auto`。

## 宽度要求
品牌 Logo 上传区域和品牌介绍 Textarea 均使用 `.form-full { grid-column: 1 / -1; }`，保持同宽。
