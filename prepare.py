import pyganim, time
from generics import *

pygame.init()
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
clock  = pygame.time.Clock()
pygame.display.set_caption('Project Super Awesome Fun Time')
pygame.mouse.set_visible(False)

# Fonts
TITLEFONT = pygame.font.SysFont('arial', 17, bold=True)
BIGFONT   = pygame.font.SysFont('arial', 30, bold=True)
TABFONT   = pygame.font.SysFont('arial', 25)
MENUFONT  = pygame.font.SysFont('arial', 20)
FPSFONT   = pygame.font.SysFont('monospace', 15)
HUDFONT   = pygame.font.SysFont('monospace', 17)
NAMEFONT  = pygame.font.SysFont('monospace', 20, bold=True)

# Graphics converted to save memory

PLAYERMENU = pygame.image.load('images/player menu.png').convert()

# Loots
COINSHEET = pygame.image.load('images/spinning gold coin.png').convert_alpha()

# Explosions
EXPLOSIONRECT = pygame.image.load('explosion rect.png')

EXPLOSHEET1 = pygame.image.load('images/explo1.png').convert()
EXPLOSHEET1_trans = EXPLOSHEET1.get_at((0, 0))
EXPLOSHEET1.set_colorkey((EXPLOSHEET1_trans))

EXPLOSHEET2 = pygame.image.load('images/explo2.png').convert()
EXPLOSHEET2.set_colorkey((WHITE))

# Enemy
UFOSHEET     = pygame.image.load('images/ufo sheet.png').convert()

EYEBALLIMAGE = pygame.image.load('images/eyeball.png').convert()
EYEBALLIMAGE.set_colorkey((WHITE))

ENEMYIMAGE   = pygame.image.load('images/enemy.png').convert()

BLANKENEMY   = pygame.image.load('images/blank enemy.png').convert()
BLANKENEMY.set_colorkey((WHITE))

ASTEROID     = pygame.image.load('images/asteroid.png').convert()
ASTEROID.set_colorkey((WHITE))

# Cursor
CROSSHAIR = pygame.image.load('images/crosshair.png').convert_alpha()

# Player
PLAYERRECT = pygame.image.load('images/player rect.png').convert()
PLAYERRECT.set_colorkey((WHITE))

BLUESHIP   = pygame.image.load('images/blueship.png').convert()
BLUESHIP.set_colorkey((WHITE))

# Weapon
LASERIMAGE = pygame.image.load('images/laser horiz.png').convert_alpha()

# Border
RIGHTWALL  = pygame.image.load('images/right wall.png').convert()
LEFTWALL   = pygame.image.load('images/left wall.png').convert()
TOPWALL    = pygame.image.load('images/top wall.png').convert()
BOTTOMWALL = pygame.image.load('images/bottom wall.png').convert()

# Background
SPACEIMAGE = pygame.image.load('images/space.png').convert()

# Planets
PLANET1 = pygame.image.load('images/planet1.png').convert_alpha()
PLANET2 = pygame.image.load('images/planet2.png').convert_alpha()
PLANET3 = pygame.image.load('images/planet3.png').convert_alpha()
PLANET4 = pygame.image.load('images/planet4.png').convert_alpha()

# UFO animation
ufo_sprites = cutSpriteSheet(84, 84, 6, 84, UFOSHEET, 6)

UFOANIM = pyganim.PygAnimation(
    [(ufo_sprites[0], 0.1), (ufo_sprites[1], 0.1), (ufo_sprites[2], 0.1),
     (ufo_sprites[3], 0.1), (ufo_sprites[4], 0.1), (ufo_sprites[5], 0.1)])

# Explosion animations
explo_sprites_1 = cutSpriteSheet(50, 128, 18, 128, EXPLOSHEET1, 18)

EXPLOANIM1 = pyganim.PygAnimation(
    [(explo_sprites_1[0], 0.05), (explo_sprites_1[1], 0.05), (explo_sprites_1[2], 0.05),
     (explo_sprites_1[3], 0.05), (explo_sprites_1[4], 0.05), (explo_sprites_1[5], 0.05),
     (explo_sprites_1[6], 0.05), (explo_sprites_1[7], 0.05), (explo_sprites_1[8], 0.05),
     (explo_sprites_1[9], 0.05), (explo_sprites_1[10], 0.05), (explo_sprites_1[11], 0.05),
     (explo_sprites_1[12], 0.05), (explo_sprites_1[13], 0.05), (explo_sprites_1[14], 0.05),
     (explo_sprites_1[15], 0.05), (explo_sprites_1[16], 0.05), (explo_sprites_1[17], 0.05)],
    loop = False)

explo_sprites_2 = cutSpriteSheet(64, 64, 8, 512, EXPLOSHEET2, 36)

EXPLOANIM2 = pyganim.PygAnimation(
    [(explo_sprites_2[0], 0.05), (explo_sprites_2[1], 0.05), (explo_sprites_2[2], 0.05),
     (explo_sprites_2[3], 0.05), (explo_sprites_2[4], 0.05), (explo_sprites_2[5], 0.05),
     (explo_sprites_2[6], 0.05), (explo_sprites_2[7], 0.05), (explo_sprites_2[8], 0.05),
     (explo_sprites_2[9], 0.05), (explo_sprites_2[10], 0.05), (explo_sprites_2[11], 0.05),
     (explo_sprites_2[12], 0.05), (explo_sprites_2[13], 0.05), (explo_sprites_2[14], 0.05),
     (explo_sprites_2[15], 0.05), (explo_sprites_2[16], 0.05), (explo_sprites_2[17], 0.05),
     (explo_sprites_2[18], 0.05), (explo_sprites_2[19], 0.05), (explo_sprites_2[20], 0.05),
     (explo_sprites_2[21], 0.05), (explo_sprites_2[22], 0.05), (explo_sprites_2[23], 0.05),
     (explo_sprites_2[24], 0.05), (explo_sprites_2[25], 0.05), (explo_sprites_2[26], 0.05),
     (explo_sprites_2[27], 0.05), (explo_sprites_2[28], 0.05), (explo_sprites_2[29], 0.05),
     (explo_sprites_2[30], 0.05), (explo_sprites_2[31], 0.05), (explo_sprites_2[32], 0.05),
     (explo_sprites_2[33], 0.05), (explo_sprites_2[34], 0.05), (explo_sprites_2[35], 0.05)],
    loop = False)

# Sounds
LASERSOUND     = pygame.mixer.Sound('sounds/laser.wav')
EXPLOSIONSOUND = pygame.mixer.Sound('sounds/explosion.wav')
COLLECTCOIN    = pygame.mixer.Sound('sounds/collect coin.wav')
LANDINGSOUND   = pygame.mixer.Sound('sounds/landing1.wav')

