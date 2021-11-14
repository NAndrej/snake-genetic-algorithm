from Snake import Snake

class Population:
    def __init__(self, population_size):
        self.snakes = [Snake() for i in range(population_size)]
    
    def exec_snake_functions(self):
        """Exectus each function from the snake unit that is needed in every frame
        """
        for snake in self.snakes:
            snake.move()
            snake.grow()

    def is_dead(self):
        """Returns true if all of the snakes from the current population are dead

        Returns:
            [bool]: [Are all the snakes from this population dead?]
        """
        return all([s.is_dead() for s in self.snakes])