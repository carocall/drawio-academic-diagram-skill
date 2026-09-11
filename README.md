# drawio-diagram Skill

根据用户需求生成符合 draw.io (diagrams.net) 格式的 XML 图表文件，可直接保存为 `.drawio` 打开编辑。

## 目录结构

```
drawio-diagram/
├── SKILL.md              # 入口：通用层 + 路由表
├── drawio.md             # 通用格式规范（XML 结构 / 样式 / 形状 / 边 / 容器 / 示例）
├── prompt.md             # 通用生成指令（任务说明 / 输出要求 / 语言要求）
├── README.md             # 本文件
└── styles/               # 按图类型检索的样式参考目录
    ├── flowchart/        # 流程图
    │   └── guide.md
    ├── usecase/          # 用例图
    │   └── guide.md
    ├── swimlane/         # 泳道图（跨职能流程图）
    │   └── guide.md
    ├── tech-roadmap/     # 技术路线图
    │   └── guide.md
    ├── er/               # ER 图（实体关系图）
    │   ├── guide.md
    │   └── er_engine.py  # 力导向自动布局引擎（推荐）
    └── functional-module/ # 功能模块图
        ├── guide.md
        └── functional_module_engine.py # 层级布局引擎（推荐）
```

## 支持的图类型

- **流程图 / 用例图 / 泳道图 / 技术路线图**：读对应 `styles/<type>/guide.md` 手写。
- **ER 图 / 功能模块图**：提供 JSON-to-drawio 程序化引擎（`styles/er/er_engine.py`、`styles/functional-module/functional_module_engine.py`），从 JSON DSL 一键生成标准 XML。

## 使用流程

模型读取 `SKILL.md` 后：

1. 先读 `drawio.md` + `prompt.md` 掌握通用规范与约束；
2. 按图类型检索 `styles/<type>/guide.md` 获取专属样式；
3. ER / 功能模块图优先调用引擎生成。

## 程序化引擎

```bash
# ER 图：JSON DSL -> draw.io XML（力导向自动布局，Chen 风格）
python styles/er/er_engine.py input.json output.drawio

# 功能模块图：JSON DSL -> draw.io XML（三层确定性层级布局）
python styles/functional-module/functional_module_engine.py input.json output.drawio
```

两者均为纯 Python 标准库实现，零外部依赖；不带参数运行会生成 demo 示例。详细 JSON DSL 格式与字段说明见各自 `guide.md` 内的「程序化生成引擎」章节。
