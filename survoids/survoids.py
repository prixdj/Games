# Author: prixdj
# Date created: 15/02/2026
# Date updated: 03/09/2026
# Version: 0.2.2
# Description: A game like asteroids and vampire survivors

## Takeaways for Future Projects

# Use a base sprite class
# Have a class for the game, storing score and other stuff
# Use math.isclose for better float comparison
# Use more general classes to avoid repetition in docstrings
# Define an OS path
# Start with correct file layout and function passing instead of global variables
# Add sprites to groups as they are created (usually)
# Always write something small to do next time
# Have a .draw method in the base class
# Type declare sprite groups
# Private any methods only used by the class


## Improvements

# Previous runs thing
# Controls screen
# Boss enemy


## Imports

import math
import random as rand
import sys

import pygame

## Constants and Variables

WIDTH = 600
HEIGHT = 600
FPS = 60

WAVE_HOLDOFF = 120


## Events

START_GAME = pygame.event.custom_type()

RETRY = pygame.event.custom_type()

GAME_OVER = pygame.event.custom_type()

PLAYER_HIT = pygame.event.custom_type()

IMMUNE_OFF = pygame.event.custom_type()

ENEMY_HIT = pygame.event.custom_type()

LEVEL_UP = pygame.event.custom_type()

LEVEL_UP_COMPLETE = pygame.event.custom_type()


## Layers

# 0 - Background
# 1 - Bullet
# 2 - Enemy
# 3 - Buffs
# 4 - Hitmarker
# 5 - Thruster
# 6 - Player
# 7 - UserInterface
# 8 - Text
# 9 - ScreenEffect
# 10 - Mouse


## Classes


class Background(pygame.sprite.Sprite):
    """The background image class.

    Attributes:
        image (surf): The blue.png image scaled to the size of the screen.
        rect (rect): The rect of the background image.
    """

    def __init__(self):
        """Initialises the background object."""
        super().__init__()
        self._layer = 0
        self.image = pygame.image.load("survoids/images/blue.png")
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))


class Mouse(pygame.sprite.Sprite):
    """The mouse cursor class.

    Attributes:
        image (surf): The crosshair.png image.
        surf (surf): The surface of the mouse cursor.
        rect (rect): The rect of the mouse cursor.
    """

    def __init__(self, *groups):
        """Initialises the mouse object."""
        super().__init__(*groups)
        self._layer = 10
        self.image = pygame.image.load("survoids/images/crosshair.png").convert_alpha()
        self.surf = pygame.Surface((30, 33))
        self.rect = self.surf.get_rect()

    def update(self):
        """Updates the mouse object to the position of the actual mouse."""
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Player(pygame.sprite.Sprite):
    """The player spaceship class.

    Attributes:
        scaled_size (tuple[int, int]): The scaled size of the player object.
        image (surf): The player.png image scaled to half the size.
        NORMAL_IMAGE (surf): The normal player.png used to revert the player once i-frames disappear.
        IMMUNE_IMAGE (surf): The player_immune.png used when the player has i-frames.
        original_image (surf): Used as a placeholder for scaling and rotating the player image.
        surf (surf): The surface of the player.
        rect (rect): The rect of the player.
        x (float): The unrounded x coordinate of the player.
        y (float): The unrounded y coordinate of the player.
        angle (float): The angle of the player.
        acceleration_up (float): The current upwards acceleration of the player.
        acceleration_down (float): The current downwards acceleration of the player.
        acceleration_left (float): The current leftwards acceleration of the player.
        acceleration_right (float): The current rightwards acceleration of the player.
        MAX_ACCELERATION_UP (float): The max upward acceleration of the player.
        MAX_ACCELERATION_DOWN (float): The max downward acceleration of the player.
        MAX_ACCELERATION_LEFT (float): The max leftward acceleration of the player.
        MAX_ACCELERATION_RIGHT (float): The max rightward acceleration of the player.
        acceleration_speed (float): The current acceleration speed of the player.
        deceleration_speed (float): The current deceleration speed of the player.
        lives (int): The current number of lives the player has.
        immune (bool): The player's immunity state.
        immune_timer (int): The number of frames before the player's immunity runs out.
        IMMUNE_TIMEOUT (int): The number of frames when the player is no longer immune.
        experience (int): The number of experience the player has.
        level (int): The level number of the player.
        levels_used (int): The number of levels the player has used.
        LEVEL_UP_THRESHOLD (int): The threshold of experience required before the player levels up.
        LEVEL_HOLDOFF (int): The max number of frames before the player can choose another power up.
        level_delay (int): The current number of frames before the player can choose another power up.
        bullet_holdoff (int): The max number of frames before the player fires another bullet.
        bullet_delay (int): The current number of frames before the player fires another bullet.
    """

    def __init__(self, *groups):
        """Initialises the player object."""
        super().__init__(*groups)
        self._layer = 6

        self.scaled_size = (45, 37)
        unscaled_image = pygame.image.load("survoids/images/player.png").convert_alpha()
        unscaled_IMMUNE_IMAGE = pygame.image.load(
            "survoids/images/player_immune.png"
        ).convert_alpha()
        unscaled_INVULN_IMAGE_1 = pygame.image.load(
            "survoids/images/player_star_invuln_1.png"
        ).convert_alpha()
        unscaled_INVULN_IMAGE_2 = pygame.image.load(
            "survoids/images/player_star_invuln_2.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(unscaled_image, self.scaled_size)
        self.NORMAL_IMAGE = pygame.transform.scale(unscaled_image, self.scaled_size)
        self.IMMUNE_IMAGE = pygame.transform.scale(
            unscaled_IMMUNE_IMAGE, self.scaled_size
        )
        self.INVULN_IMAGE_1 = pygame.transform.scale(
            unscaled_INVULN_IMAGE_1, self.scaled_size
        )
        self.INVULN_IMAGE_2 = pygame.transform.scale(
            unscaled_INVULN_IMAGE_2, self.scaled_size
        )
        self.original_image = self.NORMAL_IMAGE

        self.surf = pygame.Surface(self.scaled_size)
        self.rect = self.surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.angle = 90.0

        self.acceleration_up = 0.0
        self.acceleration_down = 0.0
        self.acceleration_left = 0.0
        self.acceleration_right = 0.0

        self.MAX_ACCELERATION_UP = 5.0
        self.MAX_ACCELERATION_DOWN = 5.0
        self.MAX_ACCELERATION_LEFT = 5.0
        self.MAX_ACCELERATION_RIGHT = 5.0

        self.NORMAL_ACCEL_RATE = 1.0
        self.accel_rate = self.NORMAL_ACCEL_RATE
        self.BUFFED_ACCEL_RATE = 1.25

        self.acceleration_speed = 0.2
        self.deceleration_speed = 0.1

        self.lives = 3
        self.immune = False
        self.immune_timer = 0
        self.IMMUNE_TIMEOUT = FPS * 2

        self.experience = 0

        self.level = 1
        self.levels_used = 1
        self.LEVEL_UP_THRESHOLD = 40
        self.LEVEL_HOLDOFF = 10
        self.level_delay = 0

        self.bullet_holdoff = 50
        self.bullet_delay = 0

        self.ORIG_DAMAGE = 1
        self.damage = self.ORIG_DAMAGE
        self.BUFFED_DAMAGE = 3

        self.BUFF_TIMER_DURATION = FPS * 5

        self.lightning_buff_act = False
        self.lightning_buff_timer = 0
        self.DEFAULT_ATK_SPEED = 1.0
        self.atk_speed = self.DEFAULT_ATK_SPEED
        self.BUFFED_ATK_SPEED = 0.7

        self.star_buff_act = False
        self.star_buff_timer = 0
        self.STAR_INVULN_TIMEOUT = FPS * 4

        self.bpill_buff_act = False
        self.bpill_buff_timer = 0

        self.rpill_buff_act = False
        self.rpill_buff_timer = 0

    def reset(self) -> None:
        """Resets all player stats."""

        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.angle = 90.0

        self.acceleration_up = 0.0
        self.acceleration_down = 0.0
        self.acceleration_left = 0.0
        self.acceleration_right = 0.0

        self.accel_rate = self.NORMAL_ACCEL_RATE

        self.acceleration_speed = 0.2
        self.deceleration_speed = 0.1

        self.lives = 3
        self.immune = False
        self.immune_timer = 0

        self.experience = 0

        self.level = 1
        self.levels_used = 1
        self.level_delay = 0

        self.bullet_holdoff = 50
        self.bullet_delay = 0

        self.damage = self.ORIG_DAMAGE

        self.lightning_buff_act = False
        self.lightning_buff_timer = 0
        self.atk_speed = self.DEFAULT_ATK_SPEED

        self.star_buff_act = False
        self.star_buff_timer = 0

        self.bpill_buff_act = False
        self.bpill_buff_timer = 0

        self.rpill_buff_act = False
        self.rpill_buff_timer = 0

    def get_angle(self) -> float:
        """Returns the angle of the player.

        Returns:
            float: The player's angle.
        """
        return self.angle

    def get_pos(self) -> tuple[float, float]:
        """Returns the position of the player.

        Returns:
            tuple[float, float]: The unrounded x and y coordinates of the player.
        """
        x = self.x
        y = self.y
        return (x, y)

    def fix_neg_speed(self, accel_name: str) -> None:
        """Fixes issues with how the acceleration is stored, preventing negative values."""
        if getattr(self, accel_name) < 0.0:
            setattr(self, accel_name, 0.0)

    def set_vulnerable(self) -> None:
        """Sets the immune state of the player to False."""
        self.immune = False

    def update_immune_timer(self) -> None:
        """Updates the immune timer and image if needed."""
        self.immune_timer += 1
        if not self.star_buff_act and self.original_image != self.IMMUNE_IMAGE:
            self.image = self.IMMUNE_IMAGE
            self.original_image = self.IMMUNE_IMAGE

    def check_immunity(self) -> None:
        """Creates an IMMUNE_OFF event if the player's immunity has worn off."""
        if self.immune_timer >= self.IMMUNE_TIMEOUT:
            pygame.event.post(pygame.event.Event(IMMUNE_OFF))
            self.immune_timer = 0
        else:
            self.update_immune_timer()

    def apply_buff(self, buff_type: "type[Buff]"):
        """Applies the buff to the player.

        Args:
            buff_type (type[Buff]): The subclass type of the buff.
        """
        match buff_type:
            case BuffTypes.Lightning:  # here add the temp stuff
                if not self.lightning_buff_act:
                    self.atk_speed = self.BUFFED_ATK_SPEED
                    self.lightning_buff_act = True
                    self.lightning_buff_timer = self.BUFF_TIMER_DURATION
                else:
                    self.lightning_buff_timer += self.BUFF_TIMER_DURATION
            case BuffTypes.Star:
                if not self.star_buff_act:
                    self.accel_rate = self.BUFFED_ACCEL_RATE
                    self.star_buff_act = True
                    self.star_buff_timer = self.STAR_INVULN_TIMEOUT
                    self.image = self.INVULN_IMAGE_1
                    self.original_image = self.INVULN_IMAGE_1
                else:
                    self.star_buff_timer += self.STAR_INVULN_TIMEOUT
            case BuffTypes.BluePill:
                if not self.bpill_buff_act:
                    self.bpill_buff_act = True
                    self.bpill_buff_timer = self.BUFF_TIMER_DURATION
                else:
                    self.bpill_buff_timer += self.BUFF_TIMER_DURATION
            case BuffTypes.RedPill:
                if not self.rpill_buff_act:
                    self.damage = self.BUFFED_DAMAGE
                    self.rpill_buff_act = True
                    self.rpill_buff_timer = self.BUFF_TIMER_DURATION
                else:
                    self.rpill_buff_timer += self.BUFF_TIMER_DURATION

    def __remove_buff(self, buff_type: str):
        """Removes the buff from the player.

        Args:
            buff_type (str): The subclass type of the buff as a string in the form buffname_buff_.
        """
        match buff_type:
            case "lightning_buff_":
                self.atk_speed = self.DEFAULT_ATK_SPEED
            case "star_buff_":
                self.accel_rate = self.NORMAL_ACCEL_RATE
                self.image = self.NORMAL_IMAGE
                self.original_image = self.NORMAL_IMAGE
            case "bpill_buff_":
                pass
            case "rpill_buff_":
                self.damage = self.ORIG_DAMAGE

    def move(self) -> None:  # Should only trigger if the game state is in_game
        """Changes the acceleration values of the player."""
        keyboard = pygame.key.get_pressed()

        # Accelerate
        if keyboard[pygame.K_w]:
            if self.acceleration_up < self.MAX_ACCELERATION_UP:
                self.acceleration_up += self.acceleration_speed * self.accel_rate
        if keyboard[pygame.K_s]:
            if self.acceleration_down < self.MAX_ACCELERATION_DOWN:
                self.acceleration_down += self.acceleration_speed * self.accel_rate
        if keyboard[pygame.K_a]:
            if self.acceleration_left < self.MAX_ACCELERATION_LEFT:
                self.acceleration_left += self.acceleration_speed * self.accel_rate
        if keyboard[pygame.K_d]:
            if self.acceleration_right < self.MAX_ACCELERATION_RIGHT:
                self.acceleration_right += self.acceleration_speed * self.accel_rate

    def calc_movement(self) -> None:  # Should not trigger if the game state is paused
        """Calculates the movement of the player and updates the player's coordinates."""
        # Decelerate
        for accel in [
            "acceleration_up",
            "acceleration_down",
            "acceleration_left",
            "acceleration_right",
        ]:
            if getattr(self, accel) > 0.0:
                setattr(self, accel, getattr(self, accel) - self.deceleration_speed)
                self.fix_neg_speed(accel)

        # Calculate movement
        self.x += self.acceleration_right - self.acceleration_left
        self.y += self.acceleration_down - self.acceleration_up

    def update(self):
        """Updates the player's level, powers, buffs and keeps the object on screen."""
        keyboard = pygame.key.get_pressed()

        # Level up
        if self.experience >= self.LEVEL_UP_THRESHOLD:
            self.experience -= self.LEVEL_UP_THRESHOLD
            self.level += 1

        # Power up
        if self.level > self.levels_used:
            if self.level_delay <= 0:
                pygame.event.post(pygame.event.Event(LEVEL_UP))

                used_level = False

                if self.bullet_holdoff > 6 and keyboard[pygame.K_1]:
                    self.bullet_holdoff -= 2
                    used_level = True
                elif self.acceleration_speed < 0.8 and keyboard[pygame.K_2]:
                    self.acceleration_speed += 0.06
                    self.deceleration_speed += 0.03
                    used_level = True
                elif keyboard[pygame.K_3]:
                    self.lives += 1
                    used_level = True

                if used_level:
                    self.levels_used += 1
                    self.level_delay = self.LEVEL_HOLDOFF
                    pygame.event.post(pygame.event.Event(LEVEL_UP_COMPLETE))
            else:
                self.level_delay -= 1

        # Reduce buff timer

        for buff_name in [
            "lightning_buff_",
            "star_buff_",
            "bpill_buff_",
            "rpill_buff_",
        ]:
            if getattr(self, buff_name + "act"):
                setattr(
                    self, buff_name + "timer", getattr(self, buff_name + "timer") - 1
                )

                if buff_name == "star_buff_":  # updating invulnerability image
                    if (
                        getattr(self, buff_name + "timer") <= FPS * 2
                        and getattr(self, buff_name + "timer") % 10 == 0
                    ):
                        if self.original_image == self.INVULN_IMAGE_1:
                            self.image = self.INVULN_IMAGE_2
                            self.original_image = self.INVULN_IMAGE_2
                        elif self.original_image == self.INVULN_IMAGE_2:
                            self.image = self.INVULN_IMAGE_1
                            self.original_image = self.INVULN_IMAGE_1

                if getattr(self, buff_name + "timer") <= 0:
                    setattr(self, buff_name + "act", False)
                    self.__remove_buff(buff_name)

        # Keep player on-screen
        if self.x + self.scaled_size[0] / 2 > WIDTH:
            self.x = WIDTH - self.scaled_size[0] / 2
            self.acceleration_right = 0.0
        if self.x - self.scaled_size[0] / 2 < 0:
            self.x = self.scaled_size[0] / 2
            self.acceleration_left = 0.0
        if self.y + self.scaled_size[1] / 2 > HEIGHT:
            self.y = HEIGHT - self.scaled_size[1] / 2
            self.acceleration_down = 0.0
        if self.y - self.scaled_size[1] / 2 < 0:
            self.y = self.scaled_size[1] / 2
            self.acceleration_up = 0.0

        # Round x and y values to position on screen correctly
        self.rect.centerx = round(self.x)
        self.rect.centery = round(self.y)


class Thruster(pygame.sprite.Sprite):
    """The thruster class that appears behind the player.

    Attributes:
        image (surf): The thruster.png image of the thruster.
        original_image (surf): Used as a placeholder for scaling and rotating the thruster image.
        surf (surf): The surface of the thruster.
        rect (rect): The rect of the thruster.
        OFFSET (int): The offset of the thruster for correctly positioning it behind the player.
        angle (float): The angle of the thruster.
        visibility (bool): Whether the thruster is visible or not.
    """

    def __init__(self):
        """Initialises the thruster object."""
        super().__init__()
        self._layer = 5
        self.image = pygame.image.load("survoids/images/thruster.png").convert_alpha()
        self.original_image = pygame.image.load("survoids/images/thruster.png")
        self.surf = pygame.Surface((14, 31))
        self.rect = self.surf.get_rect()
        self.OFFSET = 30
        self.angle = 90.0
        self.visibility = False

    def update_visibility(self) -> None:
        """Updates the thruster's visibility."""
        keyboard = pygame.key.get_pressed()

        # Visibility
        if (
            keyboard[pygame.K_w]
            or keyboard[pygame.K_s]
            or keyboard[pygame.K_a]
            or keyboard[pygame.K_d]
        ):
            if not self.visibility:
                self.visibility = True
        else:
            if self.visibility:
                self.visibility = False


class Bullet(pygame.sprite.Sprite):
    """The bullet class for player and enemy bullets.

    Attributes:
        image (surf): The image of the bullet scaled and rotated correctly.
        original_image (surf): Used as a placeholder for scaling and rotating the bullet image in the angle of the object that fires it.
        surf (surf): The surface for the bullet.
        rect (rect): The rect of the bullet.
        x (float): The unrounded x coordinate of the bullet.
        y (float): The unrounded y coordinate of the bullet.
        angle (float): The angle of the bullet.
        SPEED (int): The speed of the bullet.
    """

    def __init__(
        self, angle: float, pos: tuple[float, float], img: str, size: tuple, speed: int
    ):
        """Initialises the bullet object.

        Args:
            angle (float): The angle of the object that fires it.
            pos (tuple[float, float]): The position of the object that fires it.
            img (str): The image of the bullet.
            size (tuple): The size the bullet should be scaled to.
            speed (int): The speed of the bullet.
        """
        super().__init__()
        self._layer = 1

        unscaled_image = pygame.image.load(f"survoids/images/{img}").convert_alpha()
        self.image = pygame.transform.scale(unscaled_image, size)
        self.original_image = pygame.transform.scale(unscaled_image, size)
        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect(center=tuple(map(lambda x: round(x), pos)))
        self.x = pos[0]
        self.y = pos[1]

        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.SPEED = speed

    def move(self) -> None:
        """Updates the bullet object's position, killing it if it exits the screen."""
        angle = -math.radians(self.angle)
        self.x += self.SPEED * math.sin(angle)
        self.y -= self.SPEED * math.cos(angle)

        if self.x > 620 or self.x < -20 or self.y > 620 or self.y < -20:
            self.kill()

        self.rect.centerx = round(self.x)
        self.rect.centery = round(self.y)


class Enemy(pygame.sprite.Sprite):
    """The base enemy class.

    Attributes:
        value (int): The value of the Enemy class.
        likelihood (int): The likelihood that the Enemy class appears.
        buff_spawn_chance (int): The chance that the Enemy class spawns a buff on death out of 100.
        SPAWN_RADIUS (int): The minimum distance from the centre of the screen that the enemy should spawn from.
        MAX_INCREASE_RADIUS (int): The maximum range from the centre of the screen that the enemy should spawn from.
        image (surf): The image of the enemy scaled and rotated correctly.
        original_image (surf): Used as a placeholder for scaling and rotating the enemy image.
        surf (surf): The surface for the enemy.
        rect (rect): The rect of the enemy.
        SPEED (int): The speed of the enemy.
        hp (int): The health points of the enemy.
        angle (float): The angle of the enemy, first used to calculate its spawn location.
        radians (float): The angle of the enemy in degrees and flipped.
        x (float): The unrounded x coordinate of the enemy.
        y (float): The unrounded y coordinate of the enemy.
    """

    value: int = 0
    likelihood: int = 0
    buff_spawn_chance: int = 0
    SPAWN_RADIUS: int = 450
    MAX_INCREASE_RADIUS: int = 50

    def __init__(
        self,
        img: str = "enemy_a.png",
        size: tuple = (26, 21),
        speed: int | float = 2,
        hp: int = 1,
    ):
        """Initialises the enemy object.

        Args:
            img (str, optional): The png of the enemy image. Defaults to "enemy_a.png".
            size (tuple, optional): The size the enemy should be scaled to. Defaults to (26, 21).
            speed (int | float, optional): The speed of the enemy. Defaults to 2.
            hp (int): The health points of the enemy. Defaults to 1.
        """
        super().__init__()
        self._layer = 2

        unscaled_image = pygame.image.load(f"survoids/images/{img}").convert_alpha()
        self.image = pygame.transform.scale(unscaled_image, size)
        self.original_image = pygame.transform.scale(unscaled_image, size)
        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect()

        self.SPEED = speed
        self.hp = hp

        self.angle = rand.randint(0, 360)
        self.radians = -math.radians(self.angle)

        self.x = WIDTH / 2 + rand.randint(
            Enemy.SPAWN_RADIUS,
            round(Enemy.SPAWN_RADIUS + Enemy.MAX_INCREASE_RADIUS * self.SPEED),
        ) * math.sin(self.radians)
        self.y = HEIGHT / 2 + rand.randint(
            Enemy.SPAWN_RADIUS,
            round(Enemy.SPAWN_RADIUS + Enemy.MAX_INCREASE_RADIUS * self.SPEED),
        ) * math.cos(self.radians)
        self.rect.centerx = round(self.x)
        self.rect.centery = round(self.y)

    def get_angle(self) -> float:
        """Returns the angle of the enemy.

        Returns:
            float: The angle of the enemy.
        """
        return self.angle

    def get_pos(self) -> tuple[float, float]:
        """Returns the position of the enemy.

        Returns:
            tuple: The unrounded x and y coordinates of the enemy.
        """
        x = self.x
        y = self.y
        return (x, y)

    def fire(self, *sprite_groups) -> None:
        """Placeholder for enemy types to fire bullets that should be overridden."""
        pass

    def move(self) -> None:
        """Moves the enemy towards the player."""
        self.radians = -math.radians(self.angle)
        self.x += self.SPEED * math.sin(self.radians)
        self.y -= self.SPEED * math.cos(self.radians)
        self.rect.centerx = round(self.x)
        self.rect.centery = round(self.y)


class EnemyA(Enemy):
    """The A type of the enemy class that tries to ram the player.

    Attributes:
        value (int): The value of the Enemy class.
        likelihood (int): The likelihood that the Enemy class appears.
        buff_spawn_chance (int): The chance that the Enemy class spawns a buff on death out of 100.
    """

    value = 5
    likelihood = 10
    buff_spawn_chance = 5

    def __init__(self):
        """Initialises the A type enemy with the enemy_a.png, a quarter of the size and a speed of 2."""
        super().__init__(img="enemy_a.png", size=(26, 21), speed=2)


class EnemyB(Enemy):
    """The B type of the enemy class that fires bullets while trying to ram the player.

    Attributes:
        value (int): The value of the Enemy class.
        likelihood (int): The likelihood that the Enemy class appears.
        buff_spawn_chance (int): The chance that the Enemy class spawns a buff on death out of 100.
        BULLET_HOLDOFF (int): The max number of frames before the B type enemy can fire another bullet.
        bullet_delay (int): The current number of frames before the B type enemy can fire another bullet.
    """

    value = 10
    likelihood = 0
    buff_spawn_chance = 7

    def __init__(self):
        """Initialises the B type enemy with the enemy_b.png, a quarter of the size and a speed of 1."""
        super().__init__(img="enemy_b.png", size=(26, 21), speed=1)

        self.BULLET_HOLDOFF = 60
        self.bullet_delay = 0

    def fire(
        self,
        all_sprites: pygame.sprite.LayeredUpdates,
        enemy_bullet_sprites: pygame.sprite.Group,
    ) -> None:
        """Fire the bullet in the direction of the B type enemy if it can.

        Args:
            all_sprites (pygame.sprite.LayeredUpdates): The main sprites LayeredUpdates group.
            enemy_bullet_sprites (pygame.sprite.Group): The enemy bullet sprites group.
        """
        if self.bullet_delay <= 0:
            bullet = Bullet(
                self.get_angle(), self.get_pos(), "enemy_b_bullet.png", (4, 16), 4
            )
            add_sprite_to_groups(bullet, all_sprites, enemy_bullet_sprites)
            self.bullet_delay = self.BULLET_HOLDOFF
        else:
            self.bullet_delay -= 1


class EnemyC(Enemy):
    """The C type of the enemy class that has a higher hp value.

    Attributes:
        value (int): The value of the Enemy class.
        likelihood (int): The likelihood that the Enemy class appears.
        buff_spawn_chance (int): The chance that the Enemy class spawns a buff on death out of 100.
    """

    value = 10
    likelihood = 0
    buff_spawn_chance = 10

    def __init__(self):
        """Initialises the C type enemy with the enemy_c.png, a quarter of the size and a speed of 1.5."""
        super().__init__(img="enemy_c.png", size=(26, 21), speed=1.5, hp=3)


class Hitmarker(pygame.sprite.Sprite):
    """The hitmarker class for when a bullet hits an enemy.

    Attributes:
        image (surf): The hit_marker.png image.
        surf (surf): The surface of the hitmarker.
        rect (rect): The rect of the hitmarker.
        time (int): The number of frames the hitmarker has been on screen.
        TIMEOUT (int): The number of frames before the hitmarker times out.
    """

    def __init__(self, pos: tuple[float, float]):
        """Initialises the hitmarker object.

        Args:
            pos (tuple[float, float]): The position of the enemy the bullet struck for the hitmarker to appear at.
        """
        super().__init__()
        self._layer = 4

        self.image = pygame.image.load("survoids/images/hit_marker.png").convert_alpha()
        self.surf = pygame.Surface((37, 37))
        self.rect = self.surf.get_rect(center=tuple(map(lambda x: round(x), pos)))

        self.time = 0
        self.TIMEOUT = 31  # 31 instead of 30 as update_time() is called immediately after initialisation of an object and before checking timeout

    def check_timeout(self) -> bool:
        """Checks whether the hitmarker has timed out or not.

        Returns:
            bool: True if the hitmarker has timed out, False if not.
        """
        if self.time >= self.TIMEOUT:
            return True
        return False

    def update_time(self):
        """Updates the hitmarker object's time variable."""
        self.time += 1


class Power(pygame.sprite.Sprite):
    """The power up class.

    Attributes:
        image (surf): The image of the power up.
        surf (surf): The surface of the power up.
        rect (rect): The rect of the power up.
    """

    def __init__(self, pos: tuple[int, int], image: str):
        """Initialisation of the power up object.

        Args:
            pos (tuple[int, int]): The position of the power up.
            image (str): The power up image png.
        """
        super().__init__()
        self._layer = 7

        self.image = pygame.image.load(f"survoids/images/{image}").convert_alpha()
        self.surf = pygame.Surface((37, 37))
        self.rect = self.surf.get_rect(center=pos)


class Buff(pygame.sprite.Sprite):
    """The buff class.

    Attributes:
        likelihood (int): The likelihood of the buff spawning when a buff is spawned.
        image (surf): The image of the buff.
        surf (surf): The surface of the buff.
        rect (rect): The rect of the buff.
    """

    likelihood: int = 0

    def __init__(
        self,
        pos: tuple[float, float],
        image: str = "buff_lightning.png",
        img_size: tuple[int, int] = (22, 21),
    ):
        """Initialisation of the buff object.

        Args:
            pos (tuple[float, float]): The position of the buff.
            image (str): The buff image png.
            img_size: tuple[int, int]: The size of the image.
        """
        super().__init__()
        self._layer = 3

        self.image = pygame.image.load(f"survoids/images/{image}").convert_alpha()
        self.surf = pygame.Surface(img_size)
        self.rect = self.surf.get_rect(center=pos)


# lightning -> temp fire rate, star -> temp invuln, bpill -> temp double shot, rpill -> temp 3x damage


class BuffLightning(Buff):
    """The lightning buff that gives temporary fire rate."""

    likelihood: int = 10

    def __init__(self, new_pos: tuple[float, float]):
        """Initialisation of the lightning buff.

        Args:
            new_pos (tuple[float, float]): The position of the lightning buff.
        """
        super().__init__(pos=(new_pos), image="buff_lightning.png", img_size=(19, 30))


class BuffStar(Buff):
    """The star buff that gives temporary invulnerability."""

    likelihood: int = 5

    def __init__(self, new_pos: tuple[float, float]):
        """Initialisation of the star buff.

        Args:
            new_pos (tuple[float, float]): The position of the star buff.
        """
        super().__init__(pos=(new_pos), image="buff_star.png", img_size=(31, 31))


class BuffBluePill(Buff):
    """The blue pill buff that gives temporary double shot."""

    likelihood: int = 3

    def __init__(self, new_pos: tuple[float, float]):
        """Initialisation of the blue pill buff.

        Args:
            new_pos (tuple[float, float]): The position of the blue pill buff.
        """
        super().__init__(pos=(new_pos), image="buff_bpill.png", img_size=(22, 21))


class BuffRedPill(Buff):
    """The red pill buff that gives temporary damage."""

    likelihood: int = 4

    def __init__(self, new_pos: tuple[float, float]):
        """Initialisation of the red pill buff.

        Args:
            new_pos (tuple[float, float]): The position of the red pill buff.
        """
        super().__init__(pos=(new_pos), image="buff_rpill.png", img_size=(22, 21))


class BuffTypes:
    """Defines the buff types for use in a case statement."""

    Lightning = BuffLightning
    Star = BuffStar
    BluePill = BuffBluePill
    RedPill = BuffRedPill


class UserInterface(pygame.sprite.Sprite):
    """The user interface class.

    Attributes:
        image (surf): The image of the user interface object.
        surf (surf): The surface of the user interface.
        rect (rect): The rect of the user interface.
        clicked (bool): The state of whether the user interface is being clicked or not.
    """

    def __init__(
        self,
        img: str,
        width: float,
        height: float,
        pos: tuple[int, int],
        scale: bool = False,
    ):
        """Initialises the user interface object.

        Args:
            img (str): The name of the user interface object including .png.
            width (float): The width of the user interface object.
            height (float): The height of the user interface object.
            pos (tuple[int, int]): The position of the user interface on the screen.
            scale (bool, optional): Whether the object should be scaled to the width and height or not. Defaults to False.
        """
        super().__init__()
        self._layer = 7

        self.image = pygame.image.load(f"survoids/images/{img}").convert_alpha()

        if scale:
            self.image = pygame.transform.scale(self.image, (width, height))

        self.surf = pygame.Surface((width, height))
        self.rect = self.surf.get_rect(center=pos)

        self.clicked = False

    def change_clicked(self, new_clicked: bool):
        """Change the value of clicked to the new clicked value.

        Args:
            new_clicked (bool): The new value of clicked.
        """
        if self.clicked != new_clicked:
            self.clicked = new_clicked


class Text(pygame.sprite.Sprite):
    """The text class.

    Attributes:
        words (str): The words of the text object.
        pos_type (str): The type of position the text object is positioned by.
        pos (tuple[int, int]): The position of the text object.
        colour (tuple[int, int, int]): The RGB value of the colour of the text object.
        font (Font): The font of the text object.
        surf (surf): The surface of the text object.
        rect (rect): The rect of the text object.
    """

    def __init__(
        self,
        initial: str,
        font_name: str,
        font_size: int,
        pos_type: str,
        pos: tuple[int, int],
        colour: tuple[int, int, int] = (255, 255, 255),
    ):
        """Initialises the text object.

        Args:
            initial (str): The initial words of the text object.
            font_name (str): The name of the text's font's file excluding .ttf.
            font_size (int): The size of the text's font.
            pos_type (str): The type of position the text object is positioned by.
            pos (tuple[int, int]): The position of the text object.
            colour (tuple[int, int, int], optional): The RGB value of the colour of the text object. Defaults to (255, 255, 255).
        """
        super().__init__()
        self._layer = 8

        self.words = initial
        self.pos_type = pos_type
        self.pos = pos
        self.colour = colour

        self.font = pygame.font.Font(f"survoids/fonts/{font_name}.ttf", font_size)
        self.surf = self.font.render(self.words, True, self.colour)
        self.rect = self.surf.get_rect()

        self.set_position()

    def set_position(self):
        """Sets the text object's position using its position type and position."""
        setattr(self.rect, self.pos_type, self.pos)

    def change_colour(self, new_colour: tuple[int, int, int]):
        """Changes the colour of the text object to the new colour.

        Args:
            new_colour (tuple[int, int, int]): The new RGB value of the colour of the text object.
        """
        self.colour = new_colour

    def update_words(self, new_words: str):
        """Updates the words of the text object to be the new words.

        Args:
            new_words (str): The new words for the text object.
        """
        self.words = new_words
        self.surf = self.font.render(self.words, True, self.colour)
        self.rect = self.surf.get_rect()
        self.set_position()


class VolumeMeter(pygame.sprite.Sprite):
    """The volume meter class.

    Attributes:
        x (float): The x coordinate of the volume meter.
        y (float): The y coordinate of the volume meter.
        width (int): The width of the volume meter.
        max_vol (int | float): The maximum volume of the volume meter.
        current_vol (int | float): The current volume of the volume meter.
        height (int): The height of the volume meter.
        front_colour (tuple[int, int, int]): The RGB value of the current volume in the volume meter.
        back_colour (tuple[int, int, int]): The RGB value of the maximum volume in the volume meter.
        obj (pygame.sprite.Sprite | None): The object that the volume meter is assigned to.
        attr (str | None): The attribute of the object or variable that the volume meter is assigned to.
    """

    def __init__(
        self,
        pos: tuple[int, int],
        initial_val: int | float,
        width: int,
        height: int,
        front_colour: tuple[int, int, int],
        back_colour: tuple[int, int, int] = (255, 255, 255),
        *,
        obj: pygame.sprite.Sprite | None = None,
        attr: str | None = None,
    ):
        """Initialises the volume meter class.

        Args:
            pos (tuple[int, int]): The left top position of the volume meter.
            initial_val (int | float): The initial value of the volume meter.
            width (int): The width of the volume meter.
            height (int): The height of the volume meter.
            front_colour (tuple[int, int, int]): The front colour of the volume meter.
            back_colour (tuple[int, int, int], optional): The colour of the background of the volume meter.. Defaults to (255, 255, 255).
            obj (pygame.sprite.Sprite | None, optional): The object that the volume meter is assigned to. Defaults to None.
            attr (str | None, optional): The attribute of the object or variable that the volume meter is assigned to. Defaults to None.
        """
        super().__init__()
        self._layer = 7

        self.x = float(pos[0])
        self.y = float(pos[1])
        self.width = width
        self.max_vol = initial_val
        self.current_vol = width
        self.height = height
        self.front_colour = front_colour
        self.back_colour = back_colour

        self.obj = obj
        self.attr = attr

    def update_max_vol(self, *new_max_vol):
        """Updates the maximum volume variable.

        Args:
            new_attr (tuple[int | float]): The new maximum volume if the volume meter is assigned to a variable.
        """
        if self.obj and self.attr:
            self.max_vol = getattr(self.obj, self.attr)
        elif self.attr:
            self.max_vol = new_max_vol[0]
        else:
            pass

    def update_current_vol(self, *new_vol):
        """Updates the current volume variable.

        Args:
            new_attr (tuple[int | float]): The new current volume if the volume meter is assigned to a variable.
        """
        if self.obj and self.attr:
            self.current_vol = getattr(self.obj, self.attr)
        elif self.attr:
            self.current_vol = new_vol[0]
        else:
            pass

    def draw(self, screen):
        """Draws the volume meter.

        Args:
            screen (Surface): The pygame screen.
        """
        back_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        volume_rect = pygame.Rect(
            self.x, self.y, (self.current_vol / self.max_vol) * self.width, self.height
        )

        pygame.draw.rect(screen, self.back_colour, back_rect)
        pygame.draw.rect(screen, self.front_colour, volume_rect)

    def update(self):
        """Updates the volume meter's position if necessary."""
        if self.obj:
            self.x = getattr(self.obj, "self.x")
            self.y = getattr(self.obj, "self.y")


class ScreenEffect(pygame.sprite.Sprite):
    """The screen effect class.

    Attributes:
        surf (surf): The surface of the screen effect object with transparency and colour values.
        rect (rect): The rect of the screen effect, centered in the middle of the screen.
    """

    def __init__(self, colour: tuple[int, int, int], alpha: int = 0):
        """Initialises the screen effect object.

        Args:
            colour (tuple[int, int, int]): The RGB value of the colour for the screen effect object.
            alpha (int, optional): The transparency value of the screen effect object.. Defaults to 0.
        """
        super().__init__()
        self._layer = 9

        self.surf = pygame.Surface((WIDTH, HEIGHT))
        self.surf.set_alpha(alpha)
        self.surf.fill(colour)
        self.rect = self.surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))


## Functions


def calculate_angle_between_points(p1, p2) -> float:
    """Calculates the angle between two points.

    Args:
        p1 (pygame Sprite): Has a rect and angle.
        p2 (pygame Sprite): Has a rect and angle.

    Returns:
        float: The angle between the two points in degrees.
    """
    p1_coordinates: tuple[int, int] = p1.rect.center
    p2_coordinates: tuple[int, int] = p2.rect.center

    x1: int = p1_coordinates[0]
    y1: int = p1_coordinates[1]

    x2: int = p2_coordinates[0]
    y2: int = p2_coordinates[1]

    dx: int = x2 - x1
    dy: int = y2 - y1

    radians: float = math.atan2(dy, dx)
    angle: float = -math.degrees(radians) - 90

    return angle


def point_object_to_object(obj1, obj2) -> None:
    """Changes the image of an object to face another object.

    Args:
        obj1 (pygame Sprite): Object being changed, has a rect, image, original image and angle.
        obj2 (pygame Sprite): Object being copied, has a rect.
    """
    obj1.angle = calculate_angle_between_points(obj1, obj2)
    obj1.image = pygame.transform.rotate(obj1.original_image, obj1.angle)
    obj1.rect = obj1.image.get_rect(center=obj1.rect.center)


def rotate_object(obj) -> None:
    """Rotates an object based on its angle.

    Args:
        obj (pygame Sprite): Has a rect, image, original image and angle.
    """
    obj.image = pygame.transform.rotate(obj.original_image, obj.angle)
    obj.rect = obj.image.get_rect(center=obj.rect.center)


def add_sprite_to_groups(
    sprite: pygame.sprite.Sprite,
    group: pygame.sprite.Group | pygame.sprite.LayeredUpdates,
    *groups: pygame.sprite.Group | pygame.sprite.LayeredUpdates,
) -> None:
    """Adds the sprite to each provided group.

    Args:
        sprite (pygame.sprite.Sprite): A pygame sprite.
        group (pygame.sprite.Group | pygame.sprite.LayeredUpdates): An arbitrary sprite group.
        *groups (pygame.sprite.Group | pygame.sprite.LayeredUpdates): Some extra number of sprite groups.
    """
    for sprite_group in (group,) + groups:
        sprite_group.add(sprite)


def remove_sprite_from_groups(
    sprite: pygame.sprite.Sprite,
    *groups: pygame.sprite.Group | pygame.sprite.LayeredUpdates,
) -> None:
    """Removes the sprite from each provided group.

    Args:
        sprite (pygame.sprite.Sprite): A pygame sprite.
        *groups (pygame.sprite.Group | pygame.sprite.LayeredUpdates): Some number of sprite groups.
    """
    for group in groups:
        group.remove(sprite)


def adjust_thruster(thruster: Thruster, player: Player) -> None:
    """Adjusts the thruster to be positioned behind the player.

    Args:
        thruster (Thruster): The thruster object.
        player (Player): The player object.
    """
    player_angle = player.get_angle()
    angle = -math.radians(player_angle)

    thruster.rect.centerx = player.rect.centerx - round(
        thruster.OFFSET * math.sin(angle)
    )
    thruster.rect.centery = player.rect.centery + round(
        thruster.OFFSET * math.cos(angle)
    )

    thruster.angle = player.angle
    thruster.image = pygame.transform.rotate(thruster.original_image, thruster.angle)
    thruster.rect = thruster.image.get_rect(center=thruster.rect.center)


def fire_bullet(
    player: Player,
    all_sprites: pygame.sprite.LayeredUpdates,
    bullet_sprites: pygame.sprite.Group,
) -> None:
    """Creates a bullet in the direction of the player if no delay and space is pressed down.

    Args:
        player (Player): The player object.
        all_sprites (pygame.sprite.LayeredUpdates): The main sprites LayeredUpdates group.
        bullet_sprites (pygame.sprite.Group): The bullet sprites group for the bullet to be added to.
    """
    keyboard = pygame.key.get_pressed()

    if player.bullet_delay <= 0:
        if keyboard[pygame.K_SPACE]:
            if not player.bpill_buff_act:
                bullet = Bullet(
                    player.get_angle(), player.get_pos(), "bullet.png", (4, 24), 25
                )
                add_sprite_to_groups(bullet, all_sprites, bullet_sprites)

            elif player.bpill_buff_act:
                bullet_1 = Bullet(
                    player.get_angle() + 10, player.get_pos(), "bullet.png", (4, 24), 25
                )
                add_sprite_to_groups(bullet_1, all_sprites, bullet_sprites)

                bullet_2 = Bullet(
                    player.get_angle() - 10, player.get_pos(), "bullet.png", (4, 24), 25
                )
                add_sprite_to_groups(bullet_2, all_sprites, bullet_sprites)

            player.bullet_delay = math.ceil(player.bullet_holdoff * player.atk_speed)
    else:
        player.bullet_delay -= 1


def end_wave(enemy_sprites: pygame.sprite.Group) -> bool:
    """Returns whether the wave has ended or not using the number of enemies.

    Args:
        enemy_sprites (pygame.sprite.Group): The enemy sprites group.

    Returns:
        bool: True if there are no enemies in the sprite group, False if not
    """
    if len(enemy_sprites) == 0:
        return True
    return False


def display_wave_clear(
    all_sprites: pygame.sprite.LayeredUpdates,
    text_sprites: pygame.sprite.Group,
    wave_clear_sprites: pygame.sprite.Group,
    wave: int,
) -> None:
    """Displays the wave clear text.

    Args:
        all_sprites (pygame.sprite.LayeredUpdates): The main sprites LayeredUpdates group.
        text_sprites (pygame.sprite.Group): The text sprites group.
        wave_clear_sprites (pygame.sprite.Group): The wave clear sprites group.
        wave (int): The wave number.
    """
    wave_clear = Text(
        f"Wave {wave} Cleared", "kenvector_future_thin", 60, "center", (300, 280)
    )
    add_sprite_to_groups(wave_clear, all_sprites, text_sprites, wave_clear_sprites)


def spawn_enemies(
    enemy_wave: list[type[Enemy]],
    all_sprites: pygame.sprite.LayeredUpdates,
    enemy_sprites: pygame.sprite.Group,
) -> None:
    """Spawns the enemies in the given wave.

    Args:
        enemy_wave (list[type[Enemy]]): The list of enemy classes to be spawned.
        all_sprites (pygame.sprite.LayeredUpdates): The main sprites LayeredUpdates group.
        enemy_sprites (pygame.sprite.Group): The enemy sprites group for the enemy to be added to.
    """
    for enemy in enemy_wave:
        new_enemy = enemy()
        add_sprite_to_groups(new_enemy, all_sprites, enemy_sprites)


def calc_wave(wave_value: int) -> list[type[Enemy]]:
    """Calculates and returns a list of enemy classes for a given wave.

    Args:
        wave_value (int): The value of the current wave.

    Returns:
        list[type[Enemy]]: A list of enemy classes for the wave value.
    """
    enemy_wave: list[type[Enemy]] = []
    enemy_types: list[type[Enemy]] = Enemy.__subclasses__()
    enemy_likelihood: list[type[Enemy]] = []
    current_wave_value: int = wave_value

    for enemy_type in enemy_types:
        for _ in range(enemy_type.likelihood):
            enemy_likelihood.append(enemy_type)

    while current_wave_value >= 5:  # smallest enemy value is 5
        random_num: int = rand.randrange(0, len(enemy_likelihood))
        enemy_type: type[Enemy] = enemy_likelihood[random_num]

        if current_wave_value - enemy_type.value < 0:
            continue

        enemy_wave.append(enemy_type)
        current_wave_value -= enemy_type.value

    return enemy_wave


def change_enemy_likelihoods() -> None:
    """Temp function that changes the likelihood values of the enemy classes."""
    EnemyA.likelihood -= 1
    EnemyB.likelihood += 1
    EnemyC.likelihood += 1


def spawn_waves(
    all_sprites: pygame.sprite.LayeredUpdates,
    enemy_sprites: pygame.sprite.Group,
    text_sprites: pygame.sprite.Group,
    wave_clear_sprites: pygame.sprite.Group,
    wave_info_sprites: pygame.sprite.Group,
    wave_num_text: Text,
    wave_bar: VolumeMeter,
    enemy_num_text: Text,
    wave: int,
    wave_value: int,
    wave_delay: int,
) -> tuple[int, int, int]:
    """Spawns waves of enemies if the previous wave has ended and wave delay is 0 or less.

    Args:
        all_sprites (pygame.sprite.LayeredUpdates): The main sprites LayeredUpdates group.
        enemy_sprites (pygame.sprite.Group): The enemy sprites group.
        text_sprites (pygame.sprite.Group): The text sprites group.
        wave_clear_sprites (pygame.sprite.Group): The wave clear sprites group.
        wave_info_sprites (pygame.sprite.Group): The wave info sprites group.
        wave_num_text (Text): The wave and wave number text object.
        wave_bar (VolumeMeter): The bar for the number of enemies in the wave.
        enemy_num_text (Text): The number of alive enemies in the current wave.
        wave (int): The wave number.
        wave_value (int): The value of the current wave.
        wave_delay (int): The delay before the next wave can spawn.

    Returns:
        tuple[int, int, int]: Updated values of wave_value, wave and wave_delay
    """
    if end_wave(enemy_sprites):
        if not wave_clear_sprites and wave != 0:
            display_wave_clear(all_sprites, text_sprites, wave_clear_sprites, wave)
            wave_delay = WAVE_HOLDOFF

        if wave_delay <= 0:
            if any(sprite not in all_sprites for sprite in wave_info_sprites):
                redisplay_wave_info(all_sprites, wave_info_sprites)

            enemy_wave = calc_wave(wave_value)
            spawn_enemies(enemy_wave, all_sprites, enemy_sprites)

            kill_sprite_group(wave_clear_sprites)
            change_enemy_likelihoods()
            wave_value += 10
            wave += 1
            wave_num_text.update_words(f"Wave {wave}")
            wave_bar.update_max_vol(len(enemy_wave))
            enemy_num_text.update_words(str(len(enemy_sprites)))
        else:
            if wave_info_sprites:
                hide_wave_info(wave_info_sprites, all_sprites)

            wave_delay -= 1
    return wave_value, wave, wave_delay


def spawn_buff(
    chance: int,
    pos: tuple[float, float],
    buff_sprites: pygame.sprite.Group,
    all_sprites: pygame.sprite.LayeredUpdates,
) -> None:
    """Spawns a random buff based on the chance given.

    Args:
        chance (int): The dead enemy's chance to spawn a buff.
        pos (tuple[float, float]): The position of the dead enemy.
        buff_sprites (pygame.sprite.Group): The buff sprites group.
        all_sprites (pygame.sprite.LayeredUpdates): The main sprites LayeredUpdates group.
    """
    if rand.randint(0, 100) <= chance:
        buff_types = Buff.__subclasses__()
        buffs_chance: list[type[Buff]] = []

        for buff_type in buff_types:
            for _ in range(buff_type.likelihood):
                buffs_chance.append(buff_type)

        new_buff_type = rand.choice(buffs_chance)
        new_buff = new_buff_type(pos)

        add_sprite_to_groups(new_buff, all_sprites, buff_sprites)


def display_main_screen(
    title_text: Text,
    play_text_effect_1: Text,
    play_text: Text,
    play_text_effect_2: Text,
    play_button: UserInterface,
    all_sprites: pygame.sprite.LayeredUpdates,
    text_sprites: pygame.sprite.Group,
    user_interface_sprites: pygame.sprite.Group,
    main_screen_sprites: pygame.sprite.Group,
) -> None:
    """Displays the main screen objects.

    Args:
        title_text (Text): The title text object.
        play_text_effect_1 (Text): The play text object's effect 1.
        play_text (Text): The play text object.
        play_text_effect_2 (Text): The play text object's effect 2.
        play_button (UserInterface): The play button.
        all_sprites (pygame.sprite.LayeredUpdates): The main sprites LayeredUpdates group.
        text_sprites (pygame.sprite.Group): The text sprites group.
        user_interface_sprites (pygame.sprite.Group): The user interface sprites group.
        main_screen_sprites (pygame.sprite.Group): The main screen sprites group.
    """
    add_sprite_to_groups(title_text, all_sprites, text_sprites, main_screen_sprites)

    add_sprite_to_groups(
        play_text_effect_1, all_sprites, text_sprites, main_screen_sprites
    )

    add_sprite_to_groups(play_text, all_sprites, text_sprites, main_screen_sprites)

    add_sprite_to_groups(
        play_text_effect_2, all_sprites, text_sprites, main_screen_sprites
    )

    add_sprite_to_groups(
        play_button, all_sprites, user_interface_sprites, main_screen_sprites
    )


def remove_main_screen(
    main_screen_sprites: pygame.sprite.Group,
    all_sprites: pygame.sprite.LayeredUpdates,
    text_sprites: pygame.sprite.Group,
    user_interface_sprites: pygame.sprite.Group,
) -> None:
    """Removes all sprites in the main screen sprites group from their groups.

    Args:
        main_screen_sprites (pygame.sprite.Group): The main screen sprites group.
        all_sprites (pygame.sprite.LayeredUpdates): The main sprites LayeredUpdates group.
        text_sprites (pygame.sprite.Group): The text sprites group.
        user_interface_sprites (pygame.sprite.Group): The user interface sprites group.
    """
    for sprite in main_screen_sprites.sprites():
        if sprite in text_sprites:
            remove_sprite_from_groups(
                sprite, all_sprites, text_sprites, main_screen_sprites
            )
        elif sprite in user_interface_sprites:
            remove_sprite_from_groups(
                sprite, all_sprites, user_interface_sprites, main_screen_sprites
            )


def kill_sprite_group(
    sprite_group: pygame.sprite.Group, *sprite_groups: pygame.sprite.Group
) -> None:
    """Kills all sprites in a sprite group.

    Args:
        sprite_group (pygame.sprite.Group): An arbitrary sprite group.
        *sprite_group (pygame.sprite.Group): Some extra number of sprite groups.
    """
    for group in (sprite_group,) + sprite_groups:
        for sprite in group:
            sprite.kill()


def display_background(
    background: Background, all_sprites: pygame.sprite.LayeredUpdates
) -> None:
    """Displays the background object.

    Args:
        background (Background): The background image object.
        all_sprites (pygame.sprite.LayeredUpdates): The main sprites LayeredUpdates group.
    """
    add_sprite_to_groups(background, all_sprites)


def display_mouse(mouse: Mouse, all_sprites: pygame.sprite.LayeredUpdates) -> None:
    """Displays the mouse object.

    Args:
        mouse (Mouse): The mouse image object.
        all_sprites (pygame.sprite.LayeredUpdates): The main sprites LayeredUpdates group.
    """
    add_sprite_to_groups(mouse, all_sprites)


def display_pause_screen(
    pause_screen: ScreenEffect,
    pause_text: Text,
    all_sprites: pygame.sprite.LayeredUpdates,
    screen_effect_sprites: pygame.sprite.Group,
    text_sprites: pygame.sprite.Group,
    pause_screen_sprites: pygame.sprite.Group,
) -> None:
    """Displays the pause screen objects.

    Args:
        pause_screen (ScreenEffect): The pause screen effect object.
        pause_text (Text): The pause screen text object.
        all_sprites (pygame.sprite.LayeredUpdates): The main sprites LayeredUpdates group.
        screen_effect_sprites (pygame.sprite.Group): The screen effect sprites group.
        text_sprites (pygame.sprite.Group): The text sprites group.
        pause_screen_sprites (pygame.sprite.Group): The pause screen sprites group.
    """
    add_sprite_to_groups(
        pause_screen, all_sprites, screen_effect_sprites, pause_screen_sprites
    )

    add_sprite_to_groups(pause_text, all_sprites, text_sprites, pause_screen_sprites)


def remove_pause_screen(
    pause_screen_sprites: pygame.sprite.Group,
    all_sprites: pygame.sprite.LayeredUpdates,
    screen_effect_sprites: pygame.sprite.Group,
    text_sprites: pygame.sprite.Group,
) -> None:
    """Removes all sprites in the pause screen sprites group from their groups.

    Args:
        pause_screen_sprites (pygame.sprite.Group): The pause screen sprites group.
        all_sprites (pygame.sprite.LayeredUpdates): The main sprites LayeredUpdates group.
        screen_effect_sprites (pygame.sprite.Group): The screen effect sprites group.
        text_sprites (pygame.sprite.Group): The text sprites group.
    """
    for sprite in pause_screen_sprites.sprites():
        if sprite in screen_effect_sprites:
            remove_sprite_from_groups(
                sprite, all_sprites, screen_effect_sprites, pause_screen_sprites
            )
        elif sprite in text_sprites:
            remove_sprite_from_groups(
                sprite, all_sprites, text_sprites, pause_screen_sprites
            )


def display_player(
    player: Player, thruster: Thruster, all_sprites: pygame.sprite.LayeredUpdates
) -> None:
    """Displays the player object and its thruster.

    Args:
        player (Player): The player object.
        thruster (Thruster): The thruster object.
        all_sprites (pygame.sprite.LayeredUpdates): The main sprites LayeredUpdates group.
    """
    add_sprite_to_groups(player, all_sprites)
    add_sprite_to_groups(thruster, all_sprites)


def display_user_interface(
    player_x_ui: UserInterface,
    player_life_icon: UserInterface,
    wave_num_text: Text,
    wave_bar: VolumeMeter,
    enemy_icon: UserInterface,
    enemy_x_ui: UserInterface,
    enemy_num_text: Text,
    lives_text: Text,
    score_text: Text,
    all_sprites: pygame.sprite.LayeredUpdates,
    user_interface_sprites: pygame.sprite.Group,
    wave_info_sprites: pygame.sprite.Group,
    text_sprites: pygame.sprite.Group,
    volume_meter_sprites: pygame.sprite.Group,
) -> None:
    """Displays the user interface objects.

    Args:
        player_x_ui (UserInterface): The X user interface object next to the player life icon.
        player_life_icon (UserInterface): The player life icon object.
        wave_num_text (Text): The wave and wave number text object.
        enemy_icon (UserInterface): The enemy icon object.
        enemy_x_ui (UserInterface): The X user interface object next to the enemy number icon.
        enemy_num_text (Text): The number of alive enemies in the current wave.
        wave_bar (VolumeMeter): The volume meter for the number of enemies.
        lives_text (Text): The lives text object.
        score_text (Text): The score text object.
        all_sprites (pygame.sprite.LayeredUpdates): The main sprites LayeredUpdates group.
        user_interface_sprites (pygame.sprite.Group): The user interface sprites group.
        wave_info_sprites (pygame.sprite.Group): The wave info sprites group.
        text_sprites (pygame.sprite.Group): The text sprites group.
        volume_meter_sprites (pygame.sprite.Group): The volume meter sprites group.
    """
    add_sprite_to_groups(player_x_ui, all_sprites, user_interface_sprites)

    add_sprite_to_groups(player_life_icon, all_sprites, user_interface_sprites)

    add_sprite_to_groups(wave_num_text, all_sprites, text_sprites, wave_info_sprites)

    add_sprite_to_groups(wave_bar, all_sprites, volume_meter_sprites, wave_info_sprites)

    add_sprite_to_groups(
        enemy_icon, all_sprites, user_interface_sprites, wave_info_sprites
    )

    add_sprite_to_groups(
        enemy_x_ui, all_sprites, user_interface_sprites, wave_info_sprites
    )

    add_sprite_to_groups(enemy_num_text, all_sprites, text_sprites, wave_info_sprites)

    add_sprite_to_groups(lives_text, all_sprites, text_sprites)

    add_sprite_to_groups(score_text, all_sprites, text_sprites)


def hide_wave_info(
    wave_info_sprites: pygame.sprite.Group, all_sprites: pygame.sprite.LayeredUpdates
) -> None:
    """Hides the sprites in the wave info sprites group.

    Args:
        wave_info_sprites (pygame.sprite.Group): The wave info sprites group.
        all_sprites (pygame.sprite.LayeredUpdates): The main sprites LayeredUpdates group.
    """
    for sprite in wave_info_sprites.sprites():
        remove_sprite_from_groups(sprite, all_sprites)


def redisplay_wave_info(
    all_sprites: pygame.sprite.LayeredUpdates, wave_info_sprites: pygame.sprite.Group
) -> None:
    """Redisplays the sprites previously in the wave info sprite group.

    Args:
        all_sprites (pygame.sprite.LayeredUpdates): The main sprites LayeredUpdates group.
        wave_info_sprites (pygame.sprite.Group): The wave info sprites group.
    """
    for sprite in wave_info_sprites:
        add_sprite_to_groups(sprite, all_sprites)


def update_stats(player: Player, score: int) -> int:
    """Updates the stats of score and player experience.

    Args:
        player (Player): The player object.
        score (int): The score number.

    Returns:
        int: Updated score number.
    """
    player.experience += 4
    return score + 20


def update_game_state(
    game_state: str, previous_game_state: str, new_state: str
) -> tuple[str, str]:
    """Updates the game's state.

    Args:
        game_state (str): The current game state.
        previous_game_state (str): The previous game state.
        new_state (str): The new game state.

    Returns:
        tuple[str, str]: The game state followed by its previous state.
    """
    previous_game_state = game_state
    game_state = new_state
    return game_state, previous_game_state


def check_mouse_click(obj) -> bool:
    """Checks whether the mouse is clicking on the object or not.

    Args:
        obj (pygame Sprite): Has a rect.

    Returns:
        bool: True if the mouse is clicking on the object, False if not
    """
    if obj.rect.collidepoint(pygame.mouse.get_pos()):
        return True
    return False


def check_game_over(lives: int) -> bool:
    """Checks whether the game is over or not using the player's lives.

    Args:
        lives (int): The number of lives of the player.

    Returns:
        bool: True if the player has died, False if they are alive.
    """
    if lives <= 0:
        return True
    else:
        return False


def display_powers(
    player: Player,
    all_sprites: pygame.sprite.LayeredUpdates,
    power_sprites: pygame.sprite.Group,
    text_sprites: pygame.sprite.Group,
    power_up_text_sprites: pygame.sprite.Group,
) -> None:
    """Displays the power objects and their text objects.

    Args:
        player (Player): The player object.
        all_sprites (pygame.sprite.LayeredUpdates): The main sprites LayeredUpdates group.
        power_sprites (pygame.sprite.Group): The power sprites group.
        text_sprites (pygame.sprite.Group): The text sprites group.
        power_up_text_sprites (pygame.sprite.Group): The power up text sprites group.
    """
    if player.bullet_holdoff > 6:
        lightning_power = Power((224, 483), "powerup1.png")
    else:
        lightning_power = Power((224, 483), "poweruplocked.png")

    lightning_text = Text("(1)", "kenvector_future_thin", 8, "midtop", (224, 520))

    add_sprite_to_groups(lightning_power, all_sprites, power_sprites)
    add_sprite_to_groups(
        lightning_text, all_sprites, text_sprites, power_up_text_sprites
    )

    if player.acceleration_speed < 0.8:
        speed_power = Power((300, 483), "powerup2.png")
    else:
        speed_power = Power((300, 483), "poweruplocked.png")

    speed_text = Text("(2)", "kenvector_future_thin", 8, "midtop", (300, 520))

    add_sprite_to_groups(speed_power, all_sprites, power_sprites)
    add_sprite_to_groups(speed_text, all_sprites, text_sprites, power_up_text_sprites)

    health_power = Power((376, 483), "powerup3.png")

    health_text = Text("(3)", "kenvector_future_thin", 8, "midtop", (376, 520))

    add_sprite_to_groups(health_power, all_sprites, power_sprites)
    add_sprite_to_groups(health_text, all_sprites, text_sprites, power_up_text_sprites)


def display_end_screen(
    end_screen: ScreenEffect,
    game_over_text: Text,
    retry_button: UserInterface,
    retry_text_effect_1: Text,
    retry_text: Text,
    retry_text_effect_2: Text,
    all_sprites: pygame.sprite.LayeredUpdates,
    end_screen_sprites: pygame.sprite.Group,
    screen_effect_sprites: pygame.sprite.Group,
    text_sprites: pygame.sprite.Group,
    user_interface_sprites: pygame.sprite.Group,
) -> None:
    """Displays the end screen objects.

    Args:
        end_screen (ScreenEffect): The end screen grey screen effect object.
        game_over_text (Text): The game over text object.
        retry_button (UserInterface): The retry button.
        retry_text_effect_1 (Text): The first text effect shadow on the retry text.
        retry_text (Text): The retry text.
        retry_text_effect_2 (Text): The second text effect shadow on the retry text.
        all_sprites (pygame.sprite.LayeredUpdates): The main sprites LayeredUpdates group.
        end_screen_sprites (pygame.sprite.Group): The end screen sprites group.
        screen_effect_sprites (pygame.sprite.Group): The screen effect sprites group.
        text_sprites (pygame.sprite.Group): The text sprites group.
        user_interface_sprites (pygame.sprite.Group): The user interface sprites group.
    """
    add_sprite_to_groups(
        end_screen, all_sprites, end_screen_sprites, screen_effect_sprites
    )

    add_sprite_to_groups(game_over_text, all_sprites, end_screen_sprites, text_sprites)

    add_sprite_to_groups(
        retry_button, all_sprites, end_screen_sprites, user_interface_sprites
    )

    add_sprite_to_groups(
        retry_text_effect_1, all_sprites, end_screen_sprites, text_sprites
    )

    add_sprite_to_groups(retry_text, all_sprites, end_screen_sprites, text_sprites)

    add_sprite_to_groups(
        retry_text_effect_2, all_sprites, end_screen_sprites, text_sprites
    )


def remove_end_screen(
    end_screen_sprites: pygame.sprite.Group,
    all_sprites: pygame.sprite.LayeredUpdates,
    screen_effect_sprites: pygame.sprite.Group,
    text_sprites: pygame.sprite.Group,
    user_interface_sprites: pygame.sprite.Group,
) -> None:
    """Removes all end screen sprites.

    Args:
        end_screen_sprites (pygame.sprite.Group): The end screen sprites group.
        all_sprites (pygame.sprite.LayeredUpdates): The main sprites LayeredUpdates group.
        screen_effect_sprites (pygame.sprite.Group): The screen effect sprites group.
        text_sprites (pygame.sprite.Group): The text sprites group.
        user_interface_sprites (pygame.sprite.Group): The user interface sprites group.
    """
    for sprite in end_screen_sprites.sprites():
        if sprite in screen_effect_sprites:
            remove_sprite_from_groups(
                sprite, all_sprites, screen_effect_sprites, end_screen_sprites
            )
        if sprite in text_sprites:
            remove_sprite_from_groups(
                sprite, all_sprites, text_sprites, end_screen_sprites
            )
        if sprite in user_interface_sprites:
            remove_sprite_from_groups(
                sprite, all_sprites, user_interface_sprites, end_screen_sprites
            )


def reset_game_results() -> None:
    """Resets the game_results.txt file."""
    with open("survoids/game_results.txt", "w") as game_results:
        game_results.write("This is the text file where game data is saved.\n\n")


def store_game_info(score: int, level: int, wave: int, time_elapsed: float) -> None:
    """Stores the game info in the game_results.txt file.

    Args:
        score (int): The score number.
        level (int): The level number of the player.
        wave (int): The wave number.
        time_elapsed (float): The number of ticks elapsed in game.
    """

    with open("survoids/game_results.txt", "a") as game_results:
        game_results.write(f"Score: {score}\n")
        game_results.write(f"Wave: {wave}\n")
        game_results.write(f"Level: {level}\n")
        game_results.write(f"Time elapsed: {time_elapsed:.2f}s\n\n")


def display_previous_runs():
    pass


## Main


def main():
    ## Initialisation

    pygame.init()

    ## Initial pygame objects and func calling
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Survoids")

    pygame.mouse.set_visible(False)

    ## Variables
    previous_game_state = "main_screen"
    game_state = "main_screen"

    score = 0

    wave_value = 10
    wave = 0
    wave_delay = 0

    time_elapsed = 0
    paused_time = 0
    start_pause_time = 0

    ## Groups

    all_sprites = pygame.sprite.LayeredUpdates()

    player_bullet_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    enemy_bullet_sprites = pygame.sprite.Group()
    hitmarker_sprites = pygame.sprite.Group()

    power_sprites = pygame.sprite.Group()
    buff_sprites = pygame.sprite.Group()

    user_interface_sprites = pygame.sprite.Group()
    wave_info_sprites = pygame.sprite.Group()

    text_sprites = pygame.sprite.Group()

    main_screen_sprites = pygame.sprite.Group()
    pause_screen_sprites = pygame.sprite.Group()
    end_screen_sprites = pygame.sprite.Group()

    wave_clear_sprites = pygame.sprite.Group()
    power_up_text_sprites = pygame.sprite.Group()

    volume_meter_sprites = pygame.sprite.Group()

    screen_effect_sprites = pygame.sprite.Group()

    ## Objects

    background = Background()

    mouse = Mouse()

    title_text = Text("Survoids", "kenvector_future", 80, "midtop", (300, 40))

    play_text = Text("PLAY", "kenvector_future", 60, "midtop", (300, 260))

    play_text_effect_1 = Text(
        "PLAY", "kenvector_future", 60, "midtop", (298, 258), (0, 0, 0)
    )

    play_text_effect_2 = Text(
        "PLAY", "kenvector_future", 60, "midtop", (301, 261), (0, 0, 0)
    )

    play_button = UserInterface("button.png", 240, 78, (293, 295), True)

    player = Player()

    thruster = Thruster()

    player_x_ui = UserInterface("x.png", 17, 17, (52, 21))

    player_life_icon = UserInterface("life_ui.png", 33, 26, (21, 20))

    lives_text = Text(str(player.lives), "kenvector_future", 24, "topleft", (68, 8))

    score_text = Text(str(score), "kenvector_future_thin", 36, "topright", (596, 8))

    wave_num_text = Text(
        f"Wave {wave}", "kenvector_future_thin", 30, "midtop", (300, 4)
    )

    wave_bar = VolumeMeter(
        (50, 80),
        len(enemy_sprites),
        500,
        5,
        (0, 120, 200),
        (255, 255, 255),
        obj=None,
        attr="len(enemy_sprites)",
    )

    enemy_x_ui = UserInterface("x.png", 17, 17, (300, 57))

    enemy_icon = UserInterface("enemy_icon.png", 31, 27, (272, 57), True)

    enemy_num_text = Text(
        str(len(enemy_sprites)),
        "kenvector_future",
        24,
        "midleft",
        (316, 57),
        (206, 37, 5),
    )

    pause_screen = ScreenEffect((0, 0, 20), 60)

    pause_text = Text("PAUSED", "kenvector_future", 120, "midtop", (300, 240))

    end_screen = ScreenEffect((0, 0, 10), 60)

    game_over_text = Text("GAME OVER", "kenvector_future", 75, "center", (300, 200))

    retry_button = UserInterface("button.png", 280, 84, (293, 395), True)

    retry_text = Text("RETRY", "kenvector_future", 60, "midtop", (300, 360))

    retry_text_effect_1 = Text(
        "RETRY", "kenvector_future", 60, "midtop", (298, 358), (0, 0, 0)
    )

    retry_text_effect_2 = Text(
        "RETRY", "kenvector_future", 60, "midtop", (301, 361), (0, 0, 0)
    )

    ## Running

    while True:
        clock.tick(FPS)

        ## Events

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == START_GAME:
                remove_main_screen(
                    main_screen_sprites,
                    all_sprites,
                    text_sprites,
                    user_interface_sprites,
                )
                display_player(player, thruster, all_sprites)
                display_user_interface(
                    player_x_ui,
                    player_life_icon,
                    wave_num_text,
                    wave_bar,
                    enemy_icon,
                    enemy_x_ui,
                    enemy_num_text,
                    lives_text,
                    score_text,
                    all_sprites,
                    user_interface_sprites,
                    wave_info_sprites,
                    text_sprites,
                    volume_meter_sprites,
                )
                game_state, previous_game_state = update_game_state(
                    game_state, previous_game_state, "in_game"
                )
                start_game_time = pygame.time.get_ticks() / 1000

            if event.type == IMMUNE_OFF:
                if not player.star_buff_act:
                    player.image = player.NORMAL_IMAGE
                    player.original_image = player.NORMAL_IMAGE
                player.set_vulnerable()

            if event.type == ENEMY_HIT:
                event.bullet.kill()
                event.enemy.hp -= player.damage
                if event.enemy.hp <= 0:
                    enemy_pos = event.enemy.get_pos()
                    hitmarker = Hitmarker(enemy_pos)
                    add_sprite_to_groups(hitmarker, all_sprites, hitmarker_sprites)
                    spawn_buff(
                        event.enemy.buff_spawn_chance,
                        enemy_pos,
                        buff_sprites,
                        all_sprites,
                    )
                    event.enemy.kill()
                    score = update_stats(player, score)
                    score_text.update_words(str(score))
                    enemy_num_text.update_words(str(len(enemy_sprites)))

            if event.type == PLAYER_HIT:
                if (
                    not player.immune and not player.star_buff_act
                ):  # not immune and doesn't have star invulnerability
                    player.lives -= 1
                    lives_text.update_words(str(player.lives))

                    if check_game_over(player.lives):
                        pygame.event.post(pygame.event.Event(GAME_OVER))
                        player.immune = True
                    else:
                        player.image = player.IMMUNE_IMAGE
                        player.original_image = player.IMMUNE_IMAGE

                        player.immune = True

            if event.type == LEVEL_UP:
                if not power_sprites:
                    display_powers(
                        player,
                        all_sprites,
                        power_sprites,
                        text_sprites,
                        power_up_text_sprites,
                    )

            if event.type == LEVEL_UP_COMPLETE:
                lives_text.update_words(str(player.lives))
                kill_sprite_group(power_sprites, power_up_text_sprites)

            if event.type == GAME_OVER:
                game_state, previous_game_state = update_game_state(
                    game_state, previous_game_state, "game_over"
                )
                time_elapsed = (
                    pygame.time.get_ticks() / 1000 - start_game_time - paused_time
                )
                store_game_info(score, player.level, wave, time_elapsed)

                remove_pause_screen(
                    pause_screen_sprites,
                    all_sprites,
                    screen_effect_sprites,
                    text_sprites,
                )

                display_end_screen(
                    end_screen,
                    game_over_text,
                    retry_button,
                    retry_text_effect_1,
                    retry_text,
                    retry_text_effect_2,
                    all_sprites,
                    end_screen_sprites,
                    screen_effect_sprites,
                    text_sprites,
                    user_interface_sprites,
                )

            if event.type == RETRY:
                game_state, previous_game_state = update_game_state(
                    game_state, previous_game_state, "in_game"
                )

                start_game_time = pygame.time.get_ticks() / 1000

                score = 0

                wave_value = 10
                wave = 0
                wave_delay = 0

                time_elapsed = 0
                paused_time = 0

                player.reset()
                lives_text.update_words(str(player.lives))
                score_text.update_words(str(score))

                kill_sprite_group(
                    enemy_sprites,
                    player_bullet_sprites,
                    enemy_bullet_sprites,
                    power_sprites,
                    power_up_text_sprites,
                )

                enemy_num_text.update_words(str(len(enemy_sprites)))

                remove_end_screen(
                    end_screen_sprites,
                    all_sprites,
                    screen_effect_sprites,
                    text_sprites,
                    user_interface_sprites,
                )

                score_text.update_words(str(score))
                enemy_num_text.update_words(str(len(enemy_sprites)))
                wave_num_text.update_words(str(wave))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if game_state == "main_screen":
                        if check_mouse_click(play_button):
                            play_button.change_clicked(True)
                    elif game_state == "game_over":
                        if check_mouse_click(retry_button):
                            retry_button.change_clicked(True)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if game_state == "main_screen":
                        if check_mouse_click(play_button):
                            if play_button.clicked:
                                pygame.event.post(pygame.event.Event(START_GAME))
                        else:
                            play_button.change_clicked(False)
                    if game_state == "game_over":
                        if check_mouse_click(retry_button):
                            if retry_button.clicked:
                                pygame.event.post(pygame.event.Event(RETRY))
                        else:
                            retry_button.change_clicked(False)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_state == "paused":
                        game_state, previous_game_state = update_game_state(
                            game_state, previous_game_state, previous_game_state
                        )
                        remove_pause_screen(
                            pause_screen_sprites,
                            all_sprites,
                            screen_effect_sprites,
                            text_sprites,
                        )
                        paused_time += pygame.time.get_ticks() / 1000 - start_pause_time
                    elif game_state == "in_game":
                        game_state, previous_game_state = update_game_state(
                            game_state, previous_game_state, "paused"
                        )
                        start_pause_time = pygame.time.get_ticks() / 1000
                # test keybinds
                if event.key == pygame.K_4:
                    player.lives = 0
                if event.key == pygame.K_5:
                    player.experience += 30
                if event.key == pygame.K_6:
                    print("game_state:", game_state)
                    print("previous game state:", previous_game_state)
                if event.key == pygame.K_7:
                    pygame.event.post(pygame.event.Event(PLAYER_HIT))
                if event.key == pygame.K_8:
                    reset_game_results()
                if event.key == pygame.K_9:
                    print(player.level)
                if event.key == pygame.K_o:
                    print(player.angle)
                if event.key == pygame.K_m:
                    print("left", player.acceleration_left)
                    print("right", player.acceleration_right)
                    print("up", player.acceleration_up)
                    print("down", player.acceleration_down)
                    print("x", player.x)
                    print("y", player.y)
                if event.key == pygame.K_l:
                    spawn_buff(
                        100,
                        (300.0, 300.0),
                        buff_sprites,
                        all_sprites,
                    )

        ## Main game functions

        match game_state:
            case "main_screen":
                if background not in all_sprites and mouse not in all_sprites:
                    display_background(background, all_sprites)
                    display_mouse(mouse, all_sprites)

                if not main_screen_sprites:
                    display_main_screen(
                        title_text,
                        play_text_effect_1,
                        play_text,
                        play_text_effect_2,
                        play_button,
                        all_sprites,
                        text_sprites,
                        user_interface_sprites,
                        main_screen_sprites,
                    )
                # display main screen with a play button for now can add other stuff later
            case "paused":
                if not pause_screen_sprites:
                    display_pause_screen(
                        pause_screen,
                        pause_text,
                        all_sprites,
                        screen_effect_sprites,
                        text_sprites,
                        pause_screen_sprites,
                    )

                if thruster.visibility:
                    thruster.visibility = False

                rotate_object(player)
            case "in_game":
                point_object_to_object(player, mouse)

                fire_bullet(player, all_sprites, player_bullet_sprites)

                wave_value, wave, wave_delay = spawn_waves(
                    all_sprites,
                    enemy_sprites,
                    text_sprites,
                    wave_clear_sprites,
                    wave_info_sprites,
                    wave_num_text,
                    wave_bar,
                    enemy_num_text,
                    wave,
                    wave_value,
                    wave_delay,
                )

                if pygame.sprite.spritecollideany(
                    player, enemy_sprites, pygame.sprite.collide_rect_ratio(0.8)
                ):
                    pygame.event.post(pygame.event.Event(PLAYER_HIT))

                if pygame.sprite.spritecollideany(
                    player, enemy_bullet_sprites, pygame.sprite.collide_rect_ratio(0.6)
                ):
                    pygame.event.post(pygame.event.Event(PLAYER_HIT))

                player.move()
                player.calc_movement()

                if player.immune:
                    player.check_immunity()

                thruster.update_visibility()

                for enemy in enemy_sprites:
                    enemy.move()
                    enemy.fire(all_sprites, enemy_bullet_sprites)

                for bullet in (
                    enemy_bullet_sprites.sprites() + player_bullet_sprites.sprites()
                ):
                    bullet.move()

                for hitmarker in hitmarker_sprites.sprites():
                    hitmarker.update_time()
                    if hitmarker.check_timeout():
                        hitmarker.kill()

                buff_collision = pygame.sprite.spritecollide(
                    player, buff_sprites, dokill=True
                )

                if buff_collision:
                    for buff in buff_collision:
                        player.apply_buff(type(buff))

                # continue HERE with player colliding with a power up -> power up stuff
            case "game_over":
                rotate_object(player)

                if thruster.visibility:
                    thruster.visibility = False

                for enemy in enemy_sprites:
                    enemy.move()
                    enemy.fire(all_sprites, enemy_bullet_sprites)

                for bullet in (
                    enemy_bullet_sprites.sprites() + player_bullet_sprites.sprites()
                ):
                    bullet.move()

                for hitmarker in hitmarker_sprites.sprites():
                    hitmarker.update_time()
                    if hitmarker.check_timeout():
                        hitmarker.kill()

        for meter in volume_meter_sprites:
            if meter.attr == "len(enemy_sprites)":
                meter.update_current_vol(len(enemy_sprites))
            else:
                meter.update_current_vol()

        for enemy in enemy_sprites:
            point_object_to_object(enemy, player)

            bullet_collision = pygame.sprite.spritecollideany(
                enemy, player_bullet_sprites
            )

            if bullet_collision:
                pygame.event.post(
                    pygame.event.Event(
                        ENEMY_HIT, {"enemy": enemy, "bullet": bullet_collision}
                    )
                )

        ## Updating objects

        all_sprites.update()

        if game_state == "in_game":
            point_object_to_object(player, mouse)

        adjust_thruster(thruster, player)

        ## Drawing objects

        screen.fill((0, 0, 0))

        for entity in all_sprites:
            if isinstance(entity, Text) or isinstance(entity, ScreenEffect):
                screen.blit(entity.surf, entity.rect)
            elif isinstance(entity, VolumeMeter):
                entity.draw(screen)
            else:
                if not (isinstance(entity, Thruster) and not entity.visibility):
                    screen.blit(entity.image, entity.rect)

        pygame.display.flip()


if __name__ == "__main__":
    main()
