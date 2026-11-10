# Author: prixdj
# Date created: 15/02/2026
# Date updated: 16/06/2026
# Version: 0.1.3
# Description: A game like asteroids and vampire survivors

## Improvements

# Even more enemy types
# Fix spawn radius
# Enemy count
# Better documentation
# Main screen
# Controls screen
# Previous runs thing


## Imports

import pygame
from pygame.locals import *     # type: ignore
import random as rand
import sys
import math

## Initialisation

pygame.init()

## Constants and Variables

WIDTH = 600
HEIGHT = 600
FPS = 60

clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Survoids")

pygame.mouse.set_visible(False)

run_once = True

enemy_number = 0

score = 0

wave_value = 10
wave = 0
WAVE_HOLDOFF = 120
wave_delay = 0


## Events

GAME_OVER = pygame.event.custom_type()

PLAYER_HIT = pygame.event.custom_type()

IMMUNE_OFF = pygame.event.custom_type()

ENEMY_HIT = pygame.event.custom_type()


## Layers

# 0 - Background
# 1 - Bullet
# 2 - Enemy
# 3 - Hitmarker
# 4 - Thruster
# 5 - Player
# 6 - UI
# 7 - ScreenEffect
# 8 - Mouse


## Functions

def calculate_angle_between_points(p1, p2) -> float:
    x1, y1 = p1.rect.center
    x2, y2 = p2.rect.center

    dx = x2 - x1
    dy = y2 - y1
    
    radians = math.atan2(dy, dx)
    angle = -math.degrees(radians) - 90

    return angle


def point_object_to_object(obj1, obj2):
    obj1.angle = calculate_angle_between_points(obj1, obj2)
    obj1.image = pygame.transform.rotate(obj1.original_image, obj1.angle)
    obj1.rect = obj1.image.get_rect(center = obj1.rect.center)


def adjust_thruster(thruster, player):
    player_angle = player.get_angle()
    angle = -math.radians(player_angle)

    thruster.rect.centerx = player.rect.centerx - thruster.OFFSET * math.sin(angle)
    thruster.rect.centery = player.rect.centery + thruster.OFFSET * math.cos(angle)

    thruster.angle = player.angle
    thruster.image = pygame.transform.rotate(thruster.original_image, thruster.angle)
    thruster.rect = thruster.image.get_rect(center = thruster.rect.center)


def fire_bullet(player):
    keyboard = pygame.key.get_pressed()
    if player.bullet_delay <= 0:
        if keyboard[K_SPACE]:
            bullet = Bullet(player.get_angle(), player.get_pos(), "bullet.png", (4, 24), 25)
            all_sprites.add(bullet)
            player_bullet_sprites.add(bullet)
            player.bullet_delay = player.bullet_holdoff
    else:
        player.bullet_delay -= 1


def spawn_enemies(enemy_wave:list):
    for enemy in enemy_wave:
        new_enemy = enemy()
        all_sprites.add(new_enemy)
        enemy_sprites.add(new_enemy)


def end_wave():
    if len(enemy_sprites) == 0:
        return True
    else:
        return False


def display_wave_clear():
    wave_clear = Text(f"Wave {wave} Cleared", "kenvector_future_thin", 60)
    wave_clear.rect.center = (300, 280)
    all_sprites.add(wave_clear)
    text_sprites.add(wave_clear)
    wave_clear_sprites.add(wave_clear)


def remove_wave_clear():
    for text in wave_clear_sprites:
        all_sprites.remove(text)
        text_sprites.remove(text)
    wave_clear_sprites.empty()


def calc_wave() -> list:
    enemy_wave = []
    enemy_types = [EnemyA, EnemyB]
    enemy_likelihood = []
    current_wave_value = wave_value

    for enemy_type in enemy_types:
        for _ in range(enemy_type.likelihood):
            enemy_likelihood.append(enemy_type)

    while current_wave_value >= 5:  # smallest enemy value is 5
        random_num = rand.randrange(0, len(enemy_likelihood))
        enemy_type = enemy_likelihood[random_num]

        if current_wave_value - enemy_type.value < 0:
            continue

        enemy_wave.append(enemy_type)
        current_wave_value -= enemy_type.value
    
    return enemy_wave


def change_enemy_likelihoods():
    EnemyA.likelihood -= 1
    EnemyB.likelihood += 1


def spawn_waves():
    global wave
    global wave_value
    global wave_delay
    if end_wave() == True:
        if not wave_clear_sprites and wave != 0:
            display_wave_clear()
            wave_delay = WAVE_HOLDOFF
        
        if wave_delay <= 0:
            enemy_wave = calc_wave()
            spawn_enemies(enemy_wave)

            remove_wave_clear()
            change_enemy_likelihoods()
            wave_value += 10
            wave += 1
        else:
            wave_delay -= 1


def update_text(lives:int):
    life_number = str(lives)
    score_number = str(score)
    lives_text.update(life_number)
    lives_text.rect.topleft = (68,8)
    score_text.update(score_number)
    score_text.rect.topright = (596,8)


def update_stats(player):
    global score
    global experience
    score += 20
    player.experience += 4


def update_run_once(boolean:bool):
    global run_once         # this function is for avoiding global in main
    run_once = boolean


def check_game_over(lives:int):
    if lives <= 0:
        return True
    else:
        return False


def display_powers():
    if player.bullet_holdoff > 6:
        lightning_power = Power((224, 483), "powerup1.png")
    else:
        lightning_power = Power((224, 483), "poweruplocked.png")
    
    all_sprites.add(lightning_power)
    power_sprites.add(lightning_power)

    lightning_text = Text("(1)", "kenvector_future_thin", 8)
    lightning_text.rect.midtop = (224, 520)
    all_sprites.add(lightning_text)
    text_sprites.add(lightning_text)
    powerup_text_sprites.add(lightning_text)
    
    if player.acceleration_speed < 0.8:
        speed_power = Power((300, 483), "powerup2.png")
    else:
        speed_power = Power((300, 483), "poweruplocked.png")

    all_sprites.add(speed_power)
    power_sprites.add(speed_power)
    speed_text = Text("(2)", "kenvector_future_thin", 8)
    speed_text.rect.midtop = (300, 520)
    all_sprites.add(speed_text)
    text_sprites.add(speed_text)
    powerup_text_sprites.add(speed_text)
    
    health_power = Power((376, 483), "powerup3.png")
    all_sprites.add(health_power)
    power_sprites.add(health_power)

    health_text = Text("(3)", "kenvector_future_thin", 8)
    health_text.rect.midtop = (376, 520)
    all_sprites.add(health_text)
    text_sprites.add(health_text)
    powerup_text_sprites.add(health_text)


def remove_powers():
    for power in power_sprites:
        all_sprites.remove(power)
    power_sprites.empty()

    for text in powerup_text_sprites:
        all_sprites.remove(text)
        text_sprites.remove(text)
    powerup_text_sprites.empty()


def reset_game_results():
    with open("survoids/game_results.txt", "w") as game_results:
        game_results.write("This is the text file where game data is saved.\n\n")


def store_game_info(score:int, level:int, wave:int):
    time_elapsed:float = pygame.time.get_ticks() / 1000

    with open("survoids/game_results.txt", "a") as game_results:
        game_results.write(f"Score: {score}\n")
        game_results.write(f"Wave: {wave}\n")
        game_results.write(f"Level: {level}\n")
        game_results.write(f"Time elapsed: {time_elapsed:.2f}s\n\n")


def change_to_end_screen():
    end_screen = ScreenEffect((0,0,10), 60)
    all_sprites.add(end_screen)
    screen_effect_sprites.add(end_screen)

    game_over_text = Text("GAME OVER", "kenvector_future", 75)
    game_over_text.rect.center = (300, 200)
    all_sprites.add(game_over_text)
    text_sprites.add(game_over_text)


## Classes 

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._layer = 0
        self.image = pygame.image.load('survoids/images/blue.png')
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.rect = self.image.get_rect(center = (WIDTH/2, HEIGHT/2))


class Mouse(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self._layer = 8
        self.image = pygame.image.load('survoids/images/crosshair.png').convert_alpha()
        self.surf = pygame.Surface((30,33))
        self.rect = self.surf.get_rect()
    
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Player(pygame.sprite.Sprite):
    can_move:bool = True

    def __init__(self, *groups):
        super().__init__(*groups)
        self._layer = 5
        unscaled_image = pygame.image.load('survoids/images/player.png').convert_alpha()
        unscaled_immune_image = pygame.image.load('survoids/images/player_immune.png').convert_alpha()
        self.image = pygame.transform.scale(unscaled_image, (45, 37))
        self.normal_image = pygame.transform.scale(unscaled_image, (45, 37))
        self.immune_image = pygame.transform.scale(unscaled_immune_image, (45, 37))
        self.original_image = self.normal_image

        self.surf = pygame.Surface((45,37))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT/2))
        self.angle = 90

        self.acceleration_up = 0.0
        self.acceleration_down = 0.0
        self.acceleration_left = 0.0
        self.acceleration_right = 0.0

        self.MAX_ACCELERATION_UP = 5.0
        self.MAX_ACCELERATION_DOWN = 5.0
        self.MAX_ACCELERATION_LEFT = 5.0
        self.MAX_ACCELERATION_RIGHT = 5.0

        self.acceleration_speed = 0.2
        self.deceleration_speed = 0.1

        self.lives = 3
        self.immune = False

        self.experience = 0

        self.level = 0
        self.levels_used = 0
        self.LEVEL_UP_THRESHOLD = 40
        self.LEVEL_HOLDOFF = 10
        self.level_delay = 0

        self.bullet_holdoff = 50
        self.bullet_delay = 0

    def get_angle(self) -> float:
        return self.angle
    
    def get_pos(self) -> tuple:
        x = self.rect.centerx
        y = self.rect.centery
        return (x,y)

    def set_vulnerable(self) -> None:
        self.immune = False
    
    def set_can_move(self, boolean:bool) -> None:
        Player.can_move = boolean

    def update(self):
        keyboard = pygame.key.get_pressed()

        if Player.can_move:

            # Accelerate
            if keyboard[K_w]:
                if self.acceleration_up < self.MAX_ACCELERATION_UP:
                    self.acceleration_up += self.acceleration_speed
            if keyboard[K_s]:
                if self.acceleration_down < self.MAX_ACCELERATION_DOWN:
                    self.acceleration_down += self.acceleration_speed
            if keyboard[K_a]:
                if self.acceleration_left < self.MAX_ACCELERATION_LEFT:
                    self.acceleration_left += self.acceleration_speed
            if keyboard[K_d]:
                if self.acceleration_right < self.MAX_ACCELERATION_RIGHT:
                    self.acceleration_right += self.acceleration_speed
        
        # Decelerate
        if self.acceleration_up > 0.0:
            self.acceleration_up -= self.deceleration_speed
        if self.acceleration_down > 0.0:
            self.acceleration_down -= self.deceleration_speed
        if self.acceleration_left > 0.0:
            self.acceleration_left -= self.deceleration_speed
        if self.acceleration_right > 0.0:
            self.acceleration_right -= self.deceleration_speed
        
        # Calculate movement
        acceleration_up_rounded = round(self.acceleration_up)
        acceleration_down_rounded = round(self.acceleration_down)
        acceleration_right_rounded = round(self.acceleration_right)
        acceleration_left_rounded = round(self.acceleration_left)
        
        self.rect.y = self.rect.y - acceleration_up_rounded + acceleration_down_rounded
        self.rect.x = self.rect.x - acceleration_left_rounded + acceleration_right_rounded

        # Level up

        if self.experience >= self.LEVEL_UP_THRESHOLD:
            self.experience -= self.LEVEL_UP_THRESHOLD
            self.level += 1

        # Power up

        if self.level > self.levels_used:
            if self.level_delay <= 0:
                if not power_sprites:
                    display_powers()

                used_level = False

                if self.bullet_holdoff > 6 and keyboard[K_1]:
                    self.bullet_holdoff -= 2
                    used_level = True
                elif self.acceleration_speed < 0.8 and keyboard[K_2]:
                    self.acceleration_speed += 0.06
                    self.deceleration_speed += 0.03
                    used_level = True
                elif keyboard[K_3]:
                    self.lives += 1
                    used_level = True
                
                if used_level:
                    self.levels_used += 1
                    self.level_delay = self.LEVEL_HOLDOFF
                    remove_powers()
            else:
                self.level_delay -= 1


        # Keep player on-screen
        if self.rect.x > WIDTH - 45:
            self.rect.x = WIDTH - 45
            self.acceleration_right = 0.0
        if self.rect.x < 0:
            self.rect.x = 0
            self.acceleration_left = 0.0
        if self.rect.y > HEIGHT - 37:
            self.rect.y = HEIGHT - 37
            self.acceleration_down = 0.0
        if self.rect.y < 0:
            self.rect.y = 0
            self.acceleration_up = 0.0
        

class Thruster(pygame.sprite.Sprite):
    can_appear:bool = True

    def __init__(self):
        super().__init__()
        self._layer = 4
        self.image = pygame.image.load('survoids/images/thruster.png').convert_alpha()
        self.original_image = pygame.image.load('survoids/images/thruster.png')
        self.surf = pygame.Surface((14,31))
        self.rect = self.surf.get_rect()
        self.OFFSET = 30
        self.angle = 90
    
    def set_can_appear(self, boolean:bool) -> None:
        Thruster.can_appear = boolean

    def update(self):
        keyboard = pygame.key.get_pressed()

        if Thruster.can_appear:

            # Visibility
            if keyboard[K_w]:
                screen.blit(self.image, self.rect)
            if keyboard[K_s]:
                screen.blit(self.image, self.rect)
            if keyboard[K_a]:
                screen.blit(self.image, self.rect)
            if keyboard[K_d]:
                screen.blit(self.image, self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, angle:float, pos:tuple, img:str, size:tuple, speed:int):
        super().__init__()
        self._layer = 1

        unscaled_image = pygame.image.load(f'survoids/images/{img}').convert_alpha()
        self.image = pygame.transform.scale(unscaled_image, size)
        self.original_image = pygame.transform.scale(unscaled_image, size)
        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect(center = pos)

        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)

        self.SPEED = speed
    
    def update(self):
        angle = -math.radians(self.angle)
        self.rect.centerx = self.rect.centerx + round(self.SPEED * math.sin(angle))
        self.rect.centery = self.rect.centery - round(self.SPEED * math.cos(angle))

        if self.rect.centerx > 620 or self.rect.centerx < -20 or self.rect.centery > 620 or self.rect.centery < -20:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    value:int = 0
    likelihood:int = 0

    def __init__(self, img:str, size:tuple, speed:int|float):
        super().__init__()
        self._layer = 2

        unscaled_image = pygame.image.load(f'survoids/images/{img}').convert_alpha()
        self.image = pygame.transform.scale(unscaled_image, size)
        self.original_image = pygame.transform.scale(unscaled_image, size)
        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect()
        
        self.SPEED = speed

        self.angle = rand.randint(0,360)
        self.radians = -math.radians(self.angle)
        self.spawn_radius = 500
        self.rect.centerx = 300 + round((self.spawn_radius + rand.randint(0,550)) * math.sin(self.radians))
        self.rect.centery = 300 + round((self.spawn_radius + rand.randint(0,550)) * math.cos(self.radians))

    def get_angle(self) -> float:
        return self.angle

    def get_pos(self) -> tuple:
        x = self.rect.centerx
        y = self.rect.centery
        return (x,y)
    
    def update(self):
        # Move towards player
        self.radians = -math.radians(self.angle)
        self.rect.centerx = self.rect.centerx + round(self.SPEED * math.sin(self.radians))
        self.rect.centery = self.rect.centery - round(self.SPEED * math.cos(self.radians))


class EnemyA(Enemy):
    value = 5
    likelihood = 10

    def __init__(self):
        super().__init__(img="enemy_a.png", size=(26, 21), speed=2)


class EnemyB(Enemy):
    value = 10
    likelihood = 0

    def __init__(self):
        super().__init__(img="enemy_b.png", size=(26, 21), speed=1)

        self.BULLET_HOLDOFF = 60
        self.bullet_delay = 0
    
    def update(self):
        super().update()

        if self.bullet_delay <= 0:
            bullet = Bullet(self.get_angle(), self.get_pos(), "enemy_b_bullet.png", (4, 16), 4)
            all_sprites.add(bullet)
            enemy_bullet_sprites.add(bullet)
            self.bullet_delay = self.BULLET_HOLDOFF
        else:
            self.bullet_delay -= 1


class Hitmarker(pygame.sprite.Sprite):
    def __init__(self, pos:tuple):
        super().__init__()
        self._layer = 3

        self.image = pygame.image.load(f'survoids/images/hit_marker.png').convert_alpha()
        self.surf = pygame.Surface((37,37))
        self.rect = self.surf.get_rect(center = pos)

        self.time = 0

    def update(self):
        self.time += 1


class Power(pygame.sprite.Sprite):
    def __init__(self, pos:tuple, image:str):
        super().__init__()
        self._layer = 6

        self.image = pygame.image.load(f'survoids/images/{image}').convert_alpha()
        self.surf = pygame.Surface((37,37))
        self.rect = self.surf.get_rect(center = pos)

    def update(self):
        pass


class UI(pygame.sprite.Sprite):
    def __init__(self, png:str, width:float, height:float, pos:tuple):
        super().__init__()
        self._layer = 6

        self.image = pygame.image.load(f'survoids/images/{png}.png').convert_alpha()
        self.original_image = pygame.image.load(f'survoids/images/{png}.png')
        self.surf = pygame.Surface((width,height))
        self.rect = self.surf.get_rect(center = pos)


class Text(pygame.sprite.Sprite):
    def __init__(self, initial:str, font_name:str, font_size:int):
        super().__init__()
        self._layer = 6

        self.words = initial

        self.font = pygame.font.Font(f'survoids/fonts/{font_name}.ttf', font_size)
        self.surf = self.font.render(initial, True, (255,255,255))
        self.rect = self.surf.get_rect()

    def update(self, new_text:str):
        self.words = new_text
        self.surf = self.font.render(new_text, True, (255,255,255))
        self.rect = self.surf.get_rect()


class ScreenEffect(pygame.sprite.Sprite):
    def __init__(self, colour:tuple, alpha:int = 0):
        super().__init__()
        self._layer = 8

        self.surf = pygame.Surface((WIDTH, HEIGHT))
        self.surf.set_alpha(alpha)
        self.surf.fill(colour)
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT/2))


## Objects

all_sprites = pygame.sprite.LayeredUpdates()
player_bullet_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
enemy_bullet_sprites = pygame.sprite.Group()
hitmarker_sprites = pygame.sprite.Group()
power_sprites = pygame.sprite.Group()
ui_sprites = pygame.sprite.Group()
text_sprites = pygame.sprite.Group()
wave_clear_sprites = pygame.sprite.Group()
powerup_text_sprites = pygame.sprite.Group()
screen_effect_sprites = pygame.sprite.Group()

background = Background()
all_sprites.add(background)

mouse = Mouse()
all_sprites.add(mouse)

player = Player()
all_sprites.add(player)

thruster = Thruster()
all_sprites.add(thruster)

x_ui = UI('x', 17, 17, (52,21))
all_sprites.add(x_ui)
ui_sprites.add(x_ui)

player_life_icon = UI('life_ui', 33, 26, (21,20))
all_sprites.add(player_life_icon)
ui_sprites.add(player_life_icon)

lives_text = Text(str(player.lives), 'kenvector_future', 24)
lives_text.rect.topleft = (68,8)
all_sprites.add(lives_text)
text_sprites.add(lives_text)

score_text = Text(str(score), 'kenvector_future_thin', 36)
score_text.rect.topright = (596,8)
all_sprites.add(score_text)
text_sprites.add(score_text)

## Main

def main():
    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == IMMUNE_OFF:
                player.image = player.immune_image
                player.original_image = player.normal_image

                player.immune = False
            
            if event.type == ENEMY_HIT:
                enemy_pos = event.enemy.get_pos()
                hitmarker = Hitmarker(enemy_pos)
                all_sprites.add(hitmarker)
                hitmarker_sprites.add(hitmarker)
                enemy_sprites.remove(event.enemy)
                player_bullet_sprites.remove(event.bullet)
                all_sprites.remove(event.enemy)
                all_sprites.remove(event.bullet)
                update_stats(player)

            if event.type == PLAYER_HIT:
                if not player.immune:
                    player.lives -= 1
                    
                    player.image = player.immune_image
                    player.original_image = player.immune_image

                    player.immune = True
                    pygame.time.set_timer(pygame.event.Event(IMMUNE_OFF), 2000)

            if event.type == GAME_OVER:
                player.set_can_move(False)
                thruster.set_can_appear(False)
                store_game_info(score, player.level, wave)
                change_to_end_screen()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_6:
                    print(player_bullet_sprites)
                if event.key == pygame.K_7:
                    pygame.event.post(pygame.event.Event(PLAYER_HIT))
                if event.key == pygame.K_8:
                    reset_game_results()
                if event.key == pygame.K_4:
                    player.lives = 0
                if event.key == pygame.K_5:
                    player.experience += 10
                if event.key == pygame.K_9:
                    print(player.level)
        
        screen.fill((0,0,0))

        update_text(player.lives)

        if check_game_over(player.lives):
            if run_once:
                pygame.event.post(pygame.event.Event(GAME_OVER))
                update_run_once(False)
        else:
            point_object_to_object(player, mouse)
        
            adjust_thruster(thruster, player)

            fire_bullet(player)
            
            spawn_waves()

            if pygame.sprite.spritecollideany(player, enemy_sprites, pygame.sprite.collide_rect_ratio(0.8)):
                pygame.event.post(pygame.event.Event(PLAYER_HIT))
            
            if pygame.sprite.spritecollideany(player, enemy_bullet_sprites, pygame.sprite.collide_rect_ratio(0.9)):
                pygame.event.post(pygame.event.Event(PLAYER_HIT))
            
        for enemy in enemy_sprites:
            point_object_to_object(enemy, player)

            bullet_collision = pygame.sprite.spritecollideany(enemy, player_bullet_sprites)

            if bullet_collision:
                pygame.event.post(pygame.event.Event(ENEMY_HIT, {"enemy": enemy, "bullet": bullet_collision}))
            
        for hitmarker in hitmarker_sprites:
            if hitmarker.time >= 30:
                hitmarker_sprites.remove(hitmarker)
                all_sprites.remove(hitmarker)


        for entity in all_sprites:
            if isinstance(entity, Text) or entity in screen_effect_sprites:
                screen.blit(entity.surf, entity.rect)
            elif entity != thruster:
                screen.blit(entity.image, entity.rect)
                entity.update()
            else:
                entity.update()

        pygame.display.flip()

if __name__ == "__main__":
    main()