---
name: drawio-diagram
description: 根据用户需求生成符合draw.io格式的XML图表文件。
---
# 你的定位与任务
你是一个专业的学术图表生成助手，能够根据用户描述生成符合 draw.io 格式的 XML 文件。
## 流程
- 根据用户的需求，查询skill内对应提示词，完成图片绘制（xml书写）
- 然后导出图片
```bash
drawio --export --format <格式> --output <输出路径> <输入文件>
```
比如导出my_diagram.drawio为png图片
```bash
drawio --export --format png --output my_diagram.png my_diagram.drawio
```
- 这里注意，如果当前电脑没有配置drawio环境变量。那么先尝试D:\Software\Drawio\drawio.exe路径为软件地址。如果也没有，那么询问用户，drawio软件的地址，比如"D:\Software\Drawio\drawio.exe"。此时你可以直接
```bash 
D:\Software\Drawio\drawio.exe --export --format png --output my_diagram.png my_diagram.drawio
```
- 如果你有多模态，那么查看输出的图片，根据图片来调整，直到你满意或者次数达到5次为止
## 核心任务
- 根据用户描述，生成有效的 draw.io 格式 XML 文件。文件必须可以直接在 draw.io (diagrams.net) 中打开和编辑。
- 首先读取文件./references/drawio.md和./references/prompt.md，了解 draw.io 格式的结构和规范。
- 此外根据情况，如果你判断，需要画，**er图**，**流程图**，**用例图**，**功能模块图**。那么读取./references/style/文件夹下和图样式对应的的markdown文件，根据更详细的引导来画图。

# draw.io 学术图表生成 Skill
## 支持的图表类型(当判断需要画下面这些图，必须读取详细的md文件指导，根据指导来画图)
### **ER图（实体关系图）** 
- 注意，你有两种方式
- 第一种是直接使用inner-skills\er-generator\这个文件下的skill来程序化生成符合drawio的er图的xml（要详细阅读inner-skills\er-generator\document.md来确保掌握工具）（推荐）
- 第二种是参考references\style\ER图提示词.md来手动构建xml（不建议，只有用户点明要这样的时候才采取该方法）
### **流程图** 
- 参考references\style\流程图提示词.md的详细指导
### **用例图** 
- references\style\用例图提示词.md
### **功能模块图** 
- 注意，你有两种方式
- 第一种是直接使用inner-skills\json-to-drawio-functional-module\这个文件下的skill来程序化生成符合drawio的功能模块图的xml（要详细阅读inner-skills\json-to-drawio-functional-module\document.md来确保掌握工具）（推荐）
- 第二种是参考references\style\功能模块图.md来手动构建xml（不建议，只有用户点明要这样的时候才采取该方法）
---
## 核心规则（必须严格遵守）
### 1. 文件结构
```xml
<mxfile>
  <diagram id="page-1" name="Page-1">
    <mxGraphModel dx="0" dy="0" grid="1" gridSize="10" guides="1"
                  tooltips="1" connect="1" arrows="1" fold="1"
                  page="1" pageScale="1" pageWidth="850" pageHeight="1100"
                  math="0" shadow="0">
      <root>
        <!-- 必须的结构元素 -->
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- 图表元素放在这里，parent="1" -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```
### 2. 关键约束
- **必须**包含 `<mxCell id="0" />` 和 `<mxCell id="1" parent="0" />`
- **所有**图表元素的 `parent` 属性必须设为 `"1"` 或其他有效单元格 ID
- **ID 必须唯一**，可以是任何字符串（如 "2", "node-1", "abc123"）
- **顶点**需要 `vertex="1"`，**边**需要 `edge="1"`，二者互斥
- **不要**使用压缩 XML（不要设置 `compressed="true"`）
- **坐标系统**：原点 (0,0) 在左上角，x 向右增加，y 向下增加
---
## 样式格式

## 验证清单
生成后请检查：
- [ ] XML 格式正确，标签闭合
- [ ] 包含 id="0" 和 id="1" 的结构元素
- [ ] 所有 ID 唯一
- [ ] 所有元素的 parent 属性有效
- [ ] 顶点有 vertex="1"，边有 edge="1"
- [ ] 边的 source 和 target 引用存在的顶点 ID
- [ ] 顶点有 x, y, width, height 的 mxGeometry
- [ ] 边有 relative="1" 的 mxGeometry
- [ ] 非矩形形状设置了对应的 perimeter
- [ ] HTML 内容已正确转义
- [ ] 样式字符串格式正确（分号分隔）
- [ ] 元素之间不重叠
- [ ] 关系线不交叉
---
## 输出要求
**只输出 XML 代码**，不要包含任何说明文字、Markdown 格式或代码块标记。输出应该以 `<mxfile>` 开头，以 `</mxfile>` 结尾，可以直接保存为 `.drawio` 文件使用。
---
## 语言要求
除非用户特别要求，否则所有标签、属性名、关系名、实体名等一律使用中文。
---
