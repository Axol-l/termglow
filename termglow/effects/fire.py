"""Improved fire effect with realistic palette and sparks."""

import random
from ..engine import rgb


class Fire:
    def __init__(self):
        self._buffer: list[list[float]] = []
        self._palette: list[tuple[int, int, int]] = []
        self._sparks: list[dict] = []

    def _gen_palette(self, size: int = 256):
        palette = []
        for i in range(size):
            t = i / (size - 1)
            if t < 0.25:
                s = t / 0.25
                r = int(s * 128)
                g = 0
                b = 0
            elif t < 0.5:
                s = (t - 0.25) / 0.25
                r = min(255, 128 + int(s * 127))
                g = int(s * 80)
                b = 0
            elif t < 0.75:
                s = (t - 0.5) / 0.25
                r = 255
                g = min(255, 80 + int(s * 175))
                b = int(s * 60)
            elif t < 0.88:
                s = (t - 0.75) / 0.13
                r = 255
                g = 255
                b = min(255, 60 + int(s * 195))
            else:
                s = (t - 0.88) / 0.12
                r = 255
                g = 255
                b = min(255, 200 + int(s * 55))

            palette.append((r, g, b))
        self._palette = palette

    def render(self, dt: float, width: int, height: int) -> list[str]:
        fire_h = height + 6
        if not self._palette:
            self._gen_palette()

        if len(self._buffer) != fire_h or len(self._buffer[0]) != width:
            self._buffer = [[0.0] * width for _ in range(fire_h)]

        buf = self._buffer

        for x in range(width):
            if random.random() < 0.55:
                val = random.uniform(0.6, 1.0)
                if random.random() < 0.15:
                    val = random.uniform(0.9, 1.0)
                buf[fire_h - 1][x] = val
            elif random.random() < 0.3:
                buf[fire_h - 1][x] = buf[fire_h - 1][x] * 0.7
            else:
                buf[fire_h - 1][x] *= 0.92

        for y in range(fire_h - 2, -1, -1):
            for x in range(1, width - 1):
                decay = random.uniform(0.97, 1.01)
                s = buf[y + 1][x] + buf[y + 1][x - 1] + buf[y + 1][x + 1] + buf[min(y + 2, fire_h - 1)][x]
                buf[y][x] = (s / 4.05) * decay

        self._sparks = [s for s in self._sparks if s["life"] > 0]
        for s in self._sparks:
            s["y"] -= s["vy"] * dt * 50
            s["x"] += s["vx"] * dt * 20
            s["life"] -= dt * 3
        if random.random() < 0.15:
            spark_x = random.randint(2, width - 3)
            spark_y = fire_h - 4
            if spark_y < height:
                self._sparks.append({
                    "x": float(spark_x), "y": float(spark_y),
                    "vx": random.uniform(-1.5, 1.5),
                    "vy": random.uniform(2.0, 6.0),
                    "life": random.uniform(0.3, 0.8),
                })

        result = []
        pal_size = len(self._palette) - 1
        for y in range(height):
            row = []
            base_y = y + (fire_h - height)
            for x in range(width):
                idx = min(pal_size, int(buf[base_y][x] * pal_size))
                r, g, b = self._palette[idx]
                row.append(rgb(r, g, b) + "\u2588")
            result.append("".join(row))

        for s in self._sparks:
            sx = int(s["x"])
            sy = int(s["y"])
            if 0 <= sx < width and 0 <= sy < height:
                alpha = s["life"]
                r = int(255 * alpha)
                g = int(200 * alpha)
                b = int(80 * alpha)
                spark_str = rgb(r, g, b) + "*"
                row = list(result[sy])
                if sx < len(row):
                    row[sx] = spark_str
                result[sy] = "".join(row)

        return result


_fire = Fire()


def fire_effect(dt: float, width: int, height: int) -> list[str]:
    return _fire.render(dt, width, height)
