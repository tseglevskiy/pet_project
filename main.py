#!/usr/bin/env python3
"""🐾 Virtual Pet CLI — main entry point."""

from __future__ import annotations

import os
import sys

from art import get_art
from pet import Pet, Species
from ui import (
    BOLD, CYAN, GREEN, MAGENTA, RED, RESET, YELLOW,
    banner, display_menu, display_stats,
)


def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def prompt(text: str) -> str:
    try:
        return input(f"{CYAN}> {RESET}{text}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return "q"


def adopt_pet() -> Pet:
    """Interactive new-pet creation."""
    print(f"\n{BOLD}Choose a species:{RESET}")
    print(f"  {GREEN}[1]{RESET} 🐱 Cat")
    print(f"  {GREEN}[2]{RESET} 🐶 Dog")
    print(f"  {GREEN}[3]{RESET} 🐰 Rabbit")

    species_map = {"1": Species.CAT, "2": Species.DOG, "3": Species.RABBIT}
    while True:
        choice = prompt("Species (1/2/3)")
        if choice in species_map:
            break
        print(f"{RED}Please choose 1, 2, or 3.{RESET}")

    species = species_map[choice]
    while True:
        name = prompt("Give your pet a name")
        if name and name != "q":
            break
        print(f"{RED}Your pet needs a name!{RESET}")

    pet = Pet(name=name, species=species)
    print(f"\n{GREEN}🎉 Welcome home, {name} the {species.value}!{RESET}\n")
    return pet


def main_menu() -> Pet:
    """Show the start screen — load or adopt."""
    clear()
    print(banner())

    saved = Pet.load()
    if saved and saved.is_alive:
        print(f"  {YELLOW}Saved game found:{RESET} {BOLD}{saved.name}{RESET}"
              f" the {saved.species.value} (age {saved.age_display})\n")
        print(f"  {GREEN}[1]{RESET} Continue with {saved.name}")
        print(f"  {GREEN}[2]{RESET} Adopt a new pet")
        while True:
            choice = prompt("Choice (1/2)")
            if choice == "1":
                return saved
            if choice == "2":
                return adopt_pet()
            print(f"{RED}Please choose 1 or 2.{RESET}")
    else:
        print(f"  {YELLOW}No saved pet found.{RESET}\n")
        return adopt_pet()


def game_loop(pet: Pet) -> None:
    """Main interaction loop."""
    actions = {
        "1": pet.feed,
        "2": pet.play,
        "3": pet.sleep,
        "4": pet.heal,
    }

    while True:
        # Apply time-based changes
        alerts = pet.tick()
        pet.save()

        clear()
        print(banner())
        print(get_art(pet.species, pet.mood))
        print(display_stats(pet))

        for alert in alerts:
            print(f"\n  {YELLOW}{alert}{RESET}")

        if not pet.is_alive:
            print(f"\n  {RED}{BOLD}Game Over.{RESET} "
                  f"Thanks for caring for {pet.name}. 🕊️\n")
            break

        print(display_menu(pet))
        choice = prompt("Action")

        if choice in ("q", "quit", "exit"):
            pet.save()
            print(f"\n{GREEN}💾 Game saved! "
                  f"See you later, {pet.name}!{RESET}\n")
            break

        if choice == "5":
            # Stats already shown, just pause
            prompt("Press Enter to continue")
            continue

        action = actions.get(choice)
        if action:
            result = action()
            pet.save()
            clear()
            print(banner())
            print(get_art(pet.species, pet.mood))
            print(f"\n  {GREEN}{result}{RESET}\n")
            prompt("Press Enter to continue")
        else:
            print(f"\n  {RED}Unknown choice. Try 1-5 or q.{RESET}")
            prompt("Press Enter to continue")


if __name__ == "__main__":
    try:
        pet = main_menu()
        game_loop(pet)
    except KeyboardInterrupt:
        print(f"\n\n{GREEN}👋 Goodbye!{RESET}\n")
        sys.exit(0)
