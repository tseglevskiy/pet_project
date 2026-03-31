"""Terminal UI helpers — colors, stat bars, and display functions."""

from __future__ import annotations

from pet import Mood, Pet

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
DIM = "\033[2m"


MOOD_EMOJI = {
    Mood.HAPPY: "😊 Happy",
    Mood.NEUTRAL: "😐 Okay",
    Mood.SAD: "😢 Sad",
    Mood.SLEEPY: "😴 Sleepy",
    Mood.SICK: "🤢 Sick",
}


def bar(value: int, max_val: int = 100, width: int = 20,
        invert: bool = False) -> str:
    """Render a colored progress bar. If invert, lower = better."""
    effective = (max_val - value) if invert else value
    ratio = effective / max_val
    filled = int(ratio * width)
    if ratio >= 0.6:
        color = GREEN
    elif ratio >= 0.3:
        color = YELLOW
    else:
        color = RED
    return f"{color}{'█' * filled}{'░' * (width - filled)}{RESET} {value}/{max_val}"


def display_stats(pet: Pet) -> str:
    """Return a formatted string with all pet stats."""
    mood_str = MOOD_EMOJI.get(pet.mood, str(pet.mood))
    species_emoji = {"cat": "🐱", "dog": "🐶", "rabbit": "🐰", "dragon": "🐉"}
    emoji = species_emoji.get(pet.species.value, "🐾")

    lines = [
        f"{BOLD}{CYAN}╔══════════════════════════════════╗{RESET}",
        f"{BOLD}{CYAN}║{RESET}  {emoji} {BOLD}{pet.name}{RESET}"
        f"  {DIM}({pet.species.value} · {pet.age_display}){RESET}",
        f"{BOLD}{CYAN}║{RESET}  Mood: {mood_str}",
        f"{BOLD}{CYAN}╠══════════════════════════════════╣{RESET}",
        f"{BOLD}{CYAN}║{RESET}  🍖 Hunger:    {bar(pet.hunger, invert=True)}",
        f"{BOLD}{CYAN}║{RESET}  😊 Happiness: {bar(pet.happiness)}",
        f"{BOLD}{CYAN}║{RESET}  ⚡ Energy:    {bar(pet.energy)}",
        f"{BOLD}{CYAN}║{RESET}  ❤️  Health:    {bar(pet.health)}",
        f"{BOLD}{CYAN}╚══════════════════════════════════╝{RESET}",
    ]
    return "\n".join(lines)


def display_menu(pet: Pet) -> str:
    sick = pet.mood == Mood.SICK
    lines = [
        f"\n{BOLD}What would you like to do?{RESET}",
        f"  {GREEN}[1]{RESET} Feed 🍖",
        f"  {GREEN}[2]{RESET} Play 🎾",
        f"  {GREEN}[3]{RESET} Sleep 😴",
    ]
    if sick:
        lines.append(f"  {RED}[4]{RESET} Heal 💊  ← {RED}URGENT!{RESET}")
    else:
        lines.append(f"  {DIM}[4] Heal 💊{RESET}")
    lines.extend([
        f"  {BLUE}[5]{RESET} View Stats 📊",
        f"  {MAGENTA}[q]{RESET} Save & Quit",
    ])
    return "\n".join(lines)


def banner() -> str:
    return f"""{BOLD}{MAGENTA}
╔═══════════════════════════════════╗
║     🐾  Virtual Pet CLI  🐾      ║
╚═══════════════════════════════════╝{RESET}
"""
