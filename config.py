"""
Game-wide constants. Tweak these if you want to experiment with how the game feels.

Nothing in this file does anything by itself — it's just numbers and colors that
other files import.
"""

# --- window ---
WIDTH = 600
HEIGHT = 700
FPS = 60
TITLE = "Catch the Falling Items"

# --- colors (R, G, B) ---
BG_COLOR = (20, 24, 40)
TEXT_COLOR = (240, 240, 240)
BASKET_COLOR = (180, 140, 60)

# --- basket ---
BASKET_WIDTH = 90
BASKET_HEIGHT = 18
BASKET_SPEED = 7
BASKET_Y_OFFSET = 40  # distance from bottom of screen

# --- movement physics (dash / jump) ---
GRAVITY = 0.7             # downward pull added to vertical speed each frame
JUMP_VELOCITY = -14       # initial upward speed of a jump (negative = up)
AIR_CONTROL = 0.5         # how much of normal left/right speed you keep mid-air
GROUND_FRICTION = 0.80    # horizontal speed kept per frame while grounded
AIR_FRICTION = 0.95       # horizontal speed kept per frame while airborne

DASH_SPEED = 20           # horizontal burst speed of a dash (px/frame)
DASH_DURATION_MS = 130    # how long the dash burst holds full speed
DASH_JUMP_WINDOW_MS = 250 # press jump within this window of a dash for the combo
DASH_JUMP_BOOST = 12      # extra horizontal speed granted by a dash-jump
DASH_JUMP_VY_MULT = 1.15  # dash-jumps leap a little higher than a normal jump

# --- stamina ---
MAX_STAMINA = 3             # number of stamina bars
DASH_COST = 1               # stamina spent per dash
STAMINA_REGEN_PER_SEC = 0.5 # bars regenerated per second (slow trickle)

# --- stamina bar UI ---
STAMINA_BAR_CENTER = (WIDTH // 2, 64)  # center point of the bar (it's centered here)
STAMINA_BAR_WIDTH = 180
STAMINA_BAR_HEIGHT = 14
STAMINA_SEG_GAP = 5                    # gap between the segment pips
STAMINA_COLOR = (205, 210, 220)        # white/grey when stamina is just stamina
STAMINA_EMPTY_COLOR = (60, 66, 84)     # dim background of a depleted segment
STAMINA_READY_COLOR = (70, 150, 255)   # blue: a dash-jump combo is available

# --- spawning ---
SPAWN_INTERVAL_MS = 700   # how often a new item appears
MAX_MISSES = 5            # game over after this many missed items
