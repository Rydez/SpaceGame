from enemyControl import *
from loot import *
from weapon import *

player_group    = pygame.sprite.RenderUpdates()

# Create player to be added to group
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        # Define a starting time
        self.initial_time = time.time()

        # Bools for motion upon key press
        self.pressed_w = False
        self.pressed_s = False
        self.pressed_d = False
        self.pressed_a = False

        # Bools for where to blit explosions upon deaths
        self.enemy_explo = False
        self.current_explo = EXPLOANIM1.getCopy()

        self.change_check = False

        self.name = ''
        self.max_health = 10.0
        self.health = 10.0
        self.max_energy = 250.0
        self.energy = 250.0
        self.money  = 1000
        self.image  = image
        self.active_plyr_img = BLUESHIP
        self.angle  = 0
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed  = PLAYERSPEED

        self.collision_x = 0
        self.collision_y = 0

    # Change speeds depending on input
    def goRight(self):
        self.rect.x += self.speed

    def goLeft(self):
        self.rect.x -= self.speed

    def goUp(self):
        self.rect.y -= self.speed

    def goDown(self):
        self.rect.y += self.speed

    def visible(self, player_image):
        self.image = player_image

    def invisible(self, blank_image):
        self.image = blank_image

    def move(self):
        # Check for border collision and change player speed
        if self.pressed_w:
            if not pygame.sprite.collide_rect(self, top_wall):
                self.goUp()
        if self.pressed_s:
            if not pygame.sprite.collide_rect(self, bottom_wall):
                self.goDown()
        if self.pressed_d:
            if not pygame.sprite.collide_rect(self, right_wall):
                self.goRight()
        if self.pressed_a:
            if not pygame.sprite.collide_rect(self, left_wall):
                self.goLeft()

    def upgradeHealth(self):
        if (self.money - 150) >= 0:
            self.max_health += 50
            self.health += 50
            self.money  -= 150

    def upgradeEnergy(self):
        if (self.money - 150) >= 0:
            self.max_energy += 50
            self.energy += 50
            self.money  -= 150

    def upgradeSpeed(self):
        if (self.money - 300) >= 0:
            self.speed += 5
            self.money -= 300

    def drawEnergyBar(self):
        if self.energy > 0:
            pygame.draw.rect(screen, (255, 208, 0), (10, 70, self.energy * (200/self.max_energy), 10))
        energy_rect = customRect(10, 70, 200, 10)
        return energy_rect

    def drawHealthBar(self):
        if self.health > 0:
            pygame.draw.rect(screen, (75, 189, 0), (10, 50, self.health * (200/self.max_health), 10))
        health_rect = customRect(10, 50, 200, 10)
        return health_rect

    def regenEnergy(self):
        if self.energy < self.max_energy:
            self.energy += 1

    def useEnergy(self):
        if (self.energy - 50) >= 0:
            self.energy -= 50
            return True

    def namePlayer(self):
        name_input = NAMEFONT.render(self.name, True, (255, 255, 255))
        input_rect = name_input.get_rect()
        input_rect.center = screen.get_rect().center
        screen.blit(name_input, input_rect)
        return input_rect

    def damagePlayer(self):
        if pygame.sprite.groupcollide(player_group, enemy_attackers, False, False) and self.health > 1:
            pygame.sprite.groupcollide(player_group, enemy_attackers, False, True)
            self.health -= 1
            playExplosion(EXPLOSIONSOUND, EXPLOANIM2)

    def killPlayer(self):
        if pygame.sprite.groupcollide(player_group, enemy_attackers, True, True) and self.health == 1:
            self.health = 0
            self.change_check = False
            # Lower explosion by 78 pixels so that it appears over player
            explosion = GenericSprite(EXPLOSIONRECT, self.rect.x, self.rect.y - 78)
            arena_sprites.add(explosion)
            playExplosion(EXPLOSIONSOUND, EXPLOANIM1)
            self.active_plyr_img = PLAYERRECT
            clearGroups(enemy_attackables, enemy_attackers, kamikaze_group,
                        star_group,        loot_group,      BLANKENEMY)
            self.initial_time = time.time()
            return True

    def collectLoot(self):
        if pygame.sprite.groupcollide(player_group, loot_group, False, True):
            COLLECTCOIN.play()
            self.money += 10

    def killEnemy(self):
        if len(plyr_weap_group.sprites()) != 0:
            for enemy in enemy_attackables:
                if pygame.sprite.spritecollideany(enemy, plyr_weap_group):
                    if pygame.sprite.groupcollide(plyr_weap_group, enemy_attackables, True, True):
                        kamikaze_group.remove(enemy)
                        star_group.remove(enemy)
                        enemy_attackers.remove(enemy)
                        arena_sprites.remove(enemy)

                        self.collision_x = enemy.rect.x
                        self.collision_y = enemy.rect.y

                        explosion = GenericSprite(EXPLOSIONRECT, self.collision_x, self.collision_y - 78)
                        arena_sprites.add(explosion)

                        EXPLOSIONSOUND.play()
                        self.current_explo.play()

                        self.enemy_explo = True

                        coin = Coin(COINSHEET, self.collision_x, self.collision_y)
                        coin.COINANIM.play()

                        loot_group.add(coin)
                        arena_sprites.add(coin)

    def dockPlayer(self, home_planet):
        self.rect.center = home_planet.rect.center
        self.change_check = True

    def respawnPlayer(self):
        home_sprites.add(self)
        arena_sprites.add(self)
        player_group.add(self)
        self.active_plyr_img = BLUESHIP
        self.rect.x = 800
        self.rect.y = 450
        self.health = self.max_health

        # Update screen to show home background
        screen.blit(SPACEIMAGE, (0, 0))
        pygame.display.update()