"""CLI entry point with interactive menu and direct effect launcher."""

import sys
import os
import time
from .engine import Engine, CSI, rgb, reset, move, clear_line, CURSOR_HIDE, CURSOR_SHOW, CLEAR_SCREEN, ALT_BUFFER_ON, ALT_BUFFER_OFF


EFFECTS = {
    "matrix":    ("Matrix Rain", "Classic digital rain with Japanese katakana"),
    "plasma":    ("Plasma", "Colorful sine-wave plasma with rippling waves"),
    "starfield": ("Starfield", "3D perspective stars flying through deep space"),
    "fire":      ("Fire", "Doom-style procedural fire animation"),
    "particles": ("Particles", "Swarm particles with flocking behavior"),
}


def show_menu():
    """Display interactive effect selection menu."""
    sys.stdout.write(ALT_BUFFER_ON)
    sys.stdout.write(CLEAR_SCREEN)
    sys.stdout.flush()

    selected = 0
    keys = list(EFFECTS.keys())

    width, height = 80, 24
    try:
        width, height = os.get_terminal_size()
    except Exception:
        pass

    try:
        import msvcrt
        _getch = msvcrt.getch
    except ImportError:
        def _getch():
            fd = sys.stdin.fileno()
            old = __import__("termios").tcgetattr(fd)
            __import__("tty").setraw(fd)
            try:
                return sys.stdin.buffer.read(1)
            finally:
                __import__("termios").tcsetattr(fd, __import__("termios").TCSANOW, old)

    def draw():
        nonlocal width, height
        try:
            width, height = os.get_terminal_size()
        except Exception:
            pass

        out = [CURSOR_HIDE]
        py = max(0, height // 2 - len(keys) - 4)

        logo = [
            r" _____                    ____ _",
            r"|_   _|__ _ __ _ __ ___  / ___| | _____      __",
            r"  | |/ _ \ '__| '_ ` _ \| |  _| |/ _ \ \ /\ / /",
            r"  | |  __/ |  | | | | | | |_| | | (_) \ V  V /",
            r"  |_|\___|_|  |_| |_| |_|\____|_|\___/ \_/\_/",
            "",
            "  Terminal Visual Effects Engine v2.0",
            "  arrow keys: navigate   enter: select   q/esc: quit",
        ]

        for i, line in enumerate(logo):
            pos = max(0, (width - len(line)) // 2)
            out.append(move(pos + 1, py + i + 1))
            out.append(rgb(0, 255, 100) + line + reset())

        item_start = py + len(logo) + 2
        for i, key in enumerate(keys):
            name, desc = EFFECTS[key]
            y = item_start + i * 2
            x = max(0, width // 2 - 20)

            out.append(move(x + 1, y + 1))
            if i == selected:
                out.append(rgb(0, 200, 255))
                out.append("\u25B6 ")
            else:
                out.append("  ")

            out.append(name)
            out.append(reset())

            out.append(move(x + 3, y + 2))
            out.append(rgb(128, 128, 128) + desc + reset())

        out.append(move(1, height))
        sys.stdout.write("".join(out))
        sys.stdout.flush()

    draw()

    while True:
        ch = _getch()
        ch_lower = ch.lower() if isinstance(ch, bytes) else ch

        if ch in (b"q", b"Q", b"\x1b"):
            break

        if ch in (b"\r", b"\n"):
            _cleanup_menu()
            return keys[selected]

        if (os.name == "nt" and ch == b"\xe0"):
            ch2 = _getch()
            if ch2 == b"H":      selected = (selected - 1) % len(keys)
            elif ch2 == b"P":    selected = (selected + 1) % len(keys)
        elif os.name != "nt" and ch == b"\x1b":
            ch2 = _getch()
            if ch2 == b"[":
                ch3 = _getch()
                if ch3 == b"A":      selected = (selected - 1) % len(keys)
                elif ch3 == b"B":    selected = (selected + 1) % len(keys)

        draw()

    _cleanup_menu()
    return None


def _cleanup_menu():
    sys.stdout.write(reset())
    sys.stdout.write(CURSOR_SHOW)
    sys.stdout.write(ALT_BUFFER_OFF)
    sys.stdout.write(CLEAR_SCREEN)
    sys.stdout.flush()


def run_effect(name: str):
    """Run a specific visual effect."""
    if name == "matrix":
        from .effects.matrix import matrix_effect
        render_fn = matrix_effect
    elif name == "plasma":
        from .effects.plasma import plasma_effect
        render_fn = plasma_effect
    elif name == "starfield":
        from .effects.starfield import starfield_effect
        render_fn = starfield_effect
    elif name == "fire":
        from .effects.fire import fire_effect
        render_fn = fire_effect
    elif name == "particles":
        from .effects.particles import particles_effect
        render_fn = particles_effect
    else:
        print(f"Unknown effect: {name}")
        print("Available: " + ", ".join(EFFECTS.keys()))
        return

    engine = Engine(fps=60)
    engine.run(render_fn)


def main():
    if len(sys.argv) > 1:
        name = sys.argv[1].lower()
        if name in EFFECTS:
            run_effect(name)
        elif name == "list" or name == "--list":
            for key, (name, desc) in EFFECTS.items():
                print(f"  {key:12} {name:20} {desc}")
        else:
            print(f"Unknown effect: {name}", file=sys.stderr)
            print("Available: " + ", ".join(EFFECTS.keys()), file=sys.stderr)
            sys.exit(1)
    else:
        choice = show_menu()
        if choice:
            run_effect(choice)


if __name__ == "__main__":
    main()
