"""Tests for the Pet model."""

import json
import tempfile
import time
from pathlib import Path

from pet import MAX_STAT, MIN_STAT, SICK_THRESHOLD, Mood, Pet, Species


def test_new_pet_defaults():
    p = Pet(name="Kitty", species=Species.CAT)
    assert p.name == "Kitty"
    assert p.species == Species.CAT
    assert p.hunger == 30
    assert p.happiness == 70
    assert p.energy == 80
    assert p.health == 100
    assert p.is_alive is True


def test_mood_happy():
    p = Pet(name="X", species=Species.DOG, happiness=70, hunger=20)
    assert p.mood == Mood.HAPPY


def test_mood_sad():
    p = Pet(name="X", species=Species.DOG, happiness=10, hunger=90)
    assert p.mood == Mood.SAD


def test_mood_sleepy():
    p = Pet(name="X", species=Species.DOG, energy=10)
    assert p.mood == Mood.SLEEPY


def test_mood_sick():
    p = Pet(name="X", species=Species.DOG, health=15)
    assert p.mood == Mood.SICK


def test_feed():
    p = Pet(name="X", species=Species.CAT, hunger=50)
    msg = p.feed()
    assert "Yum" in msg
    assert p.hunger == 25


def test_play():
    p = Pet(name="X", species=Species.CAT, energy=50, happiness=50)
    msg = p.play()
    assert "fun" in msg
    assert p.happiness == 70
    assert p.energy == 30


def test_play_too_tired():
    p = Pet(name="X", species=Species.CAT, energy=5)
    old_happiness = p.happiness
    msg = p.play()
    assert "tired" in msg
    assert p.happiness == old_happiness


def test_sleep():
    p = Pet(name="X", species=Species.DOG, energy=30)
    msg = p.sleep()
    assert "nap" in msg
    assert p.energy == 70


def test_heal_when_sick():
    p = Pet(name="X", species=Species.DOG, health=10)
    msg = p.heal()
    assert "medicine" in msg
    assert p.health == 50


def test_heal_when_healthy():
    p = Pet(name="X", species=Species.DOG, health=80)
    msg = p.heal()
    assert "not sick" in msg
    assert p.health == 80


def test_clamp_no_overflow():
    p = Pet(name="X", species=Species.CAT, hunger=5)
    p.feed()
    assert p.hunger == MIN_STAT


def test_clamp_no_underflow():
    p = Pet(name="X", species=Species.CAT, hunger=95)
    p.play()  # hunger +15
    assert p.hunger == MAX_STAT


def test_dead_pet_actions():
    p = Pet(name="X", species=Species.CAT, is_alive=False)
    assert "no longer" in p.feed()
    assert "no longer" in p.play()
    assert "no longer" in p.sleep()
    assert "no longer" in p.heal()


def test_age_display_minutes():
    p = Pet(name="X", species=Species.CAT, age_minutes=45)
    assert p.age_display == "45m"


def test_age_display_hours():
    p = Pet(name="X", species=Species.CAT, age_minutes=125)
    assert p.age_display == "2h 5m"


def test_save_and_load():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        path = Path(f.name)
    try:
        p = Pet(name="Fido", species=Species.DOG, hunger=42)
        p.save(path)
        loaded = Pet.load(path)
        assert loaded is not None
        assert loaded.name == "Fido"
        assert loaded.species == Species.DOG
        assert loaded.hunger == 42
    finally:
        path.unlink(missing_ok=True)


def test_load_missing_file():
    result = Pet.load(Path("/tmp/nonexistent_pet_save.json"))
    assert result is None


def test_load_corrupt_file():
    with tempfile.NamedTemporaryFile(
        suffix=".json", delete=False, mode="w"
    ) as f:
        f.write("NOT VALID JSON {{{")
        path = Path(f.name)
    try:
        result = Pet.load(path)
        assert result is None
    finally:
        path.unlink(missing_ok=True)


def test_tick_no_change_if_recent():
    p = Pet(name="X", species=Species.CAT)
    p.last_tick = time.time()  # just now
    msgs = p.tick()
    assert msgs == []
    assert p.hunger == 30  # unchanged
