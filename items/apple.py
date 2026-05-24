"""An ordinary red apple. Catching one gives +1 point."""

import pygame

from .base import FallingItem


class Apple(FallingItem):
    radius = 14
    color = (220, 50, 50)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
        # tiny stem
        pygame.draw.rect(
            surface,
            (60, 100, 40),
            (self.x - 2, self.y - self.radius - 4, 4, 5),
        )

    def on_collect(self, game):
        game.score += 1
        super().on_collect(game)
