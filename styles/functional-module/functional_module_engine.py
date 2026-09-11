#!/usr/bin/env python3
"""
JSON-to-Drawio Functional Module Diagram Generator
====================================================
Based on hierarchical layout engine. Reads JSON DSL, auto-layouts system/role/function
hierarchy, outputs standard draw.io XML.

Usage:
    python functional_module_drawio_engine.py input.json output.drawio
"""
import json
import math
import sys
from typing import Dict, List
from dataclasses import dataclass, field


# ═══════════════════════════════════════════════════════════════
# Data Models
# ═══════════════════════════════════════════════════════════════

@dataclass
class Role:
    id: str
    name: str
    functions: List[str] = field(default_factory=list)


@dataclass
class DiagramConfig:
    sys_box_height: int = 40
    sys_box_font_size: int = 16

    role_box_width: int = 90
    role_box_height: int = 36
    role_box_font_size: int = 13

    func_box_width: int = 30
    func_box_height: int = 120
    func_font_size: int = 12
    func_char_spacing: int = 16

    level_gap: int = 20
    func_gap: int = 5
    role_gap: int = 20

    line_width: float = 1.5

    margin: int = 50


# ═══════════════════════════════════════════════════════════════
# Hierarchical Layout Engine
# ═══════════════════════════════════════════════════════════════

class HierarchyLayoutEngine:
    def __init__(self, config: DiagramConfig = None):
        self.config = config or DiagramConfig()
        self.system_name: str = ""
        self.roles: List[Role] = []
        self.sys_box: Dict = {}
        self.role_boxes: List[Dict] = []
        self.func_boxes: List[Dict] = []
        self.lines: List[Dict] = []
        self.canvas_width: int = 0
        self.canvas_height: int = 0

    def parse_input(self, data: dict) -> None:
        self.system_name = data.get("system_name", "System")
        self.roles = []
        for r_data in data.get("roles", []):
            role = Role(
                id=r_data.get("id", r_data.get("name", "")),
                name=r_data.get("name", ""),
                functions=r_data.get("functions", []),
            )
            self.roles.append(role)

    def _calc_func_box_height(self, text: str) -> float:
        cfg = self.config
        return max(cfg.func_box_height, len(text) * cfg.func_char_spacing + 20)

    def _calculate_positions(self) -> None:
        cfg = self.config
        if not self.roles:
            text_width = len(self.system_name) * cfg.sys_box_font_size + 40
            self.sys_box = {
                "x": cfg.margin, "y": cfg.margin,
                "w": text_width, "h": cfg.sys_box_height,
                "cx": cfg.margin + text_width / 2, "cy": cfg.margin + cfg.sys_box_height / 2,
                "text": self.system_name,
            }
            self.canvas_width = int(text_width + cfg.margin * 2)
            self.canvas_height = cfg.sys_box_height + cfg.margin * 2
            return

        # Step 1: Calculate each role group width
        role_group_widths = []
        for role in self.roles:
            if role.functions:
                total_func_width = len(role.functions) * cfg.func_box_width + (len(role.functions) - 1) * cfg.func_gap
            else:
                total_func_width = 0
            group_width = max(cfg.role_box_width, total_func_width)
            role_group_widths.append(group_width)

        # Step 2: Calculate system box (L0) — text-fitted width, not content width
        total_content_width = sum(role_group_widths) + (len(self.roles) - 1) * cfg.role_gap
        text_width = len(self.system_name) * cfg.sys_box_font_size + 40
        sys_box_width = text_width  # only text width + padding, NOT max with content
        sys_cx = cfg.margin + total_content_width / 2  # center over content area
        sys_x = sys_cx - sys_box_width / 2
        sys_y = cfg.margin
        sys_cy = sys_y + cfg.sys_box_height / 2
        self.sys_box = {
            "x": sys_x, "y": sys_y,
            "w": sys_box_width, "h": cfg.sys_box_height,
            "cx": sys_cx, "cy": sys_cy,
            "text": self.system_name,
        }

        # Step 3: Calculate role boxes (L1)
        role_y = sys_y + cfg.sys_box_height + cfg.level_gap
        self.role_boxes = []
        role_center_xs = []
        current_x = cfg.margin

        for i, role in enumerate(self.roles):
            group_width = role_group_widths[i]
            role_box_x = current_x + (group_width - cfg.role_box_width) / 2
            role_cx = role_box_x + cfg.role_box_width / 2
            self.role_boxes.append({
                "x": role_box_x, "y": role_y,
                "w": cfg.role_box_width, "h": cfg.role_box_height,
                "cx": role_cx, "cy": role_y + cfg.role_box_height / 2,
                "text": role.name,
                "role_index": i,
            })
            role_center_xs.append(role_cx)
            current_x += group_width + cfg.role_gap

        # Step 4: Calculate function boxes (L2)
        func_y = role_y + cfg.role_box_height + cfg.level_gap
        self.func_boxes = []
        current_x = cfg.margin

        for i, role in enumerate(self.roles):
            group_width = role_group_widths[i]
            num_funcs = len(role.functions)
            if num_funcs > 0:
                total_func_width = num_funcs * cfg.func_box_width + (num_funcs - 1) * cfg.func_gap
                func_start_x = current_x + (group_width - total_func_width) / 2

                for j, func_name in enumerate(role.functions):
                    fx = func_start_x + j * (cfg.func_box_width + cfg.func_gap)
                    fh = self._calc_func_box_height(func_name)
                    self.func_boxes.append({
                        "x": fx, "y": func_y,
                        "w": cfg.func_box_width, "h": fh,
                        "cx": fx + cfg.func_box_width / 2,
                        "cy": func_y + fh / 2,
                        "text": func_name,
                        "role_index": i,
                    })
            current_x += group_width + cfg.role_gap

        # Step 5: Calculate connections (tree branches)
        self.lines = []

        # L0 -> L1 connections
        sys_bottom_y = sys_y + cfg.sys_box_height
        branch_y = sys_bottom_y + cfg.level_gap / 2

        self.lines.append({
            "x1": sys_cx, "y1": sys_bottom_y,
            "x2": sys_cx, "y2": branch_y,
        })

        if len(role_center_xs) > 1:
            left_x = min(role_center_xs)
            right_x = max(role_center_xs)
            self.lines.append({
                "x1": left_x, "y1": branch_y,
                "x2": right_x, "y2": branch_y,
            })

        for rcx in role_center_xs:
            self.lines.append({
                "x1": rcx, "y1": branch_y,
                "x2": rcx, "y2": role_y,
            })

        # L1 -> L2 connections (per role)
        for i, role_box in enumerate(self.role_boxes):
            role_funcs = [fb for fb in self.func_boxes if fb["role_index"] == i]
            if not role_funcs:
                continue

            role_bottom_y = role_box["y"] + role_box["h"]
            func_branch_y = role_bottom_y + cfg.level_gap / 2

            self.lines.append({
                "x1": role_box["cx"], "y1": role_bottom_y,
                "x2": role_box["cx"], "y2": func_branch_y,
            })

            func_cxs = [fb["cx"] for fb in role_funcs]
            if len(func_cxs) > 1:
                left_x = min(func_cxs)
                right_x = max(func_cxs)
                self.lines.append({
                    "x1": left_x, "y1": func_branch_y,
                    "x2": right_x, "y2": func_branch_y,
                })

            for fcx in func_cxs:
                self.lines.append({
                    "x1": fcx, "y1": func_branch_y,
                    "x2": fcx, "y2": func_y,
                })

        # Step 6: Calculate canvas size + offset
        all_x = [self.sys_box["x"]]
        all_y = [self.sys_box["y"]]
        all_x.append(self.sys_box["x"] + self.sys_box["w"])
        all_y.append(self.sys_box["y"] + self.sys_box["h"])

        for rb in self.role_boxes:
            all_x.extend([rb["x"], rb["x"] + rb["w"]])
            all_y.extend([rb["y"], rb["y"] + rb["h"]])

        for fb in self.func_boxes:
            all_x.extend([fb["x"], fb["x"] + fb["w"]])
            all_y.extend([fb["y"], fb["y"] + fb["h"]])

        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)

        self.canvas_width = int(max_x - min_x + cfg.margin * 2)
        self.canvas_height = int(max_y - min_y + cfg.margin * 2)

        offset_x = cfg.margin - min_x
        offset_y = cfg.margin - min_y

        self.sys_box["x"] += offset_x
        self.sys_box["y"] += offset_y
        self.sys_box["cx"] += offset_x
        self.sys_box["cy"] += offset_y

        for rb in self.role_boxes:
            rb["x"] += offset_x
            rb["y"] += offset_y
            rb["cx"] += offset_x
            rb["cy"] += offset_y

        for fb in self.func_boxes:
            fb["x"] += offset_x
            fb["y"] += offset_y
            fb["cx"] += offset_x
            fb["cy"] += offset_y

        for line in self.lines:
            line["x1"] += offset_x
            line["y1"] += offset_y
            line["x2"] += offset_x
            line["y2"] += offset_y

    def layout(self, data: dict) -> None:
        self.parse_input(data)
        self._calculate_positions()


# ═══════════════════════════════════════════════════════════════
# Draw.io XML Renderer
# ═══════════════════════════════════════════════════════════════

class DrawioXMLRenderer:
    """Renders layout result to draw.io (diagrams.net) XML format."""

    SYS_STYLE = (
        "rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;"
        "fontSize=16;fontStyle=1;align=center;verticalAlign=middle;strokeWidth=2;"
    )
    ROLE_STYLE = (
        "rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;"
        "fontSize=13;fontStyle=1;align=center;verticalAlign=middle;strokeWidth=1.5;"
    )
    FUNC_STYLE = (
        "rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;"
        "fontSize=12;align=center;verticalAlign=middle;strokeWidth=1;"
    )
    LINE_STYLE = "endArrow=none;html=1;strokeColor=#000000;"

    def __init__(self, config: DiagramConfig = None):
        self.config = config or DiagramConfig()

    @staticmethod
    def _xml_escape(s: str) -> str:
        return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                 .replace('"', "&quot;"))

    @staticmethod
    def _make_vertical_html(text: str) -> str:
        """Convert text to vertical display using <br> tags."""
        return "<br>".join(text)

    def render(self, engine: HierarchyLayoutEngine) -> str:
        parts = []
        parts.append('<?xml version="1.0" encoding="UTF-8"?>')
        parts.append('<mxfile host="drawio">')
        parts.append('  <diagram id="functional-module" name="Functional Module">')
        parts.append(
            f'    <mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1" '
            f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
            f'pageWidth="{engine.canvas_width}" pageHeight="{engine.canvas_height}" '
            f'math="0" shadow="0">'
        )
        parts.append('      <root>')
        parts.append('        <mxCell id="0"/>')
        parts.append('        <mxCell id="1" parent="0"/>')

        cid = 2

        def add_vertex(cell_id, value, style, x, y, w, h):
            parts.append(
                f'    <mxCell id="{cell_id}" value="{DrawioXMLRenderer._xml_escape(value)}" '
                f'style="{style}" vertex="1" parent="1">'
            )
            parts.append(
                f'      <mxGeometry x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" as="geometry"/>'
            )
            parts.append('    </mxCell>')

        def add_line(line_id, x1, y1, x2, y2):
            parts.append(
                f'    <mxCell id="{line_id}" style="{DrawioXMLRenderer.LINE_STYLE}" '
                f'edge="1" parent="1">'
            )
            parts.append('      <mxGeometry relative="1" as="geometry">')
            parts.append(f'        <mxPoint x="{x1:.1f}" y="{y1:.1f}" as="sourcePoint"/>')
            parts.append(f'        <mxPoint x="{x2:.1f}" y="{y2:.1f}" as="targetPoint"/>')
            parts.append('      </mxGeometry>')
            parts.append('    </mxCell>')

        # ── Lines (bottom layer) ──
        for line in engine.lines:
            add_line(cid, line["x1"], line["y1"], line["x2"], line["y2"])
            cid += 1

        # ── System box (L0) ──
        sb = engine.sys_box
        add_vertex(cid, sb["text"], self.SYS_STYLE,
                   sb["x"], sb["y"], sb["w"], sb["h"])
        cid += 1

        # ── Role boxes (L1) ──
        for rb in engine.role_boxes:
            add_vertex(cid, rb["text"], self.ROLE_STYLE,
                       rb["x"], rb["y"], rb["w"], rb["h"])
            cid += 1

        # ── Function boxes (L2, vertical text) ──
        for fb in engine.func_boxes:
            vertical_html = self._make_vertical_html(fb["text"])
            add_vertex(cid, vertical_html, self.FUNC_STYLE,
                       fb["x"], fb["y"], fb["w"], fb["h"])
            cid += 1

        parts.append('      </root>')
        parts.append('    </mxGraphModel>')
        parts.append('  </diagram>')
        parts.append('</mxfile>')

        return "\n".join(parts)


# ═══════════════════════════════════════════════════════════════
# Main Interface
# ═══════════════════════════════════════════════════════════════

class FunctionalModuleDiagram:
    def __init__(self, config: DiagramConfig = None):
        self.config = config or DiagramConfig()
        self.engine = HierarchyLayoutEngine(self.config)
        self.renderer = DrawioXMLRenderer(self.config)

    def from_dict(self, data: dict) -> "FunctionalModuleDiagram":
        self.engine.layout(data)
        return self

    def from_json(self, json_str: str) -> "FunctionalModuleDiagram":
        return self.from_dict(json.loads(json_str))

    def from_json_file(self, filepath: str) -> "FunctionalModuleDiagram":
        with open(filepath, "r", encoding="utf-8") as f:
            return self.from_dict(json.load(f))

    def to_drawio(self) -> str:
        return self.renderer.render(self.engine)

    def save_drawio(self, filepath: str) -> None:
        xml = self.to_drawio()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(xml)
        print(f"Draw.io XML saved to: {filepath}")
        print(f"  Canvas: {self.engine.canvas_width} x {self.engine.canvas_height}")
        print(f"  Roles: {len(self.engine.roles)}")
        total_funcs = sum(len(r.functions) for r in self.engine.roles)
        print(f"  Functions: {total_funcs}")

    def get_layout_info(self) -> dict:
        return {
            "canvas_width": self.engine.canvas_width,
            "canvas_height": self.engine.canvas_height,
            "system_name": self.engine.system_name,
            "num_roles": len(self.engine.roles),
            "num_functions": sum(len(r.functions) for r in self.engine.roles),
        }


# ═══════════════════════════════════════════════════════════════
# CLI Entry
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) == 3:
        input_json = sys.argv[1]
        output_drawio = sys.argv[2]
        diagram = FunctionalModuleDiagram().from_json_file(input_json)
        diagram.save_drawio(output_drawio)
    else:
        # Demo
        demo_data = {
            "system_name": "咖啡管理系统",
            "roles": [
                {
                    "name": "管理员",
                    "functions": ["用户管理", "饮品管理", "分类管理", "口味标签管理", "库存管理", "顾客档案管理", "销售统计"]
                },
                {
                    "name": "员工",
                    "functions": ["登录注册", "饮品查看", "销售开单", "库存操作", "顾客管理", "个人中心"]
                },
            ]
        }
        diagram = FunctionalModuleDiagram().from_dict(demo_data)
        output = "demo_functional_module.drawio"
        diagram.save_drawio(output)
