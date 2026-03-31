"""Virtual Pet model — tracks stats, moods, and aging."""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path

SAVE_FILE = Path(__file__).parent / "savegame.json"

MAX_STAT = 100
MIN_STAT = 0
TICK_SECONDS = 30
SICK_THRESHOLD = 20


class Species(str, Enum):
    CAT = "cat"
    DOG = "dog"
    RABBIT = "rabbit"
    DRAGON = "dragon"


class Mood(str, Enum):
    HAPPY = "happy"
    NEUTRAL = "neutral"
    SAD = "sad"
    SLEEPY = "sleepy"
    SICK = "sick"


@dataclass
class Pet:
    name: str
    species: Species
    hunger: int = 30       # 0 = full, 100 = starving
    happiness: int = 70
    energy: int = 80
    health: int = 100
    age_minutes: float = 0.0
    is_alive: bool = True
    created_at: float = field(default_factory=time.time)
    last_tick: float = field(default_factory=time.time)

    @property
    def mood(self) -> Mood:
        if not self.is_alive:
            return Mood.SAD
        if self.health <= SICK_THRESHOLD:
            return Mood.SICK
        if self.energy <= 15:
            return Mood.SLEEPY
        if self.happiness >= 60 and self.hunger <= 50:
            return Mood.HAPPY
        if self.happiness <= 30 or self.hunger >= 80:
            return Mood.SAD
        return Mood.NEUTRAL

    @property
    def age_display(self) -> str:
        mins = int(self.age_minutes)
        if mins < 60:
            return f"{mins}m"
        return f"{mins // 60}h {mins % 60}m"

    def _clamp(self, value: int) -> int:
        return max(MIN_STAT, min(MAX_STAT, value))

    def feed(self) -> str:
        if not self.is_alive:
            return f"{self.name} is no longer with us… 💔"
        self.hunger = self._clamp(self.hunger - 25)
        self.energy = self._clamp(self.energy + 5)
        self.health = self._clamp(self.health + 2)
        return f"You fed {self.name}! 🍖 Yum!"

    def play(self) -> str:
        if not self.is_alive:
            return f"{self.name} is no longer with us… 💔"
        if self.energy < 10:
            return f"{self.name} is too tired to play! 😴"
        self.happiness = self._clamp(self.happiness + 20)
        self.hunger = self._clamp(self.hunger + 15)
        self.energy = self._clamp(self.energy - 20)
        return f"You played with {self.name}! 🎾 So much fun!"

    def sleep(self) -> str:
        if not self.is_alive:
            return f"{self.name} is no longer with us… 💔"
        self.energy = self._clamp(self.energy + 40)
        self.hunger = self._clamp(self.hunger + 10)
        self.happiness = self._clamp(self.happiness - 5)
        return f"{self.name} took a nice nap! 😴💤"

    def heal(self) -> str:
        if not self.is_alive:
            return f"{self.name} is no longer with us… 💔"
        if self.health > SICK_THRESHOLD:
            return f"{self.name} is not sick! No healing needed. 👍"
        self.health = self._clamp(self.health + 40)
        self.happiness = self._clamp(self.happiness + 10)
        return f"You gave {self.name} medicine! 💊 Feeling better!"

    def tick(self) -> list[str]:
        """Apply time-based stat changes. Returns event messages."""
        now = time.time()
        elapsed = now - self.last_tick
        ticks = int(elapsed // TICK_SECONDS)
        if ticks <= 0:
            return []
        self.last_tick = now
        self.age_minutes += (ticks * TICK_SECONDS) / 60.0
        messages: list[str] = []
        for _ in range(ticks):
            if not self.is_alive:
                break
            self.hunger = self._clamp(self.hunger + 3)
            self.happiness = self._clamp(self.happiness - 2)
            self.energy = self._clamp(self.energy - 2)
            if self.hunger >= 90:
                self.health = self._clamp(self.health - 5)
            if self.happiness <= 10:
                self.health = self._clamp(self.health - 3)
            if self.health <= 0:
                self.is_alive = False
                self.health = 0
                messages.append(f"💔 {self.name} has passed away…")
                break
        if self.is_alive and self.mood == Mood.SICK:
            messages.append(f"⚠️  {self.name} is sick! Heal quickly!")
        elif self.is_alive and self.hunger >= 80:
            messages.append(f"⚠️  {self.name} is very hungry!")
        elif self.is_alive and self.energy <= 15:
            messages.append(f"⚠️  {self.name} is exhausted!")
        return messages

    def save(self, path: Path = SAVE_FILE) -> None:
        data = asdict(self)
        data["species"] = self.species.value
        path.write_text(json.dumps(data, indent=2))

    @classmethod
    def load(cls, path: Path = SAVE_FILE) -> Pet | None:
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text())
            data["species"] = Species(data["species"])
            return cls(**data)
        except (json.JSONDecodeError, KeyError, TypeError):
            return None
