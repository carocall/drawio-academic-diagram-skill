# 用例图 —— 分离式（一个参与者一张图，用例自上而下纵排一列）

> 标准形态见 `output/分离式用例图案例.drawio`：左侧**只有一个小人**，右侧一列椭圆**自上而下排开**，
> 每个用例都用一条无箭头直线**直接连到这个小人的身上**，没有父用例、没有第二层。

## 本风格与 `style.md`（合并式）的区别

| | 合并式（见 `style.md`） | **分离式（本文件）** |
|---|---|---|
| 图形数量 | 1 张 | **N 张**：有几个参与者就出几张图 |
| 参与者 | 多个小人同图（挤在左/右两侧） | **每张图只有一个小人**，放左侧垂直居中 |
| 用例 | 全部用例 + 父子层级（子用例挂右侧下一列） | 该参与者的用例**全部平级，一列自上而下纵排** |
| 连线 | 参与者→用例，父用例→子用例 | **每个用例一条线直接连到唯一的参与者** |
| 适用 | 参与者 ≤ 2、用例 ≤ 11 | **参与者 ≥ 2** 或用例 ≥ 12；论文里"管理员用例图""用户用例图"逐角色出图 |

### 什么时候选分离式（命中任一即可）

1. 参与者 ≥ 2 个（合并式里多个小人挤一起，连线必然乱）；
2. 用例总数 ≥ 12，一张图纵排下来太长；
3. 用户说"每个角色一张图""按用户分开画""画一组用例图"；
4. 论文/课设正文需要"图 3-2 管理员用例图、图 3-3 会员用例图、图 3-4 商家用例图"这种逐角色配图。

---

## 一、单张图的版式（照案例画）

```
        参与者（唯一的小人）
              │
              ├── 用例 1
              ├── 用例 2          ← 一列纵排，全部直连小人
              ├── 用例 3
              └── 用例 4
```

- **只有一个 `umlActor`**，放左侧，**垂直居中于整列用例**。
- 用例**一列排到底**，`x` 严格相同；`y` 自上而下递增。
- 用例之间**不分层、不互相连线**（没有父子关系，全靠与参与者的连线表达"该角色能做这些事"）。
- 用例名是**模块级/功能级**短语：`课程管理`、`用户管理`、`分类管理`、`系统配置`、`订单管理`。

---

## 二、元素规格

| 元素 | 形状 | 尺寸（px） | 字体 | 样式串 |
|------|------|-----------|------|--------|
| 参与者 | UML 小人 | 30 × 60 | 默认 | `shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;` |
| 用例 | 椭圆 | 高 **70**；宽按字数定（下表） | 16 | `ellipse;whiteSpace=wrap;html=1;fontSize=16;` |
| 连线 | 无箭头直线 | — | — | `rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;endFill=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;` |

椭圆宽度按字数：

| 用例名长度 | 宽度 |
|-----------|------|
| 2～4 字（`课程管理`） | 160 |
| 5～6 字（`查看商品详情`） | 180 |
| 7～8 字（`导出成绩统计报表`） | 200 |
| ≥ 9 字 | 200 + 换行，`h` 改 90 |

- 用例 value 直接写中文，**不要套无属性的 `&lt;span&gt;`**（没意义还容易转义出错）。
- 用例保持**默认白底**，不加 `fillColor` / `strokeColor`。
- 边**不要写 `sourcePoint` / `targetPoint`**，让 draw.io 自动走线；手动拖出来的端点会残留固定坐标，
  导致连线飘到画布外（案例文件里就有这种残留点，`x=730` 已超出画布）。

---

## 三、连线落点：固定到椭圆最左边（关键）

不设落点时，draw.io 按"两图形中心连线与边界的交点"算端点，越靠上/靠下的椭圆，线越斜插进椭圆侧面，
一列线看起来歪歪扭扭。**加上 `entryX` / `entryY` 就能把落点钉死在椭圆最左侧中点。**

```xml
<mxCell id="e1" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;endFill=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="act-admin" target="uc-course">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

| 属性 | 含义 | 取值 |
|------|------|------|
| `entryX` / `entryY` | **目标**（target）上的入口点，相对坐标 | `0`=左 / `1`=右 / `0.5`=中，`0, 0.5` = **左边界中点** |
| `exitX` / `exitY` | **源**（source）上的出口点，相对坐标 | `1, 0.5` = 小人右边界中点 |
| `entryDx` / `entryDy` | 入口点的像素微调 | 一般写 `0` |

要点：

1. `entryX=0;entryY=0.5` 对椭圆天然就是**边界点**（椭圆中心高度处的最左端），draw.io 的椭圆 perimeter
   会把它精确投影到边界上，不会画进图形内部。
2. **只设入口、不设出口**就够了：draw.io 会自动把多条线的出口点沿小人右边界**分散开**
   （实测 y 间隔 8.2px），形成干净的扇形发散，不会挤成一个点。
3. 如果同时写 `exitX=1;exitY=0.5`，所有线会从**同一个点**出发，起点段完全重叠成一束，反而不如扇形好看
   ——除非你就是要这种"完全共点"的效果，否则别加。
4. 实测对比（导出 SVG 读端点坐标）：不设时落点 x 为 `222.1 / 201.7 / 183 / 201.7 / 222.1`（斜插），
   设了之后**全部 = 183**（椭圆最左），且 y 与各椭圆中心高度一致。
5. 想让用例列的线走**水平折线**，再加 `edgeStyle=orthogonalEdgeStyle;`（用例图一般用不上）。

---

## 四、布局公式

```
用例列：  x1 = 320，h = 70，纵向间距 gap = 90（间隙 20；用例少时可放宽到 110）
          y_i = y0 + i * gap，y0 = 110（可按需整体平移）
参与者：  x0 = x1 - 180 = 140，w = 30，h = 60
          y0 = (用例列顶 + 用例列底) / 2 - 30        ← 小人垂直居中于整列用例
          （用例列顶 = y_first，用例列底 = y_last + 70）
画布：    W = 用例列右边界(x1 + w) + 100
          H = max(用例列底, 参与者底 y0 + 60) + 80
```

例：5 个用例 `y = 110,200,290,380,470` → 列顶 110、列底 540、中心 325 → 参与者 `y = 325 - 30 = 295`。

**用例很多时（> 8 个）**：不要硬拉长一列，按下面顺序处理
1. 先确认该角色的用例是否还能再拆出一个子角色（如"管理员"拆成"商品管理员""订单管理员"）；
2. 确属同一角色的，改**两列纵排**：第二列 `x = x1 + 240`，两列用例数尽量均分，
   参与者仍放两列左侧、垂直居中于两列整体；
3. 实在太多才把 `gap` 压到 80（间隙 10），不要更小，否则椭圆快贴上了。

---

## 五、XML 模板（已验证，可直接套坐标）

```xml
<mxfile host="app.diagrams.net">
  <diagram id="uc-admin" name="管理员用例图">
    <mxGraphModel dx="0" dy="0" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="580" pageHeight="620" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- ===== 参与者（唯一的小人，垂直居中） ===== -->
        <mxCell id="act-admin" value="管理员" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;" vertex="1" parent="1">
          <mxGeometry x="140" y="295" width="30" height="60" as="geometry" />
        </mxCell>

        <!-- ===== 用例：一列自上而下 ===== -->
        <mxCell id="uc-course" value="课程管理" style="ellipse;whiteSpace=wrap;html=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="320" y="110" width="160" height="70" as="geometry" />
        </mxCell>
        <mxCell id="uc-user" value="用户管理" style="ellipse;whiteSpace=wrap;html=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="320" y="200" width="160" height="70" as="geometry" />
        </mxCell>
        <mxCell id="uc-cate" value="分类管理" style="ellipse;whiteSpace=wrap;html=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="320" y="290" width="160" height="70" as="geometry" />
        </mxCell>
        <mxCell id="uc-config" value="系统配置" style="ellipse;whiteSpace=wrap;html=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="320" y="380" width="160" height="70" as="geometry" />
        </mxCell>
        <mxCell id="uc-order" value="订单管理" style="ellipse;whiteSpace=wrap;html=1;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="320" y="470" width="160" height="70" as="geometry" />
        </mxCell>

        <!-- ===== 每个用例一条线直连参与者 ===== -->
        <mxCell id="e1" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;endFill=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="act-admin" target="uc-course">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e2" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;endFill=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="act-admin" target="uc-user">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e3" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;endFill=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="act-admin" target="uc-cate">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e4" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;endFill=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="act-admin" target="uc-config">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e5" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;endFill=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="act-admin" target="uc-order">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

## 六、多页文件结构（推荐：一个 .drawio 装全部角色）

分离式**首选单文件多页**：一个参与者一页，`diagram name` 直接当图标题。
导出 PNG 时按页导出（`draw.io` Desktop 页码 **从 1 开始**）。

```xml
<mxfile host="app.diagrams.net">
  <diagram id="uc-admin"    name="管理员用例图"> …管理员 + 他的用例… </diagram>
  <diagram id="uc-member"   name="会员用例图">   …会员 + 他的用例…   </diagram>
  <diagram id="uc-merchant" name="商家用例图">   …商家 + 他的用例…   </diagram>
  <!-- 有几个参与者就有几页 -->
</mxfile>
```

- 每页都自带 `pageWidth` / `pageHeight`，按该页用例数单独算。
- 各页 ID 独立，页间重名不会冲突；拆成独立 `.drawio` 文件时建议加页前缀（如 `p2-act-member`）。
- 用户要求"每个图一个文件"时再拆成多个 `.drawio`，内容照抄各页。
- **一般不再画总览图**；用户明确要"先来一张总的"时，总览页按 `style.md`（合并式）画即可。

---

## 七、命名与一致性（分离式的关键）

- 页名 = `<参与者名>用例图`（如"管理员用例图"），正文图题直接引用。
- 参与者名全图统一：这一页叫"管理员"，另一页就不能写成"系统管理员"。
- 用例名一律**中文**：模块级用名词短语（`订单管理`），动作级用动宾（`提交订单`、`审核课程`）。
- **同一用例可以出现在多张图上**（如"登录"对会员和管理员都可见），这是正常的，不必合并。
- 参与者可以是人或外部系统（"支付系统""物流系统"），同样用 `umlActor`，同样独占一页。

---

## 八、自查清单

- [ ] 每张图**只有一个** `shape=umlActor` 的小人，且垂直居中于用例列
- [ ] 所有用例 **x 严格相同**、一列纵排、纵向等距
- [ ] 用例之间**没有连线**，每个用例各自连到参与者
- [ ] 边上**没写** `sourcePoint` / `targetPoint`（避免端点漂移）
- [ ] 每条边都带 `entryX=0;entryY=0.5;entryDx=0;entryDy=0;`，落点钉在椭圆最左侧中点
- [ ] 用例椭圆默认白底，`fontSize=16`，未被 `&lt;span&gt;` 包裹
- [ ] 参与者数与页数一致，页名 = 参与者名 + "用例图"
- [ ] 每页都有 `<mxCell id="0" />` 与 `<mxCell id="1" parent="0" />`；ID 唯一
- [ ] 顶点 `vertex="1"` + `x,y,width,height`；边 `edge="1"` + `relative="1"`
- [ ] 只输出 `<mxfile>`…`</mxfile>`
