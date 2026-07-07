#!/usr/bin/env python3
"""
JSON-to-Drawio ER Diagram Generator
====================================
Cycle-Based Polygon Layout (CBPL) algorithm.
Uses networkx.cycle_basis to find cycles, layouts them as polygons,
then hangs remaining nodes outward.

Usage:
    python er_cycle_engine.py input.json output.drawio
"""
import json
import math
import random
import sys
import networkx as nx
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum


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
    cycle_radius_base: float = 120
    cycle_radius_factor: float = 30
    non_cycle_offset: float = 180
    min_entity_spacing: float = 60
    
    entity_width: int = 110
    entity_height: int = 40
    rel_width: int = 90
    rel_height: int = 44
    attr_ellipse_rx: int = 35
    attr_ellipse_ry: int = 12
    attr_spacing: int = 30

    margin: int = 80
    padding: int = 50

    cril_max_iterations: int = 10
    cril_radii: Tuple[int, int, int] = (40, 80, 120)


def _segments_intersect(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
    def ccw(a_x, a_y, b_x, b_y, c_x, c_y):
        return (c_y - a_y) * (b_x - a_x) > (b_y - a_y) * (c_x - a_x)
    return ccw(ax1, ay1, bx1, by1, bx2, by2) != ccw(ax2, ay2, bx1, by1, bx2, by2) and \
           ccw(ax1, ay1, ax2, ay2, bx1, by1) != ccw(ax1, ay1, ax2, ay2, bx2, by2)


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


class CycleLayoutEngine:
    def __init__(self, config: Optional[LayoutConfig] = None):
        self.config = config or LayoutConfig()
        self.entities: Dict[str, Entity] = {}
        self.relationships: Dict[str, Relationship] = {}
        self.canvas_width: int = 0
        self.canvas_height: int = 0
        self.cycles: List[List[str]] = []
        self.entity_to_cycle: Dict[str, int] = {}

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

    def _build_entity_graph(self) -> nx.Graph:
        G = nx.Graph()
        G.add_nodes_from(self.entities.keys())
        for rel in self.relationships.values():
            G.add_edge(rel.from_entity, rel.to_entity)
        return G

    def _find_cycles(self) -> None:
        G = self._build_entity_graph()
        self.cycles = nx.cycle_basis(G)
        self.cycles.sort(key=lambda c: len(c))
        self.entity_to_cycle = {}
        for idx, cycle in enumerate(self.cycles):
            for eid in cycle:
                if eid not in self.entity_to_cycle:
                    self.entity_to_cycle[eid] = idx

    def _layout_cycle_as_polygon(self, cycle: List[str], center_x: float, center_y: float) -> None:
        cfg = self.config
        n = len(cycle)
        radius = cfg.cycle_radius_base + n * cfg.cycle_radius_factor
        
        start_angle = -math.pi / 2
        angle_step = 2 * math.pi / n
        
        for i, eid in enumerate(cycle):
            angle = start_angle + i * angle_step
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.entities[eid].x = x - self.entities[eid].width / 2
            self.entities[eid].y = y - self.entities[eid].height / 2

    def _layout_non_cycle_nodes(self) -> None:
        cfg = self.config
        cycle_nodes = set(eid for cycle in self.cycles for eid in cycle)
        owned_nodes = set(self.entity_to_cycle.keys())
        non_cycle_nodes = [eid for eid in self.entities if eid not in owned_nodes]
        G = self._build_entity_graph()
        
        for eid in non_cycle_nodes:
            neighbors = list(G.neighbors(eid))
            if not neighbors:
                continue
            
            anchor_eid = None
            for n in neighbors:
                if n in owned_nodes:
                    anchor_eid = n
                    break
            if anchor_eid is None:
                anchor_eid = neighbors[0]
            
            anchor = self.entities[anchor_eid]
            acx = anchor.x + anchor.width / 2
            acy = anchor.y + anchor.height / 2
            
            ecx, ecy = acx, acy
            
            if anchor_eid in self.entity_to_cycle:
                cycle_idx = self.entity_to_cycle[anchor_eid]
                cycle = self.cycles[cycle_idx]
                n = len(cycle)
                radius = cfg.cycle_radius_base + n * cfg.cycle_radius_factor
                idx = cycle.index(anchor_eid)
                angle = -math.pi / 2 + idx * 2 * math.pi / n
                ecx = acx + radius * math.cos(angle) * 0.6
                ecy = acy + radius * math.sin(angle) * 0.6
            
            dx = ecx - acx
            dy = ecy - acy
            dist = math.sqrt(dx * dx + dy * dy) + 0.001
            
            self.entities[eid].x = acx + (dx / dist) * cfg.non_cycle_offset - self.entities[eid].width / 2
            self.entities[eid].y = acy + (dy / dist) * cfg.non_cycle_offset - self.entities[eid].height / 2

    def _position_relationships(self) -> None:
        cfg = self.config
        entity_pair_rels: Dict[Tuple[str, str], List[Relationship]] = {}
        for rel in self.relationships.values():
            key = tuple(sorted([rel.from_entity, rel.to_entity]))
            if key not in entity_pair_rels:
                entity_pair_rels[key] = []
            entity_pair_rels[key].append(rel)

        for rel in self.relationships.values():
            if rel.from_entity == rel.to_entity:
                entity = self.entities[rel.from_entity]
                ecx = entity.x + entity.width / 2
                ecy = entity.y + entity.height / 2
                offset = cfg.cycle_radius_base + cfg.rel_width
                rel.x = ecx + offset - rel.width / 2
                rel.y = ecy - rel.height / 2
            else:
                a = self.entities[rel.from_entity]
                b = self.entities[rel.to_entity]
                mx = (a.x + a.width / 2 + b.x + b.width / 2) / 2
                my = (a.y + a.height / 2 + b.y + b.height / 2) / 2
                dx = b.x + b.width / 2 - (a.x + a.width / 2)
                dy = b.y + b.height / 2 - (a.y + a.height / 2)
                length = math.sqrt(dx * dx + dy * dy) + 0.001
                nx_dir = -dy / length
                ny_dir = dx / length

                key = tuple(sorted([rel.from_entity, rel.to_entity]))
                rels_for_pair = entity_pair_rels[key]
                if len(rels_for_pair) == 1:
                    rel.x = mx - rel.width / 2
                    rel.y = my - rel.height / 2
                else:
                    idx = rels_for_pair.index(rel)
                    offset_idx = idx - (len(rels_for_pair) - 1) / 2
                    offset = offset_idx * 30
                    rel.x = mx + nx_dir * offset - rel.width / 2
                    rel.y = my + ny_dir * offset - rel.height / 2

    def _get_edge_segments(self) -> List[Tuple[float, float, float, float]]:
        segments = []
        for rel in self.relationships.values():
            if rel.from_entity == rel.to_entity:
                entity = self.entities[rel.from_entity]
                ecx = entity.x + entity.width / 2
                ecy = entity.y + entity.height / 2
                rel_cx = rel.x + rel.width / 2
                rel_cy = rel.y + rel.height / 2
                segments.append((ecx, ecy, rel_cx, rel_cy))
            else:
                a = self.entities[rel.from_entity]
                b = self.entities[rel.to_entity]
                rel_cx = rel.x + rel.width / 2
                rel_cy = rel.y + rel.height / 2
                segments.append((a.x + a.width / 2, a.y + a.height / 2, rel_cx, rel_cy))
                segments.append((rel_cx, rel_cy, b.x + b.width / 2, b.y + b.height / 2))
        return segments

    def _count_edge_crossings(self) -> int:
        segments = self._get_edge_segments()
        count = 0
        n = len(segments)
        for i in range(n):
            for j in range(i + 1, n):
                ax1, ay1, ax2, ay2 = segments[i]
                bx1, by1, bx2, by2 = segments[j]
                if _segments_intersect(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
                    count += 1
        return count

    def _count_entity_overlaps(self) -> int:
        cfg = self.config
        entity_list = list(self.entities.values())
        count = 0
        n = len(entity_list)
        for i in range(n):
            for j in range(i + 1, n):
                e1, e2 = entity_list[i], entity_list[j]
                dx = (e1.x + e1.width / 2) - (e2.x + e2.width / 2)
                dy = (e1.y + e1.height / 2) - (e2.y + e2.height / 2)
                dist = math.sqrt(dx * dx + dy * dy)
                min_dist = (e1.width + e2.width) / 2 + cfg.min_entity_spacing
                if dist < min_dist:
                    count += 1
        return count

    def _count_relationship_overlaps(self) -> int:
        rel_list = list(self.relationships.values())
        count = 0
        n = len(rel_list)
        for i in range(n):
            for j in range(i + 1, n):
                r1, r2 = rel_list[i], rel_list[j]
                dx = (r1.x + r1.width / 2) - (r2.x + r2.width / 2)
                dy = (r1.y + r1.height / 2) - (r2.y + r2.height / 2)
                dist = math.sqrt(dx * dx + dy * dy)
                min_dist = (r1.width + r2.width) / 2 + 20
                if dist < min_dist:
                    count += 1
        return count

    def _compute_edge_length_variance(self) -> float:
        segments = self._get_edge_segments()
        if len(segments) == 0:
            return 0.0
        lengths = []
        for ax1, ay1, ax2, ay2 in segments:
            lengths.append(math.sqrt((ax2 - ax1) ** 2 + (ay2 - ay1) ** 2))
        mean_len = sum(lengths) / len(lengths)
        variance = sum((l - mean_len) ** 2 for l in lengths) / len(lengths)
        return variance

    def _compute_layout_score(self, crossings: int, entity_overlaps: int, 
                              rel_overlaps: int, edge_variance: float, displacement: float) -> float:
        return 10000 * crossings + 500 * entity_overlaps + 80 * rel_overlaps + 10 * edge_variance + 2 * displacement

    def _get_current_score(self) -> float:
        crossings = self._count_edge_crossings()
        entity_overlaps = self._count_entity_overlaps()
        rel_overlaps = self._count_relationship_overlaps()
        edge_variance = self._compute_edge_length_variance()
        return self._compute_layout_score(crossings, entity_overlaps, rel_overlaps, edge_variance, 0)

    def _local_search_optimize(self) -> float:
        cfg = self.config
        radii = cfg.cril_radii
        entity_list = list(self.entities.keys())

        for eid in entity_list:
            entity = self.entities[eid]
            original_x, original_y = entity.x, entity.y
            best_x, best_y = original_x, original_y
            best_score = float('inf')

            for r in radii:
                for angle_deg in range(0, 360, 15):
                    angle_rad = math.radians(angle_deg)
                    dx = r * math.cos(angle_rad)
                    dy = r * math.sin(angle_rad)
                    entity.x = original_x + dx
                    entity.y = original_y + dy
                    self._position_relationships()
                    crossings = self._count_edge_crossings()
                    entity_overlaps = self._count_entity_overlaps()
                    rel_overlaps = self._count_relationship_overlaps()
                    edge_variance = self._compute_edge_length_variance()
                    displacement = abs(dx) + abs(dy)
                    score = self._compute_layout_score(crossings, entity_overlaps, rel_overlaps, edge_variance, displacement)
                    if score < best_score:
                        best_score = score
                        best_x, best_y = entity.x, entity.y

            entity.x = best_x
            entity.y = best_y
            self._position_relationships()

        for i in range(len(entity_list)):
            for j in range(i + 1, len(entity_list)):
                eid1, eid2 = entity_list[i], entity_list[j]
                x1, y1 = self.entities[eid1].x, self.entities[eid1].y
                x2, y2 = self.entities[eid2].x, self.entities[eid2].y

                self.entities[eid1].x, self.entities[eid1].y = x2, y2
                self.entities[eid2].x, self.entities[eid2].y = x1, y1
                self._position_relationships()

                crossings = self._count_edge_crossings()
                entity_overlaps = self._count_entity_overlaps()
                rel_overlaps = self._count_relationship_overlaps()
                edge_variance = self._compute_edge_length_variance()
                score = self._compute_layout_score(crossings, entity_overlaps, rel_overlaps, edge_variance, 0)

                if score >= self._get_current_score():
                    self.entities[eid1].x, self.entities[eid1].y = x1, y1
                    self.entities[eid2].x, self.entities[eid2].y = x2, y2
                    self._position_relationships()

        return self._get_current_score()

    def _cril_optimize(self) -> None:
        cfg = self.config
        prev_score = self._get_current_score()
        for iteration in range(cfg.cril_max_iterations):
            self._local_search_optimize()
            current_score = self._get_current_score()
            if current_score >= prev_score:
                break
            prev_score = current_score

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
        self._find_cycles()
        
        cfg = self.config
        if self.cycles:
            max_radius = max(cfg.cycle_radius_base + len(c) * cfg.cycle_radius_factor for c in self.cycles)
            spacing = max_radius * 2 + 200
            
            cols = int(math.ceil(math.sqrt(len(self.cycles))))
            rows = int(math.ceil(len(self.cycles) / cols))
            
            start_x = cfg.margin + max_radius + cfg.entity_width
            start_y = cfg.margin + max_radius + cfg.entity_height
            
            placed_nodes = set()
            for idx, cycle in enumerate(self.cycles):
                col = idx % cols
                row = idx // cols
                center_x = start_x + col * spacing
                center_y = start_y + row * spacing
                
                for eid in cycle:
                    if eid not in placed_nodes:
                        placed_nodes.add(eid)
                
                self._layout_cycle_as_polygon(cycle, center_x, center_y)
        
        self._layout_non_cycle_nodes()
        self._position_relationships()
        self._cril_optimize()
        self._collision_detection()
        self._position_attributes()
        self._calculate_canvas_size()


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

    def render(self, engine: CycleLayoutEngine) -> str:
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


class ERDiagram:
    """Main interface: JSON in -> draw.io XML out."""

    def __init__(self, config: Optional[LayoutConfig] = None):
        self.config = config or LayoutConfig()
        self.engine = CycleLayoutEngine(self.config)
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
        print(f"  Cycles found: {len(self.engine.cycles)}")
        for i, cycle in enumerate(self.engine.cycles):
            print(f"    Cycle {i+1}: {', '.join(cycle)}")


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
                {"id": "Student", "attributes": [{"name": "id", "is_primary_key": True}, {"name": "name"}]},
                {"id": "Course", "attributes": [{"name": "id", "is_primary_key": True}, {"name": "title"}]},
                {"id": "Teacher", "attributes": [{"name": "id", "is_primary_key": True}, {"name": "name"}]},
            ],
            "relationships": [
                {"id": "Enrolls", "from": "Student", "to": "Course", "cardinality": "N:M"},
                {"id": "Teaches", "from": "Teacher", "to": "Course", "cardinality": "1:N"},
            ]
        }
        diagram = ERDiagram().from_dict(demo_data)
        diagram.save_drawio("demo_cycle_er.drawio")