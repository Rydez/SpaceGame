import sys
from pygame.locals import *
from player import *
from playerMenu import *
from loot import *
from enemyControl import *
from hud import *
from storeMenu import *
from confirmationMenu import *

def enemyWeaponCollide(weapon_group, enemytype_group):
    if len(weapon_group.sprites()) != 0:     
        for enemy in enemytype_group:
            if pygame.sprite.spritecollideany(enemy, weapon_group):
                if pygame.sprite.groupcollide(weapon_group, enemytype_group, True, True):
                    return True

class Control:
    def __init__(self):

        self.environment = Environment()
        self.enemyControl = EnemyControl()
        self.hud = Hud()
        self.angle_between = 0
        # Create the player
        self.player = Player(800, 450, PLAYERRECT)
        player_group.add(self.player)
        # Create crosshair object
        self.crosshair = Crosshair(CROSSHAIR, pygame.mouse.get_pos())
        cursor_group.add(self.crosshair)
        # Call and create a player menu to be toggled
        self.playermenu = PlayerMenu(self.player.rect.x + PLAYERWIDTH, self.player.rect.y + PLAYERHEIGHT)
        # Call and create a player menu to be toggled
        self.storemenu = StoreMenu()
        # Call and create a confirmation menu to prompt the player
        self.confirmationmenu = ConfirmationMenu()

        # Groups to minimize what is updated. One location updated at a time
        home_sprites.add(player_group, planet_group, cursor_group)
        arena_sprites.add(player_group, cursor_group)

        # Move player to front of layers
        arena_sprites.move_to_front(self.player)

        # Update so background appears
        screen.blit(SPACEIMAGE, (0, 0))
        pygame.display.update()

    def mainGameLoop(self):
        # Main game loop
        while True:
            self.eventLoop()
            self.update()
            self.draw()
            clock.tick(FPS)

    def eventLoop(self):
        events = pygame.event.get()
        for event in events:

            # Handle quitting
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif self.environment.go_start:
                if event.type == KEYDOWN:
                    if event.unicode.isalpha():
                        self.player.name += event.unicode
                    elif event.key == K_BACKSPACE:
                        self.player.name = self.player.name[:-1]
                    elif event.key == K_SPACE:
                        self.player.name += ' '
                    elif event.key == K_RETURN:
                        self.environment.go_start = False
                        self.environment.go_home  = True
                        screen.blit(SPACEIMAGE, (0, 0))
                        pygame.display.update()

            elif not self.environment.go_start:

                # Handle player controls
                # Vector from player to cursor
                moveVect = normalize(sub(pygame.mouse.get_pos(), (self.player.rect.x + (PLAYERWIDTH/2), self.player.rect.y + (PLAYERHEIGHT/2))))
                # Unit vector pointing east
                currentVect = (1, 0)
                # Get angle of rotation and give it to the player
                self.angle_between = 180 * angle(moveVect, currentVect) / math.pi

                # Change player to new angle
                if moveVect != None:
                    if moveVect[1] > 0:
                        self.angle_between *= -1
                    self.player.angle = self.angle_between

                # Fire when mouse is clicked
                if self.environment.game_over == False:
                    if event.type == pygame.MOUSEBUTTONDOWN and self.environment.go_arena:
                        if self.player.useEnergy():
                            LASERSOUND.play()
                            target_vector = normalize(sub(event.pos, (self.player.rect.x + (PLAYERWIDTH/2), self.player.rect.y + (PLAYERHEIGHT/2))))
                            weapon = Weapon(LASERIMAGE, self.player.rect.x + (PLAYERWIDTH/2), self.player.rect.y + (PLAYERHEIGHT/2), self.player.angle, target_vector)
                            plyr_weap_group.add(weapon)
                            arena_sprites.add(weapon)
                            arena_sprites.move_to_back(weapon)

                # Give option to leave arena when esc is pressed
                if self.environment.go_arena and not self.player.change_check:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.player.change_check = True

                # Switch bools upon WASD key press
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.player.pressed_w = True
                    elif event.key == pygame.K_s:
                        self.player.pressed_s = True
                    elif event.key == pygame.K_d:
                        self.player.pressed_d = True
                    elif event.key == pygame.K_a:
                        self.player.pressed_a = True

                    # Toggle fps
                    elif event.key == pygame.K_f:
                        if not self.hud.fps_toggle:
                            self.hud.fps_toggle = True
                        elif self.hud.fps_toggle:
                            self.hud.fps_toggle = False

                    # Toggle player menu
                    elif event.key == pygame.K_c:
                        if not self.playermenu.plyr_menu_toggle:
                            self.playermenu.plyr_menu_toggle = True
                            home_sprites.add(self.playermenu)
                            arena_sprites.add(self.playermenu)
                        elif self.playermenu.plyr_menu_toggle:
                            self.playermenu.plyr_menu_toggle = False
                            home_sprites.remove(self.playermenu)
                            arena_sprites.remove(self.playermenu)


                    elif self.player.change_check:

                        # Handle store navigation
                        if self.player.rect.center == store_planet.rect.center:
                            if event.key == pygame.K_RIGHT and self.storemenu.tab_number < 3:
                                self.storemenu.tab_number += 1
                            elif event.key == pygame.K_LEFT and self.storemenu.tab_number > 0:
                                self.storemenu.tab_number -= 1

                            elif event.key == pygame.K_ESCAPE:
                                home_sprites.remove(self.storemenu)
                                self.player.rect.x = 800
                                self.player.rect.y = 450
                                self.player.change_check = False
                                screen.blit(SPACEIMAGE, (0, 0))
                                pygame.display.update()
                                self.environment.confirmed = False

                            if self.storemenu.tab_number == 0:
                                pass

                            elif self.storemenu.tab_number == 1:
                                if event.key == pygame.K_1:
                                    self.player.upgradeSpeed()
                            
                            elif self.storemenu.tab_number == 2:
                                if event.key == pygame.K_1:
                                    self.player.upgradeHealth()
                            
                            elif self.storemenu.tab_number == 3:
                                if event.key == pygame.K_1:
                                    self.player.upgradeEnergy()

                        # Handle yes or no prompt in arena
                        elif self.environment.go_arena:
                            if event.key == pygame.K_y:
                                self.environment.go_home = True
                                self.environment.go_arena = False
                                self.player.change_check = False
                                self.player.rect.x = 800
                                self.player.rect.y = 450
                                self.player.health = self.player.max_health
                                arena_sprites.remove(self.confirmationmenu)
                                clearGroups(enemy_attackables, enemy_attackers, kamikaze_group,
                                            star_group,        loot_group,      BLANKENEMY)
                            elif event.key == pygame.K_n:
                                self.player.change_check = False
                                arena_sprites.remove(self.confirmationmenu)                                

                        # Handle yes or no prompt at home
                        else:
                            if event.key == pygame.K_y:
                                self.playermenu.plyr_menu_toggle = False
                                home_sprites.remove(self.playermenu)
                                arena_sprites.remove(self.playermenu)
                                home_sprites.remove(self.confirmationmenu)
                                self.environment.confirmed = True
                                self.player.change_check = False
                            elif event.key == pygame.K_n:
                                home_sprites.remove(self.confirmationmenu)
                                self.player.rect.x = 800
                                self.player.rect.y = 450
                                self.player.change_check = False
                                self.environment.confirmed = False
                                screen.blit(SPACEIMAGE, (0, 0))
                                pygame.display.update()

                # Switch bools when WASD keys are released
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.player.pressed_w = False
                    elif event.key == pygame.K_s:
                        self.player.pressed_s = False
                    elif event.key == pygame.K_d:
                        self.player.pressed_d = False
                    elif event.key == pygame.K_a:
                        self.player.pressed_a = False

    def update(self):
        # Call update methods on objects
        # Handle cursor display
        self.crosshair.rect.center = pygame.mouse.get_pos()
        # Handle collisions between enemies and player weapon(kill enemies)
        self.player.killEnemy()
        # Regenerate energy
        self.player.regenEnergy()
        # Handle the current position of the player's menu, based on wall collisions
        self.playermenu.handlePlayerMenuPos(right_wall, left_wall, top_wall, bottom_wall)
        # Collect loot when player collides
        self.player.collectLoot()
        # Do damage to player with enemies
        self.player.damagePlayer()
        if self.environment.go_arena and not self.environment.game_over:
            self.enemyControl.spawnEnemies()
        # Check and allow enemies to kill player
        if self.player.killPlayer():
            self.environment.player_explo = True
            self.environment.game_over    = True

        # Where player menu should actually be
        self.playermenu.update(self.player.rect.x + PLAYERWIDTH, self.player.rect.y + PLAYERHEIGHT)

        # Move player
        if not self.environment.game_over:
            self.player.move()

        if self.environment.go_home and not self.environment.game_over:

            # Switch location of player upon collision of arena planet
            if pygame.sprite.collide_rect(self.player, arena_planet):
                self.player.dockPlayer(arena_planet)
                if self.environment.confirmed:
                    self.environment.planet_collision = True
                    self.environment.handleLocation(self.player.initial_time)
                    self.player.rect.x = 800
                    self.player.rect.y = 450
                    self.player.change_check = False
                    self.environment.confirmed = False

            elif pygame.sprite.collide_rect(self.player, store_planet):
                self.player.dockPlayer(store_planet)

            elif pygame.sprite.collide_rect(self.player, training_planet):
                self.player.dockPlayer(training_planet)

            elif pygame.sprite.collide_rect(self.player, armory_planet):
                self.player.dockPlayer(armory_planet)

        kamikaze_group.update(self.player.rect.x + (PLAYERWIDTH/2), self.player.rect.y + (PLAYERHEIGHT/2))
        star_group.update(enemy_weap_group, arena_sprites, LASERSOUND, LASERIMAGE, self.enemyControl.spawn_ctr)
        asteroid_group.update()
        
        # Update the shots fired
        if len(plyr_weap_group.sprites()) != 0:
            for obj in plyr_weap_group:
                obj.update(obj.target_vector)

        if len(enemy_weap_group.sprites()) != 0:
            for obj in enemy_weap_group:
                obj.update(obj.target_vector)

    def draw(self):
        # Call draw methods on objects
        if self.environment.go_start:
            screen.blit(SPACEIMAGE, (0, 0))

            dirty_rects = self.environment.handleLocation(self.player.initial_time)
            dirty_rects[1] = self.player.namePlayer()
            dirty_rects[2] = screen.get_rect()
            dirty_groups = start_sprites.draw(screen)

        

        # Handle home display
        elif self.environment.go_home:
            home_sprites.clear(screen, SPACEIMAGE)
            screen.blit(SPACEIMAGE, (0, 0))
            dirty_groups = home_sprites.draw(screen)

            # Update angle of player
            screen.blit(rotCenter(self.player.active_plyr_img, self.angle_between), (self.player.rect.x, self.player.rect.y))
            self.playermenu.drawMenuContent(self.player.max_health, self.player.max_energy, self.player.speed)

            # Get list from hud function
            dirty_rects = self.hud.drawHud(self.player.money, self.player.name)

            dirty_rects[3] = screen.get_rect()
            dirty_rects[4] = self.player.drawEnergyBar()
            dirty_rects[5] = self.player.drawHealthBar()

            # Blit home menus
            if self.player.change_check:
                if self.player.rect.center == store_planet.rect.center:
                    home_sprites.add(self.storemenu)
                    home_sprites.move_to_front(self.storemenu)
                    self.storemenu.drawMenuContent()

                elif self.player.rect.center == arena_planet.rect.center:
                    home_sprites.add(self.confirmationmenu)
                    home_sprites.move_to_front(self.confirmationmenu)
                    self.confirmationmenu.drawMenuContent(self.environment.go_home, self.environment.go_arena)

                else:
                    menu_box = customRect(400, 300, WINDOWWIDTH/2 - MENUWIDTH/2, WINDOWHEIGHT/2 - MENUHEIGHT/2)
                    screen.blit(PLAYERMENU, (WINDOWWIDTH/2 - MENUWIDTH/2, WINDOWHEIGHT/2 - MENUHEIGHT/2))
                    dirty_rects[7] = menu_box

            
        # Handle arena display
        elif self.environment.go_arena:
            screen.fill(BGCOLOR)
            screen.blit(rotCenter(self.player.active_plyr_img, self.angle_between), (self.player.rect.x, self.player.rect.y))
            self.playermenu.drawMenuContent(self.player.max_health, self.player.max_energy, self.player.speed)

            # Toggle menu to leave the arena
            if self.player.change_check:
                arena_sprites.add(self.confirmationmenu)
                arena_sprites.move_to_front(self.confirmationmenu)
                self.confirmationmenu.drawMenuContent(self.environment.go_home, self.environment.go_arena)

            # Blit explosion on player when dead
            if self.environment.player_explo:
                EXPLOANIM1.blit(screen, (self.player.rect.x, self.player.rect.y - 78))
                if self.environment.handleLocation(self.player.initial_time):
                    self.player.respawnPlayer()

            # Blit list of explosions to screen
            if self.player.enemy_explo:
                self.player.current_explo.blit(screen, (self.player.collision_x, self.player.collision_y - 78))
            EXPLOANIM2.blit(screen, (self.player.rect.x, self.player.rect.y))

            # Display coins
            for obj in loot_group:
                obj.COINANIM.blit(screen, (obj.rect.x, obj.rect.y))

            dirty_rects = self.hud.drawHud(self.player.money, self.player.name)
            dirty_groups = arena_sprites.draw(screen)

            dirty_rects.append(self.player.drawEnergyBar())
            dirty_rects.append(self.player.drawHealthBar())


        # Update groups of sprites
        pygame.display.update(dirty_groups)

        # Update rects
        pygame.display.update(dirty_rects)

app = Control()
app.mainGameLoop()