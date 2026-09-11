# 技术路线图生成提示词

## 任务说明

根据用户描述的研究方案 / 技术路线，生成一个符合 draw.io 格式的**技术路线图** XML 文件。

一会可能会发给你一些研究方案描述（可能是开题报告、项目申请书、论文的技术路线章节，也可能是其他格式），你需要从中提取出：

- **总题目**（找不到就根据内容自拟）
- **研究阶段（3~6 个）**：每一步要做什么，一句话概括成阶段标题
- **每个阶段的研究步骤名**：写在左列，短、竖排（4~6 字一行）
- **每个阶段使用的研究方法**：写在右列，短、竖排
- **每个阶段的拆解内容**：3~5 个并列的研究内容卡片
- **每个阶段的产出 / 小结**：一句话，写在阶段底部的汇总条

然后生成一个符合 draw.io 格式的技术路线图 XML 文件。

---

## 一、整体骨架

技术路线图是**自上而下的三段式纵向结构**：

```
      ┌─────────┐  ┌──────────── 总题目（蓝色深底白字）────────────┐  ┌─────────┐
      │ 研究步骤│  │                                                │  │ 研究方法│
      └────┬────┘  └────────────────────────────────────────────────┘  └────┬────┘
           │                                                                │
   ┌───────┴──┐  ┌────────────────────────────────────────────────────┐  ┌──┴───────┐
   │          │  │  ┌──────── 阶段 1 标题条（主题深色底）──────────┐  │  │          │
   │  步骤 1  │  │  ├──────────────────────────────────────────────┤  │  │  方法 1  │
   │          │  │  │  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐         │  │  │          │
   └───────┬──┘  │  │  │卡片│ │卡片│ │卡片│ │卡片│ │卡片│         │  │  └──┬───────┘
           │     │  │  └────┘ └────┘ └────┘ └────┘ └────┘         │  │     │
           ▼     │  │  ┌──────── 汇总条（浅色斜体）────────────┐   │  │     ▼
   ┌───────┴──┐  │  └────────────────────────────────────────────────┘  │  ┌──┴───────┐
   │  步骤 2  │  └───────────────────────┬───────────────────────────────┘  │  方法 2  │
   │          │                       ▼ flexArrow                          │          │
   └──────────┘  ┌────────────────────────────────────────────────────┐   └──────────┘
                 │              阶段 2 …                               │
                 └────────────────────────────────────────────────────┘
```

### 画布参数（推荐基准值，可按阶段数缩放）

| 参数 | 值 | 说明 |
|------|-----|------|
| `X_STEP` | 110 | 左侧"研究步骤"列左边缘 |
| `W_STEP` | 90 | 步骤列宽度（占 x: 110~200） |
| `X_OUT` | 220 | 阶段外框左边缘（= 步骤列右侧 + 20） |
| `W_OUT` | 1160 | 阶段外框宽度（占 x: 220~1380） |
| `X_MTD` | 1397 | 右侧"研究方法"列左边缘（= 外框右侧 + 17~20） |
| `W_MTD` | 90 | 方法列宽度 |
| `CX` | 800 | 画布水平中心轴（= `X_OUT + W_OUT/2`），所有跨阶段箭头都走这条轴 |
| `PAD` | 20 | 外框内边距 |
| 内容区 | x: 240~1360，宽 1120 | 外框内缩 20px |
| 卡片区 | x: 250~1350，宽 1100 | 内容区再内缩 10px |
| `GAP` | 60 | 相邻两个外框之间的垂直间距 |

对应 `<mxGraphModel>` 建议：`pageWidth="1700"`，`pageHeight` = 图总高 + 200。

---

## 二、图元素类型

### 1. 顶部总标题条

```xml
<mxCell id="title_bar" parent="1"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#0050ef;strokeColor=#001DBC;fontSize=22;fontStyle=1;align=center;verticalAlign=middle;fontColor=#ffffff;"
        value="多组学解析田菁干草替代苜蓿调控育肥羔羊瘤胃微生态与羊肉风味形成的潜在分子机制" vertex="1">
  <mxGeometry height="50" width="1080" x="260" y="20" as="geometry" />
</mxCell>
```

- `y = 20`，`height = 50`，水平居中于 `CX`
- `fillColor=#0050ef` / `strokeColor=#001DBC` / `fontColor=#ffffff`（蓝底白字）
- `fontSize=22`、`fontStyle=1`（加粗）

### 2. 左上"研究步骤" / 右上"研究方法"表头

```xml
<mxCell id="head_step" parent="1"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#0050ef;strokeColor=#001DBC;fontSize=18;fontStyle=1;align=center;verticalAlign=middle;fontColor=#ffffff;"
        value="研究步骤" vertex="1">
  <mxGeometry height="50" width="150" x="80" y="20" as="geometry" />
</mxCell>
```

```xml
<mxCell id="head_method" parent="1"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#0050ef;strokeColor=#001DBC;fontSize=18;fontStyle=1;align=center;verticalAlign=middle;fontColor=#ffffff;"
        value="研究方法" vertex="1">
  <mxGeometry height="50" width="150" x="1367" y="20" as="geometry" />
</mxCell>
```

- `y = 20`，`height = 50`，`width = 150`，`fontSize=18`
- 位置：标题条左右各留 30px 间隙后放置，整体以 `CX` 为中心对称
- 列宽不足时，表头文字可换成"步骤"/"方法"，但**左右两个表头必须字数一致**

### 3. 左侧步骤列 / 右侧方法列

每阶段各一个矩形，**竖排短文本**（每行 4~6 字，用 `&#xa;` 换行），上下紧密相接：

```xml
<mxCell id="r1_step" parent="1"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;"
        value="立论依据&#xa;与&#xa;研究现状综述" vertex="1">
  <mxGeometry height="270" width="90" x="110" y="90" as="geometry" />
</mxCell>
```

```xml
<mxCell id="r1_method" parent="1"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;"
        value="文献研究法&#xa;归纳总结法" vertex="1">
  <mxGeometry height="270" width="90" x="1397" y="90" as="geometry" />
</mxCell>
```

- `width = 90`，`x = 110`（步骤列）/ `1397`（方法列）
- `y` 与 `height` **必须与对应阶段的外框完全一致**
- `fontSize=16`、`fontStyle=1`（加粗）、居中
- 配色用该阶段的**浅色填充 + 深色描边**（见第三节配色表）

### 4. 阶段外框（白色容器）

一个**无文字**的白色黑框矩形，把该阶段所有内容框起来：

```xml
<mxCell id="r1_outer" parent="1"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontSize=16;"
        value="" vertex="1">
  <mxGeometry height="270" width="1160" x="220" y="90" as="geometry" />
</mxCell>
```

- `value=""`（必须留空），`fillColor=#ffffff`，`strokeColor=#000000`
- **必须画在内部内容之前**（XML 中位置靠前），否则会盖住内容

### 5. 阶段标题条（主题深色底）

```xml
<mxCell id="r1_title" parent="1"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#0050ef;strokeColor=#001DBC;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;fontColor=#ffffff;"
        value="田菁干草替代苜蓿调控育肥羔羊瘤胃微生态与羊肉风味形成的研究背景与立论依据" vertex="1">
  <mxGeometry height="40" width="1120" x="240" y="110" as="geometry" />
</mxCell>
```

- `x = X_OUT + 20`（240），`width = W_OUT − 40`（1120），`height = 40`
- `y = 外框 y + 20`
- 配色 = 该阶段的**标题条深色 + 描边 + fontColor**（见配色表）

### 6. 内容卡片（三种排布，按需选用）

#### 类型 A：并列小卡（内容少，一行或两行）

```xml
<mxCell id="r1_a1" parent="1"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=16;align=center;verticalAlign=middle;"
        value="田菁的生物学特性&#xa;与利用潜力" vertex="1">
  <mxGeometry height="50" width="220" x="250" y="170" as="geometry" />
</mxCell>
```

#### 类型 B：带小标题的内容框（内容多，需要列举要点）

标题条用**该阶段的深色**，内容框用**该阶段的浅色**，两者上下紧贴：

```xml
<!-- 小标题条 -->
<mxCell id="r2_sub1_t" parent="1"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=#005700;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;fontColor=#ffffff;"
        value="体外产气试验" vertex="1">
  <mxGeometry height="30" width="350" x="251.5" y="510" as="geometry" />
</mxCell>

<!-- 内容框（左对齐，左右各留 10px） -->
<mxCell id="r2_sub1_c" parent="1"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=16;align=left;verticalAlign=middle;spacingLeft=10;spacingRight=10;"
        value="5只瘘管羊（多浪羯羊）采集瘤胃液，39℃厌氧培养72 h&#xa;· 0/2/4/8/12/24/48/72 h 动态产气量 → Ørskov模型 GPt = a + b×(1-e^(-ct))&#xa;· 发酵液 pH 值、NH3-N 浓度（冯宗慈法）、菌体蛋白 MCP" vertex="1">
  <mxGeometry height="120" width="350" x="251.5" y="540" as="geometry" />
</mxCell>
```

- 小标题条 `height = 30`，内容框 `y = 小标题条 y + 30`（紧贴）
- 内容框 `align=left;verticalAlign=middle;spacingLeft=10;spacingRight=10`
- 要点用 `· ` 开头，换行用 `&#xa;`

#### 类型 C：双层分组（一个阶段内有两大块）

在阶段标题下再放一条深色分组条，然后放卡片行；第二组同理：

```xml
<mxCell id="r4_top_bar" parent="1"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#6a00ff;strokeColor=#3700CC;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;fontColor=#ffffff;"
        value="瘤胃微生态解析（第 60 d 育肥羔羊屠宰采样）" vertex="1">
  <mxGeometry height="30" width="1120" x="241.5" y="1290" as="geometry" />
</mxCell>
```

### 7. 阶段汇总条（浅色斜体）

放在外框底部内缩 20px，一句话总结该阶段的产出：

```xml
<mxCell id="r1_sum" parent="1"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=16;fontStyle=2;align=center;verticalAlign=middle;"
        value="目的：明确田菁作为育肥羔羊粗饲料的替代潜力与活性成分功能，提出科学假设——田菁替代苜蓿通过调控瘤胃微生态影响羊肉风味形成" vertex="1">
  <mxGeometry height="35" width="1120" x="240" y="305" as="geometry" />
</mxCell>
```

- `fontStyle=2`（斜体），`height = 35~50`（按文字长度定）
- `y = 外框 y + 外框高 − 20 − H_sum`
- 文字前缀用 `产出：` / `目的：` / `总结：` 开头，读起来更顺

---

## 三、配色主题（按阶段循环）

**每个阶段一套颜色**：标题条用深色（配白字），内容卡与左右侧列用浅色。

| 阶段 | 标题条 fill | 标题条 stroke | fontColor | 内容/侧列 fill | 内容/侧列 stroke |
|------|-------------|---------------|-----------|----------------|------------------|
| 1 | `#0050ef` | `#001DBC` | `#ffffff` | `#dae8fc` | `#6c8ebf` |
| 2 | `#008a00` | `#005700` | `#ffffff` | `#d5e8d4` | `#82b366` |
| 3 | `#f0a30a` | `#BD7000` | `#000000` | `#fff2cc` | `#d6b656` |
| 4 | `#6a00ff` | `#3700CC` | `#ffffff` | `#e1d5e7` | `#9673a6` |
| 5 | `#d80073` | `#A50040` | `#ffffff` | `#f8cecc` | `#b85450` |
| 6+ | 从第 1 行开始循环 | | | | |

**重要例外**：阶段 3 的 `#f0a30a` 是橙黄色，**必须用黑字 `fontColor=#000000`**，其余阶段一律白字。

顶部总标题条与左上/右上表头统一使用**阶段 1 的蓝色** `#0050ef` / `#001DBC` / 白字。

> 全部 `rounded=0`（直角），禁止圆角、禁止渐变、禁止阴影。

---

## 四、边与箭头

### 1. 顶部表头连接

```xml
<!-- 总标题条 → 左表头（从右边缘接入） -->
<mxCell id="e_h1" edge="1" parent="1" source="title_bar"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=1;entryY=0.5;entryDx=0;entryDy=0;"
        target="head_step">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- 总标题条 → 右表头（从左边缘接入） -->
<mxCell id="e_h2" edge="1" parent="1" source="title_bar"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"
        target="head_method">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- 左表头 → 第 1 阶段步骤列 -->
<mxCell id="e_h3" edge="1" parent="1" source="head_step" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" target="r1_step">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- 右表头 → 第 1 阶段方法列 -->
<mxCell id="e_h4" edge="1" parent="1" source="head_method" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" target="r1_method">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### 2. 步骤列 / 方法列的纵向串联

```xml
<mxCell id="e_s12" edge="1" parent="1" source="r1_step"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
        target="r2_step">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

- `entryX=0.5;entryY=0` 表示从上边缘正中接入
- 方法列同理：`r1_method → r2_method → r3_method → …`

### 3. 阶段之间的粗箭头（flexArrow）

放在 `CX` 轴上，从上一个外框底边指到下一个外框顶边：

```xml
<mxCell id="arw12" edge="1" parent="1"
        style="shape=flexArrow;endArrow=classic;html=1;rounded=0;endWidth=43.30578512396694;endSize=11.67878787878788;width=41.21212121212121;fillColor=#d5e8d4;strokeColor=#82b366;">
  <mxGeometry height="50" relative="1" width="50" as="geometry">
    <mxPoint x="805.39" y="360" as="sourcePoint" />
    <mxPoint x="805.39" y="420" as="targetPoint" />
  </mxGeometry>
</mxCell>
```

- `x` 恒为 `CX`（800 左右，允许 ±6 的微调）
- `sourcePoint.y = 上一个外框底边`，`targetPoint.y = 下一个外框顶边`（长度 = `GAP` = 50~60）
- `fillColor` 用**下一个阶段**的浅色，`strokeColor` 用下一个阶段的深色（表示"流向下一阶段"）
- `endWidth` / `endSize` / `width` 三个参数**原样照抄**，不要改

### 4. 阶段标题 → 内容卡（可选装饰连线）

用于强化"标题统领下面几张卡"的层次感，不是必须：

```xml
<mxCell id="e_t_a1" edge="1" parent="1" source="r1_title"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
        target="r1_a1">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="800" y="160" />
      <mxPoint x="360" y="160" />
    </Array>
  </mxGeometry>
</mxCell>
```

- 折线走法：标题条底边中点 `(CX, y0)` → 水平走到卡片中心 x → 垂直进入卡片顶边
- `y0` 取"标题条底边 + 10"，且**不能压到卡片**

---

## 五、布局算法（照此顺序推导坐标）

### 步骤 1：算卡片宽度

卡片区宽 `W_CARD = 1100`（x: 250~1350），卡片间距 `10`：

```
每张卡片宽 w = (1100 − 10 × (n − 1)) / n
第 k 张卡片 x = 250 + k × (w + 10)      （k 从 0 开始）
```

| 卡片数 n | 每张宽度 |
|---------|---------|
| 3 | 360 |
| 4 | 267（取整 270） |
| 5 | 212（可按内容微调成 220/220/220/220/180） |

### 步骤 2：算每个外框的高度

```
H_outer = 20                         ← 外框顶 → 阶段标题条
        + 40                         ← 阶段标题条高
        + 20                         ← 阶段标题条 → 内容区顶
        + Σ(各内容层高) + Σ(层间距 10~20)
        + 15~20                      ← 内容区底 → 汇总条
        + H_sum (35~50)              ← 汇总条高
        + 20                         ← 汇总条 → 外框底
```

参考值（来自标准示例）：

| 阶段 | 内容结构 | 内容层高 | H_sum | H_outer |
|------|----------|----------|-------|---------|
| 1 | 两行并列小卡 | 50 + 20 + 50 | 35 | 270 |
| 2 | 3 组（小标题 30 + 内容 120） | 150 | 50 | 320 |
| 3 | 4 组（小标题 30 + 内容 160） | 190 | 50 | 360 |
| 4 | 双层：条 30 + 卡 90 + 条 30 + 卡 110 | 300 | 40 | 450 |
| 5 | 一行四卡 | 90 | 45 | 260 |

### 步骤 3：纵向排布

```
r1_outer.y = 90                                  ← 顶部表头 y(20) + h(50) + 20
rN_outer.y = r(N-1)_outer.y + r(N-1)_outer.H + GAP     （GAP = 60）
步骤列/方法列的 y、height 与对应外框完全相同
```

### 步骤 4：画箭头

在每两个外框之间，于 `CX` 轴上画一条 flexArrow。

---

## 六、绘制顺序（影响图层叠放，务必遵守）

1. `id="0"` / `id="1"` 结构元素
2. 顶部表头三条（总标题条、研究步骤、研究方法）及其连线
3. **逐阶段循环**：
   1. 步骤列 `rN_step`、方法列 `rN_method`
   2. 外框 `rN_outer` ← **必须早于内部内容**
   3. 阶段标题条 `rN_title`
   4. 内容卡片 / 分组条 / 内容框
   5. 汇总条 `rN_sum`
4. 步骤列串联边、方法列串联边
5. 阶段标题 → 卡片的装饰连线
6. **阶段间 flexArrow（最后画）**，保证箭头压在最上层

---

## 七、完整示例结构

以下是标准技术路线图（5 阶段）的完整 XML，可直接保存为 `.drawio` 文件使用，**样式必须完全照抄**：

```xml
<mxfile host="Electron" agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) draw.io/29.6.6 Chrome/144.0.7559.236 Electron/40.8.4 Safari/537.36" version="29.6.6">
  <diagram id="route_map" name="田菁干草替代苜蓿技术路线图">
    <mxGraphModel dx="2696" dy="1840" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1700" pageHeight="2200" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="title_bar" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#0050ef;strokeColor=#001DBC;fontSize=22;fontStyle=1;align=center;verticalAlign=middle;fontColor=#ffffff;" value="多组学解析田菁干草替代苜蓿调控育肥羔羊瘤胃微生态与羊肉风味形成的潜在分子机制" vertex="1">
          <mxGeometry height="50" width="1080" x="260" y="20" as="geometry" />
        </mxCell>
        <mxCell id="head_step" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#0050ef;strokeColor=#001DBC;fontSize=18;fontStyle=1;align=center;verticalAlign=middle;fontColor=#ffffff;" value="研究步骤" vertex="1">
          <mxGeometry height="50" width="150" x="80" y="20" as="geometry" />
        </mxCell>
        <mxCell id="head_method" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#0050ef;strokeColor=#001DBC;fontSize=18;fontStyle=1;align=center;verticalAlign=middle;fontColor=#ffffff;" value="研究方法" vertex="1">
          <mxGeometry height="50" width="150" x="1367" y="20" as="geometry" />
        </mxCell>
        <mxCell id="e_h1" edge="1" parent="1" source="title_bar" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" target="head_step">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_h2" edge="1" parent="1" source="title_bar" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" target="head_method">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_h3" edge="1" parent="1" source="head_step" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" target="r1_step">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_h4" edge="1" parent="1" source="head_method" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" target="r1_method">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- ============ 阶段 1 ============ -->
        <mxCell id="r1_step" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;" value="立论依据&#xa;与&#xa;研究现状综述" vertex="1">
          <mxGeometry height="270" width="90" x="110" y="90" as="geometry" />
        </mxCell>
        <mxCell id="r1_method" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;" value="文献研究法&#xa;归纳总结法" vertex="1">
          <mxGeometry height="270" width="90" x="1397" y="90" as="geometry" />
        </mxCell>
        <mxCell id="r1_outer" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontSize=16;" value="" vertex="1">
          <mxGeometry height="270" width="1160" x="220" y="90" as="geometry" />
        </mxCell>
        <mxCell id="r1_title" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#0050ef;strokeColor=#001DBC;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;fontColor=#ffffff;" value="田菁干草替代苜蓿调控育肥羔羊瘤胃微生态与羊肉风味形成的研究背景与立论依据" vertex="1">
          <mxGeometry height="40" width="1120" x="240" y="110" as="geometry" />
        </mxCell>
        <mxCell id="r1_a1" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=16;align=center;verticalAlign=middle;" value="田菁的生物学特性&#xa;与利用潜力" vertex="1">
          <mxGeometry height="50" width="220" x="250" y="170" as="geometry" />
        </mxCell>
        <mxCell id="r1_a2" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=16;align=center;verticalAlign=middle;" value="田菁在动物营养中的&#xa;应用（单胃/反刍动物）" vertex="1">
          <mxGeometry height="50" width="220" x="480" y="170" as="geometry" />
        </mxCell>
        <mxCell id="r1_a3" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=16;align=center;verticalAlign=middle;" value="澳湖杂交羊研究现状&#xa;与杂种优势" vertex="1">
          <mxGeometry height="50" width="220" x="710" y="170" as="geometry" />
        </mxCell>
        <mxCell id="r1_a4" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=16;align=center;verticalAlign=middle;" value="育肥羔羊瘤胃发育&#xa;与微生态特征" vertex="1">
          <mxGeometry height="50" width="220" x="940" y="170" as="geometry" />
        </mxCell>
        <mxCell id="r1_a5" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=16;align=center;verticalAlign=middle;" value="肉质理化性质与&#xa;风味研究进展" vertex="1">
          <mxGeometry height="50" width="180" x="1170" y="170" as="geometry" />
        </mxCell>
        <mxCell id="r1_b1" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=16;align=center;verticalAlign=middle;" value="微生物组学（16S rDNA/宏基因组）" vertex="1">
          <mxGeometry height="50" width="220" x="250" y="240" as="geometry" />
        </mxCell>
        <mxCell id="r1_b2" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=16;align=center;verticalAlign=middle;" value="代谢组学（靶向/非靶向/脂质）" vertex="1">
          <mxGeometry height="50" width="220" x="480" y="240" as="geometry" />
        </mxCell>
        <mxCell id="r1_b3" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=16;align=center;verticalAlign=middle;" value="挥发性风味物质与&#xa;风味前体物质研究" vertex="1">
          <mxGeometry height="50" width="220" x="710" y="240" as="geometry" />
        </mxCell>
        <mxCell id="r1_b4" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=16;align=center;verticalAlign=middle;" value="田菁活性成分&#xa;（黄酮、皂苷、多糖）" vertex="1">
          <mxGeometry height="50" width="220" x="940" y="240" as="geometry" />
        </mxCell>
        <mxCell id="r1_b5" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=16;align=center;verticalAlign=middle;" value="饲料资源短缺与&#xa;盐碱地改良需求" vertex="1">
          <mxGeometry height="50" width="180" x="1170" y="240" as="geometry" />
        </mxCell>
        <mxCell id="r1_sum" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=16;fontStyle=2;align=center;verticalAlign=middle;" value="目的：明确田菁作为育肥羔羊粗饲料的替代潜力与活性成分功能，提出科学假设——田菁替代苜蓿通过调控瘤胃微生态影响羊肉风味形成" vertex="1">
          <mxGeometry height="35" width="1120" x="240" y="305" as="geometry" />
        </mxCell>
        <mxCell id="arw12" edge="1" parent="1" style="shape=flexArrow;endArrow=classic;html=1;rounded=0;endWidth=43.30578512396694;endSize=11.67878787878788;width=41.21212121212121;fillColor=#d5e8d4;strokeColor=#82b366;">
          <mxGeometry height="50" relative="1" width="50" as="geometry">
            <mxPoint x="805.39" y="360" as="sourcePoint" />
            <mxPoint x="805.39" y="420" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- ============ 阶段 2 ============ -->
        <mxCell id="r2_step" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;" value="体外发酵参数&#xa;与&#xa;营养物质降解率" vertex="1">
          <mxGeometry height="320" width="90" x="111.5" y="420" as="geometry" />
        </mxCell>
        <mxCell id="r2_method" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;" value="体外产气法&#xa;尼龙袋法&#xa;概略养分分析法" vertex="1">
          <mxGeometry height="320" width="90" x="1398.5" y="420" as="geometry" />
        </mxCell>
        <mxCell id="r2_outer" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontSize=16;" value="" vertex="1">
          <mxGeometry height="320" width="1160" x="221.5" y="420" as="geometry" />
        </mxCell>
        <mxCell id="r2_title" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=#005700;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;fontColor=#ffffff;" value="田菁替换苜蓿对体外瘤胃发酵参数和营养物质降解率的影响（含0%、25%、50%、75%、100%田菁替代比例）" vertex="1">
          <mxGeometry height="40" width="1120" x="241.5" y="440" as="geometry" />
        </mxCell>
        <mxCell id="r2_sub1_t" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=#005700;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;fontColor=#ffffff;" value="体外产气试验" vertex="1">
          <mxGeometry height="30" width="350" x="251.5" y="510" as="geometry" />
        </mxCell>
        <mxCell id="r2_sub1_c" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=16;align=left;verticalAlign=middle;spacingLeft=10;spacingRight=10;" value="5只瘘管羊（多浪羯羊）采集瘤胃液，39℃厌氧培养72 h&#xa;· 0/2/4/8/12/24/48/72 h 动态产气量 → Ørskov模型 GPt = a + b×(1-e^(-ct))&#xa;· 发酵液 pH 值、NH3-N 浓度（冯宗慈法）、菌体蛋白 MCP" vertex="1">
          <mxGeometry height="120" width="350" x="251.5" y="540" as="geometry" />
        </mxCell>
        <mxCell id="r2_sub2_t" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=#005700;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;fontColor=#ffffff;" value="尼龙袋降解试验" vertex="1">
          <mxGeometry height="30" width="350" x="611.5" y="510" as="geometry" />
        </mxCell>
        <mxCell id="r2_sub2_c" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=16;align=left;verticalAlign=middle;spacingLeft=10;spacingRight=10;" value="分批放入尼龙袋（2/4/8/12/24/48/72 h），65℃烘干48 h 称重&#xa;· 干物质及养分降解率 A = 100×(B-C)/B&#xa;· 降解参数 dp = a + b×(1-e^(-ct))&#xa;· 有效降解率 ED = a + b×c/(k+c)，k=0.0666/h" vertex="1">
          <mxGeometry height="120" width="350" x="611.5" y="540" as="geometry" />
        </mxCell>
        <mxCell id="r2_sub3_t" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#008a00;strokeColor=#005700;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;fontColor=#ffffff;" value="试验分组设计" vertex="1">
          <mxGeometry height="30" width="380" x="971.5" y="510" as="geometry" />
        </mxCell>
        <mxCell id="r2_sub3_c" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=16;align=left;verticalAlign=middle;spacingLeft=10;spacingRight=10;" value="· 5组：0% / 25% / 50% / 75% / 100% 田菁替代苜蓿&#xa;· 等能等氮原则配制，每组 5 个重复&#xa;· 瘤胃液与培养液按 1:2 混合&#xa;· 39℃恒温摇床避光培养，冰水终止反应" vertex="1">
          <mxGeometry height="120" width="380" x="971.5" y="540" as="geometry" />
        </mxCell>
        <mxCell id="r2_sum" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=16;fontStyle=2;align=center;verticalAlign=middle;" value="产出：5组日粮 72 h 动态产气曲线与产气参数（a、b、c）、pH、NH3-N、MCP，以及干物质/NDF/ADF/CP 瘤胃降解率与有效降解率 ED" vertex="1">
          <mxGeometry height="50" width="1120" x="241.5" y="670" as="geometry" />
        </mxCell>
        <mxCell id="arw23" edge="1" parent="1" style="shape=flexArrow;endArrow=classic;html=1;rounded=0;endWidth=43.30578512396694;endSize=11.67878787878788;width=41.21212121212121;fillColor=#fff2cc;strokeColor=#d6b656;">
          <mxGeometry height="50" relative="1" width="50" as="geometry">
            <mxPoint x="799.38" y="740" as="sourcePoint" />
            <mxPoint x="800" y="790" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- ============ 阶段 3 ============ -->
        <mxCell id="r3_step" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;" value="饲养试验&#xa;与&#xa;消化代谢试验" vertex="1">
          <mxGeometry height="360" width="90" x="111.5" y="790" as="geometry" />
        </mxCell>
        <mxCell id="r3_method" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;" value="饲养试验法&#xa;消化代谢试验&#xa;血液生理生化检测" vertex="1">
          <mxGeometry height="360" width="90" x="1398.5" y="790" as="geometry" />
        </mxCell>
        <mxCell id="r3_outer" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontSize=16;" value="" vertex="1">
          <mxGeometry height="360" width="1160" x="221.5" y="790" as="geometry" />
        </mxCell>
        <mxCell id="r3_title" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f0a30a;strokeColor=#BD7000;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;fontColor=#000000;" value="田菁替代苜蓿对澳湖杂交育肥羔羊生长性能、营养物质表观消化率及血液指标的影响" vertex="1">
          <mxGeometry height="40" width="1120" x="241.5" y="810" as="geometry" />
        </mxCell>
        <mxCell id="r3_sub1_t" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f0a30a;strokeColor=#BD7000;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;fontColor=#000000;" value="生长性能测定" vertex="1">
          <mxGeometry height="30" width="270" x="251.5" y="875" as="geometry" />
        </mxCell>
        <mxCell id="r3_sub1_c" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=16;align=left;verticalAlign=middle;spacingLeft=10;spacingRight=10;" value="40只4月龄雄性澳湖杂交育肥羔羊（5组×8只）&#xa;· DMI / 末重 / ADG&#xa;· FCR = 总耗料 / 总增重&#xa;测定时点：1、20、40、60 d" vertex="1">
          <mxGeometry height="160" width="270" x="251.5" y="910" as="geometry" />
        </mxCell>
        <mxCell id="r3_sub2_t" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f0a30a;strokeColor=#BD7000;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;fontColor=#000000;" value="营养物质表观消化率" vertex="1">
          <mxGeometry height="30" width="270" x="531.5" y="875" as="geometry" />
        </mxCell>
        <mxCell id="r3_sub2_c" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=16;align=left;verticalAlign=middle;spacingLeft=10;spacingRight=10;" value="第50–59 d 全收粪法（5 d适应 + 5 d收集）&#xa;· 每天取总排泄量 10%（两份）&#xa;· 一份加10%硫酸固氮（CP）&#xa;· 一份测 EE、NDF、ADF&#xa;65℃烘干后过40目筛" vertex="1">
          <mxGeometry height="160" width="270" x="531.5" y="910" as="geometry" />
        </mxCell>
        <mxCell id="r3_sub3_t" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f0a30a;strokeColor=#BD7000;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;fontColor=#000000;" value="血液生理生化指标" vertex="1">
          <mxGeometry height="30" width="270" x="811.5" y="875" as="geometry" />
        </mxCell>
        <mxCell id="r3_sub3_c" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=16;align=left;verticalAlign=middle;spacingLeft=10;spacingRight=10;" value="0 d 与 60 d 颈静脉采血，ELISA 双抗体夹心法&#xa;· 蛋白代谢：TP、ALB&#xa;· 糖脂代谢：GLU、TG、TC、β-羟丁酸&#xa;· 血清酶活：AST、ALT、ALP、谷氨酸脱氢酶&#xa;· 代谢产物：总胆红素" vertex="1">
          <mxGeometry height="160" width="270" x="811.5" y="910" as="geometry" />
        </mxCell>
        <mxCell id="r3_sub4_t" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f0a30a;strokeColor=#BD7000;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;fontColor=#000000;" value="抗氧化指标" vertex="1">
          <mxGeometry height="30" width="270" x="1091.5" y="875" as="geometry" />
        </mxCell>
        <mxCell id="r3_sub4_c" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=16;align=left;verticalAlign=middle;spacingLeft=10;spacingRight=10;" value="2~8℃保存血清，-80℃待测&#xa;· T-AOC / MDA&#xa;· SOD / CAT / GSH-Px&#xa;· 非酶抗氧化剂：维生素C、维生素E&#xa;→ 综合反映机体氧化还原状态" vertex="1">
          <mxGeometry height="160" width="270" x="1091.5" y="910" as="geometry" />
        </mxCell>
        <mxCell id="r3_sum" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=16;fontStyle=2;align=center;verticalAlign=middle;" value="产出：确定田菁适宜替代比例；建立不同替代比例下生长性能、消化率、血液生理生化、抗氧化指标的剂量-效应曲线" vertex="1">
          <mxGeometry height="50" width="1110" x="251.5" y="1080" as="geometry" />
        </mxCell>
        <mxCell id="arw34" edge="1" parent="1" style="shape=flexArrow;endArrow=classic;html=1;rounded=0;endWidth=43.30578512396694;endSize=11.67878787878788;width=41.21212121212121;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fillColor=#e1d5e7;strokeColor=#9673a6;" target="r4_outer">
          <mxGeometry height="50" relative="1" width="50" as="geometry">
            <mxPoint x="799.23" y="1150" as="sourcePoint" />
            <mxPoint x="799.85" y="1200" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- ============ 阶段 4 ============ -->
        <mxCell id="r4_step" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;" value="瘤胃微生态&#xa;解析&#xa;与&#xa;肉品质评价" vertex="1">
          <mxGeometry height="450" width="90" x="111.5" y="1220" as="geometry" />
        </mxCell>
        <mxCell id="r4_method" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;" value="16S rDNA测序&#xa;瘤胃代谢组学&#xa;肉品质理化检测&#xa;GC×GC-TOF MS" vertex="1">
          <mxGeometry height="450" width="90" x="1398.5" y="1220" as="geometry" />
        </mxCell>
        <mxCell id="r4_outer" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontSize=16;" value="" vertex="1">
          <mxGeometry height="450" width="1160" x="221.5" y="1220" as="geometry" />
        </mxCell>
        <mxCell id="r4_title" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#6a00ff;strokeColor=#3700CC;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;fontColor=#ffffff;" value="田菁替代苜蓿对澳湖杂交育肥羔羊瘤胃微生态、屠宰性能、肉品质及风味的影响" vertex="1">
          <mxGeometry height="40" width="1120" x="241.5" y="1240" as="geometry" />
        </mxCell>
        <mxCell id="r4_top_bar" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#6a00ff;strokeColor=#3700CC;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;fontColor=#ffffff;" value="瘤胃微生态解析（第 60 d 育肥羔羊屠宰采样）" vertex="1">
          <mxGeometry height="30" width="1120" x="241.5" y="1290" as="geometry" />
        </mxCell>
        <mxCell id="r4_top1" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=16;align=center;verticalAlign=middle;" value="瘤胃发酵参数&#xa;· pH&#xa;· VFAs（乙/丙/丁酸）&#xa;· NH3-N" vertex="1">
          <mxGeometry height="90" width="218" x="251.5" y="1330" as="geometry" />
        </mxCell>
        <mxCell id="r4_top2" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=16;align=center;verticalAlign=middle;" value="瘤胃酶活性&#xa;· 总蛋白酶&#xa;· 纤维素酶&#xa;· 半纤维素酶&#xa;· α-淀粉酶" vertex="1">
          <mxGeometry height="90" width="218" x="479.5" y="1330" as="geometry" />
        </mxCell>
        <mxCell id="r4_top3" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=16;align=center;verticalAlign=middle;" value="瘤胃组织形态&#xa;· RPL 瘤胃乳头长度&#xa;· RPW 瘤胃乳头宽度&#xa;· RMT 瘤胃肌层厚度" vertex="1">
          <mxGeometry height="90" width="218" x="707.5" y="1330" as="geometry" />
        </mxCell>
        <mxCell id="r4_top4" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=16;align=center;verticalAlign=middle;" value="16S rDNA高通量测序&#xa;· 菌群 α/β 多样性&#xa;· 物种组成与丰度&#xa;· 差异菌群筛选" vertex="1">
          <mxGeometry height="90" width="218" x="935.5" y="1330" as="geometry" />
        </mxCell>
        <mxCell id="r4_top5" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=16;align=center;verticalAlign=middle;" value="瘤胃代谢组学&#xa;（非靶向LC-MS）&#xa;· 差异代谢物筛选&#xa;· KEGG通路富集&#xa;· 菌群-代谢物关联" vertex="1">
          <mxGeometry height="90" width="188" x="1163.5" y="1330" as="geometry" />
        </mxCell>
        <mxCell id="r4_bot_bar" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#6a00ff;strokeColor=#3700CC;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;fontColor=#ffffff;" value="屠宰性能、肉品质及风味物质分析" vertex="1">
          <mxGeometry height="30" width="1120" x="241.5" y="1440" as="geometry" />
        </mxCell>
        <mxCell id="r4_bot1" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=16;align=center;verticalAlign=middle;" value="屠宰性能&#xa;· 宰前活重、胴体重&#xa;· 屠宰率&#xa;· 背膘厚度、GR值&#xa;· 眼肌面积" vertex="1">
          <mxGeometry height="110" width="278" x="251.5" y="1480" as="geometry" />
        </mxCell>
        <mxCell id="r4_bot2" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=16;align=center;verticalAlign=middle;" value="常规肉品质&#xa;· pH（45 min / 24 h）&#xa;· 剪切力（嫩度）&#xa;· 系水力、蒸煮损失&#xa;· L*、a*、b*肉色" vertex="1">
          <mxGeometry height="110" width="278" x="539.5" y="1480" as="geometry" />
        </mxCell>
        <mxCell id="r4_bot3" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=16;align=center;verticalAlign=middle;" value="营养成分谱&#xa;· 氨基酸谱（LC-MS）&#xa;· 脂肪酸谱（GC-MS）&#xa;· 水分 / 蛋白 / IMF / 灰分" vertex="1">
          <mxGeometry height="110" width="248" x="827.5" y="1480" as="geometry" />
        </mxCell>
        <mxCell id="r4_bot4" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=16;align=center;verticalAlign=middle;" value="挥发性风味物质&#xa;· GC×GC-TOF MS&#xa;· 醛/酮/醇/酯/含硫化合物&#xa;· ROAV 气味活性值&#xa;· NIST2020 + Flavor DB" vertex="1">
          <mxGeometry height="110" width="266" x="1085.5" y="1480" as="geometry" />
        </mxCell>
        <mxCell id="r4_sum" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=16;fontStyle=2;align=center;verticalAlign=middle;" value="产出：各组瘤胃菌群结构、差异代谢物；屠宰性能、肉品质、氨基酸/脂肪酸谱、挥发性风味物质谱全链条数据" vertex="1">
          <mxGeometry height="40" width="1120" x="241.5" y="1610" as="geometry" />
        </mxCell>
        <mxCell id="arw45" edge="1" parent="1" style="shape=flexArrow;endArrow=classic;html=1;rounded=0;endWidth=43.30578512396694;endSize=11.67878787878788;width=41.21212121212121;fillColor=#f8cecc;strokeColor=#b85450;">
          <mxGeometry height="50" relative="1" width="50" as="geometry">
            <mxPoint x="805.11" y="1670" as="sourcePoint" />
            <mxPoint x="805" y="1730" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- ============ 阶段 5 ============ -->
        <mxCell id="r5_step" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;" value="多组学关联&#xa;与&#xa;网络拓扑分析" vertex="1">
          <mxGeometry height="260" width="90" x="111.5" y="1730" as="geometry" />
        </mxCell>
        <mxCell id="r5_method" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;" value="Pearson 相关性&#xa;度中心性 / 介数中心性&#xa;网络拓扑分析" vertex="1">
          <mxGeometry height="260" width="90" x="1398.5" y="1730" as="geometry" />
        </mxCell>
        <mxCell id="r5_outer" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontSize=16;" value="" vertex="1">
          <mxGeometry height="260" width="1160" x="221.5" y="1730" as="geometry" />
        </mxCell>
        <mxCell id="r5_title" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#d80073;strokeColor=#A50040;fontSize=16;fontStyle=1;align=center;verticalAlign=middle;fontColor=#ffffff;" value="多组学关联分析与风味代谢网络拓扑演变" vertex="1">
          <mxGeometry height="40" width="1120" x="241.5" y="1750" as="geometry" />
        </mxCell>
        <mxCell id="r5_a" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=16;align=center;verticalAlign=middle;" value="① 瘤胃内部关联&#xa;细菌群落、差异代谢物&#xa;与瘤胃发酵消化指标的关联" vertex="1">
          <mxGeometry height="90" width="260" x="261.5" y="1810" as="geometry" />
        </mxCell>
        <mxCell id="r5_b" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=16;align=center;verticalAlign=middle;" value="② 跨组织关联&#xa;瘤胃代谢特征与机体&#xa;生理、屠宰表型的联系" vertex="1">
          <mxGeometry height="90" width="260" x="541.5" y="1810" as="geometry" />
        </mxCell>
        <mxCell id="r5_c" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=16;align=center;verticalAlign=middle;" value="③ 肌肉内部关联&#xa;风味前体物质与羊肉&#xa;挥发性风味物质 Pearson 关联" vertex="1">
          <mxGeometry height="90" width="260" x="821.5" y="1810" as="geometry" />
        </mxCell>
        <mxCell id="r5_d" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=16;align=center;verticalAlign=middle;" value="④ 风味代谢网络拓扑演变&#xa;度中心性、介数中心性&#xa;网络解耦-重组机制" vertex="1">
          <mxGeometry height="90" width="240" x="1101.5" y="1810" as="geometry" />
        </mxCell>
        <mxCell id="r5_sum" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=16;fontStyle=2;align=center;verticalAlign=middle;" value="总结：阐明瘤胃-宿主-肌肉风味的跨层次调控关联，揭示田菁替代苜蓿经瘤胃菌群与差异代谢物重塑肌肉风味网络的分子机制" vertex="1">
          <mxGeometry height="45" width="1120" x="241.5" y="1925" as="geometry" />
        </mxCell>

        <!-- ============ 纵向串联边 ============ -->
        <mxCell id="e_s12" edge="1" parent="1" source="r1_step" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" target="r2_step">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_s23" edge="1" parent="1" source="r2_step" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" target="r3_step">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_s34" edge="1" parent="1" source="r3_step" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" target="r4_step">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_s45" edge="1" parent="1" source="r4_step" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" target="r5_step">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_m12" edge="1" parent="1" source="r1_method" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" target="r2_method">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_m23" edge="1" parent="1" source="r2_method" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" target="r3_method">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_m34" edge="1" parent="1" source="r3_method" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" target="r4_method">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_m45" edge="1" parent="1" source="r4_method" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" target="r5_method">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- ============ 阶段标题 → 卡片装饰连线（可选） ============ -->
        <mxCell id="e_t1a1" edge="1" parent="1" source="r1_title" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" target="r1_a1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="800" y="160" />
              <mxPoint x="360" y="160" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="e_t1a5" edge="1" parent="1" source="r1_title" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" target="r1_a5">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="800" y="160" />
              <mxPoint x="1260" y="160" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="e_t2s1" edge="1" parent="1" source="r2_title" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" target="r2_sub1_t">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="801.5" y="490" />
              <mxPoint x="426.5" y="490" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="e_t2s3" edge="1" parent="1" source="r2_title" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" target="r2_sub3_t">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="801.5" y="490" />
              <mxPoint x="1161.5" y="490" />
            </Array>
          </mxGeometry>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### 该示例的结构拆解

| 阶段 | 研究步骤（左列） | 研究方法（右列） | 外框 y / 高 | 内容排布 | 配色 |
|------|------------------|------------------|-------------|----------|------|
| 1 | 立论依据与研究现状综述 | 文献研究法、归纳总结法 | 90 / 270 | 2 行 × 5 张并列小卡 | 蓝 |
| 2 | 体外发酵参数与营养物质降解率 | 体外产气法、尼龙袋法、概略养分分析法 | 420 / 320 | 3 组（小标题 + 内容框） | 绿 |
| 3 | 饲养试验与消化代谢试验 | 饲养试验法、消化代谢试验、血液生理生化检测 | 790 / 360 | 4 组（小标题 + 内容框） | 橙黄（**黑字**） |
| 4 | 瘤胃微生态解析与肉品质评价 | 16S rDNA测序、瘤胃代谢组学、肉品质理化检测、GC×GC-TOF MS | 1220 / 450 | 双层：5 卡 + 4 卡 | 紫 |
| 5 | 多组学关联与网络拓扑分析 | Pearson 相关性、度中心性/介数中心性、网络拓扑分析 | 1730 / 260 | 1 行 × 4 张卡 | 品红 |

5 条 flexArrow 分别位于 y: 360→420、740→790、1150→1200、1670→1730，x 均为 ≈800。

---

## 八、输出要求

- 只输出 XML 代码，以 `<mxfile>` 开头，`</mxfile>` 结尾，可以直接保存为 `.drawio` 文件使用。
- 除非用户特别要求，一律写**中文**（题目、阶段名、步骤、方法、卡片内容、汇总）。专业缩写（16S rDNA、GC-MS、ELISA 等）保留原文。
- 除非用户特别要求，**不得改变样式**：字号（总标题 22 / 顶部表头 18 / 其余 16）、全直角 `rounded=0`、五阶段配色表、flexArrow 的三个尺寸参数都要照抄示例。
- 文本换行统一用 `&#xa;`；内容框里的要点用 `· ` 开头。

### 生成后自检清单

- [ ] 每个阶段都有：步骤列、方法列、外框、阶段标题条、内容卡、汇总条，六件套齐全
- [ ] 步骤列 / 方法列的 `y` 和 `height` 与对应外框**完全一致**
- [ ] 外框 `value=""` 且画在内部内容之前
- [ ] 阶段标题条、内容卡、汇总条都落在 `X_OUT+20` 到 `X_OUT+W_OUT-20` 之间
- [ ] 卡片区左右边界一致（250 起、1350 止），卡片间距 10
- [ ] 汇总条底边到外框底边留 20px
- [ ] 相邻阶段之间有 flexArrow，且 x 都在 `CX` 上
- [ ] 阶段 3 用了黑字（`fontColor=#000000`），其他阶段白字
- [ ] 文字没有溢出方框（溢出就把框加高，宁可加高不要改字号）
- [ ] 所有 ID 唯一，所有 `source`/`target` 引用的节点都存在
