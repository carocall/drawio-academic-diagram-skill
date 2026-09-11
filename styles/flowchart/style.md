# 流程图生成提示词

## 样式规范

生成的流程图必须遵循以下五点样式规范。

### 1. 全图采用纯黑白论文风格

流程图中所有节点和连线均不使用彩色填充或渐变，仅使用黑色边框与白色背景，整体呈现简洁、正式的论文插图风格。

**示例：** 样例中的所有节点都没有显式设置填充色或边框色，默认即为白色背景、黑色描边，例如开始节点：

```xml
<mxCell id="LktgZs_kaKpMm6gGBoRD-1" value="&lt;span style=&quot;font-size: 16px;&quot;&gt;开始&lt;/span&gt;" style="strokeWidth=1;html=1;shape=mxgraph.flowchart.terminator;whiteSpace=wrap;" parent="1" vertex="1">
    <mxGeometry x="375" y="40" width="100" height="60" as="geometry"/>
</mxCell>
```

> 注意：`style` 中不要加入 `fillColor`、`strokeColor`、`gradientColor` 等颜色属性，保持默认黑白即可。

---

### 2. 开始和结束节点使用胶囊体（terminator）形状

流程的**开始**和**结束**节点必须使用 draw.io 流程图中的标准胶囊体/终端形状（`shape=mxgraph.flowchart.terminator`），而不是椭圆或圆角矩形。

**示例：** 样例中的开始节点和结束节点均使用 `terminator` 形状：

```xml
<!-- 开始节点 -->
<mxCell id="LktgZs_kaKpMm6gGBoRD-1" value="&lt;span style=&quot;font-size: 16px;&quot;&gt;开始&lt;/span&gt;" style="strokeWidth=1;html=1;shape=mxgraph.flowchart.terminator;whiteSpace=wrap;" parent="1" vertex="1">
    <mxGeometry x="375" y="40" width="100" height="60" as="geometry"/>
</mxCell>

<!-- 结束节点 -->
<mxCell id="LktgZs_kaKpMm6gGBoRD-2" value="&lt;span style=&quot;font-size: 16px;&quot;&gt;结束&lt;/span&gt;" style="strokeWidth=1;html=1;shape=mxgraph.flowchart.terminator;whiteSpace=wrap;" parent="1" vertex="1">
    <mxGeometry x="375" y="820" width="100" height="60" as="geometry"/>
</mxCell>
```

---

### 3. 用户输入节点使用平行四边形

凡是表示**用户输入**或**数据输入**的节点，必须使用平行四边形（`shape=parallelogram`），并设置 `perimeter=parallelogramPerimeter` 与 `fixedSize=1`。

**示例：** 样例中"用户输入账号密码"节点使用平行四边形：

```xml
<mxCell id="k3qjh213Gn-w5bPCmU27-1" value="用户输入账号密码" style="shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;fixedSize=1;" parent="1" vertex="1">
    <mxGeometry x="345" y="140" width="155" height="60" as="geometry"/>
</mxCell>
```

---

### 4. 判断/决策节点使用菱形

流程中的**判断**或**分支决策**节点必须使用菱形（`rhombus`），并设置 `perimeter=rhombusPerimeter`；节点文案通常以问号结尾，表示一个需要判断的条件。

**示例：** 样例中"格式校验通过？"和"身份验证通过？"均为菱形判断节点：

```xml
<mxCell id="check1" value="格式校验通过？" style="rhombus;perimeter=rhombusPerimeter;whiteSpace=wrap;html=1;" parent="1" vertex="1">
    <mxGeometry x="325" y="300" width="200" height="80" as="geometry"/>
</mxCell>
```

---

### 5. 其余处理/操作节点使用矩形

除开始、结束、用户输入、判断之外的**普通处理步骤、操作、输出**等节点，统一使用矩形表示（`rounded=1;whiteSpace=wrap;html=1;`）。

**示例：** 样例中的"前端格式校验"、"后端身份验证"、"生成JWT Token"、"返回Token到前端"以及错误提示节点均为矩形：

```xml
<mxCell id="frontend" value="前端格式校验" style="rounded=1;whiteSpace=wrap;html=1;" parent="1" vertex="1">
    <mxGeometry x="345" y="220" width="160" height="60" as="geometry"/>
</mxCell>

<mxCell id="error1" value="提示格式错误" style="rounded=1;whiteSpace=wrap;html=1;" parent="1" vertex="1">
    <mxGeometry x="570" y="310" width="120" height="60" as="geometry"/>
</mxCell>
```

---
## 6.边（Edge）的连接

### 1. 基本顺序边

```xml
<mxCell id="edge1" edge="1" parent="1" source="node1" target="node2"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=16;">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

- `edgeStyle=orthogonalEdgeStyle` - 正交边样式
- `rounded=0` - 不圆角
- `endArrow=classic` - 经典实心箭头
- `fontSize=16` - 字体大小 16

### 2. 带标签的判断边

```xml
<mxCell id="edge2" edge="1" parent="1" source="decision1" target="node1"
        style="endArrow=classic;html=1;fontSize=16;" value="是">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

- `value="是"` 或 `value="否"` - 边标签

### 3. 正交返回边（用于"否"分支）

```xml
<mxCell id="edge3" edge="1" parent="1" source="decision1" target="node1"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;entryX=1;entryY=0.25;entryDx=0;entryDy=0;fontSize=16;html=1;" value="否">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="X1" y="Y1" />
      <mxPoint x="X2" y="Y2" />
      <mxPoint x="X3" y="Y3" />
    </Array>
    <mxPoint x="X源" y="Y源" as="sourcePoint" />
    <mxPoint x="X目标" y="Y目标" as="targetPoint" />
  </mxGeometry>
</mxCell>
```

- `edgeStyle=orthogonalEdgeStyle` - 正交边样式
- `entryX`, `entryY` - 入口位置
- `<Array as="points">` - 拐点坐标
- `sourcePoint` / `targetPoint` - 源点和目标点

---

## 布局建议

### 节点垂直排列
- 从顶部开始，向下排列
- 节点间距约 90-100px（从一个节点底部到下一个节点顶部）

### 开始节点
- y 坐标约 550-600
- 放在顶部中央

### 处理节点
- 从上到下依次排列
- 每个 y 坐标递增约 90-100

### 判断节点
- 放在流程中间
- 比处理节点稍高（80px）

### 结束节点
- 放在底部

### 判断分支的返回边
- 从菱形侧面出发，绕过其他节点
- 使用正交边和拐点

---
## 完整示例结构

以下是一个完整的 draw.io 流程图 XML 示例，可直接保存为 `.drawio` 文件使用。该示例综合了上述全部样式规范：黑白风格、胶囊体开始/结束、平行四边形输入、菱形判断、矩形处理。

```xml
<mxfile host="65bd71144e">
    <diagram id="flowchart1" name="用户注册登录流程图">
        <mxGraphModel dx="679" dy="887" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
            <root>
                <mxCell id="0"/>
                <mxCell id="1" parent="0"/>
                <mxCell id="frontend" value="前端格式校验" style="rounded=1;whiteSpace=wrap;html=1;" parent="1" vertex="1">
                    <mxGeometry x="345" y="220" width="160" height="60" as="geometry"/>
                </mxCell>
                <mxCell id="check1" value="格式校验通过？" style="rhombus;perimeter=rhombusPerimeter;whiteSpace=wrap;html=1;" parent="1" vertex="1">
                    <mxGeometry x="325" y="300" width="200" height="80" as="geometry"/>
                </mxCell>
                <mxCell id="error1" value="提示格式错误" style="rounded=1;whiteSpace=wrap;html=1;" parent="1" vertex="1">
                    <mxGeometry x="570" y="310" width="120" height="60" as="geometry"/>
                </mxCell>
                <mxCell id="backend" value="后端身份验证" style="rounded=1;whiteSpace=wrap;html=1;" parent="1" vertex="1">
                    <mxGeometry x="345" y="420" width="160" height="60" as="geometry"/>
                </mxCell>
                <mxCell id="check2" value="身份验证通过？" style="rhombus;perimeter=rhombusPerimeter;whiteSpace=wrap;html=1;" parent="1" vertex="1">
                    <mxGeometry x="325" y="510" width="200" height="80" as="geometry"/>
                </mxCell>
                <mxCell id="error2" value="提示账号或密码错误" style="rounded=1;whiteSpace=wrap;html=1;" parent="1" vertex="1">
                    <mxGeometry x="130" y="520" width="140" height="60" as="geometry"/>
                </mxCell>
                <mxCell id="token" value="生成JWT Token" style="rounded=1;whiteSpace=wrap;html=1;" parent="1" vertex="1">
                    <mxGeometry x="345" y="630" width="160" height="60" as="geometry"/>
                </mxCell>
                <mxCell id="return" value="返回Token到前端" style="rounded=1;whiteSpace=wrap;html=1;" parent="1" vertex="1">
                    <mxGeometry x="345" y="710" width="160" height="60" as="geometry"/>
                </mxCell>
                <mxCell id="e1" style="endArrow=classic;html=1;" parent="1" edge="1">
                    <mxGeometry relative="1" as="geometry">
                        <mxPoint x="425.0000000000002" y="100" as="sourcePoint"/>
                        <mxPoint x="425" y="140" as="targetPoint"/>
                    </mxGeometry>
                </mxCell>
                <mxCell id="e2" style="endArrow=classic;html=1;" parent="1" target="frontend" edge="1">
                    <mxGeometry relative="1" as="geometry">
                        <mxPoint x="425" y="200" as="sourcePoint"/>
                    </mxGeometry>
                </mxCell>
                <mxCell id="e3" style="endArrow=classic;html=1;" parent="1" source="frontend" target="check1" edge="1">
                    <mxGeometry relative="1" as="geometry"/>
                </mxCell>
                <mxCell id="e4" value="" style="endArrow=classic;html=1;" parent="1" source="check1" target="error1" edge="1">
                    <mxGeometry relative="1" as="geometry"/>
                </mxCell>
                <mxCell id="e5" value="是" style="endArrow=classic;html=1;" parent="1" source="check1" target="backend" edge="1">
                    <mxGeometry relative="1" as="geometry"/>
                </mxCell>
                <mxCell id="e6" style="endArrow=classic;html=1;edgeStyle=orthogonalEdgeStyle;rounded=1;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=0.536;exitY=-0.018;exitDx=0;exitDy=0;exitPerimeter=0;" parent="1" source="error1" target="k3qjh213Gn-w5bPCmU27-1" edge="1">
                    <mxGeometry relative="1" as="geometry">
                        <Array as="points">
                            <mxPoint x="634" y="170"/>
                        </Array>
                        <mxPoint x="635" y="300" as="sourcePoint"/>
                        <mxPoint x="425" y="119.99" as="targetPoint"/>
                    </mxGeometry>
                </mxCell>
                <mxCell id="e7" style="endArrow=classic;html=1;" parent="1" source="backend" target="check2" edge="1">
                    <mxGeometry relative="1" as="geometry"/>
                </mxCell>
                <mxCell id="e8" value="" style="endArrow=classic;html=1;" parent="1" source="check2" target="error2" edge="1">
                    <mxGeometry relative="1" as="geometry"/>
                </mxCell>
                <mxCell id="2" value="否" style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];" vertex="1" connectable="0" parent="e8">
                    <mxGeometry x="-0.4424" relative="1" as="geometry">
                        <mxPoint as="offset"/>
                    </mxGeometry>
                </mxCell>
                <mxCell id="e9" value="是" style="endArrow=classic;html=1;" parent="1" source="check2" target="token" edge="1">
                    <mxGeometry relative="1" as="geometry"/>
                </mxCell>
                <mxCell id="e10" style="endArrow=classic;html=1;edgeStyle=orthogonalEdgeStyle;rounded=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" parent="1" target="k3qjh213Gn-w5bPCmU27-1" edge="1">
                    <mxGeometry relative="1" as="geometry">
                        <Array as="points">
                            <mxPoint x="195" y="170"/>
                        </Array>
                        <mxPoint x="195.00298701298698" y="520" as="sourcePoint"/>
                        <mxPoint x="350" y="120" as="targetPoint"/>
                    </mxGeometry>
                </mxCell>
                <mxCell id="e11" style="endArrow=classic;html=1;" parent="1" source="token" target="return" edge="1">
                    <mxGeometry relative="1" as="geometry"/>
                </mxCell>
                <mxCell id="e12" style="endArrow=classic;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;entryPerimeter=0;" parent="1" source="return" target="LktgZs_kaKpMm6gGBoRD-2" edge="1">
                    <mxGeometry relative="1" as="geometry">
                        <mxPoint x="425" y="800" as="targetPoint"/>
                    </mxGeometry>
                </mxCell>
                <mxCell id="k3qjh213Gn-w5bPCmU27-1" value="用户输入账号密码" style="shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;fixedSize=1;" parent="1" vertex="1">
                    <mxGeometry x="345" y="140" width="155" height="60" as="geometry"/>
                </mxCell>
                <mxCell id="LktgZs_kaKpMm6gGBoRD-1" value="&lt;span style=&quot;font-size: 16px;&quot;&gt;开始&lt;/span&gt;" style="strokeWidth=1;html=1;shape=mxgraph.flowchart.terminator;whiteSpace=wrap;" parent="1" vertex="1">
                    <mxGeometry x="375" y="40" width="100" height="60" as="geometry"/>
                </mxCell>
                <mxCell id="LktgZs_kaKpMm6gGBoRD-2" value="&lt;span style=&quot;font-size: 16px;&quot;&gt;结束&lt;/span&gt;" style="strokeWidth=1;html=1;shape=mxgraph.flowchart.terminator;whiteSpace=wrap;" parent="1" vertex="1">
                    <mxGeometry x="375" y="820" width="100" height="60" as="geometry"/>
                </mxCell>
            </root>
        </mxGraphModel>
    </diagram>
</mxfile>
```

---

## 输出要求

只输出 XML 代码，以 `<mxfile>` 开头，`</mxfile>` 结尾，可以直接保存为 `.drawio` 文件使用。
