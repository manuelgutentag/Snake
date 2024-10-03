from pickle import SETITEM

import pygame,sys,random
from pygame.math import Vector2

class Snake():
    def __init__(self):
        self.body = [Vector2(4,9), Vector2(4,10), Vector2(4,11)]
        self.direction = Vector2(0,0)

        self.head_up = pygame.image.load('Grafiken/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Grafiken/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Grafiken/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Grafiken/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Grafiken/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Grafiken/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Grafiken/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Grafiken/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Grafiken/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Grafiken/body_horizontal.png').convert_alpha()

        self.body_br = pygame.image.load('Grafiken/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Grafiken/body_bl.png').convert_alpha()
        self.body_tr = pygame.image.load('Grafiken/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Grafiken/body_tl.png').convert_alpha()

    def draw_snake(self):
        for index,block in enumerate(self.body):
            #rect für die Positionierung erstellen
            snake_rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
            self.update_head_graphics()
            self.update_tail_graphics()

            if index == 0:
                # Kopf abbilden
                screen.blit(self.head, snake_rect)
            elif index == len(self.body) - 1:
                # Schwanz abbilden
                screen.blit(self.tail, snake_rect)
            else:
                next_block = self.body[index + 1] - block  # Vektor des nächsten Blocks minus der momentane Vektor
                prev_block = self.body[index - 1] - block  # Vektor des vorherigen Blocks minus momentaner Vektor

                #print(self.body[index].x, self.body[index].x)
                #print(self.body[index].y, self.body[index].y)
                #print(next_block.x, prev_block.x)
                #print(next_block.y, prev_block.y)
                #print('')
                # gerade Körperteile abbilden
                if next_block.x == -prev_block.x and next_block.y == 0 and prev_block.y == 0:
                    screen.blit(self.body_horizontal, snake_rect)
                elif next_block.x + prev_block.x == 20 or next_block.x + prev_block.x == -20:
                    screen.blit(self.body_horizontal, snake_rect)
                elif next_block.y == -prev_block.y and next_block.x == 0 and prev_block.x == 0:
                    screen.blit(self.body_vertical, snake_rect)
                elif next_block.y + prev_block.y == 20 or next_block.y + prev_block.y == -20:
                    screen.blit(self.body_vertical, snake_rect)

                # gebogene Körperteile abbilden
                if (next_block.y == -1 and prev_block.x == -1) or (next_block.x == -1 and prev_block.y == -1):
                    screen.blit(self.body_tl, snake_rect)
                if (next_block.y == -1 and prev_block.x == 1) or (next_block.x == 1 and prev_block.y == -1):
                    screen.blit(self.body_tr, snake_rect)
                if (next_block.y == 1 and prev_block.x == -1) or (next_block.x == -1 and prev_block.y == 1):
                    screen.blit(self.body_bl, snake_rect)
                if (next_block.y == 1 and prev_block.x == 1) or (next_block.x == 1 and prev_block.y == 1):
                    screen.blit(self.body_br, snake_rect)

    def update_head_graphics(self):
        head_relation = self.body[0] - self.body[1]
        if head_relation == Vector2(0,-1):
            self.head = self.head_up
        elif head_relation == Vector2(0,1):
            self.head = self.head_down
        elif head_relation == Vector2(1,0):
            self.head = self.head_right
        elif head_relation == Vector2(-1,0):
            self.head = self.head_left

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0,1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1):
            self.tail = self.tail_down


    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy

    def grow_snake(self):
        body_copy = self.body
        body_copy.insert(len(self.body), body_copy[len(self.body) - 1])
        self.body = body_copy

    def walls(self):
        #Grenzen in x-Richtung
        if int(self.body[0].x) == -1:
            body_copy = self.body[1:]
            body_copy.insert(0, body_copy[0] + Vector2(19,0))
            self.body = body_copy

        if int(self.body[0].x) == 20:
            body_copy = self.body[1:]
            body_copy.insert(0, body_copy[0] + Vector2(-19, 0))
            self.body = body_copy

        #Grenzen in y-Richtung
        if int(self.body[0].y) == -1:
            body_copy = self.body[1:]
            body_copy.insert(0, body_copy[0] + Vector2(0, 19))
            self.body = body_copy

        if int(self.body[0].y) == 20:
            body_copy = self.body[1:]
            body_copy.insert(0, body_copy[0] + Vector2(0, -19))
            self.body = body_copy

    def selfcollide(self):
        for i in self.body[1:]:
            if self.body[0] == i:
                maingame.game_over()

    def reset(self):
        self.body = [Vector2(4,9), Vector2(4,10), Vector2(4,11)]
        self.direction = Vector2(0,0)
        maingame.flag = True

class Fruit():
    #x und y position der Frucht
    def __init__(self, snake):
        self.snake = snake
        self.apple = pygame.image.load('Grafiken/apple.png').convert_alpha()

        self.x = random.randint(0, cell_count - 1)
        self.y = random.randint(0, cell_count - 1)
        self.pos = Vector2(self.x, self.y)

    #frucht malen
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(self.apple, fruit_rect)

    def randomize(self):
        self.fruit_blocked = True

        while self.fruit_blocked:
            self.x = random.randint(0, cell_count - 1)
            self.y = random.randint(0, cell_count - 1)
            for index, block in enumerate(self.snake.body):
                if self.x == self.snake.body[index].x and self.y == self.snake.body[index].y:
                    break
                elif index == len(self.snake.body) - 1:
                    self.pos = Vector2(self.x, self.y)
                    self.fruit_blocked = False
                    break

class Main():
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit(self.snake)
        self.flag = True

    def update(self):
        self.snake.move_snake()
        self.check_collision_fruit()
        self.check_collisions_snake()

    def draw_elements(self):
        self.draw_board()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        if self.scoreflag:
            self.draw_controls()

    def check_collision_fruit(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.grow_snake()

    def check_collisions_snake(self):
        self.snake.walls()
        self.snake.selfcollide()

    def game_over(self):
        self.snake.reset()

    def draw_board(self):
        board_color_dark = (10,200,0)

        for col in range(cell_count):
            for row in range(cell_count):
                if col%2 == 1 and row%2 == 1:
                    grass_rect_x_uneven = pygame.Rect(row * cell_size, col * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, board_color_dark, grass_rect_x_uneven)
                elif col%2 == 0 and row%2 == 0:
                    grass_rect_x_even = pygame.Rect(row * cell_size, col * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, board_color_dark, grass_rect_x_even)

    def draw_score(self):
        score_text = 'Score:      ' + str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56,74,12))
        score_x = int(cell_size * cell_count - 90)
        score_y = int(40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = self.fruit.apple.get_rect(midright = (score_x + 55, score_y - 5))
        background_rect = pygame.Rect(score_rect.left - 6, apple_rect.top - 2, score_rect.width + 14, apple_rect.height + 4)

        pygame.draw.rect(screen, (116, 230, 51), background_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(self.fruit.apple, apple_rect)
        pygame.draw.rect(screen, (56,74,12), background_rect, 4)

    def draw_controls(self):
        controls_text = 'Use W,A,S,D to move snake'
        controls_surface = game_font.render(controls_text, True, (56,74,12))
        controls_x = int(cell_size * cell_count/2)
        controls_y = int(cell_size * cell_count/2) - 150
        controls_rect = controls_surface.get_rect(center = (controls_x, controls_y))

        screen.blit(controls_surface, controls_rect)


pygame.init()
cell_size = 40
cell_count = 20
screen = pygame.display.set_mode((cell_size*cell_count, cell_size*cell_count))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 45)

screen_update = pygame.USEREVENT
pygame.time.set_timer(screen_update, 150)

maingame = Main()

maingame.scoreflag = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.quit:
            pygame.quit()
            sys.exit()
        if event.type == screen_update:
            maingame.update()
        if event.type == pygame.KEYDOWN:
            maingame.scoreflag = False
            if event.key == pygame.K_w and int(maingame.snake.direction.y) != 1:
                maingame.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_s and int(maingame.snake.direction.y) != -1:
                maingame.snake.direction = Vector2(0,1)
            if event.key == pygame.K_d and int(maingame.snake.direction.x) != -1:
                maingame.snake.direction = Vector2(1,0)
            if event.key == pygame.K_a and int(maingame.snake.direction.x) != 1:
                maingame.snake.direction = Vector2(-1,0)

    screen.fill((116, 230, 51))
    maingame.draw_elements()
    pygame.display.update()
    clock.tick(60)


