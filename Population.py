from Snake import Snake

class Population:
    def __init__(self, population_size):
        self.snakes = [Snake() for i in range(population_size)]
    
    def exec_snake_functions(self):
        for snake in self.snakes:
            snake.move()
            snake.grow()

    def is_dead(self):
        return all([s.is_dead() for s in self.snakes])