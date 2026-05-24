"""
The FallingItem base class.

Every item that falls from the sky (apple, star, and the ones YOU add) inherits
from this class. To add a new item, create a new file in items/ and subclass
FallingItem. See items/apple.py for the simplest example.

----------------------------------------------------------------------
Refactor notes (newupdate):

This class used to be initialized as `FallingItem(x, y)` and the catch hook
was named `on_caught`. Both have changed:

    - __init__ now takes a (x, y) position tuple `pos` and a `weight` float
      that scales the fall speed (heavier things fall faster).
    - The catch hook is now `on_collect` (the rename matches `on_missed` and
      makes it clearer that "collect" applies whether or not points are gained).

Subclasses must update their `super().__init__(...)` calls and rename their
override of `on_caught` to `on_collect`.
----------------------------------------------------------------------
"""


class FallingItem:
    """A thing that falls from the top of the screen and can be caught."""

    # subclasses can override these
    base_fall_speed = 5
    radius = 12

    def __init__(self, pos, weight=1.0):
        # pos = (x, y) center of the item in screen pixels
        # weight = multiplier on fall speed (1.0 = normal, 2.0 = twice as fast)
        self.x, self.y = pos
        self.weight = weight
        self.alive = True

    def update(self):
        """Move one frame's worth of motion. Called every tick by the game loop."""
        self.y += self.base_fall_speed * self.weight

    def draw(self, surface):
        """Render this item onto the given pygame surface. Subclasses override."""
        raise NotImplementedError("Subclasses must implement draw()")

    def on_collect(self, game):
        """
        Called once when the basket catches this item.
        Override to add score, trigger effects, etc., then call super().on_collect(game)
        so the item is removed from the screen.
        """
        self.alive = False

    def on_missed(self, game):
        """Called once when this item falls off the bottom of the screen."""
        self.alive = False
        game.misses += 1
