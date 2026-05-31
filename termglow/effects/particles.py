"""Particle swarm with neighbor connections and smooth color flow."""

import random
import math
from ..engine import rgb


CONNECTION_DIST = 14


class Particle:
    def __init__(self, w: int, h: int):
        self.x = random.uniform(0, w)
        self.y = random.uniform(0, h)
        self.vx = random.uniform(-25, 25)
        self.vy = random.uniform(-25, 25)
        self.hue = random.uniform(0, 360)
        self.speed_var = random.uniform(0.7, 1.3)

    def update(self, dt: float, w: int, h: int, neighbors: list["Particle"]):
        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.x < 0:      self.x += w
        elif self.x >= w:   self.x -= w
        if self.y < 0:      self.y += h
        elif self.y >= h:   self.y -= h

        cx, cy = 0.0, 0.0
        count = 0

        sep_x, sep_y = 0.0, 0.0
        sep_count = 0

        for p in neighbors:
            dx = p.x - self.x
            if abs(dx) > CONNECTION_DIST * 2:
                continue
            dy = p.y - self.y
            if abs(dy) > CONNECTION_DIST * 2:
                continue
            dist = math.sqrt(dx * dx + dy * dy)
            if dist <= 0:
                continue

            if dist < CONNECTION_DIST:
                factor = 1.0 - dist / CONNECTION_DIST
                cx += dx * factor * 2.5
                cy += dy * factor * 2.5
                count += 1

            if dist < 6:
                sep_x -= dx / dist * 3
                sep_y -= dy / dist * 3
                sep_count += 1

        if count > 0:
            self.vx += (cx / count) * dt * 1.8
            self.vy += (cy / count) * dt * 1.8
        if sep_count > 0:
            self.vx += sep_x * dt * 0.5
            self.vy += sep_y * dt * 0.5

        self.vx *= 0.997
        self.vy *= 0.997

        speed = math.sqrt(self.vx * self.vx + self.vy * self.vy)
        max_speed = 45 * self.speed_var
        min_speed = 8
        if speed > max_speed:
            self.vx = (self.vx / speed) * max_speed
            self.vy = (self.vy / speed) * max_speed
        elif speed < min_speed:
            self.vx = (self.vx / max(speed, 0.001)) * min_speed
            self.vy = (self.vy / max(speed, 0.001)) * min_speed

        self.hue = (self.hue + 25 * dt) % 360

    def color(self, t: float) -> str:
        hue = (self.hue + t * 40) % 360
        r, g, b = _hsv_to_rgb(hue, 0.85, 0.95)
        return rgb(int(r), int(g), int(b))


def _hsv_to_rgb(h: float, s: float, v: float) -> tuple[float, float, float]:
    h = h / 60
    i = int(h) % 6
    f = h - i
    p = v * (1 - s)
    q = v * (1 - s * f)
    t_ = v * (1 - s * (1 - f))
    table = [
        (v, t_, p), (q, v, p), (p, v, t_),
        (p, q, v), (t_, p, v), (v, p, q),
    ]
    r, g, b = table[i]
    return r * 255, g * 255, b * 255


_particles: list[Particle] = []
_time = 0.0


def particles_effect(dt: float, width: int, height: int) -> list[str]:
    global _particles, _time
    _time += dt

    target = max(30, width * height // 55)
    while len(_particles) < target:
        _particles.append(Particle(width, height))
    _particles = _particles[:target]

    for p in _particles:
        p.update(dt, width, height, _particles)

    screen = [[" " for _ in range(width)] for _ in range(height)]

    for i, p in enumerate(_particles):
        for j in range(i + 1, len(_particles)):
            q = _particles[j]
            dx = q.x - p.x
            dy = q.y - p.y

            if abs(dx) > CONNECTION_DIST:
                continue
            if abs(dy) > CONNECTION_DIST:
                continue

            dist = math.sqrt(dx * dx + dy * dy)
            if dist < CONNECTION_DIST:
                alpha = 1.0 - dist / CONNECTION_DIST
                mid_hue = (p.hue + q.hue) / 2
                r, g, b = _hsv_to_rgb((mid_hue + _time * 40) % 360, 0.6, alpha * 0.4)
                color = rgb(int(r), int(g), int(b))
                _draw_line(screen, int(p.x), int(p.y), int(q.x), int(q.y), color, width, height)

    for p in _particles:
        x, y = int(p.x), int(p.y)
        if 0 <= x < width and 0 <= y < height:
            screen[y][x] = p.color(_time) + "\u25CF"

    return ["".join(row) for row in screen]


def _draw_line(screen: list[list[str]], x0: int, y0: int, x1: int, y1: int,
               color: str, w: int, h: int):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    for _ in range(20):
        if 0 <= x0 < w and 0 <= y0 < h:
            current = screen[y0][x0]
            if current == " " or (not current.startswith("\033")):
                screen[y0][x0] = color + "\u00B7"
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
