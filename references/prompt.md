# draw.io XML 生成提示词

## 任务说明

请根据用户描述，生成一个有效的 draw.io 格式的 XML 文件。文件必须可以直接在 draw.io（diagrams.net）中打开和编辑。

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
        
        <!-- 你的图表元素放在这里，parent="1" -->
        
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

样式字符串使用分号分隔的键值对：

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#DAE8FC;
```

### 常用样式属性

| 属性 | 值 | 说明 |
|------|-----|------|
| fillColor | #RRGGBB | 填充颜色 |
| strokeColor | #RRGGBB | 边框颜色 |
| strokeWidth | 数字 | 边框宽度 |
| rounded | 0/1 | 圆角矩形 |
| html | 0/1 | 启用 HTML 标签 |
| whiteSpace | wrap/nowrap | 文本换行 |
| align | left/center/right | 水平对齐 |
| verticalAlign | top/middle/bottom | 垂直对齐 |

### 预定义样式类

可以直接使用这些类名：
- `text` - 无填充无描边文本
- `ellipse` - 椭圆
- `rhombus` - 菱形
- `triangle` - 三角形
- `swimlane` - 泳道
- `group` - 透明容器
- 颜色主题：`blue`, `green`, `yellow`, `orange`, `red`, `purple`, `gray`

---

## 常用形状

### 核心形状

| 形状值 | 说明 |
|--------|------|
| rectangle | 矩形（默认） |
| ellipse | 椭圆 |
| rhombus | 菱形（需要 `perimeter=rhombusPerimeter`） |
| triangle | 三角形（需要 `perimeter=trianglePerimeter`） |
| hexagon | 六边形 |
| cloud | 云朵 |
| cylinder | 圆柱 |
| swimlane | 泳道 |
| actor | 小人 |

### 扩展形状

| 形状值 | 说明 |
|--------|------|
| note | 便签 |
| document | 文档 |
| folder | 文件夹 |
| process | 进程框 |
| step | 箭头步骤 |
| callout | 对话气泡 |
| datastore | 数据存储 |
| cube | 3D 立方体 |

---

## 顶点（Vertex）示例

### 基本矩形

```xml
<mxCell id="rect1" value="Hello" 
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#DAE8FC;strokeColor=#6C8EBF;" 
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry" />
</mxCell>
```

### 椭圆

```xml
<mxCell id="ellipse1" value="Start" 
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#D5E8D4;strokeColor=#82B366;" 
        vertex="1" parent="1">
  <mxGeometry x="340" y="40" width="120" height="60" as="geometry" />
</mxCell>
```

### 菱形（决策点）

```xml
<mxCell id="decision1" value="Condition?" 
        style="rhombus;perimeter=rhombusPerimeter;whiteSpace=wrap;html=1;fillColor=#FFF2CC;strokeColor=#D6B656;" 
        vertex="1" parent="1">
  <mxGeometry x="320" y="150" width="160" height="80" as="geometry" />
</mxCell>
```

---

## 边（Edge）示例

### 基本连接边

```xml
<mxCell id="edge1" value="" 
        style="endArrow=classic;html=1;" 
        edge="1" parent="1" source="rect1" target="ellipse1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### 带标签的边

```xml
<mxCell id="edge2" value="Yes" 
        style="endArrow=classic;html=1;" 
        edge="1" parent="1" source="decision1" target="rect1">
  <mxGeometry x="-0.5" y="0" relative="1" as="geometry" />
</mxCell>
```

### 正交边样式

```xml
<mxCell id="edge3" value="" 
        style="edgeStyle=orthogonalEdgeStyle;rounded=1;endArrow=classic;html=1;" 
        edge="1" parent="1" source="node1" target="node2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### 箭头类型

| 箭头值 | 说明 |
|--------|------|
| none | 无箭头 |
| classic | 实心三角形（默认） |
| block | 实心方块 |
| open | 空心三角形 |
| diamond | 菱形 |
| circle | 圆形 |

### 边样式

| edgeStyle 值 | 说明 |
|--------------|------|
| orthogonalEdgeStyle | 直角转弯（最常用） |
| elbowEdgeStyle | 单弯角 |
| entityRelationEdgeStyle | ER 图风格 |
| （空） | 直线 |

---

## 组和容器

### 透明组

```xml
<mxCell id="group1" value="Group" 
        style="group;" 
        vertex="1" parent="1">
  <mxGeometry x="50" y="50" width="300" height="200" as="geometry" />
</mxCell>

<!-- 组内元素，parent 设为组 ID -->
<mxCell id="child1" value="Inside" 
        style="rounded=1;html=1;" 
        vertex="1" parent="group1">
  <mxGeometry x="10" y="10" width="100" height="40" as="geometry" />
</mxCell>
```

### 泳道

```xml
<mxCell id="swimlane1" value="DMZ" 
        style="swimlane;startSize=25;fillColor=#F5F5F5;strokeColor=#666666;fontStyle=1;html=1;" 
        vertex="1" parent="1">
  <mxGeometry x="50" y="50" width="300" height="200" as="geometry" />
</mxCell>
```

---

## 常用颜色

### 浅色填充

- 蓝色：`#DAE8FC`
- 绿色：`#D5E8D4`
- 黄色：`#FFF2CC`
- 红色：`#F8CECC`
- 紫色：`#E1D5E7`
- 灰色：`#F5F5F5`
- 橙色：`#FFCD28`

### 深色边框（对应）

- 蓝色：`#6C8EBF`
- 绿色：`#82B366`
- 黄色：`#D6B656`
- 红色：`#B85450`
- 紫色：`#9673A6`
- 灰色：`#666666`
- 橙色：`#D79B00`

---

## HTML 标签

当设置 `html=1` 时，value 属性可以包含 HTML（需要 XML 转义）：

```xml
<mxCell value="&lt;b&gt;标题&lt;/b&gt;&lt;br&gt;描述" 
        style="rounded=1;whiteSpace=wrap;html=1;" 
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="150" height="60" as="geometry" />
</mxCell>
```

### HTML 转义规则

- `<` → `&lt;`
- `>` → `&gt;`
- `&` → `&amp;`
- `"` → `&quot;`

---

## 完整示例：简单流程图

```xml
<mxfile>
  <diagram id="flowchart" name="Flowchart">
    <mxGraphModel dx="0" dy="0" grid="1" gridSize="10" guides="1"
                  tooltips="1" connect="1" arrows="1" fold="1"
                  page="1" pageScale="1" pageWidth="850" pageHeight="1100">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- 开始 -->
        <mxCell id="start" value="Start" 
                style="ellipse;whiteSpace=wrap;html=1;fillColor=#D5E8D4;strokeColor=#82B366;" 
                vertex="1" parent="1">
          <mxGeometry x="340" y="40" width="120" height="60" as="geometry" />
        </mxCell>

        <!-- 决策 -->
        <mxCell id="decision" value="Condition?" 
                style="rhombus;perimeter=rhombusPerimeter;whiteSpace=wrap;html=1;fillColor=#FFF2CC;strokeColor=#D6B656;" 
                vertex="1" parent="1">
          <mxGeometry x="320" y="150" width="160" height="80" as="geometry" />
        </mxCell>

        <!-- 处理 A -->
        <mxCell id="procA" value="Process A" 
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#DAE8FC;strokeColor=#6C8EBF;" 
                vertex="1" parent="1">
          <mxGeometry x="160" y="290" width="120" height="60" as="geometry" />
        </mxCell>

        <!-- 处理 B -->
        <mxCell id="procB" value="Process B" 
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#DAE8FC;strokeColor=#6C8EBF;" 
                vertex="1" parent="1">
          <mxGeometry x="520" y="290" width="120" height="60" as="geometry" />
        </mxCell>

        <!-- 结束 -->
        <mxCell id="end" value="End" 
                style="ellipse;whiteSpace=wrap;html=1;fillColor=#F8CECC;strokeColor=#B85450;" 
                vertex="1" parent="1">
          <mxGeometry x="340" y="420" width="120" height="60" as="geometry" />
        </mxCell>

        <!-- 边 -->
        <mxCell id="e1" style="endArrow=classic;html=1;" 
                edge="1" parent="1" source="start" target="decision">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e2" value="Yes" style="endArrow=classic;html=1;" 
                edge="1" parent="1" source="decision" target="procA">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e3" value="No" style="endArrow=classic;html=1;" 
                edge="1" parent="1" source="decision" target="procB">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e4" style="endArrow=classic;html=1;" 
                edge="1" parent="1" source="procA" target="end">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e5" style="endArrow=classic;html=1;" 
                edge="1" parent="1" source="procB" target="end">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

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

---

## 输出要求

**只输出 XML 代码**，不要包含任何说明文字、Markdown 格式或代码块标记。输出应该以 `<mxfile>` 开头，以 `</mxfile>` 结尾，可以直接保存为 `.drawio` 文件使用。
