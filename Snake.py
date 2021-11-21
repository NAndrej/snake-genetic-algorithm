import random, math
import numpy as np
from Brain import Brain

class Snake:
    def __init__(self):
        # make sure to change these variables as well if you decide to change the initial window size !!!

        self.frame_size_x = 400
        self.frame_size_y = 400
        self.snake_box_size = 10
        self.snake_head = self.get_initial_snake_head()
        self.snake_body = self.get_initial_snake_body()
        self.food_pos = [random.randrange(1, (self.frame_size_x // self.snake_box_size)) * self.snake_box_size, random.randrange(1, (self.frame_size_y // self.snake_box_size)) * self.snake_box_size]
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.moving = True
        self.change_to = self.direction
        self.brain = Brain(input_size = 8)
        self.score = 0
        self.moves = 0
        self.directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

    def move(self):
        """Moves the snake in the direction based on the output from the Brain.
        """

        prediction = self.brain.get_movement([self.get_state()])
        change_to = self.directions[prediction]

        if self.is_dead():
            return

        # Making sure the snake cannot move in the opposite direction instantaneously
        if change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

        # Moving the snake
        if self.direction == 'UP':
            self.snake_head[1] -= self.snake_box_size
        if self.direction == 'DOWN':
            self.snake_head[1] += self.snake_box_size
        if self.direction == 'LEFT':
            self.snake_head[0] -= self.snake_box_size
        if self.direction == 'RIGHT':
            self.snake_head[0] += self.snake_box_size

        self.moves+=1

    def grow(self):
        """Checks whether the snake ate its apple. If yes, the snake grows accordingly.
        """
        self.snake_body.insert(0, list(self.snake_head))
        if self.snake_head[0] == self.food_pos[0] and self.snake_head[1] == self.food_pos[1]:
            self.score += 1
            self.food_spawn = False
        else:
            self.snake_body.pop()

        # Generate new food position if the previous has been eaten
        if not self.food_spawn:
            self.food_pos = [random.randrange(1, (self.frame_size_x//self.snake_box_size)) * self.snake_box_size, random.randrange(1, (self.frame_size_y//self.snake_box_size)) * self.snake_box_size]
        self.food_spawn = True

    def is_dead(self):
        """Self-explanatory.

        Returns:
            [bool]: [Is this snake dead?]
        """
        return not self.moving
    
    def check_collision(self):
        """Executes the needed checks to see if the snake has collided to the borders or itself.
        """
        if (self.snake_head[0] < 0 or self.snake_head[0] > self.frame_size_x - self.snake_box_size) or (self.snake_head[1] < 0 or self.snake_head[1] > self.frame_size_y - self.snake_box_size):
            self.moving = False
        for block in self.snake_body[1:]:
            if self.snake_head[0] == block[0] and self.snake_head[1] == block[1]:
                self.moving = False

    def calculate_fitness(self):
        """Calculates fitness value for the current snake unit. Gives more attention to apples eaten.

        Returns:
            [int]: [Fitness value]
        """
        return (2**self.score * self.moves)

    def get_apple_relative_position(self):
        """Generates a list that represents where the apple is, relative to the snake direction. This is used for the state

        Returns:
            [array]: [Array of boolean values]
        """
        # apple right
        if self.direction == "UP":
            apple_right = self.food_pos[0] - self.snake_head[0] > 0 
        if self.direction == "DOWN":
            apple_right = self.snake_head[0] - self.food_pos[0] > 0 
        if self.direction == "RIGHT":
            apple_right = self.food_pos[1] - self.snake_head[1] > 0 
        if self.direction == "LEFT":
            apple_right = self.snake_head[1] - self.food_pos[1] > 0 

        # apple left
        if self.direction == "UP":
            apple_left = self.snake_head[0] - self.food_pos[0] > 0 
        if self.direction == "DOWN":
            apple_left = self.food_pos[0] - self.snake_head[0] > 0 
        if self.direction == "RIGHT":
            apple_left = self.snake_head[1] - self.food_pos[1] > 0 
        if self.direction == "LEFT":
            apple_left = self.food_pos[1] - self.snake_head[1] > 0 


        # apple back
        if self.direction == "UP":
            apple_back = self.food_pos[1] - self.snake_head[1] > 0 
        if self.direction == "DOWN":
            apple_back = self.snake_head[1] - self.food_pos[1] > 0 
        if self.direction == "RIGHT":
            apple_back = self.snake_head[0] - self.food_pos[0] > 0 
        if self.direction == "LEFT":
            apple_back = self.food_pos[0] - self.snake_head[0] > 0 

        # apple front
        if self.direction == "UP":
            apple_front = self.snake_head[1] - self.food_pos[0] > 0 
        if self.direction == "DOWN":
            apple_front = self.food_pos[1] - self.snake_head[1] > 0 
        if self.direction == "RIGHT":
            apple_front = self.food_pos[0] - self.snake_head[0] > 0 
        if self.direction == "LEFT":
            apple_front = self.snake_head[0] - self.food_pos[0] > 0 

        return [apple_front, apple_back, apple_right, apple_left]

    def get_state(self):
        """Generates the state for each snake. This is needed as input for the NN model

        Returns:
            [array]: [Represents the current snake state]
        """
        X = []

        distance_right_wall = (self.frame_size_x - self.snake_head[0]) / self.frame_size_x
        distance_left_wall = self.snake_head[0] / self.frame_size_x
        distance_top_wall = self.snake_head[1] / self.frame_size_y
        distance_bottom_wall = (self.frame_size_y - self.snake_head[1]) / self.frame_size_y

        # apple_direction_vector = np.array(self.food_pos)-np.array(self.snake_head[0])
        # snake_direction_vector = np.array(snake_position[0])-np.array(snake_position[1])
        X = [distance_top_wall, distance_right_wall, distance_bottom_wall, distance_left_wall]
        apple_position = self.get_apple_relative_position()
        X = X + apple_position
        return X
    
    def check_infinite_loop(self):
        """Won't allow a snake to enter an infinite loop, they all have expire date
        """
        if self.calculate_fitness() >= 300 * (self.score + 1):
            self.kill()
    
    def kill(self):
        """Kills the current snake
        """
        self.moving = False

    def get_initial_snake_head(self):
        """Gets initial snake head position
        """
        self.snake_head = [self.frame_size_x / 2, self.frame_size_y / 2]

        return self.snake_head
    
    def get_initial_snake_body(self):
        """Gets initial snake body position
        """
        self.snake_body = [
            [self.frame_size_x / 2, self.frame_size_y / 2],
            [(self.frame_size_x / 2) - self.snake_box_size, (self.frame_size_y / 2)],
            [(self.frame_size_x / 2) - 2 * self.snake_box_size, (self.frame_size_y / 2)]
        ]

        return self.snake_body  