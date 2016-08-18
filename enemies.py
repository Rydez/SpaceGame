from weapon import *

enemy_attackables = pygame.sprite.RenderUpdates()

kamikaze_group = pygame.sprite.RenderUpdates()
star_group     = pygame.sprite.RenderUpdates()
asteroid_group = pygame.sprite.RenderUpdates()


# Make enemy sprite to be put in groups
class KamikazeEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image  = image
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # Particular enemy movement style (chase and then kamikaze into player)
    def update(self, victim_x, victim_y):
        self.victim_x = victim_x
        self.victim_y = victim_y
        if self.rect.x > self.victim_x:
            self.rect.x -= ENEMYSPEED
        if self.rect.x < self.victim_x:
            self.rect.x += ENEMYSPEED
        if self.rect.y < self.victim_y:
            self.rect.y += ENEMYSPEED
        if self.rect.y > self.victim_y:
            self.rect.y -= ENEMYSPEED

# Maybe do asteroid too
class AsteroidEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image  = image
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed  = random.randint(1, 10)

        target_x = random.randint(-self.rect.x, WINDOWWIDTH - self.rect.x)
        target_y = random.randint(-self.rect.y, WINDOWHEIGHT - self.rect.y)
        # if self.rect.x == WINDOWWIDTH or self.rect.y == WINDOWHEIGHT:
        #     self.target_vector = (-target_x, -target_y)
        # else:
        self.target_vector = (target_x, target_y)

    def update(self):

        # Only update if fired shot is within 500 pixels of display
        if self.rect.x >= -500 and self.rect.x <= WINDOWWIDTH + 500 and self.rect.y >= -500 and self.rect.y <= WINDOWHEIGHT + 500:
            if self.speed != 0:
                move_vector = [c * self.speed for c in normalize(self.target_vector)]
                self.rect.x, self.rect.y = add((self.rect.x, self.rect.y), move_vector)

        else:
            arena_sprites.remove(self)
            enemy_attackers.remove(self)
            enemy_attackables.remove(self)
            asteroid_group.remove(self)

class StarEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image  = image
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dest_x = random.randint(0, WINDOWWIDTH - ENEMYWIDTH)
        self.dest_y = random.randint(0, WINDOWHEIGHT - ENEMYHEIGHT)

    def update(self, enemy_weap_group, arena_sprites, LASERSOUND, LASERIMAGE, spawn_ctr):
        if abs(self.rect.x - self.dest_x) > ENEMYSPEED or abs(self.rect.y - self.dest_y) > ENEMYSPEED:
            if self.rect.x > self.dest_x:
                self.rect.x -= ENEMYSPEED
            if self.rect.x < self.dest_x:
                self.rect.x += ENEMYSPEED
            if self.rect.y < self.dest_y:
                self.rect.y += ENEMYSPEED
            if self.rect.y > self.dest_y:
                self.rect.y -= ENEMYSPEED
        else:
            if spawn_ctr % 50 == 0:
                # Lists configured for weapon starting coords, to prevent weapon and enemy collision upon enemy firing
                coords_x = [0, 0, (ENEMYWIDTH), -(ENEMYWIDTH)]
                coords_y = [-(ENEMYHEIGHT), (ENEMYHEIGHT), 0, 0]

                LASERSOUND.play()
                enemy_center_x = self.rect.x + (ENEMYWIDTH/2)
                enemy_center_y = self.rect.y + (ENEMYHEIGHT/2)
                north_vector = normalize(sub((enemy_center_x, enemy_center_y - 1), (enemy_center_x, enemy_center_y)))
                south_vector = normalize(sub((enemy_center_x, enemy_center_y + 1), (enemy_center_x, enemy_center_y)))
                east_vector  = normalize(sub((enemy_center_x + 1, enemy_center_y), (enemy_center_x, enemy_center_y)))
                west_vector  = normalize(sub((enemy_center_x - 1, enemy_center_y), (enemy_center_x, enemy_center_y)))
                ortho_vects = [north_vector, south_vector, east_vector, west_vector]
                i = 0
                while i < len(ortho_vects):
                    if i == 0 or i == 1:
                        shot_angle = 90

                    elif i == 2 or i == 3:
                        shot_angle = 0

                    weapon = Weapon(LASERIMAGE, enemy_center_x + coords_x[i], enemy_center_y + coords_y[i], shot_angle, ortho_vects[i])
                    enemy_weap_group.add(weapon)
                    arena_sprites.add(weapon)
                    enemy_attackers.add(weapon)
                    arena_sprites.move_to_back(weapon)
                    i += 1