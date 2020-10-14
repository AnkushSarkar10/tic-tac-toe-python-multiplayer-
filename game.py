import pygame
from grid import Grid
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "500, 150"

width = 600
height = 600

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic-tac-toe")


def main() :    
    running = True
    player = "X"
    grid = Grid()  # making the grid object
    clock = pygame.time.Clock() 

    while running: 
        clock.tick(60) # frames i think
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    cell = (pos[0]//200, pos[1]//200) #this gets me the cell being clicked

                    grid.get_mouse(cell[0], cell[1], player)
                    if grid.switch_player:
                        if player == "X":
                            player = "O"
                        else:
                            player = "X"    
                        
                    grid.print_grid()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and grid.game_over:
                    grid.clear_grid()
                    grid.game_over = False

        win.fill((22,32,101))
        grid.draw(win)

        pygame.display.flip()

main()