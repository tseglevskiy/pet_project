"""ASCII art for each species and mood."""

from pet import Mood, Species

CAT_HAPPY = r"""
  /\_____/\
 /  ^   ^  \
( (  ◕ ◕  ) )
 \ ( = ^ = ) /
  \  '---'  /
  / |     | \
 (_/       \_)
"""

CAT_SAD = r"""
  /\_____/\
 /  ^   ^  \
( (  ╥ ╥  ) )
 \ ( - ~ - ) /
  \  '---'  /
  / |     | \
 (_/       \_)
"""

CAT_SLEEPY = r"""
  /\_____/\
 /  ^   ^  \
( (  - -  ) ) z Z
 \ ( = ~ = ) /
  \  '---'  /
  / |     | \
 (_/       \_)
"""

CAT_SICK = r"""
  /\_____/\
 /  ^   ^  \
( (  x x  ) )
 \ ( = ~ = ) /  ~
  \  '---'  /
  / |     | \
 (_/       \_)
"""

CAT_NEUTRAL = r"""
  /\_____/\
 /  ^   ^  \
( (  o o  ) )
 \ ( = ^ = ) /
  \  '---'  /
  / |     | \
 (_/       \_)
"""

DOG_HAPPY = r"""
  __   __
 /  \ /  \
| ^o^ |---'
 \__U__/  |
  |   |  /J
 _|___|__/
(_________)
"""

DOG_SAD = r"""
  __   __
 /  \ /  \
| ;_; |---'
 \__U__/  |
  |   |  /J
 _|___|__/
(_________)
"""

DOG_SLEEPY = r"""
  __   __
 /  \ /  \
| -.- |---' zZ
 \__U__/  |
  |   |  /J
 _|___|__/
(_________)
"""

DOG_SICK = r"""
  __   __
 /  \ /  \
| x.x |---'
 \__U__/  |
  |   |  /J
 _|___|__/
(_________)
"""

DOG_NEUTRAL = r"""
  __   __
 /  \ /  \
| o.o |---'
 \__U__/  |
  |   |  /J
 _|___|__/
(_________)
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
