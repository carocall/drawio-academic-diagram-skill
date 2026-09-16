# ER 图 —— 分离式（总 E-R 图 + 每个实体一张属性图）

## 本风格与 `style.md` 的区别

| | 合并式（见 `style.md`） | **分离式（本文件）** |
|---|---|---|
| 图形数量 | 1 张 | 1 张总图 + N 张属性图 |
| 总图内容 | 实体 + 属性 + 联系都画在一起 | **只有实体（矩形）和联系（菱形）**，不画属性 |
| 属性 | 椭圆挂在实体周围 | 每个实体单独一张"实体属性图" |
| 适用 | 实体 ≤ 5 个 | **实体 ≥ 6 个**（合并式会挤成一团、线交叉严重） |
| 正文配套写法 | 逐个实体说明属性 | 总图后接"下面对各实体的属性组成分别进行说明"，再逐个给出属性图 |

毕业论文常用分离式：**图 3-2 系统 E-R 图 + 图 3-3～图 3-12 各实体属性图**。

---

## 一、总 E-R 图

### 元素规格

| 元素 | 形状 | 尺寸（px） | 字体 | 样式串 |
|------|------|-----------|------|--------|
| 实体 | 矩形 | 150 × 64（名字长可到 190） | 24 | `rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontSize=24;` |
| 联系 | 菱形 | 150 × 84 | 22 | `rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontSize=22;` |
| 连线 | 直线无箭头 | — | — | `endArrow=none;html=1;rounded=0;` |
| 基数标注 | 子标签 | — | 20 | `edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=20;` |

- 联系名用**中文动词**：`收藏`、`加入`、`提交`、`发布`、`包含`、`组成`、`下架`、`登记`、`反馈`、`被收藏`、`对应`、`针对`、`关联`。
- 基数用 `1` / `n`；**标在靠实体的那一侧**（参考图中"1"紧贴实体、"n"紧贴菱形）。
- 基数写成边的**子 cell**（`parent="<边ID>"`，`mxGeometry x` 取 `2t-1`，t 为边上位置比例 0~1）。

### 布局策略（10 个实体的常用排法）

采用**双枢纽 + 中间列**，能避免长斜线：

```
左列（核心实体 A）      左菱形列      中间列（业务实体）      右菱形列      右列（核心实体 B）
   用户 x≈40         x≈330         商品收藏/购物车/…       x≈880         商品分类/商品/通知 x≈1110
   收货地址                        纵向排布 5 个                         纵向排布 3 个
```

四条硬规则：

1. **左、右菱形列各留一条"水平空走廊"**：核心实体之间的长联系（如"发布"）走这条走廊，
   落位前必须确认走廊高度上没有菱形（菱形列纵向间距 240 时，走廊取两条消息的中间 y）。
2. 核心实体 A 与它的从属实体（如"用户—收货地址"）用**同一列纵向串联**，联系菱形夹在中间。
3. 中间列的业务实体**纵向等距**排布（间距约 240~260），两个实体之间若还要插联系菱形（如"订单—组成—订单明细"），
   留出 170 的纵向空间。
4. 所有连线一律**中心到中心直连**，靠白底图形盖住穿入图形内部的部分；但**不能穿过任何图形**
   ——画之前逐个核对：菱形/矩形之间是否重叠、连线是否经过第三个图形。

画布：`W = 最右列右边 + 40`，`H = 最下节点下边 + 40`。10 个实体典型为 1320 × 1464。

### 总图 XML 片段

```xml
<mxCell id="U" value="用户" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontSize=24;" vertex="1" parent="1">
  <mxGeometry x="40" y="700" width="150" height="64" as="geometry" />
</mxCell>
<mxCell id="R1" value="收藏" style="rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontSize=22;" vertex="1" parent="1">
  <mxGeometry x="255" y="290" width="150" height="84" as="geometry" />
</mxCell>
<mxCell id="edge1" style="endArrow=none;html=1;rounded=0;" edge="1" parent="1" source="U" target="R1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
<mxCell id="edge1_l" value="1" style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=20;" vertex="1" connectable="0" parent="edge1">
  <mxGeometry x="-0.500" relative="1" as="geometry"><mxPoint as="offset" /></mxGeometry>
</mxCell>
```

---

## 二、实体属性图（每个实体一张）

### 版式

**实体矩形在下方居中，属性椭圆在其上方呈扇形（放射状）排布**，用直线把矩形与每个椭圆连起来。

### 元素规格

| 元素 | 形状 | 尺寸 | 字体 | 样式串 |
|------|------|------|------|--------|
| 实体 | 矩形 | `w = 文本宽 + 66`（最小 170），`h = 70` | 22 | `rounded=0;…;fontSize=22;` |
| 属性 | 椭圆 | `w = 文本宽 + 44`（最小 120），`h = 60` | 20 | `ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontSize=20;` |
| 连线 | 直线无箭头 | — | — | `endArrow=none;html=1;rounded=0;`（中心到中心） |

文本宽估算：中文 1 字 = 1 × 字号，西文 1 字 ≈ 0.58 × 字号。

### 扇形布局公式

```
属性数 n，扇形张角 span = 132°（从 156° 递减到 24°）
角度   θ_i = 156 - i * span / (n - 1)          （单位：度，y 轴向下）
半径   R = max(165,  (w_i + w_{i+1}) * 0.5 * 1.14 / (2 * sin(Δθ/2)))   Δθ = span/(n-1)
椭圆心 ax = cx + R*cos θ_i，ay = ytop - R*sin θ_i      （cx 为实体中心，ytop 为实体矩形上边）
画布   W = 2 * (R*0.906 + max(w)/2) + 余量，最小 = 实体宽 + 120
       H = (46 + R + 30) + 70 + 34
```

R 的含义：保证相邻椭圆不相切。n 越大 R 越大（n=4 约 220，n=8 约 417，n=10 约 536）。
若某张图显得过宽，应**减少该实体的属性个数**（保留关键属性，外键类字段留在正文表里说明），
而不是硬缩半径——缩半径会让椭圆重叠。

### 属性图 XML 模板（4 个属性，已验证）

```xml
<mxfile host="app.diagrams.net" agent="figure_engine">
  <diagram name="商品收藏实体属性图" id="p1">
    <mxGraphModel dx="1400" dy="900" grid="0" gridSize="10" guides="0" tooltips="0" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="465.88" pageHeight="368.68" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="E" value="商品收藏" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontSize=22;" vertex="1" parent="1">
          <mxGeometry x="147.94" y="264.68" width="170" height="70" as="geometry" />
        </mxCell>
        <mxCell id="A0" value="收藏编号" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontSize=20;" vertex="1" parent="1">
          <mxGeometry x="-1.42" y="157.94" width="124" height="60" as="geometry" />
        </mxCell>
        <mxCell id="A1" value="用户名" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontSize=20;" vertex="1" parent="1">
          <mxGeometry x="102.26" y="59.74" width="120" height="60" as="geometry" />
        </mxCell>
        <mxCell id="A2" value="商品编号" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontSize=20;" vertex="1" parent="1">
          <mxGeometry x="241.62" y="59.74" width="124" height="60" as="geometry" />
        </mxCell>
        <mxCell id="A3" value="收藏时间" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontSize=20;" vertex="1" parent="1">
          <mxGeometry x="341.62" y="157.94" width="124" height="60" as="geometry" />
        </mxCell>
        <mxCell id="edge1" style="endArrow=none;html=1;rounded=0;" edge="1" parent="1" source="E" target="A0">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <!-- edge2 → A1，edge3 → A2，edge4 → A3，同理 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

## 三、命名与一致性

- 实体名与属性名**全部中文**，与数据库表的字段注释保持一致（如"下单时间""上架状态""下架原因"）。
- **属性图里的属性名必须能在正文的数据表里找到**，反过来不必强求（外键、更新时间等可只在表中出现）。
- 属性按"主键 → 外键 → 业务字段 → 状态 → 时间"的顺序排列，扇面上从左到右读下来逻辑连贯。

---

## 四、自查清单

- [ ] 总图只有实体和联系，**没有椭圆属性**
- [ ] 有几个实体就有几张属性图，正文"画几个就写几个"，一一对应
- [ ] 每个联系两侧都有 `1` / `n`，且 `1` 在"一"方、`n` 在"多"方
- [ ] 所有 ID 唯一（总图用 `U`/`P`/`R1`…；属性图用 `E`/`A0`/`A1`…）
- [ ] 相邻椭圆不相交、连线不穿过第三个图形
- [ ] 顶点 `vertex="1"` + `x,y,width,height`；边 `edge="1"` + `relative="1"`
- [ ] 图形一律白底黑线（`fillColor=#FFFFFF`，不是 `none`）
- [ ] 只输出 `<mxfile>`…`</mxfile>`
