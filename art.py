"""ASCII art for each species and mood."""

from pet import Mood, Species

CAT_HAPPY = r"""
  /\_/\
 ( ^.^ )
  > ^ <
 /|   |\
(_|   |_)
"""

CAT_SAD = r"""
  /\_/\
 ( T.T )
  > ~ <
 /|   |\
(_|   |_)
"""

CAT_SLEEPY = r"""
  /\_/\
 ( -.- ) z Z
  > ~ <
 /|   |\
(_|   |_)
"""

CAT_SICK = r"""
  /\_/\
 ( x.x )
  > ~ <
 /|   |\
(_|   |_)
"""

CAT_NEUTRAL = r"""
  /\_/\
 ( o.o )
  > ^ <
 /|   |\
(_|   |_)
"""

DOG_HAPPY = r"""
  / \__
 (    @\___
 /         O
/   (_____/
/_____/  U
"""

DOG_SAD = r"""
  / \__
 (    ;\___ 
 /         O
/   (_____/
/_____/  U
"""

DOG_SLEEPY = r"""
  / \__
 (    -\___ z Z
 /         O
/   (_____/
/_____/  U
"""

DOG_SICK = r"""
  / \__
 (    x\___
 /         O
/   (_____/
/_____/  U
"""

DOG_NEUTRAL = r"""
  / \__
 (    .\___
 /         O
/   (_____/
/_____/  U
"""

RABBIT_HAPPY = r"""
 (\(\
 ( ^.^)
 o_(")(")
"""

RABBIT_SAD = r"""
 (\(\
 ( T.T)
 o_(")(")
"""

RABBIT_SLEEPY = r"""
 (\(\
 ( -.-) z Z
 o_(")(")
"""

RABBIT_SICK = r"""
 (\(\
 ( x.x)
 o_(")(")
"""

RABBIT_NEUTRAL = r"""
 (\(\
 ( o.o)
 o_(")(")
"""

_ART = {
    Species.CAT: {
        Mood.HAPPY: CAT_HAPPY, Mood.SAD: CAT_SAD,
        Mood.SLEEPY: CAT_SLEEPY, Mood.SICK: CAT_SICK,
        Mood.NEUTRAL: CAT_NEUTRAL,
    },
    Species.DOG: {
        Mood.HAPPY: DOG_HAPPY, Mood.SAD: DOG_SAD,
        Mood.SLEEPY: DOG_SLEEPY, Mood.SICK: DOG_SICK,
        Mood.NEUTRAL: DOG_NEUTRAL,
    },
    Species.RABBIT: {
        Mood.HAPPY: RABBIT_HAPPY, Mood.SAD: RABBIT_SAD,
        Mood.SLEEPY: RABBIT_SLEEPY, Mood.SICK: RABBIT_SICK,
        Mood.NEUTRAL: RABBIT_NEUTRAL,
    },
}


def get_art(species: Species, mood: Mood) -> str:
    return _ART.get(species, {}).get(mood, "🐾")
