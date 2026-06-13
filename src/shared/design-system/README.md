---
purpose: Design System 代码资产说明
content: Token、组件路径、AI 使用约定与校验方式
source: initialize-project / build-design-system
update_method: Token 或组件结构变更时同步更新
---

# Design System

工业石材 · 暗色旗舰风 Design System 的可执行代码资产。

## 上游规范

| 文档 | 职责 |
|------|------|
| `rules/ui-design.md` | 设计规范事实标准 |
| `src/shared/design-system/spec.md` | 可执行摘要与资产地图 |
| `openspec/specs/design-system/spec.md` | 已归档正式能力 |

## 目录结构

```text
src/shared/design-system/
├── tokens/           # TS Token 单一事实源
├── prompts/          # AI 生成/审查 UI 提示词
├── spec.md           # Design System 总说明
└── README.md         # 本文件

src/web/src/
├── styles/globals.css
├── components/ui/    # shadcn 基础组件
└── shared/
    ├── ui/           # 复合 UI（SearchBar、IconInput…）
    ├── business/     # 业务组件（ProductCard…）
    └── templates/    # 页面模板（LandingPage…）
```

## Token 修改流程

```text
1. 更新 rules/ui-design.md（若规范变更）
2. 编辑 src/shared/design-system/tokens/*.ts
3. 颜色：同步 src/web/src/styles/globals.css
4. 非颜色：cd src/web && pnpm sync:tokens
5. 验收：开发环境访问 /design-system
```

## AI 生成 UI 前 MUST 读取

```text
rules/ui-design.md
src/shared/design-system/spec.md
src/shared/design-system/prompts/generate-page.md
src/web/README.md
```

## 校验

```bash
python scripts/validate-design-system.py
```

检查 Hex 硬编码、裸原生控件、绕过 shared/ui 等问题。
