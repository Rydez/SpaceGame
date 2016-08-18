from prepare import *
from constants import *

class StoreMenu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Player menu background
        self.image = pygame.Surface((STOREWIDTH, STOREHEIGHT))
        self.image.set_alpha(128)
        self.image.fill((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = WINDOWWIDTH/2 - STOREWIDTH/2
        self.rect.y = WINDOWHEIGHT/2 - STOREHEIGHT/2

        self.tab_number = 0
        self.first_color = WHITE
        self.second_color = GRAY
        self.third_color = GRAY
        self.fourth_color = GRAY

    def drawMenuContent(self):
        # Store menu text
        menu_title = BIGFONT.render('Space Store', 1, WHITE)

        first_tab_text = TABFONT.render('Weapon', 1, self.first_color)
        second_tab_text = TABFONT.render('Propulsion', 1, self.second_color)
        third_tab_text = TABFONT.render('Hull', 1, self.third_color)
        fourth_tab_text = TABFONT.render('Battery', 1, self.fourth_color)

        propulsion_content = MENUFONT.render('- 1. Enchance propulsion system ($300)', 1, WHITE)
        hull_content = MENUFONT.render('- 1. Enchance hull ($150)', 1, WHITE)
        battery_content = MENUFONT.render('- 1. Enchance batteries ($150)', 1, WHITE)


        # Put the menu stuff on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(menu_title, (self.rect.x + 10, self.rect.y + 10))
        screen.blit(first_tab_text, (self.rect.x + 30, self.rect.y + 90))
        screen.blit(second_tab_text, (self.rect.x + TABWIDTH + 34, self.rect.y + 90))
        screen.blit(third_tab_text, (self.rect.x + 2*TABWIDTH + 33, self.rect.y + 90))
        screen.blit(fourth_tab_text, (self.rect.x + 3*TABWIDTH + 32, self.rect.y + 90))

        # Give the menu a thin border
        self.border = pygame.draw.rect(screen, GRAY, (self.rect.x, self.rect.y, STOREWIDTH, STOREHEIGHT), 1)

        # Draw line which tabs rest on
        self.top_line = pygame.draw.rect(screen, GRAY, (self.rect.x, self.rect.y + 120, STOREWIDTH, 1), 1)

        # Draw tabs on line
        self.first_tab = pygame.draw.rect(screen, GRAY, (self.rect.x + 20, self.rect.y + 80, TABWIDTH, TABHEIGHT), 1)
        self.second_tab = pygame.draw.rect(screen, GRAY, (self.rect.x + TABWIDTH + 19, self.rect.y + 80, TABWIDTH, TABHEIGHT), 1)
        self.third_tab = pygame.draw.rect(screen, GRAY, (self.rect.x + 2*TABWIDTH + 18, self.rect.y + 80, TABWIDTH, TABHEIGHT), 1)
        self.fourth_tab = pygame.draw.rect(screen, GRAY, (self.rect.x + 3*TABWIDTH + 17, self.rect.y + 80, TABWIDTH, TABHEIGHT), 1)

        if self.tab_number == 0:
            self.first_color = WHITE
            self.second_color = GRAY
            self.third_color = GRAY
            self.fourth_color = GRAY

        elif self.tab_number == 1:
            self.first_color = GRAY
            self.second_color = WHITE
            self.third_color = GRAY
            self.fourth_color = GRAY
            screen.blit(propulsion_content, (self.rect.x + 100, self.rect.y + 200))

        elif self.tab_number == 2:
            self.first_color = GRAY
            self.second_color = GRAY
            self.third_color = WHITE
            self.fourth_color = GRAY
            screen.blit(hull_content, (self.rect.x + 100, self.rect.y + 200))

        elif self.tab_number == 3:
            self.first_color = GRAY
            self.second_color = GRAY
            self.third_color = GRAY
            self.fourth_color = WHITE
            screen.blit(battery_content, (self.rect.x + 100, self.rect.y + 200))






