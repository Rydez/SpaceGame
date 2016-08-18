import pygame

from constants import *
from prepare import *

class ConfirmationMenu(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		# Confirmation menu background
		self.image = pygame.Surface((MENUWIDTH, MENUHEIGHT))
		self.image.set_alpha(128)
		self.image.fill((0, 0, 0))

		self.rect = self.image.get_rect()
		self.rect.x = WINDOWWIDTH/2 - MENUWIDTH/2
		self.rect.y = WINDOWHEIGHT/2 - MENUHEIGHT/2

	def drawMenuContent(self, go_home, go_arena):
		question_string = 'Enter the arena?'

		if go_home:
			question_string = 'Enter the arena?'
		elif go_arena:
			question_string = 'Exit the arena?'

		# Confirmation menu text
		confirm_question = NAMEFONT.render(question_string, 1, WHITE)
		options = NAMEFONT.render('No[n]          Yes[y]', 1, WHITE)

		question_width = confirm_question.get_width()
		options_width  = options.get_width()

		screen.blit(self.image, (self.rect.x, self.rect.y))
		screen.blit(confirm_question, (self.rect.x + MENUWIDTH/2 - question_width/2, self.rect.y + 100))
		screen.blit(options, (self.rect.x + MENUWIDTH/2 - options_width/2, self.rect.y + 175))

		self.border = pygame.draw.rect(screen, GRAY, (self.rect.x, self.rect.y, MENUWIDTH, MENUHEIGHT), 1)
