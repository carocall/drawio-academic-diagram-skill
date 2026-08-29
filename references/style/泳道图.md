# 泳道图（跨职能流程图）生成提示词

## 任务说明

根据用户描述的业务流程，生成一个符合 draw.io 格式的**泳道图（Swimlane / 跨职能流程图）** XML 文件。

一会可能会发给你一些流程描述（可能是制度条文、审批流程说明、论文里的流程描述，也可能是其他格式），你需要从中提取出：

- **流程总标题**（找不到就根据内容自拟一个）
- **列 = 角色 / 部门 / 参与方**（谁来做）
- **行 = 阶段 / 环节 / 业务板块**（流程分几大步）
- **节点 = 每个阶段里各方要做的具体动作**（含判断分支、退回分支）

然后生成一个符合 draw.io 格式的泳道图 XML 文件。

> **泳道图的本质**：横轴是"谁负责"，纵轴是"流程走到哪一步"。每个节点必须落在**唯一的 (行, 列) 交叉格**里，节点颜色表达它的语义类型。

---

## 一、整体骨架

泳道图由 **5 类元素**组成，缺一不可：

```
┌─────────────────────────── ① 总标题条 ───────────────────────────┐
├──────┬──────────┬──────────┬──────────┬──────────┬──────────────┤
│      │ 角色 A   │ 角色 B   │ 角色 C   │ 角色 D   │  ← ② 列头   │
│      │          │          │          │          │              │
│ 阶   │  ┌────┐  │  ┌────┐  │  ┌────┐  │  ┌────┐  │              │
│ 段   │  │节点│──┼─▶│节点│──┼─▶│节点│  │  │节点│  │              │
│ 一   │  └────┘  │  └────┘  │  └────┘  │  └────┘  │              │
│      │          │          │          │          │              │
├──────┼──────────┼──────────┼──────────┼──────────┼──────────────┤  ← ⑤ 横向分隔线
│ 阶   │          │          │          │          │              │
│ 段   │  ┌────┐  │  ◇判断   │  ┌────┐  │  ┌────┐  │              │
│ 二   │  │节点│  │          │  │节点│  │  │节点│  │   ← ④ 节点   │
├──────┼──────────┼──────────┼──────────┼──────────┼──────────────┤
   ↑         ↑         ↑         ↑         ↑         ↑
 ③ 行头                              ⑤ 纵向分隔线
```

### 画布参数（推荐基准值，可按内容缩放）

| 参数 | 值 | 说明 |
|------|-----|------|
| `X0` | 100 | 画布左边界 |
| `X1` | 1640 | 画布右边界 |
| `Y_HEAD` | 50 | 列头区起始 y |
| `H_HEAD` | 60 | 列头区高度（列头占 y: 50~110） |
| `W_ROW` | 60 | 行头列宽度（占 x: 100~160） |
| `H_TITLE` | 50 | 总标题条高度（占 y: 0~50） |
| 列宽 | 220~300 | 每列可不等宽，按角色名长度定 |
| 行高 | 290~750 | 每行必须按内容自适应 |

对应 `<mxGraphModel>` 建议：`pageWidth="1650" pageHeight="2330"`（可随总高度增大）。

---

## 二、图元素类型

### 1. 总标题条

横跨整个画布宽度的白底矩形，位于最顶部：

```xml
<mxCell id="t" parent="1"
        style="rounded=0;whiteSpace=wrap;html=1;fontSize=24;fontStyle=1;align=center;verticalAlign=middle;strokeWidth=1;"
        value="科技经营资质主要负责人及执业资格管理规定（修订）流程图" vertex="1">
  <mxGeometry height="50" width="1540" x="100" y="0" as="geometry" />
</mxCell>
```

- `width = X1 - X0`，`x = X0`，`y = 0`，`height = 50`
- `fontSize=24`、`fontStyle=1`（加粗）、居中
- **不设 fillColor**（白底黑框）

### 2. 列头（角色 / 部门）

每行一个矩形，**横向紧密铺满**，左右与列边界完全对齐（相邻列头共享边框）：

```xml
<mxCell id="h1" parent="1"
        style="rounded=0;whiteSpace=wrap;html=1;fontSize=22;fontStyle=1;align=center;verticalAlign=middle;"
        value="决策机构（院会议）" vertex="1">
  <mxGeometry height="60" width="240" x="160" y="50" as="geometry" />
</mxCell>
```

- `y = 50`，`height = 60`，`x` 与 `width` **必须等于该列的左边界与列宽**
- `fontSize=22`、`fontStyle=1`、居中
- 列数建议 **4~7 个**，过多则图会过宽；名称过长用 `&#xa;` 换行

### 3. 行头（阶段 / 环节）

左侧竖窄条，文字**竖排短行**（每行约 4~5 个汉字，用 `&#xa;` 换行）：

```xml
<mxCell id="r1" parent="1"
        style="rounded=0;whiteSpace=wrap;html=1;fontSize=22;fontStyle=1;align=center;verticalAlign=middle;"
        value="资质规划与&#xa;总量控制" vertex="1">
  <mxGeometry height="290" width="60" x="100" y="50" as="geometry" />
</mxCell>
```

- `x = 100`，`width = 60`，`y` 与 `height` **必须等于该行的上边界与行高**
- 行头纵向紧密相接：`r1` 的下边界 = `r2` 的上边界
- `fontSize=22`、`fontStyle=1`

### 4. 节点（流程动作）

节点按**语义**决定形状与配色，详见第三节。通用属性：

```xml
<!-- 处理 / 申请 / 审批 / 备案：圆角矩形 -->
<mxCell id="A0" parent="1"
        style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        value="研究院资质&#xa;总体规划" vertex="1">
  <mxGeometry height="50" width="220" x="170" y="170" as="geometry" />
</mxCell>
```

```xml
<!-- 判断 / 分支：菱形 -->
<mxCell id="Bc" parent="1"
        style="rhombus;perimeter=rhombusPerimeter;whiteSpace=wrap;html=1;fontSize=12;fillColor=#fff2cc;strokeColor=#d6b656;"
        value="符合总量&#xa;控制指标？" vertex="1">
  <mxGeometry height="80" width="230" x="655" y="385" as="geometry" />
</mxCell>
```

```xml
<!-- 输入 / 触发 / 员工侧发起：平行四边形 -->
<mxCell id="B0" parent="1"
        style="shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;fixedSize=1;fontSize=12;fillColor=#f8cecc;strokeColor=#b85450;"
        value="申报执业资格考试" vertex="1">
  <mxGeometry height="50" width="200" x="1430" y="400" as="geometry" />
</mxCell>
```

```xml
<!-- 流程终点：终止符（胶囊体） -->
<mxCell id="END" parent="1"
        style="shape=mxgraph.flowchart.terminator;whiteSpace=wrap;html=1;fontSize=13;fontStyle=1;fillColor=#ffe6cc;strokeColor=#d79b00;"
        value="制度正式执行&#xa;(2026年10月1日起)" vertex="1">
  <mxGeometry height="55" width="240" x="640" y="2160" as="geometry" />
</mxCell>
```

**尺寸基准**

| 类型 | 宽 | 高 |
|------|-----|-----|
| 圆角矩形（处理/审批/备案） | 列宽 − 20~30 | 50（文字 3 行时 55~70） |
| 菱形（判断） | 列宽 − 20~30 | 80 |
| 平行四边形（输入/触发） | 列宽 − 20 | 50 |
| 终止符（终点） | 240 | 55 |

- 节点 `fontSize=12`（列头/行头是 22，标题是 24，**节点必须小一号**）
- 节点 `x = 列左边界 + 10~30`，即列内水平居中，左右各留 10~30px
- 文本换行用 `&#xa;`（XML 换行实体），**不要用 `<br>`**

### 5. 网格线

网格线用**独立的纯坐标边**绘制（不设 `source`/`target`，只用 `sourcePoint`/`targetPoint`），保证不会被节点吸附拖拽。

```xml
<!-- 纵向分隔线：位于每一列的左边界，以及最右侧边界 -->
<mxCell id="v1" edge="1" parent="1" style="endArrow=none;html=1;strokeColor=#666666;">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="160" y="110" as="sourcePoint" />
    <mxPoint x="160" y="2230" as="targetPoint" />
  </mxGeometry>
</mxCell>

<!-- 横向分隔线：位于每一行的上边界，以及最底部边界 -->
<mxCell id="hsep2" edge="1" parent="1" style="endArrow=none;html=1;strokeColor=#666666;">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="100" y="640" as="sourcePoint" />
    <mxPoint x="1640" y="640" as="targetPoint" />
  </mxGeometry>
</mxCell>
```

- 纵向线：`x` = 各列左边界 + 最右边界 `X1`，`y` 从 `110`（列头底）到画布底
- 横向线：`y` = 各行上边界 + 最底边界，`x` 从 `X0` 到 `X1`
- 线数：列数 + 1 条竖线，行数 + 1 条横线
- `strokeColor=#666666`（浅灰），`endArrow=none`

---

## 三、配色规范（按节点语义着色）

**这是泳道图的灵魂**：颜色表达"这个节点是干什么的"，而不是"它在哪一列"。不过因为每个角色的职责相对固定，颜色通常会在视觉上与该列自然对应。

| 语义 | 形状 | fillColor | strokeColor |
|------|------|-----------|-------------|
| 顶层决策 / 总体规划 / 规则说明 | 圆角矩形 | `#dae8fc` | `#6c8ebf` |
| 申请 / 提出 / 办理 / 执行（发起动作） | 圆角矩形 | `#fff2cc` | `#d6b656` |
| 归口部门审核 / 核验 / 技术审查 | 圆角矩形 | `#d5e8d4` | `#82b366` |
| 领导审批 / 批准同意 | 圆角矩形 | `#ffe6cc` | `#d79b00` |
| 备案 / 归档 / 记录留存 | 圆角矩形 | `#e1d5e7` | `#9673a6` |
| 输入 / 触发 / 取得成果（外部或员工侧发起） | 平行四边形 | `#f8cecc` | `#b85450` |
| 驳回 / 退回 / 异常终止 | 圆角矩形 | `#f8cecc` | `#b85450` |
| 判断 / 分支 | 菱形 | `#fff2cc` | `#d6b656` |
| 流程终点 | 终止符 | `#ffe6cc` | `#d79b00` |

> 全部为 **浅填充 + 深描边** 配对，禁止使用高饱和纯色填充，禁止渐变。

---

## 四、边（Edge）的连接

### 1. 顺序边（默认）

```xml
<mxCell id="e_A1A2" edge="1" parent="1" source="A1" target="A2"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### 2. 跨列边（需要拐点时）

当两点不在同一行/列、直接正交会压到别的节点时，用 `<Array as="points">` 指定拐点：

```xml
<mxCell id="e_A0A1" edge="1" parent="1" source="A0" target="A1"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="280" y="260" />
      <mxPoint x="1040" y="260" />
    </Array>
  </mxGeometry>
</mxCell>
```

> 拐点的 y 必须落在两条横向分隔线之间的空白带里（不能压到节点），x 同理。

### 3. 判断分支边（必须带"是/否"标签）

```xml
<mxCell id="e_BcB1" edge="1" parent="1" source="Bc" target="B1"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;"
        value="是">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="770" y="480" />
      <mxPoint x="990" y="480" />
    </Array>
  </mxGeometry>
</mxCell>
```

- 菱形出来的每条边**必须**有 `value="是"` 或 `value="否"`（多分支可用其他短标签）
- `endArrow=classic`（实心箭头），`fontSize=11`

### 4. 边样式说明

| 属性 | 值 | 说明 |
|------|-----|------|
| `edgeStyle` | `orthogonalEdgeStyle` | 正交折线 |
| `rounded` | `0` | 直角，不圆角 |
| `endArrow` | `classic` | 实心箭头 |
| `strokeColor` | `#333333` | 深灰，比网格线（#666666）深 |
| `fontSize` | `11` | 边标签字号，比节点（12）再小一号 |

---

## 五、布局算法（照此顺序推导坐标）

### 步骤 1：定列

1. 列出所有角色/部门，按**流程中出场的先后顺序**从左到右排
2. 计算列边界：`col[0].left = X0 + W_ROW = 160`；`col[i+1].left = col[i].left + col[i].width`
3. 列宽建议：`max(220, 角色名长度 × 24 + 40)`，控制在 220~300
4. `X1 = col[last].left + col[last].width`

### 步骤 2：定行

1. 把流程切成若干**阶段**（通常 3~6 个）
2. 估算每行需要几"层"节点（同一批次并列出现的算一层）
3. 行高 = 上留白(40~60) + Σ层高(普通 50 / 判断 80) + Σ层间距(30~60) + 下留白(30~60)
4. `row[0].top = Y_HEAD = 50`；`row[j+1].top = row[j].top + row[j].height`

### 步骤 3：放节点

1. 每个节点归属到 (行 j, 列 i)
2. `x = col[i].left + 10~30`，`width = col[i].width − 20~30`（列内居中）
3. `y` 按该行内的执行顺序从上往下排，**同层节点 y 对齐**
4. 单行只有一层时，节点垂直居中于该行

### 步骤 4：画网格线

按列边界画竖线（列数 + 1 条），按行边界画横线（行数 + 1 条）。

### 步骤 5：连边

按流程顺序连接，判断节点分出"是/否"两路。

---

## 六、绘制顺序（影响图层叠放，务必遵守）

1. `id="0"` / `id="1"` 结构元素
2. 总标题条
3. 列头（h1…hN）→ 行头（r1…rN）
4. 所有节点
5. **所有流程边**
6. **网格线（最后画）** —— 保证分隔线压在最上层、清晰可见

---

## 七、完整示例结构

以下是标准泳道图（6 列 × 5 行）的完整 XML，可直接保存为 `.drawio` 文件使用，**样式必须完全照抄**：

```xml
<mxfile host="Electron" agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) draw.io/29.6.6 Chrome/144.0.7559.236 Electron/40.8.4 Safari/537.36" version="29.6.6">
  <diagram id="qualification-flow" name="科技经营资质管理流程泳道图">
    <mxGraphModel dx="1733" dy="1183" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1650" pageHeight="2330" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="t" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fontSize=24;fontStyle=1;align=center;verticalAlign=middle;strokeWidth=1;" value="科技经营资质主要负责人及执业资格管理规定（修订）流程图" vertex="1">
          <mxGeometry height="50" width="1540" x="100" y="0" as="geometry" />
        </mxCell>
        <mxCell id="h1" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fontSize=22;fontStyle=1;align=center;verticalAlign=middle;" value="决策机构（院会议）" vertex="1">
          <mxGeometry height="60" width="240" x="160" y="50" as="geometry" />
        </mxCell>
        <mxCell id="h2" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fontSize=22;fontStyle=1;align=center;verticalAlign=middle;" value="分管领导" vertex="1">
          <mxGeometry height="60" width="240" x="400" y="50" as="geometry" />
        </mxCell>
        <mxCell id="h3" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fontSize=22;fontStyle=1;align=center;verticalAlign=middle;" value="总工办（归口管理）" vertex="1">
          <mxGeometry height="60" width="260" x="640" y="50" as="geometry" />
        </mxCell>
        <mxCell id="h4" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fontSize=22;fontStyle=1;align=center;verticalAlign=middle;" value="资质责任单位" vertex="1">
          <mxGeometry height="60" width="280" x="900" y="50" as="geometry" />
        </mxCell>
        <mxCell id="h5" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fontSize=22;fontStyle=1;align=center;verticalAlign=middle;" value="人力资源部" vertex="1">
          <mxGeometry height="60" width="240" x="1180" y="50" as="geometry" />
        </mxCell>
        <mxCell id="h6" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fontSize=22;fontStyle=1;align=center;verticalAlign=middle;" value="员工" vertex="1">
          <mxGeometry height="60" width="220" x="1420" y="50" as="geometry" />
        </mxCell>
        <mxCell id="r1" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fontSize=22;fontStyle=1;align=center;verticalAlign=middle;" value="资质规划与&#xa;总量控制" vertex="1">
          <mxGeometry height="290" width="60" x="100" y="50" as="geometry" />
        </mxCell>
        <mxCell id="r2" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fontSize=22;fontStyle=1;align=center;verticalAlign=middle;" value="执业资格考试&#xa;报考审批" vertex="1">
          <mxGeometry height="300" width="60" x="100" y="340" as="geometry" />
        </mxCell>
        <mxCell id="r3" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fontSize=22;fontStyle=1;align=center;verticalAlign=middle;" value="执业资格注册&#xa;管理" vertex="1">
          <mxGeometry height="410" width="60" x="100" y="640" as="geometry" />
        </mxCell>
        <mxCell id="r4" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fontSize=22;fontStyle=1;align=center;verticalAlign=middle;" value="证书保管与&#xa;津贴管理" vertex="1">
          <mxGeometry height="430" width="60" x="100" y="1050" as="geometry" />
        </mxCell>
        <mxCell id="r5" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fontSize=22;fontStyle=1;align=center;verticalAlign=middle;" value="变更/延续/注销&#xa;与动态调整" vertex="1">
          <mxGeometry height="750" width="60" x="100" y="1480" as="geometry" />
        </mxCell>
        <mxCell id="A0" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#dae8fc;strokeColor=#6c8ebf;" value="研究院资质&#xa;总体规划" vertex="1">
          <mxGeometry height="50" width="220" x="170" y="170" as="geometry" />
        </mxCell>
        <mxCell id="A1" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#fff2cc;strokeColor=#d6b656;" value="提出控制指标&#xa;/新增资质类型申请" vertex="1">
          <mxGeometry height="50" width="220" x="930" y="170" as="geometry" />
        </mxCell>
        <mxCell id="A2" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#d5e8d4;strokeColor=#82b366;" value="征求相关部门意见&#xa;审核审批" vertex="1">
          <mxGeometry height="50" width="230" x="660" y="170" as="geometry" />
        </mxCell>
        <mxCell id="A3" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#ffe6cc;strokeColor=#d79b00;" value="主管领导&#xa;审批同意" vertex="1">
          <mxGeometry height="50" width="220" x="410" y="170" as="geometry" />
        </mxCell>
        <mxCell id="A4" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#e1d5e7;strokeColor=#9673a6;" value="备案" vertex="1">
          <mxGeometry height="50" width="220" x="1190" y="170" as="geometry" />
        </mxCell>
        <mxCell id="B0" parent="1" style="shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;fixedSize=1;fontSize=12;fillColor=#f8cecc;strokeColor=#b85450;" value="申报执业资格考试" vertex="1">
          <mxGeometry height="50" width="200" x="1430" y="400" as="geometry" />
        </mxCell>
        <mxCell id="Bc" parent="1" style="rhombus;perimeter=rhombusPerimeter;whiteSpace=wrap;html=1;fontSize=12;fillColor=#fff2cc;strokeColor=#d6b656;" value="符合总量&#xa;控制指标？" vertex="1">
          <mxGeometry height="80" width="230" x="655" y="385" as="geometry" />
        </mxCell>
        <mxCell id="Breject" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#f8cecc;strokeColor=#b85450;" value="不符合条件&#xa;退回本人" vertex="1">
          <mxGeometry height="50" width="220" x="1190" y="400" as="geometry" />
        </mxCell>
        <mxCell id="B1" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#fff2cc;strokeColor=#d6b656;" value="初审通过&#xa;提交审批" vertex="1">
          <mxGeometry height="50" width="220" x="930" y="515" as="geometry" />
        </mxCell>
        <mxCell id="B2" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#d5e8d4;strokeColor=#82b366;" value="资质归口管理部门&#xa;审批" vertex="1">
          <mxGeometry height="50" width="230" x="660" y="515" as="geometry" />
        </mxCell>
        <mxCell id="B3" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#ffe6cc;strokeColor=#d79b00;" value="主管领导&#xa;审批同意" vertex="1">
          <mxGeometry height="50" width="220" x="410" y="515" as="geometry" />
        </mxCell>
        <mxCell id="B4" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#fff2cc;strokeColor=#d6b656;" value="参加执业&#xa;资格考试" vertex="1">
          <mxGeometry height="50" width="200" x="1430" y="560" as="geometry" />
        </mxCell>
        <mxCell id="C0" parent="1" style="shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;fixedSize=1;fontSize=12;fillColor=#f8cecc;strokeColor=#b85450;" value="取得执业&#xa;资格证书" vertex="1">
          <mxGeometry height="50" width="200" x="1430" y="700" as="geometry" />
        </mxCell>
        <mxCell id="C1" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#fff2cc;strokeColor=#d6b656;" value="提出注册申请" vertex="1">
          <mxGeometry height="50" width="220" x="930" y="700" as="geometry" />
        </mxCell>
        <mxCell id="C2" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#d5e8d4;strokeColor=#82b366;" value="审批 核验劳动关系&#xa;及社保" vertex="1">
          <mxGeometry height="50" width="230" x="655" y="700" as="geometry" />
        </mxCell>
        <mxCell id="Cc" parent="1" style="rhombus;perimeter=rhombusPerimeter;whiteSpace=wrap;html=1;fontSize=12;fillColor=#fff2cc;strokeColor=#d6b656;" value="劳动关系/社保&#xa;符合要求？" vertex="1">
          <mxGeometry height="80" width="230" x="655" y="790" as="geometry" />
        </mxCell>
        <mxCell id="Creject" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#f8cecc;strokeColor=#b85450;" value="不予受理注册" vertex="1">
          <mxGeometry height="50" width="220" x="1190" y="760" as="geometry" />
        </mxCell>
        <mxCell id="C3" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#e1d5e7;strokeColor=#9673a6;" value="备案" vertex="1">
          <mxGeometry height="50" width="220" x="1190" y="900" as="geometry" />
        </mxCell>
        <mxCell id="C4" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#fff2cc;strokeColor=#d6b656;" value="办理注册手续&#xa;领取注册证书" vertex="1">
          <mxGeometry height="50" width="220" x="930" y="900" as="geometry" />
        </mxCell>
        <mxCell id="D1" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#fff2cc;strokeColor=#d6b656;" value="证书(电子签章)&#xa;由资质责任单位保管" vertex="1">
          <mxGeometry height="50" width="220" x="930" y="1120" as="geometry" />
        </mxCell>
        <mxCell id="D2" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#e1d5e7;strokeColor=#9673a6;" value="扫描件备案&#xa;(津贴发放依据)" vertex="1">
          <mxGeometry height="50" width="220" x="1190" y="1120" as="geometry" />
        </mxCell>
        <mxCell id="Dc" parent="1" style="rhombus;perimeter=rhombusPerimeter;whiteSpace=wrap;html=1;fontSize=12;fillColor=#fff2cc;strokeColor=#d6b656;" value="津贴计发&#xa;标准如何确定？" vertex="1">
          <mxGeometry height="80" width="230" x="655" y="1225" as="geometry" />
        </mxCell>
        <mxCell id="Drule" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#dae8fc;strokeColor=#6c8ebf;" value="多领域取最高不累加；&#xa;同类别按高级别不重复；&#xa;不同类别可累加" vertex="1">
          <mxGeometry height="70" width="220" x="930" y="1230" as="geometry" />
        </mxCell>
        <mxCell id="D3" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#e1d5e7;strokeColor=#9673a6;" value="按《津贴一览表》&#xa;发放岗位+资格津贴" vertex="1">
          <mxGeometry height="55" width="220" x="1190" y="1350" as="geometry" />
        </mxCell>
        <mxCell id="Ea0" parent="1" style="shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;fixedSize=1;fontSize=12;fillColor=#f8cecc;strokeColor=#b85450;" value="调出 提出&#xa;变更注册申请" vertex="1">
          <mxGeometry height="50" width="200" x="1430" y="1540" as="geometry" />
        </mxCell>
        <mxCell id="Ea1" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#fff2cc;strokeColor=#d6b656;" value="向资质责任&#xa;单位申请" vertex="1">
          <mxGeometry height="50" width="220" x="930" y="1540" as="geometry" />
        </mxCell>
        <mxCell id="Ea2" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#d5e8d4;strokeColor=#82b366;" value="审批" vertex="1">
          <mxGeometry height="50" width="230" x="660" y="1540" as="geometry" />
        </mxCell>
        <mxCell id="Ea3" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#e1d5e7;strokeColor=#9673a6;" value="备案" vertex="1">
          <mxGeometry height="50" width="220" x="1190" y="1540" as="geometry" />
        </mxCell>
        <mxCell id="Ea4" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#fff2cc;strokeColor=#d6b656;" value="办理变更注册" vertex="1">
          <mxGeometry height="50" width="220" x="930" y="1635" as="geometry" />
        </mxCell>
        <mxCell id="Eb1" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#fff2cc;strokeColor=#d6b656;" value="按规定&#xa;申报延续注册" vertex="1">
          <mxGeometry height="50" width="220" x="930" y="1725" as="geometry" />
        </mxCell>
        <mxCell id="Ebc" parent="1" style="rhombus;perimeter=rhombusPerimeter;whiteSpace=wrap;html=1;fontSize=12;fillColor=#fff2cc;strokeColor=#d6b656;" value="需继续&#xa;教育？" vertex="1">
          <mxGeometry height="80" width="230" x="660" y="1710" as="geometry" />
        </mxCell>
        <mxCell id="Eb2" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#e1d5e7;strokeColor=#9673a6;" value="组织继续教育&#xa;总工办协助" vertex="1">
          <mxGeometry height="55" width="220" x="1190" y="1735" as="geometry" />
        </mxCell>
        <mxCell id="Ebc2" parent="1" style="rhombus;perimeter=rhombusPerimeter;whiteSpace=wrap;html=1;fontSize=12;fillColor=#fff2cc;strokeColor=#d6b656;" value="因个人原因&#xa;证书失效？" vertex="1">
          <mxGeometry height="80" width="230" x="405" y="1840" as="geometry" />
        </mxCell>
        <mxCell id="Eb3" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#f8cecc;strokeColor=#b85450;" value="暂停发放津贴" vertex="1">
          <mxGeometry height="50" width="220" x="1190" y="1850" as="geometry" />
        </mxCell>
        <mxCell id="Ec1" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#fff2cc;strokeColor=#d6b656;" value="办理注销" vertex="1">
          <mxGeometry height="50" width="220" x="930" y="1950" as="geometry" />
        </mxCell>
        <mxCell id="Ec2a" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#d5e8d4;strokeColor=#82b366;" value="报总工办备案" vertex="1">
          <mxGeometry height="50" width="230" x="660" y="1950" as="geometry" />
        </mxCell>
        <mxCell id="Ec2b" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#e1d5e7;strokeColor=#9673a6;" value="报人力资源部备案" vertex="1">
          <mxGeometry height="50" width="220" x="1190" y="1950" as="geometry" />
        </mxCell>
        <mxCell id="Ed0" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#dae8fc;strokeColor=#6c8ebf;" value="院研究批准&#xa;动态调整" vertex="1">
          <mxGeometry height="60" width="220" x="170" y="2050" as="geometry" />
        </mxCell>
        <mxCell id="Ed1" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fontSize=12;fillColor=#fff2cc;strokeColor=#d6b656;" value="报考/注册/津贴&#xa;按总量控制 先到先得" vertex="1">
          <mxGeometry height="55" width="220" x="930" y="2052.5" as="geometry" />
        </mxCell>
        <mxCell id="END" parent="1" style="shape=mxgraph.flowchart.terminator;whiteSpace=wrap;html=1;fontSize=13;fontStyle=1;fillColor=#ffe6cc;strokeColor=#d79b00;" value="制度正式执行&#xa;(2026年10月1日起)" vertex="1">
          <mxGeometry height="55" width="240" x="640" y="2160" as="geometry" />
        </mxCell>
        <mxCell id="e_A0A1" edge="1" parent="1" source="A0" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="A1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="280" y="260" />
              <mxPoint x="1040" y="260" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="e_A1A2" edge="1" parent="1" source="A1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="A2">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_A2A3" edge="1" parent="1" source="A2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="A3">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_A3A4" edge="1" parent="1" source="A3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="A4">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="520" y="140" />
              <mxPoint x="1300" y="140" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="e_B0Bc" edge="1" parent="1" source="B0" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Bc">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1530" y="360" />
              <mxPoint x="770" y="360" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="e_BcReject" edge="1" parent="1" source="Bc" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Breject" value="否">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1050" y="425" />
              <mxPoint x="1050" y="425" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="e_BcB1" edge="1" parent="1" source="Bc" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="B1" value="是">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="770" y="480" />
              <mxPoint x="990" y="480" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="e_B1B2" edge="1" parent="1" source="B1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="B2">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_B2B3" edge="1" parent="1" source="B2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="B3">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_B3B4" edge="1" parent="1" source="B3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="B4">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="520" y="580" />
              <mxPoint x="1530" y="580" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="e_B4C0" edge="1" parent="1" source="B4" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="C0">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_C0C1" edge="1" parent="1" source="C0" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="C1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_C1C2" edge="1" parent="1" source="C1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="C2">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_C2Cc" edge="1" parent="1" source="C2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Cc">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_CcCreject" edge="1" parent="1" source="Cc" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Creject" value="否">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_CcC3" edge="1" parent="1" source="Cc" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="C3" value="是">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_C3C4" edge="1" parent="1" source="C3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="C4">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_D1D2" edge="1" parent="1" source="D1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="D2">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_D2D3" edge="1" parent="1" source="D2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="D3">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_D1Dc" edge="1" parent="1" source="D1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Dc">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_DcDrule" edge="1" parent="1" source="Dc" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Drule">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_DruleD3" edge="1" parent="1" source="Drule" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="D3">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_D3Ea0" edge="1" parent="1" source="D3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Ea0">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_Ea0Ea1" edge="1" parent="1" source="Ea0" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Ea1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1480" y="1510" />
              <mxPoint x="1040" y="1510" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="e_Ea1Ea2" edge="1" parent="1" source="Ea1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Ea2">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_Ea2Ea3" edge="1" parent="1" source="Ea2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Ea3">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="775" y="1500" />
              <mxPoint x="1300" y="1500" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="e_Ea3Ea4" edge="1" parent="1" source="Ea3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Ea4">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1300" y="1610" />
              <mxPoint x="1040" y="1610" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="e_Ea4Eb1" edge="1" parent="1" source="Ea4" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Eb1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_Eb1Ebc" edge="1" parent="1" source="Eb1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Ebc">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_EbcEb2" edge="1" parent="1" source="Ebc" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Eb2" value="是">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1300" y="1800" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="e_EbcEbc2" edge="1" parent="1" source="Ebc" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Ebc2" value="否">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_Eb2Ebc2" edge="1" parent="1" source="Eb2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Ebc2">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1300" y="1820" />
              <mxPoint x="520" y="1820" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="e_Ebc2Eb3" edge="1" parent="1" source="Ebc2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Eb3" value="是">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1050" y="1880" />
              <mxPoint x="1050" y="1880" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="e_Ebc2Ec1" edge="1" parent="1" source="Ebc2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Ec1" value="否">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="520" y="1930" />
              <mxPoint x="1040" y="1930" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="e_Eb3Ec1" edge="1" parent="1" source="Eb3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Ec1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1300" y="1930" />
              <mxPoint x="1040" y="1930" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="e_Ec1Ec2a" edge="1" parent="1" source="Ec1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Ec2a">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_Ec1Ec2b" edge="1" parent="1" source="Ec1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Ec2b">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_Ec2aEd0" edge="1" parent="1" source="Ec2a" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Ed0">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_Ec2bEd0" edge="1" parent="1" source="Ec2b" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Ed0">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1300" y="2030" />
              <mxPoint x="280" y="2030" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="e_Ed0Ed1" edge="1" parent="1" source="Ed0" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="Ed1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_Ed1END" edge="1" parent="1" source="Ed1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;html=1;fontSize=11;strokeColor=#333333;" target="END">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1040" y="2130" />
              <mxPoint x="760" y="2130" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="v1" edge="1" parent="1" style="endArrow=none;html=1;strokeColor=#666666;">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="160" y="110" as="sourcePoint" />
            <mxPoint x="160" y="2230" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="v2" edge="1" parent="1" style="endArrow=none;html=1;strokeColor=#666666;">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="400" y="110" as="sourcePoint" />
            <mxPoint x="400" y="2230" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="v3" edge="1" parent="1" style="endArrow=none;html=1;strokeColor=#666666;">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="640" y="110" as="sourcePoint" />
            <mxPoint x="640" y="2230" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="v4" edge="1" parent="1" style="endArrow=none;html=1;strokeColor=#666666;">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="900" y="110" as="sourcePoint" />
            <mxPoint x="900" y="2230" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="v5" edge="1" parent="1" style="endArrow=none;html=1;strokeColor=#666666;">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1180" y="110" as="sourcePoint" />
            <mxPoint x="1180" y="2230" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="v6" edge="1" parent="1" style="endArrow=none;html=1;strokeColor=#666666;">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1420" y="110" as="sourcePoint" />
            <mxPoint x="1420" y="2230" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="v7" edge="1" parent="1" style="endArrow=none;html=1;strokeColor=#666666;">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1640" y="110" as="sourcePoint" />
            <mxPoint x="1640" y="2230" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="hsep1" edge="1" parent="1" style="endArrow=none;html=1;strokeColor=#666666;">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="100" y="340" as="sourcePoint" />
            <mxPoint x="1640" y="340" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="hsep2" edge="1" parent="1" style="endArrow=none;html=1;strokeColor=#666666;">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="100" y="640" as="sourcePoint" />
            <mxPoint x="1640" y="640" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="hsep3" edge="1" parent="1" style="endArrow=none;html=1;strokeColor=#666666;">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="100" y="1050" as="sourcePoint" />
            <mxPoint x="1640" y="1050" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="hsep4" edge="1" parent="1" style="endArrow=none;html=1;strokeColor=#666666;">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="100" y="1480" as="sourcePoint" />
            <mxPoint x="1640" y="1480" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="hsep5" edge="1" parent="1" style="endArrow=none;html=1;strokeColor=#666666;">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="100" y="2230" as="sourcePoint" />
            <mxPoint x="1640" y="2230" as="targetPoint" />
          </mxGeometry>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### 该示例的结构拆解

**列（角色，6 个）**

| 列 | 角色 | 左边界 | 列宽 | 节点横向占位 |
|----|------|--------|------|--------------|
| 1 | 决策机构（院会议） | 160 | 240 | 170~390 |
| 2 | 分管领导 | 400 | 240 | 410~630 |
| 3 | 总工办（归口管理） | 640 | 260 | 655~890 |
| 4 | 资质责任单位 | 900 | 280 | 930~1150 |
| 5 | 人力资源部 | 1180 | 240 | 1190~1410 |
| 6 | 员工 | 1420 | 220 | 1430~1630 |

**行（阶段，5 个）**

| 行 | 阶段 | 上边界 | 行高 |
|----|------|--------|------|
| 1 | 资质规划与总量控制 | 50 | 290 |
| 2 | 执业资格考试报考审批 | 340 | 300 |
| 3 | 执业资格注册管理 | 640 | 410 |
| 4 | 证书保管与津贴管理 | 1050 | 430 |
| 5 | 变更/延续/注销与动态调整 | 1480 | 750 |

**节点（34 个）**

| 语义类型 | 示例节点 |
|----------|----------|
| 决策/规划/规则 | 研究院资质总体规划、多领域取最高不累加…、院研究批准动态调整 |
| 申请/办理/执行 | 提出控制指标、初审通过提交审批、参加执业资格考试、办理注销 |
| 归口审核/核验 | 征求相关部门意见审核审批、审批核验劳动关系及社保、报总工办备案 |
| 领导审批 | 主管领导审批同意 |
| 备案/归档 | 备案、扫描件备案、报人力资源部备案 |
| 输入/触发 | 申报执业资格考试、取得执业资格证书、调出提出变更注册申请 |
| 驳回/异常 | 不符合条件退回本人、不予受理注册、暂停发放津贴 |
| 判断 | 符合总量控制指标？、劳动关系/社保符合要求？、津贴计发标准如何确定？、需继续教育？、因个人原因证书失效？ |
| 终点 | 制度正式执行（2026年10月1日起） |

---

## 八、输出要求

- 只输出 XML 代码，以 `<mxfile>` 开头，`</mxfile>` 结尾，可以直接保存为 `.drawio` 文件使用。
- 除非用户特别要求，一律写**中文**（角色名、阶段名、节点名、判断条件、是/否标签）。
- 除非用户特别要求，**不得改变样式**：字号（标题 24 / 列头行头 22 / 节点 12 / 边 11）、直角 `rounded=0`（节点除外，节点为 `rounded=1`）、配色表、形状规则都要照抄示例。

### 生成后自检清单

- [ ] 列头横向紧密拼接，无空隙、无重叠，且覆盖 `X0+W_ROW` 到 `X1`
- [ ] 行头纵向紧密拼接，且从 `Y_HEAD` 一直排到画布底部
- [ ] 网格线数量正确：竖线 = 列数 + 1，横线 = 行数 + 1
- [ ] 每个节点都完整落在某一格内，**不跨列、不压线**（左右各留 ≥10px）
- [ ] 节点文字没有溢出方框（溢出就把框加高/加宽）
- [ ] 每个判断菱形都有"是/否"两条出边
- [ ] 连线尽量不交叉、不穿越无关节点
- [ ] 文本换行统一用 `&#xa;`，未使用裸 `<br>`
- [ ] 所有 ID 唯一，所有 `source`/`target` 引用的节点都存在
- [ ] 网格线的 `<mxGeometry>` 用了 `sourcePoint`/`targetPoint`，未设 `source`/`target` 属性
