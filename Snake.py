import random

class Snake:
    def __init__(self):
        self.frame_size_x = 400
        self.frame_size_y = 400
        self.snake_box_size = 10
        self.snake_head = [self.frame_size_x / 2, self.frame_size_y / 2]
        self.snake_body = [
            [self.frame_size_x / 2, self.frame_size_y / 2],
            [(self.frame_size_x / 2) - self.snake_box_size, (self.frame_size_y / 2)],
            [(self.frame_size_x / 2) - 2 * self.snake_box_size, (self.frame_size_y / 2)]
        ]
        self.food_pos = [random.randrange(1, (self.frame_size_x//self.snake_box_size)) * self.snake_box_size, random.randrange(1, (self.frame_size_y//self.snake_box_size)) * self.snake_box_size]
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0

    def move(self):
        """Moves the snake in the direction based on the output from the Brain.
        """
        change_to = random.choice(['UP', 'DOWN', 'LEFT', 'DOWN'])

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
        """Checks whether the snake is dead or not.

        Returns:
            bool: [Is this snake dead?]
        """
        if (self.snake_head[0] < 0 or self.snake_head[0] > self.frame_size_x - self.snake_box_size) or (self.snake_head[1] < 0 or self.snake_head[1] > self.frame_size_y - self.snake_box_size):
            return True
        for block in self.snake_body[1:]:
            if self.snake_head[0] == block[0] and self.snake_head[1] == block[1]:
                return True
            
