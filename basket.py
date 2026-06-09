"""
The player-controlled basket.

Moves left/right with arrow keys (or A/D). Can also dash (Shift) and jump
(Space). Dashing spends one stamina bar and gives a quick horizontal burst;
jumping is free. Jump within a short window of a dash and you get a
Deadlock-style dash-jump: a big momentum boost that flings the basket across
the screen. Stamina (3 bars) regenerates slowly.
"""

import pygame

from config import (
    AIR_CONTROL,
    AIR_FRICTION,
    BASKET_COLOR,
    BASKET_HEIGHT,
    BASKET_SPEED,
    BASKET_WIDTH,
    BASKET_Y_OFFSET,
    DASH_COST,
    DASH_DURATION_MS,
    DASH_JUMP_BOOST,
    DASH_JUMP_VY_MULT,
    DASH_JUMP_WINDOW_MS,
    DASH_SPEED,
    GRAVITY,
    GROUND_FRICTION,
    HEIGHT,
    JUMP_VELOCITY,
    MAX_STAMINA,
    STAMINA_REGEN_PER_SEC,
    WIDTH,
)


class Basket:
    def __init__(self):
        self.width = BASKET_WIDTH
        self.height = BASKET_HEIGHT
        self.x = WIDTH // 2 - self.width // 2
        self.base_y = HEIGHT - BASKET_Y_OFFSET - self.height  # resting "ground" line
        self.y = self.base_y
        self.speed = BASKET_SPEED

        self.vx = 0.0          # horizontal velocity (from dashes / dash-jumps)
        self.vy = 0.0          # vertical velocity (from jumps + gravity)
        self.on_ground = True
        self.facing = 1        # 1 = right, -1 = left (last direction moved/dashed)

        self.stamina = float(MAX_STAMINA)
        self.dash_timer = 0.0       # ms left of the active dash burst
        self.dash_jump_window = 0.0  # ms left where a jump becomes a dash-jump

    # --- discrete actions (called from KEYDOWN events) ---

    def dash(self):
        """Burst horizontally in the facing direction. Costs one stamina bar."""
        if self.stamina < DASH_COST:
            return
        self.stamina -= DASH_COST
        self.vx = self.facing * DASH_SPEED
        self.dash_timer = DASH_DURATION_MS
        self.dash_jump_window = DASH_JUMP_WINDOW_MS

    def jump(self):
        """Leap upward. If a dash just happened, chain into a dash-jump."""
        if not self.on_ground:
            return  # no double-jumping
        self.on_ground = False
        if self.dash_jump_window > 0:
            # Dash-jump combo: keep (and boost) the dash momentum and leap higher.
            self.vx = self.facing * (DASH_SPEED + DASH_JUMP_BOOST)
            self.vy = JUMP_VELOCITY * DASH_JUMP_VY_MULT
            self.dash_jump_window = 0
        else:
            self.vy = JUMP_VELOCITY

    @property
    def dash_jump_ready(self):
        """True during the brief window where pressing jump yields the combo."""
        return self.dash_jump_window > 0

    # --- per-frame update ---

    def update(self, dt, keys):
        # Left/right input. Full control on the ground, reduced control in the air.
        move = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move += 1
        if move != 0:
            self.facing = move
        control = self.speed if self.on_ground else self.speed * AIR_CONTROL
        self.x += move * control

        # Carry dash / dash-jump momentum and vertical motion.
        self.x += self.vx
        self.y += self.vy
        self.vy += GRAVITY

        # Land on the ground line.
        if self.y >= self.base_y:
            self.y = self.base_y
            self.vy = 0.0
            self.on_ground = True

        # Decay horizontal momentum once the dash burst is over.
        if self.dash_timer > 0:
            self.dash_timer -= dt
        else:
            self.vx *= GROUND_FRICTION if self.on_ground else AIR_FRICTION
            if abs(self.vx) < 0.1:
                self.vx = 0.0

        # Tick down the dash-jump window.
        if self.dash_jump_window > 0:
            self.dash_jump_window -= dt

        # Slow stamina regen.
        if self.stamina < MAX_STAMINA:
            self.stamina = min(MAX_STAMINA, self.stamina + STAMINA_REGEN_PER_SEC * dt / 1000.0)

        # Clamp to the screen; kill momentum when we hit a wall.
        clamped = max(0, min(WIDTH - self.width, self.x))
        if clamped != self.x:
            self.vx = 0.0
        self.x = clamped

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            BASKET_COLOR,
            (self.x, self.y, self.width, self.height),
            border_radius=6,
        )

    def catches(self, item):
        """Return True if the basket's top edge overlaps the item."""
        within_x = self.x <= item.x <= self.x + self.width
        within_y = self.y <= item.y <= self.y + self.height
        return within_x and within_y
