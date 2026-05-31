"""Swarm particle system with flocking behavior."""

import random
import math
from ..engine import rgb


class Particle:
    def __init__(self, w: int, h: int):
        self.x = random.uniform(0, w)
        self.y = random.uniform(0, h)
        self.vx = random.uniform(-30, 30)
        self.vy = random.uniform(-30, 30)
        self.hue = random.uniform(0, 360)
        self.size = random.choice([" ", "\u00B7", "\u25CF", "\u25A0"])

    def update(self, dt: float, w: int, h: int, particles: list["Particle"]):
        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.x < 0:
            self.x += w
        elif self.x >= w:
            self.x -= w
        if self.y < 0:
            self.y += h
        elif self.y >= h:
            self.y -= h

        cx, cy = 0.0, 0.0
        count = 0
        for p in particles:
            dx = p.x - self.x
            dy = p.y - self.y
            dist = math.sqrt(dx * dx + dy * dy)
            if 0 < dist < 12:
                factor = 1.0 - dist / 12
                cx += dx * factor * 2
                cy += dy * factor * 2
                count += 1

        if count > 0:
            self.vx += (cx / count) * dt * 2
            self.vy += (cy / count) * dt * 2

        self.vx *= 0.998
        self.vy *= 0.998

        speed = math.sqrt(self.vx * self.vx + self.vy * self.vy)
        max_speed = 50
        if speed > max_speed:
            self.vx = (self.vx / speed) * max_speed
            self.vy = (self.vy / speed) * max_speed

        self.hue = (self.hue + 20 * dt) % 360

    def color(self, t: float) -> str:
        hue = (self.hue + t * 30) % 360
        r, g, b = self._hsv_to_rgb(hue, 0.9, 0.95)
        return rgb(int(r), int(g), int(b))

    @staticmethod
    def _hsv_to_rgb(h: float, s: float, v: float) -> tuple[float, float, float]:
        h = h / 60
        i = int(h)
        f = h - i
        p = v * (1 - s)
        q = v * (1 - s * f)
        t_ = v * (1 - s * (1 - f))
        if i == 0:
            return v * 255, t_ * 255, p * 255
        if i == 1:
            return q * 255, v * 255, p * 255
        if i == 2:
            return p * 255, v * 255, t_ * 255
        if i == 3:
            return p * 255, q * 255, v * 255
        if i == 4:
            return t_ * 255, p * 255, v * 255
        return v * 255, p * 255, q * 255


_particles: list[Particle] = []
_time = 0.0


def particles_effect(dt: float, width: int, height: int) -> list[str]:
    global _particles, _time
    _time += dt

    target = width * height // 40
    while len(_particles) < target:
        _particles.append(Particle(width, height))
    _particles = _particles[:target]

    for p in _particles:
        p.update(dt, width, height, _particles)

    screen = [[" " for _ in range(width)] for _ in range(height)]

    for p in _particles:
        x, y = int(p.x), int(p.y)
        if 0 <= x < width and 0 <= y < height:
            screen[y][x] = p.color(_time) + p.size

    return ["".join(row) for row in screen]
