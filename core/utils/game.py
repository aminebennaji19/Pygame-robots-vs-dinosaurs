"""This module contains the implementation for the Robots-vs-Dinosaurs game. """
import logging
import sys
from random import choice, randint
from typing import Any, List, Tuple

import pygame

import core.utils.obstacle as obstacle
from core.utils.dinosaur import Dinosaur, Monster
from core.utils.generic_utils import load_font, load_image
from core.utils.laser import Laser
from core.utils.robot import Robot

pygame.font.init()


class Game:
    """ " This class implements our game."""

    def __init__(
        self,
        screen: pygame.Surface,
        screen_width: int,
        screen_height: int,
        number_of_dinosaur_rows: int,
        number_of_dinosaur_cols: int,
        obstacle_amount: int,
        moving_dinosaurs: int,
    ) -> None:
        """This method initializes our Game class with initial parameters.
        Args:
            screen: our display surface for the game.
            screen_width: the screen width of our simulation space.
            screen_height : the screen height of our simulation space.
            number_of_dinosaur_rows: the number of dinosaurs per row.
            number_of_dinosaur_cols: the number of dinosaurs per column.
            obstacle_amount: the number of obstacles on the simulation screen used
            to hide.
            moving_dinosaurs: a boolean specifying whether the dinosaurs are static
            or moving {0,1,-1}."""
        # Robot setup
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.number_of_dinosaur_rows = number_of_dinosaur_rows
        self.number_of_dinosaur_cols = number_of_dinosaur_cols
        robot_sprite = Robot(
            screen, (self.screen_width / 2, self.screen_height), self.screen_width, 5
        )
        self.robot = pygame.sprite.GroupSingle(robot_sprite)

        # Health and Score System
        self.lives = 3

        self.live_surf = load_image("core/assets/images/robot.png")
        self.live_x_start_position = self.screen_width - (
            self.live_surf.get_size()[0] * 2 + 20
        )
        self.score = 0
        self.font = load_font("core/assets/fonts/Pixeled.ttf", font_size=20)

        # Obstacles Setup
        self.shape = obstacle.shape
        self.bloc_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = obstacle_amount
        self.obstacle_x_positions = [
            num * (self.screen_width / self.obstacle_amount)
            for num in range(self.obstacle_amount)
        ]
        self.create_multiple_obstacles(
            *self.obstacle_x_positions, x_start=self.screen_width / 15, y_start=480
        )

        # Dinosaurs Setup
        self.dinosaurs = pygame.sprite.Group()
        # Dinosaurs distribution
        self.dinosaur_setup(
            rows=self.number_of_dinosaur_rows, cols=self.number_of_dinosaur_cols
        )

        self.dinosaur_lasers = pygame.sprite.Group()

        self.dinosaur_direction = moving_dinosaurs
        # Extra Dinosaur setup
        self.monster_dinosaur = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(40, 80)

    def create_obstacle(self, x_start: float, y_start: float, offset_x: Any) -> int:
        """This method is used to create an obstacle at a specific position.
        Args:
            x_start: the starting position for x.
            y_start: the starting position for y.
            offset_x: the offset of x.
        Returns:
            number_of_created_blocks: the number of created blocks.
        """
        number_of_blocks = 0
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == "x":
                    x = x_start + col_index * self.bloc_size + offset_x
                    y = y_start + row_index * self.bloc_size
                    block = obstacle.Block(self.bloc_size, (241, 79, 80), x, y)
                    number_of_blocks += 1
                    self.blocks.add(block)
        return number_of_blocks

    def create_multiple_obstacles(
        self,
        *offset: Any,
        x_start: float,
        y_start: int,
    ) -> int:
        """This method is used to create multiple obstaclse at specific positions.
        Args:
            offset: A list containing multiple offsets for our obstacles.
            x_start: the starting position for x.
            y_start: the starting position for y.
            offset_x: the offset of x.
        Returns:
            number_of_created_obstacles: the number of created obstacles.
        """
        number_of_obstacles = 0
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)
            number_of_obstacles += 1
        return number_of_obstacles

    def dinosaur_position_checker(self) -> None:
        """This method is used to check the direction for our dinosaurs and define
        their movement."""
        all_dinosaurs = self.dinosaurs.sprites()
        for dinosaur in all_dinosaurs:
            if dinosaur.rect.right >= self.screen_width:
                self.dinosaur_direction = -1
                self.dinosaur_move_down(2)
            elif dinosaur.rect.left <= 0:
                self.dinosaur_direction = 1

    def dinosaur_move_down(self, distance: int) -> None:
        """This method is used to move down dinosaurs and according to a specific distance.
        Args:
            distance: the movement step size for dinosaurs."""

        if self.dinosaurs:

            all_dinosaurs = self.dinosaurs.sprites()
            for dinosaur in all_dinosaurs:
                dinosaur.rect.y += distance

    def dinosaur_setup(
        self,
        rows: int,
        cols: int,
        x_distance: int = 150,
        y_distance: int = 90,
        x_offset: int = 70,
        y_offset: int = 150,
    ) -> Tuple[int, List[Tuple[int, int]]]:
        """This method is used to setup the dinosaurs on the simulation space.
        Args:
            rows: number of rows containing dinosaurs.
            cols: number of columns containing dinosaurs.
            x_distance: the horizontal distance  between dinosaurs.
            y_distance: the vertical distance between dinosaurs.
            x_offset: the horizontal offset  for dinosaurs.
            y_offset: the vertical offset for dinosaurs.
        Returns:
            number_of_created_dinosaurs: the number of created dinosaurs.
            positions: positions of the created dinosaurs."""
        number_of_created_dinosaurs = 0
        positions = []
        for row_index, row in enumerate(range(rows)):

            for col_index, col in enumerate(range(cols)):
                # add size and offset
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                positions.append((x, y))

                if row_index == 0:

                    dinosaur_sprite = Dinosaur(self.screen, "green", x, y)
                elif row_index == 1:
                    dinosaur_sprite = Dinosaur(self.screen, "yellow", x, y)
                else:
                    dinosaur_sprite = Dinosaur(self.screen, "red", x, y)
                self.dinosaurs.add(dinosaur_sprite)
                number_of_created_dinosaurs += 1

        return number_of_created_dinosaurs, positions

    def monster_dinosaur_timer(self) -> None:
        """This method is used to set the timer for the monster dinosaur."""
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.monster_dinosaur.add(
                Monster(self.screen, choice(["right", "left"]), self.screen_width)
            )
            self.extra_spawn_time = randint(400, 800)

    def dinosaur_shoot(self) -> bool:
        """This method is used to shoot laser from a random dinosaur."""
        shoot = False
        if self.dinosaurs.sprites():
            random_dinosaur = choice(self.dinosaurs.sprites())
            laser_sprite = Laser(
                pos=random_dinosaur.rect.center,
                screen_height=self.screen_height,
                speed=6,
                surface_dimensions=(4, 20),
            )
            self.dinosaur_lasers.add(laser_sprite)
            shoot = True
        return shoot

    def collision_checks(self) -> None:
        """This method is used to check the collision between different entities
        (robot, dinosaurs)."""

        # Robot lasers

        if self.robot.sprite.lasers:

            for laser in self.robot.sprite.lasers:
                # Obstacle Collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):

                    laser.kill()

                # Dinosaur Collisions
                dinosaur_hit = pygame.sprite.spritecollide(laser, self.dinosaurs, False)
                if dinosaur_hit:
                    for dinosaur in dinosaur_hit:
                        self.score += dinosaur.value
                        dinosaur.get_damage(50)
                        if dinosaur.current_health == 0:
                            dinosaur_hit = pygame.sprite.spritecollide(
                                laser, self.dinosaurs, True
                            )

                    laser.kill()
                # Monster dinosaur collisions (Monster)
                monster_dinosaur_hit = pygame.sprite.spritecollide(
                    laser, self.monster_dinosaur, False
                )
                if monster_dinosaur_hit:
                    for hit_monster in monster_dinosaur_hit:

                        hit_monster.get_damage(100)
                        laser.kill()

                        if hit_monster.current_health == 0:
                            monster_dinosaur_hit = pygame.sprite.spritecollide(
                                laser, self.monster_dinosaur, True
                            )

                    self.score += 100

        # Dinosaurs lasers
        if self.dinosaur_lasers:
            for laser in self.dinosaur_lasers:
                # Obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):

                    laser.kill()
                # Robot collisions
                robot_hit = pygame.sprite.spritecollide(laser, self.robot, False)
                if robot_hit:
                    for hit in robot_hit:

                        laser.kill()
                        hit.get_damage(50)
                        if hit.current_health == 0:

                            self.lives -= 1
                            hit.current_health = 150
                        if self.lives <= 0:
                            logging.info("GAME OVER!")
                            logging.info(f"Final Score:{self.score}")
                            sys.exit()

        if self.dinosaurs:
            for dinosaur in self.dinosaurs:
                pygame.sprite.spritecollide(dinosaur, self.blocks, True)
                robot_hit = pygame.sprite.spritecollide(dinosaur, self.robot, False)
                if robot_hit:
                    for hit in robot_hit:

                        dinosaur.get_damage(5)
        else:
            logging.info("GAME OVER!")
            logging.info(f"Final Score:{self.score}")

            pygame.quit()
            sys.exit()

    def display_lives(self) -> None:
        """This method  is used to display the remaining lives for the robot."""
        for live in range(self.lives - 1):
            x = self.live_x_start_position + (
                live * (self.live_surf.get_size()[0] + 10)
            )
            self.screen.blit(self.live_surf, (x, 8))

    def display_score(self) -> None:
        """This method is used to display the score for the game."""
        score_surface = self.font.render(f"score: {self.score}", False, "white")
        score_rect = score_surface.get_rect(topleft=(10, -10))
        self.screen.blit(score_surface, score_rect)

    def run(self) -> None:
        """This method is used to run our game."""
        self.dinosaurs.update(self.dinosaur_direction)
        self.dinosaur_position_checker()
        self.dinosaur_lasers.update()
        self.monster_dinosaur_timer()
        self.monster_dinosaur.update()
        self.collision_checks()
        self.robot.update()
        self.robot.sprite.lasers.draw(self.screen)
        self.robot.draw(self.screen)
        self.blocks.draw(self.screen)
        self.dinosaurs.draw(self.screen)
        self.dinosaur_lasers.draw(self.screen)
        self.monster_dinosaur.draw(self.screen)
        self.display_lives()
        self.display_score()
