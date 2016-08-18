from environment import *


class Hud:
    def __init__(self):
        # Bool for fps switch
        self.fps_toggle = False

    def drawHud(self, player_money, player_name):

        # Make labels
        fps_label = FPSFONT.render('fps: ' + str(clock.get_fps()), 1, (255, 255, 255))
        name_label = NAMEFONT.render(player_name, 1, (255, 255, 255))
        money_label = HUDFONT.render('SpaceCash: $' + str(player_money), 1, (255, 255, 255))

        # Make rects
        fps_box = customRect(1500, 10, 100, 20)
        name_box = name_label.get_rect()
        name_box.x = 10
        name_box.y = 20
        money_box = customRect(10, 90, 200, 30)

        screen.blit(name_label, (10, 20))
        screen.blit(money_label, (10, 90))

        # Display fps label
        if self.fps_toggle:
            screen.blit(fps_label, (1500, 10))

        return [fps_box, name_box, money_box, fps_box, fps_box,
                fps_box, fps_box, fps_box]