#!/usr/bin/env python3
"""
JSON-to-Drawio ER Diagram Generator
====================================
Based on force-directed layout engine. Reads JSON DSL, auto-layouts entities/
relationships/attributes, outputs standard draw.io XML.

Usage:
    python er_drawio_engine.py input.json output.drawio
"""
import json
import math
import random
import sys
from typing import Dict, List, Tuple, Optional
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
    vx: float = 0
    vy: float = 0
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
    # Force parameters
    repulsion_strength: float = 3000
    attraction_strength: float = 0.08
    ideal_edge_length: float = 250
    damping: float = 0.85
    max_iterations: int = 500
    cooling_factor: float = 0.98
    min_temperature: float = 0.01

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
# Force-Directed Layout Engine (preserved from reference)
# ═══════════════════════════════════════════════════════════════

class ForceLayoutEngine:
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

    @staticmethod
    def _louvain_clustering(adjacency: Dict[str, set], all_eids: List[str]) -> Dict[str, int]:
        n = len(all_eids)
        if n == 0:
            return {}
        community = {eid: i for i, eid in enumerate(all_eids)}
        edges = []
        for eid in all_eids:
            for neighbor in adjacency.get(eid, set()):
                if neighbor in community:
                    edges.append((eid, neighbor))
        total_edges = len(edges)
        if total_edges == 0:
            return community
        degree = {eid: 0 for eid in all_eids}
        for a, b in edges:
            degree[a] += 1
            degree[b] += 1

        def modularity_gain(node, target_comm):
            ki_in = sum(1 for neighbor in adjacency.get(node, set())
                        if neighbor in community and community[neighbor] == target_comm)
            sigma_tot = sum(degree[n] for n in all_eids if community[n] == target_comm)
            ki = degree[node]
            m2 = 2 * total_edges
            if sigma_tot == 0:
                return ki_in / m2
            return ki_in / m2 - (sigma_tot * ki) / (m2 * m2)

        improved = True
        for _ in range(20):
            if not improved:
                break
            improved = False
            random.seed(42)
            shuffled = list(all_eids)
            random.shuffle(shuffled)
            for node in shuffled:
                current_comm = community[node]
                candidate_comms = {community[n] for n in adjacency.get(node, set()) if n in community}
                candidate_comms.add(current_comm)
                best_comm = current_comm
                best_gain = 0.0
                for target_comm in candidate_comms:
                    if target_comm == current_comm:
                        continue
                    gain = modularity_gain(node, target_comm)
                    if gain > best_gain:
                        best_gain = gain
                        best_comm = target_comm
                if best_comm != current_comm:
                    community[node] = best_comm
                    improved = True
        unique_comms = sorted(set(community.values()))
        remap = {old: new for new, old in enumerate(unique_comms)}
        return {eid: remap[c] for eid, c in community.items()}

    @staticmethod
    def _layout_subgraph_radial(entity_ids, adjacency, spacing):
        if not entity_ids:
            return {}
        local_adj = {eid: adjacency.get(eid, set()) & set(entity_ids) for eid in entity_ids}
        placed = set()
        positions = {}
        sorted_ids = sorted(entity_ids, key=lambda eid: len(local_adj[eid]), reverse=True)
        center_id = sorted_ids[0]
        positions[center_id] = (0.0, 0.0)
        placed.add(center_id)
        neighbors = sorted(local_adj[center_id], key=lambda n: len(local_adj[n]), reverse=True)
        for i, nid in enumerate(neighbors):
            angle = 2 * math.pi * i / max(len(neighbors), 1) - math.pi / 2
            positions[nid] = (spacing * math.cos(angle), spacing * math.sin(angle))
            placed.add(nid)
        remaining = [eid for eid in sorted_ids if eid not in placed]
        while remaining:
            best_eid = None
            best_pn = set()
            for eid in remaining:
                pn = local_adj[eid] & placed
                if len(pn) > len(best_pn):
                    best_pn = pn
                    best_eid = eid
            if best_eid is None:
                break
            if best_pn:
                ax = sum(positions[nid][0] for nid in best_pn) / len(best_pn)
                ay = sum(positions[nid][1] for nid in best_pn) / len(best_pn)
            else:
                ax, ay = 0.0, 0.0
            best_angle = 0.0
            best_score = float('-inf')
            for k in range(36):
                angle = 2 * math.pi * k / 36
                tx, ty = ax + spacing * math.cos(angle), ay + spacing * math.sin(angle)
                score = sum(math.sqrt((tx - px) ** 2 + (ty - py) ** 2) for px, py in positions.values())
                if score > best_score:
                    best_score = score
                    best_angle = angle
            positions[best_eid] = (ax + spacing * math.cos(best_angle), ay + spacing * math.sin(best_angle))
            placed.add(best_eid)
            remaining.remove(best_eid)
        return positions

    def _init_positions(self) -> None:
        if not self.entities:
            return
        cfg = self.config
        ew, eh = cfg.entity_width, cfg.entity_height
        spacing = cfg.ideal_edge_length
        all_eids = list(self.entities.keys())
        n = len(all_eids)
        cols = max(3, int(math.ceil(math.sqrt(n))))
        rows = (n + cols - 1) // cols
        start_x = cfg.margin + ew
        start_y = cfg.margin + eh
        for i, eid in enumerate(all_eids):
            col = i % cols
            row = i // cols
            self.entities[eid].x = start_x + col * (ew + spacing)
            self.entities[eid].y = start_y + row * (eh + spacing)

    def _run_force_simulation(self) -> None:
        cfg = self.config
        entity_ids = list(self.entities.keys())
        n = len(entity_ids)
        temperature = 100.0
        adjacency = {eid: [] for eid in entity_ids}
        for rel in self.relationships.values():
            adjacency[rel.from_entity].append(rel.to_entity)
            adjacency[rel.to_entity].append(rel.from_entity)
        for iteration in range(cfg.max_iterations):
            if temperature < cfg.min_temperature:
                break
            fx = {eid: 0.0 for eid in entity_ids}
            fy = {eid: 0.0 for eid in entity_ids}
            # Repulsion
            for i in range(n):
                for j in range(i + 1, n):
                    a = self.entities[entity_ids[i]]
                    b = self.entities[entity_ids[j]]
                    dx, dy = a.x - b.x, a.y - b.y
                    rx = (a.width + b.width) / 4
                    ry = (a.height + b.height) / 4
                    if rx > 0 and ry > 0:
                        elliptical_dist = math.sqrt((dx / rx) ** 2 + (dy / ry) ** 2) * math.sqrt(rx * ry)
                    else:
                        elliptical_dist = math.sqrt(dx * dx + dy * dy)
                    dist = elliptical_dist + 0.1
                    angle = math.atan2(dy, dx) if (abs(dx) + abs(dy)) > 0.01 else 0
                    cos_a, sin_a = math.cos(angle), math.sin(angle)
                    if rx > 0 and ry > 0:
                        ellipse_r = rx * ry / math.sqrt((ry * cos_a) ** 2 + (rx * sin_a) ** 2)
                    else:
                        ellipse_r = 50
                    collision_dist = ellipse_r * 2 + 5
                    if dist < collision_dist:
                        overlap_ratio = 1.0 - dist / collision_dist
                        force = cfg.repulsion_strength * 50 * (overlap_ratio ** 2) / (dist + 1)
                    else:
                        force = cfg.repulsion_strength * 0.8 / (dist * dist)
                    if rx > 0 and ry > 0:
                        norm = math.sqrt((dx / rx) ** 2 + (dy / ry) ** 2) + 0.001
                        dir_x = (dx / rx) / norm
                        dir_y = (dy / ry) / norm
                    else:
                        mag = math.sqrt(dx * dx + dy * dy) + 0.1
                        dir_x, dir_y = dx / mag, dy / mag
                    fx[entity_ids[i]] += force * dir_x
                    fy[entity_ids[i]] += force * dir_y
                    fx[entity_ids[j]] -= force * dir_x
                    fy[entity_ids[j]] -= force * dir_y
            # Attraction
            for rel in self.relationships.values():
                a = self.entities[rel.from_entity]
                b = self.entities[rel.to_entity]
                dx, dy = b.x - a.x, b.y - a.y
                dist = math.sqrt(dx * dx + dy * dy) + 0.1
                displacement = dist - cfg.ideal_edge_length
                force = cfg.attraction_strength * displacement
                fx[rel.from_entity] += force * dx / dist
                fy[rel.from_entity] += force * dy / dist
                fx[rel.to_entity] -= force * dx / dist
                fy[rel.to_entity] -= force * dy / dist
            # Edge crossing repulsion
            rel_list = list(self.relationships.values())
            rel_midpoints = {}
            for rel in rel_list:
                ea, eb = self.entities[rel.from_entity], self.entities[rel.to_entity]
                rel_midpoints[rel.id] = ((ea.x + ea.width / 2 + eb.x + eb.width / 2) / 2,
                                          (ea.y + ea.height / 2 + eb.y + eb.height / 2) / 2)
            for i in range(len(rel_list)):
                for j in range(i + 1, len(rel_list)):
                    r1, r2 = rel_list[i], rel_list[j]
                    if r1.from_entity == r2.from_entity or r1.from_entity == r2.to_entity or \
                       r1.to_entity == r2.from_entity or r1.to_entity == r2.to_entity:
                        continue
                    e1a, e1b = self.entities[r1.from_entity], self.entities[r1.to_entity]
                    m1 = rel_midpoints[r1.id]
                    segs1 = [(e1a.x + e1a.width / 2, e1a.y + e1a.height / 2, m1[0], m1[1]),
                             (m1[0], m1[1], e1b.x + e1b.width / 2, e1b.y + e1b.height / 2)]
                    e2a, e2b = self.entities[r2.from_entity], self.entities[r2.to_entity]
                    m2 = rel_midpoints[r2.id]
                    segs2 = [(e2a.x + e2a.width / 2, e2a.y + e2a.height / 2, m2[0], m2[1]),
                             (m2[0], m2[1], e2b.x + e2b.width / 2, e2b.y + e2b.height / 2)]
                    min_dist = float('inf')
                    for s1 in segs1:
                        for s2 in segs2:
                            d = _segment_distance(s1[0], s1[1], s1[2], s1[3], s2[0], s2[1], s2[2], s2[3])
                            if d < min_dist:
                                min_dist = d
                    edge_min_gap = 120.0
                    if min_dist < edge_min_gap:
                        strength = 25000.0 * (1.0 - min_dist / edge_min_gap)
                        endpoints_1 = [(r1.from_entity, e1a.x + e1a.width / 2, e1a.y + e1a.height / 2),
                                       (r1.to_entity, e1b.x + e1b.width / 2, e1b.y + e1b.height / 2)]
                        endpoints_2 = [(r2.from_entity, e2a.x + e2a.width / 2, e2a.y + e2a.height / 2),
                                       (r2.to_entity, e2b.x + e2b.width / 2, e2b.y + e2b.height / 2)]
                        for eid1, x1, y1 in endpoints_1:
                            for eid2, x2, y2 in endpoints_2:
                                dx, dy = x1 - x2, y1 - y2
                                dist = math.sqrt(dx * dx + dy * dy) + 0.1
                                force = strength / (dist + 20)
                                fx[eid1] += force * dx / dist
                                fy[eid1] += force * dy / dist
                                fx[eid2] -= force * dx / dist
                                fy[eid2] -= force * dy / dist
            # Apply forces
            for eid in entity_ids:
                e = self.entities[eid]
                e.vx = (e.vx + fx[eid]) * cfg.damping
                e.vy = (e.vy + fy[eid]) * cfg.damping
                speed = math.sqrt(e.vx ** 2 + e.vy ** 2)
                max_speed = temperature
                if speed > max_speed:
                    e.vx = e.vx / speed * max_speed
                    e.vy = e.vy / speed * max_speed
                e.x += e.vx
                e.y += e.vy
                e.x = max(cfg.margin, e.x)
                e.y = max(cfg.margin, e.y)
            temperature *= cfg.cooling_factor

    def _position_relationships(self) -> None:
        for rel in self.relationships.values():
            a = self.entities[rel.from_entity]
            b = self.entities[rel.to_entity]
            rel.x = (a.x + a.width / 2 + b.x + b.width / 2) / 2 - rel.width / 2
            rel.y = (a.y + a.height / 2 + b.y + b.height / 2) / 2 - rel.height / 2

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
                    for rel in self.relationships.values():
                        ea, eb = self.entities[rel.from_entity], self.entities[rel.to_entity]
                        rel_cx, rel_cy = rel.x + rel.width / 2, rel.y + rel.height / 2
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
        # Attribute force simulation
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
                force = 0.12 * (dist - ideal_dist)
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
                for rel in self.relationships.values():
                    rel_cx, rel_cy = rel.x + rel.width / 2, rel.y + rel.height / 2
                    dx, dy = attr.x - rel_cx, attr.y - rel_cy
                    dist = math.sqrt(dx * dx + dy * dy) + 0.1
                    min_dist = max(rel.width, rel.height) / 2 + cfg.attr_ellipse_rx + 20
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
        self._init_positions()
        self._run_force_simulation()
        self._position_relationships()
        self._position_attributes()
        self._calculate_canvas_size()


# ═══════════════════════════════════════════════════════════════
# Draw.io XML Renderer
# ═══════════════════════════════════════════════════════════════

class DrawioXMLRenderer:
    """Renders layout result to draw.io (diagrams.net) XML format."""

    # Style constants
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

    def render(self, engine: ForceLayoutEngine) -> str:
        cells = []
        cid = 2  # 0 and 1 reserved

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

        # ── Entities + Attributes ──
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
                # Ellipse in draw.io uses bounding box: cx-rx, cy-ry, 2*rx, 2*ry
                ax = attr.x - self.config.attr_ellipse_rx
                ay = attr.y - self.config.attr_ellipse_ry
                aw = self.config.attr_ellipse_rx * 2
                ah = self.config.attr_ellipse_ry * 2
                add_cell(cid, attr.name, style, "1", ax, ay, aw, ah)
                add_edge(f"e{cid}", entity.id, cid)
                cid += 1

        # ── Relationships ──
        for rel in engine.relationships.values():
            add_cell(rel.id, rel.id, self.RELATION_STYLE, "1",
                     rel.x, rel.y, rel.width, rel.height)
            # Split cardinality: e.g., "1:N" -> from_side="1", to_side="N"
            parts = rel.cardinality.value.split(":")
            from_card = parts[0]
            to_card = parts[1]
            # Edge: entity -> relation (from side)
            add_edge(f"e{cid}", rel.from_entity, rel.id, from_card)
            cid += 1
            # Edge: relation -> entity (to side)
            add_edge(f"e{cid}", rel.id, rel.to_entity, to_card)
            cid += 1

        # ── Assemble XML ──
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
        self.engine = ForceLayoutEngine(self.config)
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
        # Demo: generate with sample data
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
