Date: 03/31/2026

# 🐾 Virtual Pet CLI

A delightful command-line virtual pet (Tamagotchi-style) built with pure Python.

## Features

- 🐱🐶🐰 Choose your pet: cat, dog, or rabbit
- 🍖 Feed, play, and put your pet to sleep
- 📊 Track hunger, happiness, energy, and health
- 🎨 ASCII art that changes with your pet's mood
- ⏰ Pets age over time and need regular care
- 💾 Auto-saves progress to a JSON file
- 🌈 Colorful terminal output (no dependencies!)

## Getting Started

```bash
# Run the game
python3 main.py

# Or make it executable
chmod +x main.py
./main.py
```

## How to Play

1. Adopt a new pet or load a saved one
2. Choose actions from the menu:
   - **Feed** 🍖 — Reduces hunger, slightly increases energy
   - **Play** 🎾 — Increases happiness, increases hunger, decreases energy
   - **Sleep** 😴 — Restores energy, slightly increases hunger
   - **Heal** 💊 — Cures sickness (available when pet is sick)
   - **Stats** 📊 — View detailed pet statistics
3. Keep all stats balanced to keep your pet happy and healthy!

## Pet Moods

Your pet's mood changes based on their stats:
- 😊 **Happy** — All stats are good
- 😐 **Neutral** — Some stats need attention  
- 😢 **Sad** — Multiple stats are low
- 😴 **Sleepy** — Energy is very low
- 🤢 **Sick** — Health dropped too low (needs healing!)

## Requirements

- Python 3.7+
- No external dependencies

## License

MIT — Have fun! 🎉

hello
