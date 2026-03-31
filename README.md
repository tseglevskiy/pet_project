# 🐾 Virtual Pet CLI

A delightful command-line virtual pet (Tamagotchi-style) built with **pure Python** — no external dependencies required.

```
╔═══════════════════════════════════╗
║     🐾  Virtual Pet CLI  🐾      ║
╚═══════════════════════════════════╝

  /\_/\        ╔══════════════════════════════════╗
 ( ♥.♥ )       ║  🐱 Whiskers  (cat · 2h 15m)
  > ^ <         ║  Mood: 😊 Happy
 /|   |\        ╠══════════════════════════════════╣
(_|   |_)       ║  🍖 Hunger:    ████████░░░░░░░░░░ 40/100
                ║  😊 Happiness: ████████████████░░ 80/100
                ║  ⚡ Energy:    ██████████████░░░░ 70/100
                ║  ❤️  Health:   ████████████████████ 100/100
                ╚══════════════════════════════════╝
```

---

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [How to Play](#how-to-play)
- [Stat Mechanics](#stat-mechanics)
- [Pet Moods](#pet-moods)
- [Time & Aging](#time--aging)
- [Save System](#save-system)
- [Project Structure](#project-structure)
- [Running Tests](#running-tests)
- [Requirements](#requirements)
- [License](#license)

---

## Features

- 🐱🐶🐰 **Three species** to adopt: Cat, Dog, or Rabbit
- 🍖 **Four actions**: Feed, Play, Sleep, and Heal
- 📊 **Four stats** to manage: Hunger, Happiness, Energy, and Health
- 🎨 **Unique ASCII art** for each species × mood combination (25 total)
- ⏰ **Real-time aging** — stats decay passively while you are away
- 💾 **Auto-save** — progress written to `savegame.json` after every action
- 🌈 **Colorful ANSI terminal output** — zero pip installs needed
- ⚠️  **Alerts** — warned when your pet is hungry, exhausted, or sick

---

## Getting Started

```bash
# Clone the project
git clone https://github.com/tseglevskiy/pet_project.git
cd pet_project

# Run (Python 3.7+ required)
python3 main.py

# Or make it directly executable (macOS / Linux)
chmod +x main.py
./main.py
```

On first launch you will be prompted to adopt a pet.
Subsequent runs offer to continue with your saved pet or start fresh.

---

## How to Play

1. **Adopt** a new pet (pick a species and give it a name) — or **continue** with a saved one.
2. **Choose an action** each turn:

   | Key | Action | Stat changes |
   |-----|--------|--------------|
   | `1` | 🍖 Feed  | Hunger −25, Energy +5, Health +2 |
   | `2` | 🎾 Play  | Happiness +20, Hunger +15, Energy −20 *(needs Energy ≥ 10)* |
   | `3` | 😴 Sleep | Energy +40, Hunger +10, Happiness −5 |
   | `4` | 💊 Heal  | Health +40, Happiness +10 *(only works when Health ≤ 20)* |
   | `5` | 📊 Stats | Show stat panel — no stat change |
   | `q` | 💾 Quit  | Save & exit |

3. **Balance all four stats** — neglect leads to sickness and eventually death.

> **Tip:** The Heal option is dimmed when your pet is healthy, and turns red with `← URGENT!` when sick.

---

## Stat Mechanics

All stats are clamped to **0–100**.

| Stat | Scale | Key thresholds |
|------|-------|----------------|
| **Hunger** | 0 = full · 100 = starving | ≥ 90 → Health −5/tick; bar is *inverted* (green = low hunger = good) |
| **Happiness** | 0 = miserable · 100 = ecstatic | ≤ 10 → Health −3/tick |
| **Energy** | 0 = exhausted · 100 = rested | ≤ 9 → cannot play |
| **Health** | 0 = dead · 100 = perfect | ≤ 20 → Sick mood; = 0 → game over |

---

## Pet Moods

Mood is evaluated each turn in priority order:

| # | Mood | Condition |
|---|------|-----------|
| 1 | 🤢 **Sick**    | Health ≤ 20 |
| 2 | 😴 **Sleepy**  | Energy ≤ 15 |
| 3 | 😊 **Happy**   | Happiness ≥ 60 **and** Hunger ≤ 50 |
| 4 | 😢 **Sad**     | Happiness ≤ 30 **or** Hunger ≥ 80 |
| 5 | 😐 **Neutral** | None of the above |

Each mood renders a different ASCII art face for all three species.

---

## Time & Aging

Stats decay based on **real wall-clock time**.
Every **30 seconds** of elapsed time is one *tick*:

| Per tick | Change |
|----------|--------|
| Hunger   | +3 |
| Happiness | −2 |
| Energy   | −2 |
| Health   | −5 *(only when Hunger ≥ 90)* |
| Health   | −3 *(only when Happiness ≤ 10)* |

Your pet ages in real minutes, displayed as `2h 15m` in the stat panel.
Ticks are applied retroactively on next launch using the `last_tick` timestamp
stored in the save file, so closing the game does not pause time.

---

## Save System

Progress is persisted to **`savegame.json`** after every action:

```json
{
  "name": "Whiskers",
  "species": "cat",
  "hunger": 30,
  "happiness": 70,
  "energy": 80,
  "health": 100,
  "age_minutes": 135.0,
  "is_alive": true,
  "created_at": 1743350400.0,
  "last_tick": 1743358500.0
}
```

- Missing or corrupted save files are handled gracefully — the game prompts for a new pet.
- `savegame.json` is listed in `.gitignore` and is never committed to version control.

---

## Project Structure

```
pet_project/
├── main.py        # Entry point — start screen, game loop, user prompts
├── pet.py         # Pet dataclass — stats, actions, tick logic, save/load
├── ui.py          # Terminal helpers — ANSI colors, stat bars, menus, banner
├── art.py         # ASCII art strings mapped by (Species, Mood)
├── test_pet.py    # Unit tests for the Pet model
└── savegame.json  # Auto-generated save file (created at runtime)
```

| Module | Responsibility |
|--------|---------------|
| `pet.py` | Core model: `Species` & `Mood` enums, `Pet` dataclass with all action methods and JSON persistence. |
| `main.py` | UI flow: banner, `adopt_pet()`, and `game_loop()` which ticks, redraws, and dispatches actions. |
| `ui.py` | Display helpers only: ANSI constants, colored `bar()`, `display_stats()`, `display_menu()`, `banner()`. |
| `art.py` | Lookup table of ASCII strings indexed by `(Species, Mood)`, exposed via `get_art()`. |
| `test_pet.py` | Tests for defaults, actions, moods, clamping, dead-pet guards, age display, save/load, and ticks. |

---

## Running Tests

```bash
# Recommended — gives verbose, coloured output
pytest test_pet.py -v

# No extra installs — stdlib runner
python3 -m unittest test_pet -v
```

All tests are self-contained; save/load tests use `tempfile` with automatic cleanup.

---

## Requirements

- **Python 3.7+** — uses `dataclasses`, `from __future__ import annotations`, and `pathlib`
- **No external dependencies** — only stdlib (`json`, `time`, `pathlib`, `dataclasses`, `enum`)
- Runs on **macOS**, **Linux**, and **Windows** (`cls` vs `clear` is auto-detected)

---

## License

MIT — Have fun and take good care of your virtual pet! 🎉
