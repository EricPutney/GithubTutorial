"""
Catch the Falling Items - main game loop.

Controls:
    Left arrow / A   -> move basket left
    Right arrow / D  -> move basket right
    Shift            -> dash (costs 1 stamina)
    Space            -> jump (dash then jump quickly for a dash-jump combo)
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
    MAX_STAMINA,
    SPAWN_INTERVAL_MS,
    STAMINA_BAR_CENTER,
    STAMINA_BAR_HEIGHT,
    STAMINA_BAR_WIDTH,
    STAMINA_COLOR,
    STAMINA_EMPTY_COLOR,
    STAMINA_READY_COLOR,
    STAMINA_SEG_GAP,
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

        self.draw_stamina()

        if self.game_over:
            text = self.big_font.render("GAME OVER", True, TEXT_COLOR)
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, rect)
            hint = self.font.render("Press R to restart", True, TEXT_COLOR)
            hint_rect = hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            self.screen.blit(hint, hint_rect)

        pygame.display.flip()

    def draw_stamina(self):
        """Deadlock-style centered stamina pips: grey normally, blue when a
        dash-jump is available."""
        cx, cy = STAMINA_BAR_CENTER
        n = MAX_STAMINA
        seg_w = (STAMINA_BAR_WIDTH - STAMINA_SEG_GAP * (n - 1)) / n
        left = cx - STAMINA_BAR_WIDTH / 2
        top = cy - STAMINA_BAR_HEIGHT / 2

        ready = self.basket.dash_jump_ready
        fill_color = STAMINA_READY_COLOR if ready else STAMINA_COLOR

        for i in range(n):
            x = left + i * (seg_w + STAMINA_SEG_GAP)
            # Dim background for the full segment.
            pygame.draw.rect(
                self.screen,
                STAMINA_EMPTY_COLOR,
                (x, top, seg_w, STAMINA_BAR_HEIGHT),
                border_radius=3,
            )
            # Filled portion (the partially-regenerated pip fills left-to-right).
            seg_fill = max(0.0, min(1.0, self.basket.stamina - i))
            if seg_fill > 0:
                pygame.draw.rect(
                    self.screen,
                    fill_color,
                    (x, top, seg_w * seg_fill, STAMINA_BAR_HEIGHT),
                    border_radius=3,
                )

    def run(self):
        while True:
            dt = self.clock.tick(FPS)  # ms since last frame

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit(0)
                    if event.key == pygame.K_r and self.game_over:
                        self.reset()
                    if not self.game_over:
                        if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                            self.basket.dash()
                        elif event.key == pygame.K_SPACE:
                            self.basket.jump()
                if event.type == self.SPAWN_EVENT and not self.game_over:
                    self.spawn_item()

            if not self.game_over:
                keys = pygame.key.get_pressed()
                self.basket.update(dt, keys)
                self.update()

            self.draw()


if __name__ == "__main__":
    Game().run()
