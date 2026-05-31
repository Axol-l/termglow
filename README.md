<div align="center">

<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python">
<img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
<img src="https://img.shields.io/badge/dependencies-0-brightgreen.svg" alt="Dependencies">

# 🌈 TermGlow

**Mesmerizing terminal visual effects engine**

*Zero dependencies. Pure Python. Pure eye candy.*

</div>

---

## 🎬 Effects

| Effect | Command | Preview |
|--------|---------|---------|
| **Matrix Rain** | `termglow matrix` | Classic digital rain with Japanese katakana |
| **Plasma** | `termglow plasma` | Colorful sine-wave plasma with rippling patterns |
| **Starfield** | `termglow starfield` | 3D perspective stars flying through deep space |
| **Fire** | `termglow fire` | Doom-style procedural fire animation |
| **Particles** | `termglow particles` | Swarm particles with flocking behavior |

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/Axol-l/termglow
cd termglow

# Run directly (no install needed!)
python -m termglow.cli

# Or install
pip install .
termglow
```

**No dependencies.** TermGlow uses only the Python standard library.

## 🎮 Usage

```bash
# Interactive menu
termglow

# Launch effects directly
termglow matrix
termglow plasma
termglow starfield
termglow fire
termglow particles

# List available effects
termglow list

# Press Ctrl+C to exit any effect
```

## 🎨 How It Works

TermGlow renders directly to your terminal using **24-bit true color ANSI escape codes** and **double-buffering** for smooth animations with zero flicker.

- **Engine**: Custom render loop with adaptive FPS control
- **Double Buffering**: Only redraws changed pixels for maximum performance
- **True Color**: Full 16.7 million color palette, not limited to 256
- **Cross-Platform**: Works on Windows Terminal, iTerm2, Kitty, Alacritty, and more

## 🖥️ Terminal Requirements

Modern terminal with true color and Unicode support:

- ✅ **Windows Terminal** (recommended on Windows)
- ✅ **iTerm2** (macOS)
- ✅ **Kitty / Alacritty / WezTerm / Ghostty** (Linux/macOS)
- ✅ **VS Code integrated terminal**
- ❌ `cmd.exe` (no ANSI support)

## 🏗️ Project Structure

```
termglow/
├── termglow/
│   ├── __init__.py
│   ├── engine.py          # Core rendering engine
│   ├── cli.py             # CLI and interactive menu
│   └── effects/
│       ├── __init__.py
│       ├── matrix.py      # Matrix rain
│       ├── plasma.py      # Plasma effect
│       ├── starfield.py   # 3D star field
│       ├── fire.py        # Fire animation
│       └── particles.py   # Particle swarm
├── setup.py
└── README.md
```

## 📄 License

MIT - do whatever you want with it!

---

<div align="center">
Made with ❤️ and terminal escape codes
</div>
