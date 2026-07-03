---
name: "json-to-drawio-functional-module"
description: "Generates functional module hierarchy diagrams (system->role->function) from JSON DSL to draw.io XML. Invoke when user asks for functional module diagram, system hierarchy chart, or use-case module diagram."
---

# JSON to Draw.io Functional Module Diagram Generator

通过 **JSON DSL** 描述系统功能模块的层次结构（系统→角色→功能），使用确定性层级布局算法自动计算位置，输出标准 **draw.io (diagrams.net) XML** 文件。

> 基于参考项目的层级布局引擎，将 SVG 渲染器替换为 draw.io XML 渲染器，保留完整的 JSON DSL 兼容性。

---

## 核心特性

| 特性 | 说明 |
|------|------|
| **输入格式** | JSON DSL（兼容原参考项目格式） |
| **布局算法** | 三层确定性层级布局（L0系统→L1角色→L2功能） |
| **输出格式** | `.drawio` XML（可直接在 draw.io / diagrams.net 打开） |
| **风格** | 白底黑框论文风格，功能框竖排文字 |
| **依赖** | 纯 Python 标准库，零外部依赖 |

---

## JSON DSL 格式

```json
{
  "system_name": "系统名称",
  "roles": [
    {
      "name": "角色名称",
      "functions": ["功能1", "功能2", "功能3"]
    }
  ]
}
```

### 字段说明

**顶层**
| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `system_name` | string | 否 | `"System"` | 系统名称，显示在顶层框中 |
| `roles` | array | 否 | `[]` | 角色列表 |

**roles[]**
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 角色名称，显示在第二层框中 |
| `id` | string | 否 | 角色标识符（缺失时回退到 name） |
| `functions` | array\<string\> | 否 | 该角色下的功能名称列表，每个字符串竖排显示在第三层框中 |

---

## 使用方式

### 命令行

```bash
python functional_module_drawio_engine.py input.json output.drawio
```

不带参数直接运行会生成 demo 示例：
```bash
python functional_module_drawio_engine.py
# 输出: demo_functional_module.drawio
```

### Python API

```python
from functional_module_drawio_engine import FunctionalModuleDiagram, DiagramConfig

# 从 JSON 文件
diagram = FunctionalModuleDiagram().from_json_file("input.json")
diagram.save_drawio("output.drawio")

# 从字典
data = {
    "system_name": "图书管理系统",
    "roles": [
        {"name": "管理员", "functions": ["图书管理", "用户管理", "借阅管理", "统计报表"]},
        {"name": "读者", "functions": ["图书查询", "借阅归还", "个人信息"]}
    ]
}
diagram = FunctionalModuleDiagram().from_dict(data)
diagram.save_drawio("output.drawio")

# 获取 XML 字符串
xml = diagram.to_drawio()

# 获取布局信息
info = diagram.get_layout_info()
print(f"Canvas: {info['canvas_width']} x {info['canvas_height']}")
```

### 自定义配置

```python
config = DiagramConfig(
    sys_box_height=50,        # 系统框高度
    role_box_width=100,       # 角色框宽度
    func_box_width=35,        # 功能框宽度
    func_char_spacing=18,     # 竖排字符间距
    level_gap=70,             # 层间距
    role_gap=90,              # 角色组间距
    margin=60,                # 画布边距
)

diagram = FunctionalModuleDiagram(config).from_json_file("input.json")
diagram.save_drawio("output.drawio")
```

---

## 布局算法

三层确定性层级布局（非力导向）：

1. **计算角色组宽度**：每个角色组的宽度 = `max(role_box_width, 功能框总宽度)`
2. **系统框定位（L0）**：宽度 = `max(文本估算宽度, 所有角色组总宽度)`，位于画布顶部
3. **角色框定位（L1）**：在系统框下方，角色框在其组宽度内居中，从左到右排列
4. **功能框定位（L2）**：在角色框下方，功能组在其组宽度内居中，高度根据文字长度动态计算
5. **树形连线**：标准分叉模式（垂直主干→水平分支→垂直到子节点）
6. **画布计算**：自动调整尺寸并偏移消除负坐标

---

## draw.io XML 样式映射

| 元素 | draw.io 形状 | 样式特征 |
|------|-------------|----------|
| 系统框 | 矩形 | 白底黑框、16px 加粗、strokeWidth=2 |
| 角色框 | 矩形 | 白底黑框、13px 加粗、strokeWidth=1.5 |
| 功能框 | 矩形 | 白底黑框、12px 常规、竖排文字、strokeWidth=1 |
| 连线 | 直线 | `endArrow=none`、黑色、无箭头 |

---

## 示例

### 咖啡管理系统

```json
{
  "system_name": "咖啡管理系统",
  "roles": [
    {
      "name": "管理员",
      "functions": ["用户管理", "饮品管理", "分类管理", "口味标签管理", "库存管理", "顾客档案管理", "销售统计"]
    },
    {
      "name": "员工",
      "functions": ["登录注册", "饮品查看", "销售开单", "库存操作", "顾客管理", "个人中心"]
    }
  ]
}
```

---

## 注意事项

- 层级固定为三层：系统→角色→功能，不支持更深层嵌套
- 功能框内文字自动竖排显示
- 零外部依赖，纯 Python 标准库实现
- 输出 `.drawio` 文件可直接在 draw.io / diagrams.net 中打开编辑

---

## 文件结构

```
json-to-drawio-functional-module/
├── SKILL.md
└── scripts/
    └── functional_module_drawio_engine.py
```
