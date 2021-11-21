"""
Snake Eater
Made with PyGame
"""

import pygame, sys, time, random
from Brain import Brain
from Population import Population

# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 25

# Window size
frame_size_x = 400
frame_size_y = 400


# Checks for errors encountered
def initialize_environment():
    check_errors = pygame.init()

    if check_errors[1] > 0:
        print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
        sys.exit(-1)

    global game_window
    global fps_controller
    # Initialise game window
    pygame.display.set_caption('Snake Eater')
    game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

    # FPS (frames per second) controller
    fps_controller = pygame.time.Clock()

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Genetic algorithm variables
number_generations = 100000
population_size = 100
selection_rate = 0.02

# Game Over
def game_over():
    """Shows the game over screen
    """
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('The generation has entirely died', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Score
def show_text(choice, color, font, size, score, generation_number):
    """Shows text on the pygame window

    Args:
        Checks usage in the game loop to get an idea for what to pass as arguments. I don't really know.
    """
    score_font = pygame.font.SysFont(font, size)

    score_surface = score_font.render('Score : ' + str(score), True, color)
    gen_number_surface = score_font.render('Generation : ' + str(generation_number), True, color)

    score_rect = score_surface.get_rect()
    gen_rect = gen_number_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
        gen_rect.midtop = (frame_size_x - 60, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y/1.25)
        gen_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)

    game_window.blit(score_surface, score_rect)
    game_window.blit(gen_number_surface, gen_rect)

    # pygame.display.flip()

population = Population(
   population_size = population_size,
   selection_size = int(selection_rate * population_size)
)
# Main logic
for gen_number in range(number_generations):
    initialize_environment()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        population.exec_snake_functions()

        game_window.fill(black)

        # Draw each snake
        for snake in population.snakes:
            for pos in snake.snake_body:
                pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], snake.snake_box_size, snake.snake_box_size))
            
            # Draw food for each snake
            if not snake.is_dead():
                pygame.draw.rect(game_window, white, pygame.Rect(snake.food_pos[0], snake.food_pos[1], snake.snake_box_size, snake.snake_box_size))

        if population.is_dead():
            population = population.generate_new_population()
            break

        show_text(1, white, 'consolas', 20, max([snake.calculate_fitness() for snake in population.snakes]), gen_number)
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(difficulty)