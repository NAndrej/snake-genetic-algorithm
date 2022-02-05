from Snake import Snake
import numpy as np
import random
import pygame
import keras

class Population:
    def __init__(self, population_size, selection_size, single_model):
        self.population_size = population_size
        self.selection_size = selection_size
        self.single_model = single_model
        self.snakes = [Snake(single_model=single_model) for i in range(self.population_size)]
        self.MUTATION_PROBABILITY = 0.1
    
    def exec_snake_functions(self):
        """Executes snake functions that are needed in every frame
        """
        for snake in self.snakes:
            snake.move()
            snake.check_collision()
            snake.grow()
            snake.check_infinite_loop()

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
        children = self.crossover(top_performers)
        children = self.mutate(children)

        fitness_values = self.calculate_fitness()

        self.snakes = []
        for unit in fitness_values[self.selection_size:]:
            unit[1].reset_unit()
            self.snakes.append(unit[1])
            # self.snakes.append(Snake())


        for c in children:
            c.color = pygame.Color(255, 0, 0)
            self.snakes.append(c)

        return self

    def calculate_fitness(self):
        """Returns calculated fitness for the whole population, ascendingly sorted.

        Returns:
            [array]: [(fitness_value, snake) pairs]
        """
        return sorted([(snake.calculate_fitness(), snake) for snake in self.snakes], key=lambda x: x[0])

    def get_strongest_parents(self):
        """Calculates fitness values for each unit in the population, and returns the best ones based on their fitness value

        Returns:
            [Snake[]]: [A list containing the top-performing snakes]
        """
        fitness_values = self.calculate_fitness()
        return [unit[1] for unit in fitness_values[-self.selection_size:]]

    def crossover(self, parents):
        """Executes crossover. The weights of the selected top performers of the current population are being mixed up\
        to generate new more powerful units. 

        Returns:
            [Snake[]]: [A list containing the generated units]
        """
        if self.single_model:
            return parents

        # TODO: Make this on layer level - the crossover should be performed on a layer level independently between layers.
        children = [Snake() for i in range(self.selection_size)]

        for child in children:
            random_parents = random.choices(parents, weights = [i for i in range(1, self.selection_size + 1, 1)], k = 2)
            
            parent1_weights = random_parents[0].brain.get_weights()
            parent2_weights = random_parents[1].brain.get_weights()

            current_child_weights = []

            for i in range(len(parents[0].brain.model.layers)):
                parent1_current_weights = np.array(parent1_weights[i]).flatten().tolist()
                parent2_current_weights = np.array(parent2_weights[i]).flatten().tolist()

                chromosome_length = len(parent1_current_weights)
                random_point_1 = random.randint(0, chromosome_length) 
                random_point_2 = random.randint(random_point_1, chromosome_length)

                current_child_weights.append(np.array(parent1_current_weights[0:random_point_1] + parent2_current_weights[random_point_1:random_point_2] + parent1_current_weights[random_point_2:]))



            # print('PARENT 1 WEIGHTS -----------')
            # print(random_parents[0].brain.get_weights())
            # print('PARENT 2 WEIGHTS -----------')
            # print(random_parents[1].brain.get_weights())
            # print('OLD CHILD WEIGHTS-----------')
            # print(child.brain.get_weights())
            child.brain.set_weights(current_child_weights)
            # print('NEW CHILD WEIGHTS -----------')
            # print(child.brain.get_weights())
            # exit()
        return children

    def mutate(self, children):
        """Executes mutation. A random element is being added to the generated units in order to reach unseen states.

        Args:
            children ([Snake[]]): [Units that will be mutated]

        Returns:
            [Snake[]]: [Mutated units]
        """
        if self.single_model:
            return children

        new_children = []
        for child in children:
            child_weights = child.brain.get_weights()
            mutated_weights = []
            for layer, layer_weights in child_weights.items():
                layer_weights = layer_weights.flatten().tolist()
                new_weights = []
                for weight in layer_weights:
                    if random.random() <= self.MUTATION_PROBABILITY:
                        new_weight = random.uniform(-1, 1)      
                        new_weights.append(new_weight)
                    else:
                        new_weights.append(weight)
                mutated_weights.append(new_weights)

            child.brain.set_weights(mutated_weights)
            new_children.append(child)

        return new_children

    def get_best_unit(self):
        """Returns the current's population best unit coupled with its fitness score

        Returns:
            [tuple]: Tuple (Snake, fitness_score)
        """
        max([snake.calculate_fitness() for snake in population.snakes])