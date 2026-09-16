# 时序图（中文论文版）生成规范

## 任务说明

根据给出的模块交互描述（或接口/代码调用链），生成符合 draw.io 格式的 **中文时序图 XML**。

与通用 UML 时序图最大的三点区别（**必须遵守**）：

1. **不出现英文标识**：生命线不写 `:AuthController`、`:ProductApi`、`existsByUsername()`、
   `SELECT * FROM users` 等类名、方法名、SQL；一律用 `:登录页`、`:接口层`、`:控制层`、`:数据访问层` 这类中文角色名。
2. **消息是中文文字叙述**：每条消息写成 `1.输入账号密码`、`4.查询用户表` 的形式
   ——序号 + 中文动宾短语，描述"做了什么"，而不是"调用了谁"。
3. **黑白线框**：白底黑线，不用配色、不用阴影、不用圆角。

---

## 一、元素规格

| 元素 | 形状 | 尺寸（px） | 字体 | 样式串 |
|------|------|-----------|------|--------|
| 角色（火柴人） | `shape=umlActor` | 32 × 62 | — | `shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;` |
| 生命线标签框 | 矩形 | 140 × 40 | 18 | `rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontSize=18;` |
| 生命线 | 虚线 | 纵向贯穿 | — | `endArrow=none;html=1;dashed=1;dashPattern=6 4;`（浮动边，用 sourcePoint/targetPoint） |
| 激活条 | 窄矩形 | 12 × 跨度 | — | `rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;` |
| 请求消息 | 实线 + 实心箭头 | 水平 | 17 | `endArrow=classic;html=1;rounded=0;` |
| 返回消息 | 虚线 + 空心箭头 | 水平 | 17 | `endArrow=open;html=1;rounded=0;dashed=1;dashPattern=6 4;` |

- 生命线标签统一写成 `:角色名` 形式（带英文冒号，如 `:登录页`），这是标准 UML 对象命名；
  除冒号外不得出现英文单词。
- 图形一律 `fillColor=#FFFFFF`（白底会挡住穿过它的连线，`fillColor=none` 会让线透出来）。

---

## 二、布局算法（照抄即可得到对齐的图）

```
列中心   col_x[i] = 90 + i * 170          # 第 0 列是角色，其余是对象
标签框   x = col_x[i] - 70, y = 108, w = 140, h = 40
火柴人   x = col_x[0] - 16, y = 6,  w = 32, h = 62
生命线   从 y = 148 到 y = H - 34，x = col_x[i]（虚线）
消息 y   y_k = 208 + k * 48               # k 从 0 开始
激活条   y = min(该列相关消息 y) - 12，h = max - min + 24，x = col_x[i] - 6，w = 12
消息箭头 起点 x = 源列 ± 6，终点 x = 目标列 ∓ 6（± 取方向）
画布     W = col_x[-1] + 100，H = 208 + (n - 1) * 48 + 60
```

**消息文字的位置**：直接写在边的 `value` 上（draw.io 默认居中于边上方），
务必加白底以免被虚线穿过导致看不清。

---

## 三、XML 结构模板（已验证可直接打开）

```xml
<mxfile host="app.diagrams.net" agent="figure_engine">
  <diagram name="用户登录模块时序图" id="p1">
    <mxGraphModel dx="1400" dy="900" grid="0" gridSize="10" guides="0" tooltips="0" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="870" pageHeight="604" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- 角色：火柴人与标签框是两个 cell，ID 必须不同（P0_a / P0） -->
        <mxCell id="P0_a" value="" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;" vertex="1" parent="1">
          <mxGeometry x="74" y="6" width="32" height="62" as="geometry" />
        </mxCell>
        <mxCell id="P0" value=":用户" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontSize=18;" vertex="1" parent="1">
          <mxGeometry x="20" y="108" width="140" height="40" as="geometry" />
        </mxCell>
        <mxCell id="P1" value=":登录页" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontSize=18;" vertex="1" parent="1">
          <mxGeometry x="190" y="108" width="140" height="40" as="geometry" />
        </mxCell>

        <!-- 生命线（浮动边：用 sourcePoint / targetPoint） -->
        <mxCell id="line1" style="endArrow=none;html=1;dashed=1;dashPattern=6 4;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="90" y="148" as="sourcePoint" />
            <mxPoint x="90" y="570" as="targetPoint" />
          </mxGeometry>
        </mxCell>

        <!-- 激活条 -->
        <mxCell id="B0" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;" vertex="1" parent="1">
          <mxGeometry x="84" y="196" width="12" height="360" as="geometry" />
        </mxCell>

        <!-- 请求：实线实心箭头；返回：虚线空心箭头。文字写 value -->
        <mxCell id="msg1" value="1.输入账号密码" style="endArrow=classic;html=1;rounded=0;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="96" y="208" as="sourcePoint" />
            <mxPoint x="254" y="208" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="msg5" value="5.返回查询结果" style="endArrow=open;html=1;rounded=0;dashed=1;dashPattern=6 4;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="774" y="400" as="sourcePoint" />
            <mxPoint x="606" y="400" as="targetPoint" />
          </mxGeometry>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

## 四、写法要点

1. **角色只有一个**：放最左列；其余列都是对象（页面/接口层/控制层/数据访问层）。
   常见组合：`用户 | :登录页 | :接口层 | :控制层 | :数据访问层`（5 列，宽约 870）。
2. **消息条数 8～13 条**最合适；太少不能体现层次，太多会拉长画布。
   典型节奏：`用户发起 → 页面转发 → 控制层处理 → 数据访问层查询 → 逐级返回 → 页面响应`。
3. **只有一次真正落库**：通常只有"查询/写入某表"那一条消息到达最右列（数据访问层之后不再延伸）。
4. **请求与返回要配对**：每条向下游的请求，后面都应有对应的返回（虚线空心箭头）。
5. **序号连续**：1、2、3……写在消息文字最前面，与后文"文字叙述"一一对应，方便正文逐条解释。

---

## 五、命名与文案

| 场景 | 正确 | 错误 |
|------|------|------|
| 生命线 | `:控制层`、`:数据访问层` | `:AuthController`、`:Repository` |
| 请求消息 | `3.校验账号与密码` | `3.existsByUsername()` |
| 落库消息 | `4.查询用户表` | `4.SELECT * FROM users` |
| 返回消息 | `6.返回校验结果` | `6.return AuthResponse` |
| 角色 | `:用户`、`:商家`、`:管理员` | `User`、`Admin` |

正文里与该图配套的说明文字也要同步"去英文化"：
写"后端控制层依次完成账号是否存在、密码是否正确两项校验"，
不要写"后端 AuthController 调用 authRepository.existsByUsername 校验"。

---

## 六、自查清单

- [ ] 只输出 `<mxfile>`…`</mxfile>`，不含多余文字
- [ ] 含 `id="0"` / `id="1"` 两个结构单元
- [ ] **所有 ID 唯一**（火柴人 `P0_a` 与标签框 `P0` 不能同名——重名会让 draw.io 报 `Duplicate ID` 打不开）
- [ ] 浮动边（生命线、消息）有 `sourcePoint`/`targetPoint`；连接边有 `source`/`target`
- [ ] 顶点有 `vertex="1"` 与 `x,y,width,height`；边有 `edge="1"` 与 `relative="1"`
- [ ] 全部中文，无类名/方法名/SQL；生命线用 `:角色名`
- [ ] 请求实线实心、返回虚线空心，序号连续
- [ ] 图形都是白底黑线，`fillColor=#FFFFFF` 而非 `none`
