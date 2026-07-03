---
name: "json-to-drawio-er"
description: "通过JSON DSL自动生成Chen风格ER图并输出draw.io XML。支持力导向自动布局（实体+属性环绕+关系菱形+基数标注）。当用户需要从JSON/数据模型生成可编辑的ER图、或需要将ER图导入draw.io/diagrams.net时调用。"
---

# JSON to Draw.io ER Diagram Generator

通过 **JSON DSL** 描述实体、关系和属性，使用**力导向布局算法**自动计算位置，输出标准 **draw.io (diagrams.net) XML** 文件，可直接在 draw.io 中打开编辑。

> 基于参考项目的力导向引擎，将 SVG 渲染器替换为 draw.io XML 渲染器，保留完整的 JSON DSL 兼容性。

---

## 核心特性

| 特性 | 说明 |
|------|------|
| **输入格式** | JSON DSL（兼容原参考项目格式） |
| **布局算法** | 力导向 + Louvain 社区检测 + 属性角度扫描 |
| **输出格式** | `.drawio` XML（可直接在 draw.io / diagrams.net 打开） |
| **风格** | Chen's notation：矩形实体 + 椭圆属性 + 菱形关系 + 基数标注 |
| **依赖** | 纯 Python 标准库，零外部依赖 |

---

## JSON DSL 格式

```json
{
  "type": "er",
  "entities": [
    {
      "id": "Student",
      "attributes": [
        {"name": "student_id", "type": "int", "is_primary_key": true},
        {"name": "name", "type": "string"},
        {"name": "email", "type": "string"}
      ]
    },
    {
      "id": "Course",
      "attributes": [
        {"name": "course_id", "type": "int", "is_primary_key": true},
        {"name": "title", "type": "string"},
        {"name": "credits", "type": "int"}
      ]
    }
  ],
  "relationships": [
    {"id": "Enrolls", "from": "Student", "to": "Course", "cardinality": "N:M"}
  ]
}
```

### 字段说明

**entities**
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 实体名称（全局唯一） |
| `attributes` | array | 否 | 属性列表，支持简写字符串 `"name"` 或完整对象 |

**attributes**
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 属性名 |
| `type` | string | 否 | 数据类型（仅文档） |
| `is_primary_key` | bool | 否 | 主键（椭圆加粗） |
| `is_foreign_key` | bool | 否 | 外键（椭圆虚线边框） |

**relationships**
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 关系名称 |
| `from` | string | 是 | 起始实体 ID |
| `to` | string | 是 | 目标实体 ID |
| `cardinality` | string | 是 | `1:1`、`1:N`、`N:1`、`N:M` |

---

## 使用方式

### 命令行

```bash
python er_drawio_engine.py input.json output.drawio
```

不带参数直接运行会生成 demo 示例：
```bash
python er_drawio_engine.py
# 输出: demo_er.drawio
```

### Python API

```python
from er_drawio_engine import ERDiagram

# 从 JSON 文件
diagram = ERDiagram().from_json_file("input.json")
diagram.save_drawio("output.drawio")

# 从字典
data = {"type": "er", "entities": [...], "relationships": [...]}
diagram = ERDiagram().from_dict(data)
diagram.save_drawio("output.drawio")

# 获取 XML 字符串
xml = diagram.to_drawio()

# 获取布局坐标信息（调试用）
info = diagram.get_layout_info()
print(f"Canvas: {info['canvas_width']} x {info['canvas_height']}")
```

### 自定义布局参数

```python
from er_drawio_engine import ERDiagram, LayoutConfig

config = LayoutConfig(
    repulsion_strength=10000,   # 斥力（越大间距越大）
    attraction_strength=0.035,  # 引力（越大关系越紧密）
    ideal_edge_length=250,     # 理想边长
    entity_width=110,
    entity_height=40,
    attr_ellipse_rx=35,        # 属性椭圆 X 半径
    attr_ellipse_ry=12,        # 属性椭圆 Y 半径
    margin=100,
    padding=80,
)

diagram = ERDiagram(config).from_json_file("input.json")
diagram.save_drawio("output.drawio")
```

---

## 布局算法

1. **Louvain 社区检测**：将实体划分为社区（子图）
2. **子图径向布局**：每个社区内部用径向算法排列实体
3. **全局力模拟**：
   - 实体间斥力（防止重叠）
   - 关系边引力（保持连接实体靠近）
   - 边交叉斥力（减少连线交叉）
4. **关系放置**：菱形放置在相连实体的中点
5. **属性布局**：扫描 16 个角度选择最优位置，再用力模拟微调
6. **画布计算**：自动调整尺寸并偏移消除负坐标

---

## draw.io XML 样式映射

| 元素 | draw.io 形状 | 样式特征 |
|------|-------------|----------|
| 实体 | 矩形 | 白底黑框、13px 加粗 |
| 属性 | 椭圆 | 白底黑框、11px 常规 |
| 主键属性 | 椭圆 | 同上 + `fontStyle=1` 加粗 |
| 外键属性 | 椭圆 | 同上 + `dashed=1` 虚线边框 |
| 关系 | 菱形 | 白底黑框、11px 居中 |
| 连线 | 直线 | `endArrow=none`、黑色、带基数标注 |

---

## 与参考项目的差异

| 项目 | 参考项目 | 本 Skill |
|------|----------|----------|
| 输出格式 | SVG | draw.io XML |
| 可编辑性 | 静态图片 | 可在 draw.io 中拖拽编辑 |
| 渲染器 | `ChenSVGRenderer` | `DrawioXMLRenderer` |
| 布局引擎 | `ForceLayoutEngine` | 完全保留，无修改 |
| JSON DSL | 原格式 | 完全兼容 |

---

## 注意事项

- 实体/关系 ID 必须全局唯一
- `from` / `to` 引用的实体 ID 必须存在于 `entities` 中
- 建议实体数量不超过 15 个，否则布局可能拥挤
- 画布大小根据内容自动计算，无需手动设置
- 零外部依赖，纯 Python 标准库实现

---

## 文件结构

```
json-to-drawio-er/
├── SKILL.md
└── scripts/
    └── er_drawio_engine.py
```