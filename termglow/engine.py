"""Core rendering engine for terminal visual effects."""

import sys
import os
import signal
import threading
from typing import Callable

CSI = "\033["
CURSOR_HIDE = f"{CSI}?25l"
CURSOR_SHOW = f"{CSI}?25h"
CLEAR_SCREEN = f"{CSI}2J{CSI}H"
ALT_BUFFER_ON = f"{CSI}?1049h"
ALT_BUFFER_OFF = f"{CSI}?1049l"


def rgb(r: int, g: int, b: int, bg: bool = False) -> str:
    """Generate 24-bit true color ANSI escape sequence."""
    code = 48 if bg else 38
    return f"{CSI}{code};2;{r};{g};{b}m"


def reset() -> str:
    """Reset all attributes."""
    return f"{CSI}0m"


def move(x: int, y: int) -> str:
    """Move cursor to position (x=col, y=row)."""
    return f"{CSI}{y};{x}H"


def clear_line() -> str:
    """Clear from cursor to end of line."""
    return f"{CSI}K"


class Engine:
    """Main rendering engine with double-buffering and FPS control."""

    def __init__(self, fps: int = 30):
        self.fps = fps
        self.running = False
        self._frame_time = 1.0 / fps if fps > 0 else 0
        self.width = 80
        self.height = 24
        self._buffer: list[str] = []
        self._last_buffer: list[str] = []

        signal.signal(signal.SIGINT, self._handle_sigint)
        if os.name == "nt":
            signal.signal(signal.SIGBREAK, self._handle_sigint)

    def _handle_sigint(self, signum, frame):
        self.running = False

    def _get_terminal_size(self) -> tuple[int, int]:
        try:
            cols, rows = os.get_terminal_size()
            return cols, rows
        except (ValueError, OSError):
            return 80, 24

    def _build_screen(self, buffer: list[str]) -> str:
        """Build the full screen string with double-buffering."""
        self.width, self.height = self._get_terminal_size()

        result = [CURSOR_HIDE]

        for y in range(min(self.height, len(buffer))):
            row = buffer[y] if y < len(buffer) else ""
            prev = self._last_buffer[y] if y < len(self._last_buffer) else ""

            display_row = row[:self.width].ljust(self.width)
            if display_row != prev:
                result.append(move(1, y + 1))
                result.append(clear_line())
                result.append(display_row)

        result.append(move(1, self.height))
        result.append(clear_line())

        return "".join(result)

    def run(self, render_fn: Callable[[float, int, int], list[str]]):
        """Run the render loop.

        Args:
            render_fn: Called each frame with (delta_time, width, height),
                       returns a list of strings (one per row).
        """
        import time

        self.running = True
        self._last_buffer = []
        last_frame = time.perf_counter()

        sys.stdout.write(ALT_BUFFER_ON)
        sys.stdout.write(CLEAR_SCREEN)
        sys.stdout.flush()

        try:
            while self.running:
                now = time.perf_counter()
                dt = now - last_frame
                last_frame = now

                self.width, self.height = self._get_terminal_size()
                new_buffer = render_fn(dt, self.width, self.height)

                screen = self._build_screen(new_buffer)
                sys.stdout.write(screen)
                sys.stdout.flush()

                self._last_buffer = new_buffer

                elapsed = time.perf_counter() - now
                sleep_time = max(0, self._frame_time - elapsed)
                time.sleep(sleep_time)
        except KeyboardInterrupt:
            pass
        finally:
            self._cleanup()

    def _cleanup(self):
        sys.stdout.write(reset())
        sys.stdout.write(CLEAR_SCREEN)
        sys.stdout.write(CURSOR_SHOW)
        sys.stdout.write(ALT_BUFFER_OFF)
        sys.stdout.flush()
