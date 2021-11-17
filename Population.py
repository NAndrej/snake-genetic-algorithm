from Snake import Snake

class Population:
    def __init__(self, population_size, selection_size):
        self.population_size = population_size
        self.selection_size = selection_size
        self.snakes = [Snake() for i in range(self.population_size)]
    
    def exec_snake_functions(self):
        """Executes snake functions that are needed in every frame
        """
        for snake in self.snakes:
            snake.move()
            snake.check_collision()
            snake.grow()

    def is_dead(self):
        """Returns true if all of the snakes from the current population are dead

        Returns:
            [bool]: [Are all the snakes from this population dead?]
        """
        return all([s.is_dead() for s in self.snakes])

    def generate_new_population(self):
        """Executes all the needed utilities in order to create a new population out of the current one

        Returns:
            [Population]: [A brand new involved population]
        """
        top_performers = self.get_strongest_parents()

        # TODO: Change this to the new generated snakes
        # self.snakes = [Snake() for i in range(self.population_size)]
        return self

    def get_strongest_parents(self):
        """Calculates fitness values for each unit in the population, and returns the best ones based on their fitness value

        Returns:
            [Snake[]]: [A list containing the top-performing snakes]
        """
        fitness_values = sorted([(snake.calculate_fitness(), snake) for snake in self.snakes], key=lambda x: x[0])
        return [unit[1] for unit in fitness_values[-self.selection_size:]]