"""3D perspective star field flying through space."""

import random
import math
from ..engine import rgb


class StarField:
    """3D star field with perspective projection."""

    def __init__(self, num_stars: int = 300):
        self.stars: list[dict] = []

    def _ensure_stars(self, width: int, height: int):
        target = max(width * height // 8, 150)
        while len(self.stars) < target:
            self.stars.append(self._new_star(width, height))
        self.stars = self.stars[:target]

    def _new_star(self, width: int, height: int, z_min: float = 0.1) -> dict:
        return {
            "x": random.uniform(-1.5, 1.5),
            "y": random.uniform(-1.0, 1.0),
            "z": random.uniform(z_min, 1.0),
            "speed": random.uniform(0.3, 2.5),
        }

    def render(self, dt: float, width: int, height: int) -> list[str]:
        self._ensure_stars(width, height)
        aspect = width / max(height, 1)
        cx, cy = width / 2, height / 2

        screen = [[" " for _ in range(width)] for _ in range(height)]
        depth_map = [[float("inf") for _ in range(width)] for _ in range(height)]

        for i, star in enumerate(self.stars):
            star["z"] -= star["speed"] * dt * 0.8
            if star["z"] <= 0.01:
                self.stars[i] = self._new_star(width, height, z_min=0.5)
                continue

            sx = int((star["x"] / star["z"]) * cx * aspect + cx)
            sy = int((star["y"] / star["z"]) * cy * 0.6 + cy)

            if not (0 <= sx < width and 0 <= sy < height):
                continue

            z_norm = star["z"]
            if z_norm < depth_map[sy][sx]:
                depth_map[sy][sx] = z_norm
                depth = 1.0 - z_norm
                r = int(180 + 75 * depth)
                g = int(200 + 55 * depth)
                b = int(220 + 35 * depth)
                brightness = min(1.0, depth * 2.0)
                r = int(r * brightness)
                g = int(g * brightness)
                b = int(b * brightness)
                screen[sy][sx] = f"{rgb(r, g, b)}\u2022"

        return ["".join(row) for row in screen]


_star_field = StarField()


def starfield_effect(dt: float, width: int, height: int) -> list[str]:
    return _star_field.render(dt, width, height)
