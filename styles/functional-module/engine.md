# 程序化生成引擎（functional_module_engine.py，推荐）

本类型提供三层确定性层级布局引擎（`styles/functional-module/functional_module_engine.py`），从 JSON DSL 一键生成功能模块图（系统 → 角色 → 功能，功能框竖排文字），样式与上面的手动规范一致。生成功能模块图时**优先用引擎**，除非用户明确要求手写。

### JSON DSL 格式

```json
{
  "system_name": "系统名称",
  "roles": [
    {"name": "角色名称", "functions": ["功能1", "功能2", "功能3"]}
  ]
}
```

- `system_name`：系统名称（缺省 `"System"`）
- `roles[].name`：角色名称
- `roles[].functions`：该角色下的功能名称列表（竖排显示在功能框中）

### 调用方式

```bash
# 命令行
python styles/functional-module/functional_module_engine.py input.json output.drawio
# 不带参数运行生成 demo 示例（demo_functional_module.drawio）

# Python API
from functional_module_engine import FunctionalModuleDiagram
diagram = FunctionalModuleDiagram().from_json_file("input.json")
diagram.save_drawio("output.drawio")
```

### 布局算法

三层确定性层级布局（非力导向）：计算角色组宽度 → 系统框（L0，文本适配宽度）定位 → 角色框（L1）居中排列 → 功能框（L2，竖排，高度按文字动态计算）→ 树形连线（垂直主干 + 水平分支）→ 自动计算画布并消除负坐标。

### 样式映射

| 元素 | 形状 | 样式 |
|------|------|------|
| 系统框 | 矩形 | 白底黑框、16px 加粗、strokeWidth=2 |
| 角色框 | 矩形 | 白底黑框、13px 加粗、strokeWidth=1.5 |
| 功能框 | 矩形 | 白底黑框、12px 常规、竖排文字、strokeWidth=1 |
| 连线 | 直线 | `endArrow=none`、黑色、无箭头 |

### 注意事项

- 层级固定三层：系统 → 角色 → 功能，不支持更深嵌套
- 功能框内文字自动竖排显示
- 纯 Python 标准库，零外部依赖
