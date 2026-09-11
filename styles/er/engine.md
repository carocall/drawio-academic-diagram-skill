# 程序化生成引擎（er_engine.py，推荐）

本类型提供力导向自动布局引擎（`styles/er/er_engine.py`），从 JSON DSL 一键生成 Chen 风格 ER 图（矩形实体 + 椭圆属性 + 菱形关系 + 基数标注），样式与上面的手动规范一致。生成 ER 图时**优先用引擎**，除非用户明确要求手写。

### JSON DSL 格式

```json
{
  "type": "er",
  "entities": [
    {
      "id": "Student",
      "attributes": [
        {"name": "student_id", "type": "int", "is_primary_key": true},
        {"name": "name", "type": "string"}
      ]
    }
  ],
  "relationships": [
    {"id": "Enrolls", "from": "Student", "to": "Course", "cardinality": "N:M"}
  ]
}
```

- `entities[].id`：实体名称（全局唯一）
- `entities[].attributes`：属性列表，支持简写字符串 `"name"` 或完整对象（`name` / `type` / `is_primary_key` / `is_foreign_key`）
- `relationships[]`：`id` / `from` / `to` / `cardinality`（`1:1`、`1:N`、`N:1`、`N:M`）

### 调用方式

```bash
# 命令行
python styles/er/er_engine.py input.json output.drawio
# 不带参数运行生成 demo 示例（demo_er.drawio）

# Python API
from er_engine import ERDiagram
diagram = ERDiagram().from_json_file("input.json")
diagram.save_drawio("output.drawio")
xml = diagram.to_drawio()
```

### 布局算法

Louvain 社区检测 → 子图径向布局 → 全局力模拟（实体斥力 / 关系引力 / 边交叉斥力）→ 关系菱形置于实体中点 → 属性 16 角度扫描 + 力模拟微调 → 自动计算画布并消除负坐标。

### 样式映射

| 元素 | 形状 | 样式 |
|------|------|------|
| 实体 | 矩形 | 白底黑框、13px 加粗 |
| 属性 | 椭圆 | 白底黑框、11px；主键加粗、外键虚线 |
| 关系 | 菱形 | 白底黑框、11px 居中 |
| 连线 | 直线 | `endArrow=none`、黑色、带基数标注 |

### 注意事项

- 实体/关系 ID 必须全局唯一；`from` / `to` 引用的实体必须存在
- 建议实体数 ≤ 15，否则布局可能拥挤
- 纯 Python 标准库，零外部依赖
