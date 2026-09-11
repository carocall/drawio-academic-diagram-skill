# 用例图生成提示词

## 任务说明

根据用户描述的系统用例，生成一个符合 draw.io 格式的用例图 XML 文件。

我一会可以会发送给你一些用例描述(可能是文本描述,可能是代码片段,也可能是论文里面的功能描述,也可能是其他格式,你要提取出角色和用例名)，你需要根据这些描述生成一个符合 draw.io 格式的用例图 XML 文件。
---

## 图元素类型

### 1. 参与者（Actor）

用 UML 小人形状表示：

```xml
<mxCell id="actor1" value="参与者名称" 
        style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;" 
        vertex="1" parent="1">
  <mxGeometry height="60" width="30" x="X坐标" y="Y坐标" as="geometry" />
</mxCell>
```

- `shape=umlActor` - UML 参与者形状（小人）
- `height="60"` - 高度 60px
- `width="30"` - 宽度 30px
- `verticalLabelPosition=bottom` - 标签在底部
- `verticalAlign=top` - 垂直对齐顶部
- `outlineConnect=0` - 轮廓连接

### 2. 用例（Use Case）

用椭圆表示：

```xml
<mxCell id="usecase1" value="用例名称" 
        style="ellipse;whiteSpace=wrap;html=1;fontSize=16;" 
        vertex="1" parent="1">
  <mxGeometry height="80" width="120" x="X坐标" y="Y坐标" as="geometry" />
</mxCell>
```

- `ellipse` - 椭圆形状
- `height="80"` - 高度 80px
- `width="120"` - 宽度 120px
- `fontSize=16` - 字体大小 16
- 可以用 HTML 标签：`value="&lt;span&gt;用例名称&lt;/span&gt;"`

记住这里保持默认的白色背景，不要添加其他样式。
---

## 边（Edge）的连接

参与者与用例之间、用例与用例之间用无箭头边连接：

```xml
<mxCell id="edge1" edge="1" parent="1" source="node1" target="node2"
        style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;endArrow=none;endFill=0;">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### 边样式说明
- `endArrow=none` - 无箭头
- `endFill=0` - 不填充
- `entryX=0; entryY=0.5` - 入口位置在左侧中心
- `rounded=0` - 不圆角
- `orthogonalLoop=1` - 正交循环
- `jettySize=auto` - 自动 jetty 大小

---

## 布局建议

### 参与者
- 放在图的左侧
- x 坐标约 50-100
- 多个参与者垂直排列，间距约 150-200px

### 用例
- 放在参与者的右侧(如果用例比较多,可以放一部分在参与者右侧,一部分在左侧.尽量保证用例与参与者的距离足够大,避免线或者用例重叠)
- 用例之间垂直排列，间距约 80-120px
- 如果有多级用例,比如作品管理包含作品上传,作品下载,作品删除等子例.那么可以将子例放在父例的右侧(如果这个用例在参与者右边)或者左边(如果这个用例在参与者左边),并用无箭头边连接起来.

---

## 完整示例结构

参考 ：

```xml
<mxfile host="app.diagrams.net" agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0">
  <diagram name="RBAC ER Diagram" id="JN_Ci7z9voKf1Z_xUlJq">
    <mxGraphModel dx="1320" dy="954" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="krFXNh0SMfMHKpyPiWYL-397" edge="1" parent="1" source="krFXNh0SMfMHKpyPiWYL-381" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;endArrow=none;endFill=0;" target="krFXNh0SMfMHKpyPiWYL-392">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-398" edge="1" parent="1" source="krFXNh0SMfMHKpyPiWYL-381" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;endArrow=none;endFill=0;" target="krFXNh0SMfMHKpyPiWYL-391">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-399" edge="1" parent="1" source="krFXNh0SMfMHKpyPiWYL-381" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;endFill=0;" target="krFXNh0SMfMHKpyPiWYL-393">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-381" parent="1" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;" value="用户" vertex="1">
          <mxGeometry height="60" width="30" x="80" y="630" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-391" parent="1" style="ellipse;whiteSpace=wrap;html=1;fontSize=16;" value="&lt;span&gt;登录&lt;/span&gt;" vertex="1">
          <mxGeometry height="80" width="120" x="240" y="620" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-392" parent="1" style="ellipse;whiteSpace=wrap;html=1;fontSize=16;" value="&lt;span&gt;注册&lt;/span&gt;" vertex="1">
          <mxGeometry height="80" width="120" x="240" y="520" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-402" edge="1" parent="1" source="krFXNh0SMfMHKpyPiWYL-393" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;endFill=0;" target="krFXNh0SMfMHKpyPiWYL-395">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-403" edge="1" parent="1" source="krFXNh0SMfMHKpyPiWYL-393" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;endArrow=none;endFill=0;" target="krFXNh0SMfMHKpyPiWYL-396">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-393" parent="1" style="ellipse;whiteSpace=wrap;html=1;fontSize=16;" value="&lt;span&gt;作品管理&lt;/span&gt;" vertex="1">
          <mxGeometry height="80" width="120" x="240" y="730" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-394" parent="1" style="ellipse;whiteSpace=wrap;html=1;fontSize=16;" value="删除作品" vertex="1">
          <mxGeometry height="80" width="120" x="430" y="630" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-395" parent="1" style="ellipse;whiteSpace=wrap;html=1;fontSize=16;" value="&lt;span&gt;添加作品&lt;/span&gt;" vertex="1">
          <mxGeometry height="80" width="120" x="440" y="730" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-396" parent="1" style="ellipse;whiteSpace=wrap;html=1;fontSize=16;" value="&lt;span&gt;修改作品&lt;/span&gt;" vertex="1">
          <mxGeometry height="80" width="120" x="430" y="820" as="geometry" />
        </mxCell>
        <mxCell id="krFXNh0SMfMHKpyPiWYL-401" edge="1" parent="1" source="krFXNh0SMfMHKpyPiWYL-393" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;endFill=0;" target="krFXNh0SMfMHKpyPiWYL-394">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

1. **参与者**：
   - 用户（UML 小人，左侧）
   
2. **用例**：
   - 登录（椭圆）
   - 注册（椭圆）
   - 作品管理（椭圆）
   - 删除作品（椭圆）
   - 添加作品（椭圆）
   - 修改作品（椭圆）
   
3. **连接关系**：
   - 用户 → 登录
   - 用户 → 注册
   - 用户 → 作品管理
   - 作品管理 → 删除作品
   - 作品管理 → 添加作品
   - 作品管理 → 修改作品

---

## 输出要求

只输出 XML 代码，以 `<mxfile>` 开头，`</mxfile>` 结尾，可以直接保存为 .drawio 文件使用。

同一级的用例保持x轴数值一致,每下一级,x轴向右移动一些.
比如：
- 登录、注册、作品管理
- 删除作品、添加作品、修改作品

其中：
- 登录、注册、作品管理 是同一级的用例
- 删除作品、添加作品、修改作品 是下一级的用例
也要把删除作品、添加作品、修改作品连接到作品管理用例。

可以适当调节椭圆大小,保证字不会超出椭圆.

尽量不要出元素重叠,可以适当调整元素位置.

样式尽量参考我给你的示例,不要添加其他样式。