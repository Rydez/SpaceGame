from prepare import *

# Create player menu sprite
class PlayerMenu(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Player menu background
        self.image = pygame.Surface((400, 300))
        self.image.set_alpha(128)
        self.image.fill((0, 0, 0))

        self.rect  = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bot_right = True
        self.bot_left  = False
        self.top_right = False
        self.top_left  = False

        # Bool used to switch player menu on and off
        self.plyr_menu_toggle = False

    def drawMenuContent(self, player_health, player_energy, player_speed):
        # Player menu stuff
        menu_title = TITLEFONT.render('Space Info', 1, (255, 255, 255))
        health_stat = FPSFONT.render(' - Health: ' + str(player_health), 1, (255, 255, 255))
        energy_stat = FPSFONT.render(' - Energy: ' + str(player_energy), 1, (255, 255, 255))
        speed_stat = FPSFONT.render(' - Speed: ' + str(player_speed), 1, (255, 255, 255))
        if self.plyr_menu_toggle:
            screen.blit(menu_title, (self.rect.x + 10, self.rect.y + 10))
            screen.blit(health_stat, (self.rect.x + 10, self.rect.y + 30))
            screen.blit(energy_stat, (self.rect.x + 10, self.rect.y + 50))
            screen.blit(speed_stat, (self.rect.x + 10, self.rect.y + 70))

            # Draw border around player menu
            self.border = pygame.draw.rect(screen, (100, 100, 100), (self.rect.x, self.rect.y, 400, 300), 1)

    def update(self, menu_origin_x, menu_origin_y):

        if self.bot_right:
            self.rect.x = menu_origin_x
            self.rect.y = menu_origin_y
        elif self.bot_left:
            self.rect.x = menu_origin_x - (PLAYERWIDTH + MENUWIDTH)
            self.rect.y = menu_origin_y
        elif self.top_right:
            self.rect.x = menu_origin_x
            self.rect.y = menu_origin_y - (PLAYERHEIGHT + MENUHEIGHT)
        elif self.top_left:
            self.rect.x = menu_origin_x - (PLAYERWIDTH + MENUWIDTH)
            self.rect.y = menu_origin_y - (PLAYERHEIGHT + MENUHEIGHT)

    # Change position of floating player menu when is collides with borders
    def handlePlayerMenuPos(self, right_wall, left_wall, top_wall, bottom_wall):
        if pygame.sprite.collide_rect(self, right_wall):
            if self.bot_right:
                self.bot_right = False
                self.bot_left  = True
            elif self.top_right:
                self.top_right = False
                self.top_left = True
        elif pygame.sprite.collide_rect(self, left_wall):
            if self.bot_left:
                self.bot_left = False
                self.bot_right = True
            elif self.top_left:
                self.top_left = False
                self.top_right = True
        elif pygame.sprite.collide_rect(self, top_wall):
            if self.top_right:
                self.top_right = False
                self.bot_right = True
            elif self.top_left:
                self.top_left = False
                self.bot_left = True
        elif pygame.sprite.collide_rect(self, bottom_wall):
            if self.bot_right:
                self.bot_right = False
                self.top_right = True
            elif self.bot_left:
                self.bot_left = False
                self.top_left = True
