"""
The item registry.

Every item type that the game can spawn must be listed in ITEMS below.
When you add a new item, you must do TWO things:
    1. import your class here
    2. add it to ITEMS, in the "good" list if it helps the player
       or the "bad" list if it hurts (e.g. subtracts points)

The game picks a category by chance (good is more common), then a random
class from that category.

----------------------------------------------------------------------
Refactor notes (newupdate):

ITEMS used to be a flat list. It is now a dict so the game can balance
how often good vs. bad items appear. If you previously did:

    ITEMS = [Apple, Star, Bomb]

you now want:

    ITEMS = {"good": [Apple, Star], "bad": [Bomb]}
----------------------------------------------------------------------
"""

from .apple import Apple
from .star import Star

# TODO (issue #1): from .bomb import Bomb         -> subtracts points
# TODO (issue #2): from .golden_apple import GoldenApple  -> rare, big points
# TODO (issue #3): from .freeze import Freeze     -> slows all items briefly
# TODO (issue #4): from .magnet import Magnet     -> pulls items toward basket

ITEMS = {
    "good": [
        Apple,
        Apple,   # listed twice so apples are twice as common as stars
        Star,
    ],
    "bad": [],
}
