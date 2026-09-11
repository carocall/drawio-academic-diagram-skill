# ER 图（实体关系图，er）

本目录提供「ER 图」的 draw.io 生成支持，有两种方式。

## 目录内容

- `er_engine.py` —— 程序化生成引擎（力导向自动布局，Chen 风格：矩形实体 + 椭圆属性 + 菱形关系 + 基数标注）。
- `engine.md` —— 引擎的 JSON DSL 格式与调用方式（**推荐**优先用）。
- `style.md` —— 手写兜底样式规范与示例（用户明确要求手写，或引擎不适用时读）。

## 怎么用

- **推荐**：准备 `input.json`，运行 `python styles/er/er_engine.py input.json output.drawio`（格式详见 `engine.md`）。
- 兜底：读 `style.md` 手写。
- 无论哪种方式，都遵守通用层 `drawio.md` / `prompt.md` 的格式与输出要求（只输出 XML）。
