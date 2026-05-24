"""
Catch the Falling Items - main game loop.

Controls:
    Left arrow / A   -> move basket left
    Right arrow / D  -> move basket right
    R                -> restart after game over
    Esc              -> quit

The game ends when you miss MAX_MISSES items (see config.py).

----------------------------------------------------------------------
Feature ideas (each one is a GitHub issue you can pick up):

    * Add a Bomb item that subtracts points when caught            (issue #1)
    * Add a GoldenApple worth bonus points (rare)                  (issue #2)
    * Add a Freeze powerup that slows all items for a few seconds  (issue #3)
    * Add a Magnet powerup that pulls items toward the basket      (issue #4)
    * Add a LifeHeart that grants +1 miss allowance                (issue #5)
    * Add a Shrink debuff that makes the basket smaller            (issue #6)
    * Add a DoublePoints powerup (2x scoring for 10 seconds)       (issue #7)
    * Add a Cloud obstacle (visual difficulty, no point effect)    (issue #8)

To add one, create a new file in items/ (e.g. items/bomb.py), subclass
FallingItem, then register your class in items/__init__.py.
----------------------------------------------------------------------
"""

import random
import sys

import pygame

from basket import Basket
from config import (
    BG_COLOR,
    FPS,
    HEIGHT,
    MAX_MISSES,
    SPAWN_INTERVAL_MS,
    TEXT_COLOR,
    TITLE,
    WIDTH,
)
from items import ITEMS


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 32)
        self.big_font = pygame.font.SysFont(None, 64)

        self.basket = Basket()
        self.reset()

        # custom event for spawning items at a regular interval
        self.SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_EVENT, SPAWN_INTERVAL_MS)

    def reset(self):
        self.items = []
        self.score = 0
        self.misses = 0
        self.game_over = False

    def spawn_item(self):
        # 80% chance of a good item, 20% bad. If "bad" is empty (default
        # before participants add bombs etc.), fall back to good.
        category = "good"
        if ITEMS.get("bad") and random.random() < 0.2:
            category = "bad"
        cls = random.choice(ITEMS[category])
        x = random.randint(20, WIDTH - 20)
        # weight varies a little so items don't all fall at the same speed
        weight = random.uniform(0.8, 1.3)
        # NOTE: keyword args here. Items built against the old (x, y) signature
        # will fail loudly with "unexpected keyword argument 'pos'", forcing
        # contributors to update their __init__ to the new signature.
        self.items.append(cls(pos=(x, 0), weight=weight))

    def update(self):
        for item in self.items:
            item.update()
            if self.basket.catches(item):
                item.on_collect(self)
            elif item.y > HEIGHT:
                item.on_missed(self)
        self.items = [it for it in self.items if it.alive]

        if self.misses >= MAX_MISSES:
            self.game_over = True

    def draw(self):
        self.screen.fill(BG_COLOR)
        for item in self.items:
            item.draw(self.screen)
        self.basket.draw(self.screen)

        hud = self.font.render(
            f"Score: {self.score}    Misses: {self.misses}/{MAX_MISSES}",
            True,
            TEXT_COLOR,
        )
        self.screen.blit(hud, (10, 10))

        if self.game_over:
            text = self.big_font.render("GAME OVER", True, TEXT_COLOR)
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, rect)
            hint = self.font.render("Press R to restart", True, TEXT_COLOR)
            hint_rect = hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            self.screen.blit(hint, hint_rect)

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.game_over:
                    self.reset()
                if event.type == self.SPAWN_EVENT and not self.game_over:
                    self.spawn_item()

            if not self.game_over:
                keys = pygame.key.get_pressed()
                self.basket.handle_input(keys)
                self.update()

            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()
