"""3D star field with nebula background and shooting stars."""

import random
import math
from ..engine import rgb


class StarField:
    def __init__(self):
        self.stars: list[dict] = []
        self._nebula_phase = 0.0
        self._shooting_stars: list[dict] = []

    def _ensure_stars(self, width: int, height: int):
        target = max(width * height // 10, 120)
        while len(self.stars) < target:
            self.stars.append(self._new_star(width, height))
        self.stars = self.stars[:target]

    def _new_star(self, width: int, height: int, z_min: float = 0.1) -> dict:
        bright_star = random.random() < 0.12
        return {
            "x": random.uniform(-2.0, 2.0),
            "y": random.uniform(-1.5, 1.5),
            "z": random.uniform(z_min, 1.0),
            "speed": random.uniform(0.15, 2.0),
            "bright": bright_star,
            "twinkle": random.uniform(0, math.pi * 2),
            "twinkle_rate": random.uniform(1, 4),
        }

    def render(self, dt: float, width: int, height: int) -> list[str]:
        self._ensure_stars(width, height)
        self._nebula_phase += dt * 0.3
        aspect = width / max(height, 1)
        cx, cy = width / 2, height / 2

        screen = [[" " for _ in range(width)] for _ in range(height)]
        depth_map = [[float("inf") for _ in range(width)] for _ in range(height)]

        for y in range(height):
            for x in range(width):
                nx = (x / width - 0.5) * 5
                ny = (y / height - 0.5) * 5
                nv = math.sin(nx * 1.7 + self._nebula_phase)
                nv += math.cos(ny * 2.1 + self._nebula_phase * 0.6)
                nv += math.sin((nx + ny) * 1.3 + self._nebula_phase * 1.1)
                nv /= 3

                brightness = max(0, nv * 0.12)
                if brightness > 0.01:
                    b = int(brightness * 255)
                    screen[y][x] = f"{rgb(b//3, b//4, b//2)} "

        for i, star in enumerate(self.stars):
            star["z"] -= star["speed"] * dt * 0.7
            if star["z"] <= 0.01:
                self.stars[i] = self._new_star(width, height, z_min=0.5)
                continue

            sx = int((star["x"] / star["z"]) * cx * aspect + cx)
            sy = int((star["y"] / star["z"]) * cy * 0.55 + cy)

            if not (0 <= sx < width and 0 <= sy < height):
                continue

            z_norm = star["z"]
            if z_norm >= depth_map[sy][sx]:
                continue
            depth_map[sy][sx] = z_norm

            depth = 1.0 - z_norm

            if star["bright"]:
                twinkle = (math.sin(star["twinkle"] + self._nebula_phase * star["twinkle_rate"]) + 1) / 2
                base_bright = 0.7 + twinkle * 0.3
            else:
                base_bright = max(0.2, min(1.0, depth * 1.3))

            r = int((180 + 75 * depth) * base_bright)
            g = int((200 + 55 * depth) * base_bright)
            b = int((220 + 35 * depth) * base_bright)

            if star["bright"] and base_bright > 0.8:
                char = "\u25C9" if random.random() < 0.3 else "\u2726"
            else:
                char = "\u2022" if depth > 0.5 else "\u00B7"

            screen[sy][sx] = f"{rgb(r, g, b)}{char}"

            if star["bright"] and base_bright > 0.9:
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    gx, gy = sx + dx, sy + dy
                    if 0 <= gx < width and 0 <= gy < height:
                        glow = screen[gy][gx]
                        if glow == " " or glow.endswith(" "):
                            screen[gy][gx] = f"{rgb(r//3, g//3, b//3)}\u00B7"

        self._shooting_stars = [s for s in self._shooting_stars if s["life"] > 0]
        for s in self._shooting_stars:
            s["x"] += s["vx"] * dt * 80
            s["y"] += s["vy"] * dt * 80
            s["life"] -= dt * 1.5
            for t in range(6):
                px = int(s["x"] + s["vx"] * t * 0.3)
                py = int(s["y"] + s["vy"] * t * 0.3)
                if 0 <= px < width and 0 <= py < height:
                    alpha = s["life"] * (1 - t / 6)
                    r = g = b = int(255 * alpha)
                    screen[py][px] = f"{rgb(r, g, b)}{'*' if t < 3 else '\u00B7'}"

        if random.random() < 0.008 and not self._shooting_stars:
            sx = random.uniform(0, width)
            sy = random.uniform(0, height / 2)
            angle = random.uniform(-0.5, 0.5)
            self._shooting_stars.append({
                "x": sx, "y": sy,
                "vx": math.cos(angle), "vy": math.sin(angle),
                "life": random.uniform(0.8, 1.2),
            })

        result = ["".join(row) for row in screen]
        return result


_star_field = StarField()


def starfield_effect(dt: float, width: int, height: int) -> list[str]:
    return _star_field.render(dt, width, height)
