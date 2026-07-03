# ER 图（实体关系图）生成提示词

## 任务说明

根据用户描述的实体关系，生成一个符合 draw.io 格式的传统 ER 图 XML 文件。

我一会可以会发送给你一些实体关系描述(可能是文本描述,可能是sql语句,也可能是其他格式,你要提取出实体、属性、关系等信息)，你需要根据这些描述生成一个符合 draw.io 格式的传统 ER 图 XML 文件。

---

## ER 图元素类型

### 1. 实体（Entity）

用矩形表示：

```xml
<mxCell id="entity1" value="实体名" 
        style="rounded=0;whiteSpace=wrap;html=1;fontSize=24;" 
        vertex="1" parent="1">
  <mxGeometry height="60" width="120" x="X坐标" y="Y坐标" as="geometry" />
</mxCell>
```

- `height="60"` - 高度 60px
- `width="120"` - 宽度 120px(根据实际情况调整,比如实体名比较长,需要调整宽度)
- `fontSize=24` - 字体大小 24

### 2. 属性（Attribute）

用椭圆表示：

```xml
<mxCell id="attr1" value="属性名" 
        style="ellipse;whiteSpace=wrap;html=1;fontSize=24;" 
        vertex="1" parent="1">
  <mxGeometry height="80" width="120" x="X坐标" y="Y坐标" as="geometry" />
</mxCell>
```

- `ellipse` - 椭圆形状
- `height="80"` - 高度 80px
- `width="120"` - 宽度 120px(根据实际情况调整,比如属性名比较长,需要调整宽度)

**主键属性**可以用 `<font>` 标签加粗或添加下划线，例如：
```xml
value="&lt;font&gt;学号&lt;/font&gt;"
```

### 3. 关系（Relationship）

用菱形表示：

```xml
<mxCell id="rel1" value="关系名" 
        style="rhombus;whiteSpace=wrap;html=1;fontSize=24;" 
        vertex="1" parent="1">
  <mxGeometry height="80" width="110" x="X坐标" y="Y坐标" as="geometry" />
</mxCell>
```

- `rhombus` - 菱形
- `height="80"` - 高度 80px
- `width="135"` - 宽度 135px左右(根据实际情况调整,比如关系名比较长,需要调整宽度)

### 4. 基数标注（Cardinality）

将基数标注（1, m, n 等）写在边的 value 属性上，或者作为边标签（edgeLabel）：

- 直接写在边的 value 属性上（推荐）：**
```xml
<mxCell id="edge1" edge="1" parent="1" source="entity1" target="rel1"
        style="endArrow=none;html=1;rounded=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;fontSize=24;" 
        value="m">
  <mxGeometry height="50" relative="1" width="50" as="geometry">
    <mxPoint x="X1" y="Y1" as="sourcePoint" />
    <mxPoint x="X2" y="Y2" as="targetPoint" />
  </mxGeometry>
</mxCell>
```

- 直接将基数写在边的 value 属性上
- 字体大小：`fontSize=24`
- 基数标注可以是：1, m, n, 1:1, 1:n, n:m 等

---

## 边（Edge）的连接

### 1. 实体与属性连接

- 连接线是直线,不是正交线

```xml
<mxCell id="edge1" edge="1" parent="1" source="entity1" target="attr1"
        style="rounded=0;jettySize=auto;html=1;endArrow=none;endFill=0;fontSize=24;">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### 2. 实体与关系连接（带基数标注）

- 连接线是直线,不是正交线

```xml
<mxCell id="edge2" edge="1" parent="1" source="entity1" target="rel1"
        style="endArrow=none;html=1;rounded=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;fontSize=24;" 
        value="m">
  <mxGeometry height="50" relative="1" width="50" as="geometry">
    <mxPoint x="X1" y="Y1" as="sourcePoint" />
    <mxPoint x="X2" y="Y2" as="targetPoint" />
  </mxGeometry>
</mxCell>
```


### 3. 边样式说明

- `endArrow=none` - 无箭头
- `endFill=0` - 不填充
- `fontSize=24` - 字体大小 24
- `rounded=0` - 不圆角
- `jettySize=auto` - 自动 jetty 大小

---

## 布局建议

### 实体布局
- 将主要实体放在中心或突出位置
- 不要出现大片空白地方没有实体的情况，比如实体之间距离过远，导致中央出现很大区域的空白。

### 属性布局
- 属性围绕实体分布

### 关系布局
- 菱形关系放在相关实体之间
- 你需要合理的设计不同属性之间的位置,来避免属性标签重叠,或者关系线交叉.一定确保关系线之间不交叉.
---

## 完整示例结构

参考：

```xml
<mxfile host="app.diagrams.net" agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0">
  <diagram name="RBAC ER Diagram" id="JN_Ci7z9voKf1Z_xUlJq">
    <mxGraphModel dx="-81" dy="539" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="krFXNh0SMfMHKpyPiWYL-404" edge="1" parent="1" source="krFXNh0SMfMHKpyPiWYL-407" style="rounded=0;jettySize=auto;html=1;endArrow=none;endFill=0;fontSize=24;" target="krFXNh0SMfMHKpyPiWYL-411">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-405" edge="1" parent="1" source="krFXNh0SMfMHKpyPiWYL-407" style="rounded=0;jettySize=auto;html=1;endArrow=none;endFill=0;fontSize=24;" target="krFXNh0SMfMHKpyPiWYL-410">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-406" edge="1" parent="1" source="krFXNh0SMfMHKpyPiWYL-407" style="rounded=0;jettySize=auto;html=1;endArrow=none;endFill=0;fontSize=24;" target="krFXNh0SMfMHKpyPiWYL-408">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-407" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fontSize=24;" value="学生" vertex="1">
          <mxGeometry height="60" width="120" x="1119.9964415564903" y="1064.4615384615383" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-408" parent="1" style="ellipse;whiteSpace=wrap;html=1;fontSize=24;" value="&lt;font&gt;学号&lt;/font&gt;" vertex="1">
          <mxGeometry height="80" width="120" x="1009.9964415564903" y="974.4615384615383" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-409" parent="1" style="ellipse;whiteSpace=wrap;html=1;fontSize=24;" value="年龄" vertex="1">
          <mxGeometry height="80" width="120" x="1159.9964415564903" y="964.4615384615383" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-410" parent="1" style="ellipse;whiteSpace=wrap;html=1;fontSize=24;" value="姓名" vertex="1">
          <mxGeometry height="80" width="120" x="989.9964415564903" y="1114.4615384615383" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-411" parent="1" style="ellipse;whiteSpace=wrap;html=1;fontSize=24;" value="性别" vertex="1">
          <mxGeometry height="80" width="120" x="1119.9964415564903" y="1154.4615384615383" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-412" edge="1" parent="1" source="krFXNh0SMfMHKpyPiWYL-407" style="rounded=0;jettySize=auto;html=1;entryX=0.309;entryY=0.991;entryDx=0;entryDy=0;entryPerimeter=0;endArrow=none;endFill=0;fontSize=24;" target="krFXNh0SMfMHKpyPiWYL-409">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-413" edge="1" parent="1" source="krFXNh0SMfMHKpyPiWYL-416" style="rounded=0;jettySize=auto;html=1;endArrow=none;endFill=0;fontSize=24;" target="krFXNh0SMfMHKpyPiWYL-420">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-414" edge="1" parent="1" source="krFXNh0SMfMHKpyPiWYL-416" style="rounded=0;jettySize=auto;html=1;endArrow=none;endFill=0;fontSize=24;entryX=0.593;entryY=0.042;entryDx=0;entryDy=0;entryPerimeter=0;" target="krFXNh0SMfMHKpyPiWYL-419">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1513.2722690256096" y="1425.4140560541805" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-415" edge="1" parent="1" source="krFXNh0SMfMHKpyPiWYL-416" style="rounded=0;jettySize=auto;html=1;endArrow=none;endFill=0;fontSize=24;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" target="krFXNh0SMfMHKpyPiWYL-417">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1460.2564415564902" y="1344.4615384615386" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-416" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fontSize=24;" value="老师" vertex="1">
          <mxGeometry height="60" width="120" x="1490.2564415564902" y="1314.4615384615383" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-417" parent="1" style="ellipse;whiteSpace=wrap;html=1;fontSize=24;" value="工号" vertex="1">
          <mxGeometry height="80" width="120" x="1330.2564415564902" y="1304.4615384615383" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-418" parent="1" style="ellipse;whiteSpace=wrap;html=1;fontSize=24;" value="年龄" vertex="1">
          <mxGeometry height="80" width="120" x="1660.2564415564902" y="1294.4615384615383" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-419" parent="1" style="ellipse;whiteSpace=wrap;html=1;fontSize=24;" value="姓名" vertex="1">
          <mxGeometry height="80" width="120" x="1430.2564415564902" y="1424.4615384615383" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-420" parent="1" style="ellipse;whiteSpace=wrap;html=1;fontSize=24;" value="性别" vertex="1">
          <mxGeometry height="80" width="120" x="1580.2564415564902" y="1404.4615384615383" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-421" edge="1" parent="1" source="krFXNh0SMfMHKpyPiWYL-416" style="rounded=0;jettySize=auto;html=1;endArrow=none;endFill=0;fontSize=24;" target="krFXNh0SMfMHKpyPiWYL-418">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1630.2564415564902" y="1264.4615384615383" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-422" edge="1" parent="1" source="krFXNh0SMfMHKpyPiWYL-424" style="rounded=0;jettySize=auto;html=1;endArrow=none;endFill=0;fontSize=24;" target="krFXNh0SMfMHKpyPiWYL-426">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-423" edge="1" parent="1" source="krFXNh0SMfMHKpyPiWYL-424" style="rounded=0;jettySize=auto;html=1;endArrow=none;endFill=0;fontSize=24;" target="krFXNh0SMfMHKpyPiWYL-425">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-424" parent="1" style="rounded=0;whiteSpace=wrap;html=1;fontSize=24;" value="课程" vertex="1">
          <mxGeometry height="60" width="120" x="1490.2564415564902" y="1064.4615384615383" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-425" parent="1" style="ellipse;whiteSpace=wrap;html=1;fontSize=24;" value="课程号" vertex="1">
          <mxGeometry height="80" width="120" x="1490.2564415564902" y="954.4615384615383" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-426" parent="1" style="ellipse;whiteSpace=wrap;html=1;fontSize=24;" value="课程名" vertex="1">
          <mxGeometry height="80" width="120" x="1660.2564415564902" y="1044.4615384615383" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-427" parent="1" style="rhombus;whiteSpace=wrap;html=1;fontSize=24;" value="&lt;font&gt;选修&lt;/font&gt;" vertex="1">
          <mxGeometry height="80" width="110" x="1320.2564415564902" y="1054.4615384615383" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-428" edge="1" parent="1" source="krFXNh0SMfMHKpyPiWYL-407" style="endArrow=none;html=1;rounded=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;fontSize=24;" target="krFXNh0SMfMHKpyPiWYL-427" value="">
          <mxGeometry height="50" relative="1" width="50" as="geometry">
            <mxPoint x="1410.2564415564902" y="1244.4615384615383" as="sourcePoint" />
            <mxPoint x="1460.2564415564902" y="1194.4615384615383" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-438" connectable="0" parent="krFXNh0SMfMHKpyPiWYL-428" style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=24;" value="m" vertex="1">
          <mxGeometry relative="1" x="-0.1992" y="-2" as="geometry">
            <mxPoint as="offset" />
          </mxGeometry>
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-429" edge="1" parent="1" source="krFXNh0SMfMHKpyPiWYL-427" style="endArrow=none;html=1;rounded=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;fontSize=24;" target="krFXNh0SMfMHKpyPiWYL-424" value="">
          <mxGeometry height="50" relative="1" width="50" as="geometry">
            <mxPoint x="1410.2564415564902" y="1244.4615384615383" as="sourcePoint" />
            <mxPoint x="1460.2564415564902" y="1194.4615384615383" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-439" connectable="0" parent="krFXNh0SMfMHKpyPiWYL-429" style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=24;" value="n" vertex="1">
          <mxGeometry relative="1" x="-0.3907" y="-1" as="geometry">
            <mxPoint as="offset" />
          </mxGeometry>
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-430" parent="1" style="rhombus;whiteSpace=wrap;html=1;fontSize=24;" value="讲授" vertex="1">
          <mxGeometry height="80" width="135" x="1482.7564415564902" y="1168.4615384615383" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-431" edge="1" parent="1" source="krFXNh0SMfMHKpyPiWYL-430" style="endArrow=none;html=1;rounded=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;fontSize=24;" target="krFXNh0SMfMHKpyPiWYL-424" value="">
          <mxGeometry height="50" relative="1" width="50" as="geometry">
            <mxPoint x="1420.2564415564902" y="1284.4615384615383" as="sourcePoint" />
            <mxPoint x="1470.2564415564902" y="1234.4615384615383" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-440" connectable="0" parent="krFXNh0SMfMHKpyPiWYL-431" style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=24;" value="n" vertex="1">
          <mxGeometry relative="1" x="0.0243" y="2" as="geometry">
            <mxPoint as="offset" />
          </mxGeometry>
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-432" edge="1" parent="1" source="krFXNh0SMfMHKpyPiWYL-416" style="endArrow=none;html=1;rounded=0;exitX=0.5;exitY=0;exitDx=0;exitDy=0;fontSize=24;" target="krFXNh0SMfMHKpyPiWYL-430" value="">
          <mxGeometry height="50" relative="1" width="50" as="geometry">
            <mxPoint x="1420.2564415564902" y="1284.4615384615383" as="sourcePoint" />
            <mxPoint x="1470.2564415564902" y="1234.4615384615383" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-442" connectable="0" parent="krFXNh0SMfMHKpyPiWYL-432" style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=24;" value="1" vertex="1">
          <mxGeometry relative="1" x="0.1282" as="geometry">
            <mxPoint as="offset" />
          </mxGeometry>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```


1. **学生** 实体（矩形）
   - 属性：学号（椭圆，带下划线）、姓名、年龄、性别
   
2. **老师** 实体（矩形）
   - 属性：工号、姓名、年龄、性别
   
3. **课程** 实体（矩形）
   - 属性：课程号、课程名
   
4. **关系**：
   - 选修（菱形，连接学生和课程）
   - 讲授（菱形，连接老师和课程）
   
5. **基数**：
   - 学生-选修：m
   - 选修-课程：n
   - 老师-讲授：n
   - 讲授-课程：1

---

## 输出要求

- 只输出 XML 代码，以 `<mxfile>` 开头，`</mxfile>` 结尾，可以直接保存为 .drawio 文件使用

- 此外还需要注意,样式需要完全参考上面的完整示例,比如字体要24px,然后方框要直角,并且椭圆和方块以及棱形的大小,在关系线上要写对应关系,是m,n,还是1,1,还是1,n,还是n,1.等等,都需要完全参考上面的示例。除非用户特别要求,否则不能改变任何样式。

- 此外需要注意,你需要写中文,无论是属性,关系,还是实体.除非用户特别要求,否则一律写中文.

- 不同方块,棱形,椭圆,线之间尽量不要出现重叠.
- 请再三确保元素之间距离足够大,来避免属性标签重叠,或者关系线交叉.
- 再三确保属性没有重叠,线没有交叉.