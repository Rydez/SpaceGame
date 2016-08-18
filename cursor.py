import pygame

# Sprite groups are made to handle collisions. Render updates are used for dirty rects
cursor_group = pygame.sprite.RenderUpdates()


# Create crosshair sprite to put in group
class Crosshair(pygame.sprite.Sprite):
    def __init__(self, image, (x, y)):
        pygame.sprite.Sprite.__init__(self)
        self.image  = image
        self.rect   = self.image.get_rect()
        self.rect.center = (x, y)
