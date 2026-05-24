"""A yellow star. Rarer than apples and worth +3 points."""

import math

import pygame

from .base import FallingItem


class Star(FallingItem):
    radius = 16
    color = (250, 210, 60)
    base_fall_speed = 4

    def draw(self, surface):
        points = []
        for i in range(10):
            angle = -math.pi / 2 + i * math.pi / 5
            r = self.radius if i % 2 == 0 else self.radius / 2.3
            points.append((self.x + r * math.cos(angle), self.y + r * math.sin(angle)))
        pygame.draw.polygon(surface, self.color, points)

    def on_collect(self, game):
        game.score += 3
        super().on_collect(game)
