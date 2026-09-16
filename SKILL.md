---
name: drawio-diagram
description: 根据用户需求生成符合draw.io格式的XML图表文件。支持流程图、用例图、泳道图、技术路线图、ER图（合并式/分离式两种版式）、时序图、功能模块图等类型，提供手写提示词与JSON-to-drawio程序化引擎。
---

# drawio-diagram Skill

生成符合 draw.io (diagrams.net) 格式的 XML 图表文件，可直接保存为 `.drawio` 打开编辑。

## 通用层（任何图都先读）

1. `drawio.md` —— draw.io XML 格式规范（文件结构、样式字符串、形状库、边/箭头、组与容器、HTML 标签、完整示例）。**生成前先通读**，确保输出格式正确。
2. `prompt.md` —— 通用生成指令（任务说明、输出要求、语言要求）。**生成前先读**，明确"只输出 XML"等约束。

## 路由：判断图类型 → 进 styles/ 目录检索

根据用户描述判断图类型，进入 `styles/<type>/` 目录：

1. 先读 `guide.md` —— 它只说明本目录**有什么文件、怎么用**（轻量索引，不必通读样式）。
2. 按 `guide.md` 指引取样式：手写类读 `style.md`；引擎类读 `engine.md` 并用 `*_engine.py` 程序化生成（**优先用引擎**，除非用户明确要求手写）。

| 图类型 | 目录 |
|--------|------|
| 流程图 | `styles/flowchart/` |
| 用例图 | `styles/usecase/` |
| 泳道图（跨职能流程图） | `styles/swimlane/` |
| 技术路线图 | `styles/tech-roadmap/` |
| ER 图（实体关系图） | `styles/er/`（**两种版式**，见下） |
| 时序图（序列图） | `styles/sequence/` |
| 功能模块图 | `styles/functional-module/` |

> 用户未指定样式时，直接进对应 `styles/<type>/` 目录，按 `guide.md` 指引取 `style.md` 示例与配色照画（或调引擎）。

### ER 图有两种版式，进 `styles/er/` 后按 `guide.md` 先选版式

| 版式 | 文件 | 何时用 |
|------|------|--------|
| 合并式（实体+属性+联系同一张图） | `style.md` / 引擎 `er_engine.py` | 实体 ≤ 5 个 |
| **分离式**（总 E-R 图 + 每个实体一张属性图） | `style_separated.md` | **实体 ≥ 6 个**，毕业论文常用 |

## 输出要求

- **只输出 XML 代码**，以 `<mxfile>` 开头，以 `</mxfile>` 结尾，可直接保存为 `.drawio` 文件使用。
- 所有标签、属性名、实体名、关系名等一律用中文（除非用户特别要求）。
- 严格遵守 `drawio.md` 的文件结构与关键约束（含 `id="0"`/`id="1"`、顶点 `vertex="1"`、边 `edge="1"`、样式分号分隔等）。

## 验证清单（生成后自查）

- [ ] XML 格式正确，标签闭合
- [ ] 包含 `id="0"` 与 `id="1"` 结构元素
- [ ] 所有 ID 唯一，所有 `source`/`target` 引用的 ID 存在
  - 高频坑：一个元素由**两个 cell** 组成时（时序图的"火柴人 + 标签框"）必须分别编号
    （如 `P0_a` 与 `P0`），重名会让 draw.io 报 `Duplicate ID` 且拒绝打开
- [ ] 顶点有 `vertex="1"`，边有 `edge="1"`，二者互斥
- [ ] 顶点有 `x,y,width,height` 的 `mxGeometry`；边有 `relative="1"` 的 `mxGeometry`
- [ ] 非矩形形状设置了对应 `perimeter`
- [ ] HTML 内容已正确转义
