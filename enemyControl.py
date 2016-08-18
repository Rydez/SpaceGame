from enemies import *
from environment import *



class EnemyControl:
    def __init__(self):
        self.spawn_ctr = 0

    def spawnEnemies(self):
        # Handle enemy spawning
        if self.spawn_ctr % 100 == 0:
            spawn_x, spawn_y = randSpawnPos(ENEMYWIDTH, ENEMYHEIGHT)
            rand_num = random.randint(0, 100)
            if rand_num < 30:
                enemy = StarEnemy(spawn_x, spawn_y, EYEBALLIMAGE)
                star_group.add(enemy)
                enemy_attackables.add(enemy)
                arena_sprites.add(enemy)
                arena_sprites.move_to_back(enemy)
            elif rand_num >= 30 and rand_num <= 60:
                enemy = KamikazeEnemy(spawn_x, spawn_y, ENEMYIMAGE)
                kamikaze_group.add(enemy)
                enemy_attackers.add(enemy)
                enemy_attackables.add(enemy)
                arena_sprites.add(enemy)
                arena_sprites.move_to_back(enemy)
            elif rand_num > 60:
                enemy = AsteroidEnemy(spawn_x, spawn_y, ASTEROID)
                asteroid_group.add(enemy)
                enemy_attackers.add(enemy)
                enemy_attackables.add(enemy)
                arena_sprites.add(enemy)
                arena_sprites.move_to_back(enemy)
        self.spawn_ctr += 1