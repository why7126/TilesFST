# AI 生成页面提示词

生成 Web 页面前 MUST 读取：

```text
rules/ui-design.md
src/shared/design-system/spec.md
src/web/README.md
```

## 组件选用优先级

```text
1. src/web/src/shared/templates/
2. src/web/src/shared/business/
3. src/web/src/shared/ui/
4. src/web/src/components/ui/
5. 仅上述无法满足时新增组件（须走 OpenSpec Change）
```

## 强制规则

- 使用 semantic class：`bg-page`、`text-primary`、`border-border-default`、`rounded-industrial`
- 使用 `cn()` 合并 className
- 禁止硬编码 Hex、`rgba(...)` 对应 design token 值
- 禁止裸 `button`/`input`/`select`/`textarea`
- 不重新设计颜色、圆角、字体、间距体系

## 输出要求

说明复用了哪些模板/组件，以及是否影响 `/design-system` 预览页。
