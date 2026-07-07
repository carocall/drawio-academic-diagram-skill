#!/usr/bin/env python3
"""
JSON-to-Drawio ER Diagram Generator
====================================
Based on radial layout engine with Barycenter Heuristic. 
Reads JSON DSL, auto-layouts entities/relationships/attributes, 
outputs standard draw.io XML.

Usage:
    python er_drawio_engine.py input.json output.drawio
"""
import json
import math
import random
import sys
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum


# ═══════════════════════════════════════════════════════════════
# Data Models
# ═══════════════════════════════════════════════════════════════

class Cardinality(Enum):
    ONE_TO_ONE = "1:1"
    ONE_TO_MANY = "1:N"
    MANY_TO_MANY = "N:M"
    MANY_TO_ONE = "N:1"


@dataclass
class Attribute:
    name: str
    type: str = "string"
    is_primary_key: bool = False
    is_foreign_key: bool = False
    x: float = 0
    y: float = 0


@dataclass
class Entity:
    id: str
    attributes: List[Attribute] = field(default_factory=list)
    x: float = 0
    y: float = 0
    width: float = 110
    height: float = 40


@dataclass
class Relationship:
    id: str
    from_entity: str
    to_entity: str
    cardinality: Cardinality
    x: float = 0
    y: float = 0
    width: float = 90
    height: float = 44


@dataclass
class LayoutConfig:
    # Radial layout parameters
    layer_spacing: float = 220
    min_entity_spacing: float = 60
    
    # Node sizes
    entity_width: int = 110
    entity_height: int = 40
    rel_width: int = 90
    rel_height: int = 44
    attr_ellipse_rx: int = 35
    attr_ellipse_ry: int = 12
    attr_spacing: int = 30

    # Canvas
    margin: int = 80
    padding: int = 50

    # Barycenter heuristic iterations
    barycenter_iterations: int = 15


# ═══════════════════════════════════════════════════════════════
# Geometry Helpers
# ═══════════════════════════════════════════════════════════════

def _segments_intersect(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
    def cross(ox, oy, px, py, qx, qy):
        return (px - ox) * (qy - oy) - (py - oy) * (qx - ox)
    d1 = cross(bx1, by1, bx2, by2, ax1, ay1)
    d2 = cross(bx1, by1, bx2, by2, ax2, ay2)
    d3 = cross(ax1, ay1, ax2, ay2, bx1, by1)
    d4 = cross(ax1, ay1, ax2, ay2, bx2, by2)
    return ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
           ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0))


def _segment_distance(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
    def dot(ax, ay, bx, by): return ax * bx + ay * by
    def cross(ax, ay, bx, by): return ax * by - ay * bx
    def clamp(v, lo, hi): return max(lo, min(hi, v))
    dx, dy = ax2 - ax1, ay2 - ay1
    ex, ey = bx2 - bx1, by2 - by1
    fx, fy = ax1 - bx1, ay1 - by1
    a = dot(dx, dy, dx, dy)
    b = dot(dx, dy, ex, ey)
    e = dot(ex, ey, ex, ey)
    c = dot(dx, dy, fx, fy)
    f = dot(ex, ey, fx, fy)
    denom = a * e - b * b
    if denom < 0.001:
        d1 = dot(dx, dy, bx1 - ax1, by1 - ay1)
        d2 = dot(dx, dy, bx2 - ax1, by2 - ay1)
        t1 = clamp(d1 / (a + 0.001), 0, 1)
        t2 = clamp(d2 / (a + 0.001), 0, 1)
        px1, py1 = ax1 + t1 * dx, ay1 + t1 * dy
        px2, py2 = ax1 + t2 * dx, ay1 + t2 * dy
        return math.sqrt((px1 - px2) ** 2 + (py1 - py2) ** 2)
    s = clamp((b * f - c * e) / denom, 0, 1)
    t = clamp((a * f - c * b) / denom, 0, 1)
    px, py = ax1 + s * dx, ay1 + s * dy
    qx, qy = bx1 + t * ex, by1 + t * ey
    return math.sqrt((px - qx) ** 2 + (py - qy) ** 2)


# ═══════════════════════════════════════════════════════════════
# Radial Layout Engine with Barycenter Heuristic
# ═══════════════════════════════════════════════════════════════

class RadialLayoutEngine:
    def __init__(self, config: Optional[LayoutConfig] = None):
        self.config = config or LayoutConfig()
        self.entities: Dict[str, Entity] = {}
        self.relationships: Dict[str, Relationship] = {}
        self.canvas_width: int = 0
        self.canvas_height: int = 0

    def parse_input(self, data: dict) -> None:
        self.entities = {}
        self.relationships = {}
        for e_data in data.get("entities", []):
            attributes = []
            for attr_data in e_data.get("attributes", []):
                if isinstance(attr_data, str):
                    attributes.append(Attribute(name=attr_data))
                elif isinstance(attr_data, dict):
                    attributes.append(Attribute(
                        name=attr_data.get("name", ""),
                        type=attr_data.get("type", "string"),
                        is_primary_key=attr_data.get("is_primary_key", False),
                        is_foreign_key=attr_data.get("is_foreign_key", False),
                    ))
            self.entities[e_data["id"]] = Entity(
                id=e_data["id"], attributes=attributes,
                width=self.config.entity_width, height=self.config.entity_height,
            )
        for r_data in data.get("relationships", []):
            self.relationships[r_data["id"]] = Relationship(
                id=r_data["id"],
                from_entity=r_data["from"],
                to_entity=r_data["to"],
                cardinality=Cardinality(r_data.get("cardinality", "1:N")),
                width=self.config.rel_width, height=self.config.rel_height,
            )

    def _build_entity_graph(self) -> Tuple[Dict[str, Set[str]], Dict[str, int]]:
        adjacency: Dict[str, Set[str]] = {eid: set() for eid in self.entities}
        degree: Dict[str, int] = {eid: 0 for eid in self.entities}
        for rel in self.relationships.values():
            adjacency[rel.from_entity].add(rel.to_entity)
            adjacency[rel.to_entity].add(rel.from_entity)
            degree[rel.from_entity] += 1
            degree[rel.to_entity] += 1
        return adjacency, degree

    def _find_connected_components(self, adjacency: Dict[str, Set[str]]) -> List[List[str]]:
        visited = set()
        components = []
        for eid in self.entities:
            if eid not in visited:
                component = []
                queue = [eid]
                visited.add(eid)
                while queue:
                    curr = queue.pop(0)
                    component.append(curr)
                    for neighbor in adjacency.get(curr, set()):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                components.append(component)
        return components

    def _find_center_node(self, component: List[str], degree: Dict[str, int]) -> str:
        max_degree = -1
        center = component[0]
        for eid in component:
            if degree[eid] > max_degree:
                max_degree = degree[eid]
                center = eid
        return center

    def _bfs_layering(self, center: str, adjacency: Dict[str, Set[str]]) -> Dict[str, int]:
        layers: Dict[str, int] = {center: 0}
        queue = [(center, 0)]
        while queue:
            curr, curr_layer = queue.pop(0)
            for neighbor in adjacency.get(curr, set()):
                if neighbor not in layers:
                    layers[neighbor] = curr_layer + 1
                    queue.append((neighbor, curr_layer + 1))
        return layers

    def _barycenter_heuristic(self, layers: Dict[str, int], adjacency: Dict[str, Set[str]]) -> Dict[int, List[str]]:
        layer_nodes: Dict[int, List[str]] = {}
        for eid, layer in layers.items():
            if layer not in layer_nodes:
                layer_nodes[layer] = []
            layer_nodes[layer].append(eid)
        max_layer = max(layers.values())

        for _ in range(self.config.barycenter_iterations):
            for layer in range(1, max_layer + 1):
                if layer not in layer_nodes:
                    continue
                node_positions = {eid: i for i, eid in enumerate(layer_nodes.get(layer - 1, []))}
                weighted_positions = []
                for node in layer_nodes[layer]:
                    neighbors = adjacency.get(node, set())
                    valid_neighbors = [n for n in neighbors if n in node_positions]
                    if valid_neighbors:
                        avg_pos = sum(node_positions[n] for n in valid_neighbors) / len(valid_neighbors)
                    else:
                        avg_pos = len(layer_nodes[layer]) / 2
                    weighted_positions.append((node, avg_pos))
                weighted_positions.sort(key=lambda x: x[1])
                layer_nodes[layer] = [n for n, _ in weighted_positions]

        return layer_nodes

    def _compute_radial_coordinates(self, component: List[str], center: str, 
                                     layer_nodes: Dict[int, List[str]]) -> Dict[str, Tuple[float, float]]:
        cfg = self.config
        positions: Dict[str, Tuple[float, float]] = {}
        max_layer = max(layer_nodes.keys())

        for layer in sorted(layer_nodes.keys()):
            nodes = layer_nodes[layer]
            if layer == 0:
                positions[center] = (0.0, 0.0)
                continue
            
            radius = cfg.layer_spacing * layer
            n_nodes = len(nodes)
            if n_nodes == 1:
                positions[nodes[0]] = (radius, 0.0)
                continue

            angle_step = 2 * math.pi / n_nodes
            start_angle = -math.pi / 2
            for i, eid in enumerate(nodes):
                angle = start_angle + i * angle_step
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                positions[eid] = (x, y)

        return positions

    def _assign_component_positions(self, component: List[str], positions: Dict[str, Tuple[float, float]], 
                                    offset_x: float, offset_y: float) -> None:
        for eid in component:
            x, y = positions[eid]
            self.entities[eid].x = offset_x + x - self.entities[eid].width / 2
            self.entities[eid].y = offset_y + y - self.entities[eid].height / 2

    def _estimate_component_bounds(self, component: List[str], positions: Dict[str, Tuple[float, float]]) -> Tuple[float, float]:
        ew = self.config.entity_width
        eh = self.config.entity_height
        min_x = min(positions[eid][0] - ew/2 for eid in component)
        max_x = max(positions[eid][0] + ew/2 for eid in component)
        min_y = min(positions[eid][1] - eh/2 for eid in component)
        max_y = max(positions[eid][1] + eh/2 for eid in component)
        return max_x - min_x, max_y - min_y

    def _layout_components(self) -> None:
        adjacency, degree = self._build_entity_graph()
        components = self._find_connected_components(adjacency)

        if not components:
            return

        if len(components) == 1:
            component = components[0]
            center = self._find_center_node(component, degree)
            layers = self._bfs_layering(center, adjacency)
            layer_nodes = self._barycenter_heuristic(layers, adjacency)
            positions = self._compute_radial_coordinates(component, center, layer_nodes)
            offset_x = self.config.margin + self.config.entity_width
            offset_y = self.config.margin + self.config.entity_height
            self._assign_component_positions(component, positions, offset_x, offset_y)
            return

        all_positions = []
        for component in components:
            center = self._find_center_node(component, degree)
            layers = self._bfs_layering(center, adjacency)
            layer_nodes = self._barycenter_heuristic(layers, adjacency)
            positions = self._compute_radial_coordinates(component, center, layer_nodes)
            w, h = self._estimate_component_bounds(component, positions)
            all_positions.append((component, positions, w, h))

        all_positions.sort(key=lambda x: -(x[2] * x[3]))

        offset_y = self.config.margin + self.config.entity_height
        current_x = self.config.margin + self.config.entity_width

        for component, positions, w, h in all_positions:
            self._assign_component_positions(component, positions, current_x, offset_y)
            current_x += w + self.config.layer_spacing

    def _position_relationships(self) -> None:
        cfg = self.config
        for rel in self.relationships.values():
            if rel.from_entity == rel.to_entity:
                entity = self.entities[rel.from_entity]
                ecx = entity.x + entity.width / 2
                ecy = entity.y + entity.height / 2
                offset = cfg.layer_spacing / 2 + cfg.rel_width
                rel.x = ecx + offset - rel.width / 2
                rel.y = ecy - rel.height / 2
            else:
                a = self.entities[rel.from_entity]
                b = self.entities[rel.to_entity]
                rel.x = (a.x + a.width / 2 + b.x + b.width / 2) / 2 - rel.width / 2
                rel.y = (a.y + a.height / 2 + b.y + b.height / 2) / 2 - rel.height / 2

    def _collision_detection(self) -> None:
        cfg = self.config
        entity_list = list(self.entities.values())
        n = len(entity_list)
        for i in range(n):
            for j in range(i + 1, n):
                e1, e2 = entity_list[i], entity_list[j]
                dx = (e1.x + e1.width / 2) - (e2.x + e2.width / 2)
                dy = (e1.y + e1.height / 2) - (e2.y + e2.height / 2)
                dist = math.sqrt(dx * dx + dy * dy)
                min_dist = (e1.width + e2.width) / 2 + cfg.min_entity_spacing
                if dist < min_dist:
                    overlap = min_dist - dist
                    angle = math.atan2(dy, dx)
                    move_x = math.cos(angle) * overlap / 2
                    move_y = math.sin(angle) * overlap / 2
                    e1.x += move_x
                    e1.y += move_y
                    e2.x -= move_x
                    e2.y -= move_y

    def _position_attributes(self) -> None:
        cfg = self.config
        obstacles = []
        for entity in self.entities.values():
            obstacles.append((entity.x + entity.width / 2, entity.y + entity.height / 2,
                              max(entity.width, entity.height) / 2 + cfg.attr_ellipse_rx))
        for rel in self.relationships.values():
            obstacles.append((rel.x + rel.width / 2, rel.y + rel.height / 2,
                              max(rel.width, rel.height) / 2 + cfg.attr_ellipse_rx))
        for entity in self.entities.values():
            if not entity.attributes:
                continue
            ecx, ecy = entity.x + entity.width / 2, entity.y + entity.height / 2
            ideal_dist = cfg.attr_ellipse_rx * 3 + 30
            for attr in entity.attributes:
                best_angles = []
                for i in range(32):
                    angle = 2 * math.pi * i / 32 + random.uniform(-0.05, 0.05)
                    ax = ecx + ideal_dist * math.cos(angle)
                    ay = ecy + ideal_dist * math.sin(angle)
                    crowdedness = 0.0
                    for ox, oy, orad in obstacles:
                        if abs(ox - ecx) < 1 and abs(oy - ecy) < 1:
                            continue
                        dx, dy = ax - ox, ay - oy
                        dist = math.sqrt(dx * dx + dy * dy)
                        if dist < orad * 2:
                            crowdedness += 1000.0 / (dist + 1)
                        else:
                            crowdedness += 10.0 / (dist + 1)
                    for rel_obj in self.relationships.values():
                        ea, eb = self.entities[rel_obj.from_entity], self.entities[rel_obj.to_entity]
                        rel_cx, rel_cy = rel_obj.x + rel_obj.width / 2, rel_obj.y + rel_obj.height / 2
                        for sx1, sy1, sx2, sy2 in [
                            (ea.x + ea.width / 2, ea.y + ea.height / 2, rel_cx, rel_cy),
                            (rel_cx, rel_cy, eb.x + eb.width / 2, eb.y + eb.height / 2),
                        ]:
                            d = _segment_distance(ax, ay, ax, ay, sx1, sy1, sx2, sy2)
                            if d < 20:
                                crowdedness += 3000.0 / (d + 1)
                    best_angles.append((crowdedness, angle, ax, ay))
                best_angles.sort(key=lambda x: x[0])
                _, _, ax, ay = best_angles[0]
                attr.x = ax
                attr.y = ay
                obstacles.append((attr.x, attr.y, cfg.attr_ellipse_rx))
        all_attrs = []
        for entity in self.entities.values():
            for attr in entity.attributes:
                all_attrs.append((attr, entity))
        attr_temp = 50.0
        for _ in range(200):
            if attr_temp < 0.1:
                break
            for attr, parent_entity in all_attrs:
                fx, fy = 0.0, 0.0
                ecx, ecy = parent_entity.x + parent_entity.width / 2, parent_entity.y + parent_entity.height / 2
                dx, dy = ecx - attr.x, ecy - attr.y
                dist = math.sqrt(dx * dx + dy * dy) + 0.1
                ideal_dist = cfg.attr_ellipse_rx * 3 + 30
                force = 0.20 * (dist - ideal_dist)
                fx += force * dx / dist
                fy += force * dy / dist
                for entity in self.entities.values():
                    ent_cx, ent_cy = entity.x + entity.width / 2, entity.y + entity.height / 2
                    dx, dy = attr.x - ent_cx, attr.y - ent_cy
                    dist = math.sqrt(dx * dx + dy * dy) + 0.1
                    min_dist = entity.width / 2 + cfg.attr_ellipse_rx + 20
                    force = 50000.0 / (dist * dist) if dist < min_dist else 5000.0 / (dist * dist)
                    fx += force * dx / dist
                    fy += force * dy / dist
                for rel_obj in self.relationships.values():
                    rel_cx, rel_cy = rel_obj.x + rel_obj.width / 2, rel_obj.y + rel_obj.height / 2
                    dx, dy = attr.x - rel_cx, attr.y - rel_cy
                    dist = math.sqrt(dx * dx + dy * dy) + 0.1
                    min_dist = max(rel_obj.width, rel_obj.height) / 2 + cfg.attr_ellipse_rx + 20
                    force = 100000.0 / (dist * dist) if dist < min_dist else 8000.0 / (dist * dist)
                    fx += force * dx / dist
                    fy += force * dy / dist
                for other_attr, _ in all_attrs:
                    if other_attr is attr:
                        continue
                    dx, dy = attr.x - other_attr.x, attr.y - other_attr.y
                    dist = math.sqrt(dx * dx + dy * dy) + 0.1
                    min_dist = cfg.attr_ellipse_rx * 2 + 2
                    force = 30000.0 / (dist * dist) if dist < min_dist else 800.0 / (dist * dist)
                    fx += force * dx / dist
                    fy += force * dy / dist
                speed = math.sqrt(fx * fx + fy * fy)
                if speed > attr_temp:
                    fx, fy = fx / speed * attr_temp, fy / speed * attr_temp
                attr.x += fx
                attr.y += fy
            attr_temp *= 0.97

    def _calculate_canvas_size(self) -> None:
        cfg = self.config
        all_x, all_y = [], []
        for entity in self.entities.values():
            all_x.extend([entity.x, entity.x + entity.width])
            all_y.extend([entity.y, entity.y + entity.height])
            for attr in entity.attributes:
                all_x.extend([attr.x - cfg.attr_ellipse_rx, attr.x + cfg.attr_ellipse_rx])
                all_y.extend([attr.y - cfg.attr_ellipse_ry, attr.y + cfg.attr_ellipse_ry])
        for rel in self.relationships.values():
            all_x.extend([rel.x, rel.x + rel.width])
            all_y.extend([rel.y, rel.y + rel.height])
        min_x = min(all_x) - cfg.margin
        min_y = min(all_y) - cfg.margin
        max_x = max(all_x) + cfg.padding
        max_y = max(all_y) + cfg.padding
        self.canvas_width = int(max_x - min_x)
        self.canvas_height = int(max_y - min_y)
        offset_x, offset_y = -min_x, -min_y
        for entity in self.entities.values():
            entity.x += offset_x
            entity.y += offset_y
            for attr in entity.attributes:
                attr.x += offset_x
                attr.y += offset_y
        for rel in self.relationships.values():
            rel.x += offset_x
            rel.y += offset_y

    def layout(self, data: dict) -> None:
        self.parse_input(data)
        self._layout_components()
        self._position_relationships()
        self._collision_detection()
        self._position_attributes()
        self._calculate_canvas_size()


# ═══════════════════════════════════════════════════════════════
# Draw.io XML Renderer
# ═══════════════════════════════════════════════════════════════

class DrawioXMLRenderer:
    """Renders layout result to draw.io (diagrams.net) XML format."""

    ENTITY_STYLE = (
        "rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;"
        "fontSize=13;fontStyle=1;align=center;verticalAlign=middle;"
    )
    ATTR_STYLE = (
        "ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;"
        "fontSize=11;align=center;verticalAlign=middle;perimeter=ellipsePerimeter;"
    )
    ATTR_PK_STYLE = (
        "ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;"
        "fontSize=11;align=center;verticalAlign=middle;perimeter=ellipsePerimeter;"
        "fontStyle=1;"
    )
    ATTR_FK_STYLE = (
        "ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;"
        "fontSize=11;align=center;verticalAlign=middle;perimeter=ellipsePerimeter;"
        "dashed=1;"
    )
    RELATION_STYLE = (
        "rhombus;perimeter=rhombusPerimeter;whiteSpace=wrap;html=1;"
        "fillColor=#FFFFFF;strokeColor=#000000;fontSize=11;"
        "align=center;verticalAlign=middle;"
    )
    EDGE_STYLE = "endArrow=none;html=1;strokeColor=#000000;fontSize=11;"

    def __init__(self, config: Optional[LayoutConfig] = None):
        self.config = config or LayoutConfig()

    @staticmethod
    def _xml_escape(s: str) -> str:
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def render(self, engine: RadialLayoutEngine) -> str:
        cells = []
        cid = 2

        def add_cell(cell_id, value, style, vertex, x, y, w, h, parent="1"):
            cells.append(
                f'    <mxCell id="{cell_id}" value="{self._xml_escape(value)}" style="{style}" '
                f'vertex="{vertex}" parent="{parent}">\n'
                f'      <mxGeometry x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" as="geometry"/>\n'
                f'    </mxCell>'
            )

        def add_edge(edge_id, source, target, label=""):
            lbl = f' value="{self._xml_escape(label)}"' if label else ''
            cells.append(
                f'    <mxCell id="{edge_id}"{lbl} style="{self.EDGE_STYLE}" edge="1" parent="1" '
                f'source="{source}" target="{target}">\n'
                f'      <mxGeometry relative="1" as="geometry"/>\n'
                f'    </mxCell>'
            )

        for entity in engine.entities.values():
            add_cell(entity.id, entity.id, self.ENTITY_STYLE, "1",
                     entity.x, entity.y, entity.width, entity.height)
            for attr in entity.attributes:
                if attr.is_primary_key:
                    style = self.ATTR_PK_STYLE
                elif attr.is_foreign_key:
                    style = self.ATTR_FK_STYLE
                else:
                    style = self.ATTR_STYLE
                ax = attr.x - self.config.attr_ellipse_rx
                ay = attr.y - self.config.attr_ellipse_ry
                aw = self.config.attr_ellipse_rx * 2
                ah = self.config.attr_ellipse_ry * 2
                add_cell(cid, attr.name, style, "1", ax, ay, aw, ah)
                add_edge(f"e{cid}", entity.id, cid)
                cid += 1

        for rel in engine.relationships.values():
            add_cell(rel.id, rel.id, self.RELATION_STYLE, "1",
                     rel.x, rel.y, rel.width, rel.height)
            parts = rel.cardinality.value.split(":")
            from_card = parts[0]
            to_card = parts[1]
            add_edge(f"e{cid}", rel.from_entity, rel.id, from_card)
            cid += 1
            add_edge(f"e{cid}", rel.id, rel.to_entity, to_card)
            cid += 1

        w = engine.canvas_width
        h = engine.canvas_height
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<mxfile host="drawio">',
            '  <diagram id="er-diagram" name="ER Diagram">',
            f'    <mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1" tooltips="1"',
            f'                  connect="1" arrows="1" fold="1" page="1" pageScale="1"',
            f'                  pageWidth="{w}" pageHeight="{h}" math="0" shadow="0">',
            '      <root>',
            '        <mxCell id="0"/>',
            '        <mxCell id="1" parent="0"/>',
        ]
        lines.extend(cells)
        lines.extend([
            '      </root>',
            '    </mxGraphModel>',
            '  </diagram>',
            '</mxfile>',
        ])
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# Main Interface
# ═══════════════════════════════════════════════════════════════

class ERDiagram:
    """Main interface: JSON in -> draw.io XML out."""

    def __init__(self, config: Optional[LayoutConfig] = None):
        self.config = config or LayoutConfig()
        self.engine = RadialLayoutEngine(self.config)
        self.renderer = DrawioXMLRenderer(self.config)

    def from_dict(self, data: dict) -> "ERDiagram":
        self.engine.layout(data)
        return self

    def from_json(self, json_str: str) -> "ERDiagram":
        return self.from_dict(json.loads(json_str))

    def from_json_file(self, filepath: str) -> "ERDiagram":
        with open(filepath, 'r', encoding='utf-8') as f:
            return self.from_dict(json.load(f))

    def to_drawio(self) -> str:
        return self.renderer.render(self.engine)

    def save_drawio(self, filepath: str) -> None:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_drawio())
        print(f"Draw.io XML saved to: {filepath}")
        print(f"  Canvas: {self.engine.canvas_width} x {self.engine.canvas_height}")
        print(f"  Entities: {len(self.engine.entities)}")
        print(f"  Relationships: {len(self.engine.relationships)}")

    def get_layout_info(self) -> dict:
        return {
            "canvas_width": self.engine.canvas_width,
            "canvas_height": self.engine.canvas_height,
            "entities": [
                {"id": e.id, "x": e.x, "y": e.y, "width": e.width, "height": e.height,
                 "attributes": [{"name": a.name, "x": a.x, "y": a.y,
                                 "is_primary_key": a.is_primary_key,
                                 "is_foreign_key": a.is_foreign_key} for a in e.attributes]}
                for e in self.engine.entities.values()
            ],
            "relationships": [
                {"id": r.id, "from": r.from_entity, "to": r.to_entity,
                 "cardinality": r.cardinality.value,
                 "x": r.x, "y": r.y, "width": r.width, "height": r.height}
                for r in self.engine.relationships.values()
            ],
        }


if __name__ == "__main__":
    if len(sys.argv) == 3:
        input_json = sys.argv[1]
        output_drawio = sys.argv[2]
        diagram = ERDiagram().from_json_file(input_json)
        diagram.save_drawio(output_drawio)
    else:
        demo_data = {
            "type": "er",
            "entities": [
                {
                    "id": "Student",
                    "attributes": [
                        {"name": "student_id", "type": "int", "is_primary_key": True},
                        {"name": "name", "type": "string"},
                        {"name": "email", "type": "string"},
                    ]
                },
                {
                    "id": "Course",
                    "attributes": [
                        {"name": "course_id", "type": "int", "is_primary_key": True},
                        {"name": "title", "type": "string"},
                        {"name": "credits", "type": "int"},
                    ]
                },
                {
                    "id": "Teacher",
                    "attributes": [
                        {"name": "teacher_id", "type": "int", "is_primary_key": True},
                        {"name": "name", "type": "string"},
                        {"name": "title", "type": "string"},
                    ]
                },
            ],
            "relationships": [
                {"id": "Enrolls", "from": "Student", "to": "Course", "cardinality": "N:M"},
                {"id": "Teaches", "from": "Teacher", "to": "Course", "cardinality": "1:N"},
            ]
        }
        diagram = ERDiagram().from_dict(demo_data)
        diagram.save_drawio("demo_er.drawio")