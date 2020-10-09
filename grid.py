import pygame
import os 


# loading the images as python object 
x_img = pygame.image.load(os.path.join("images","the-letter-x.png")) 
o_img = pygame.image.load(os.path.join("images","the-letter-o.png")) 
# resizing images 
x_img = pygame.transform.scale(x_img, (200, 200)) 
o_img = pygame.transform.scale(o_img, (200, 200)) 
   


class Grid:
    def __init__(self):
        self.grid_lines = [((0,200), (600,200)), #first h-line
                        ((0,400), (600,400)),   #second h-line
                        ((200,0), (200,600)),   #first v-line
                        ((400,0), (400,600))]   #second v-line

        self.grid = [[0,0,0]
                    ,[0,0,0]
                    ,[0,0,0]]

    def draw(self, win):
        for line in self.grid_lines:
            pygame.draw.line(win, (255,255,255), line[0], line[1], 2)

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell_value(x,y) == "X":
                    win.blit(x_img, (x*200, y*200))
                elif self.get_cell_value(x,y) == "O":
                    win.blit(o_img, (x*200, y*200))

    def print_grid(self):
        for row in self.grid:
            print(row)

    def get_cell_value(self ,x ,y):
        return self.grid[y][x]

    def set_cell_value(self ,x ,y, value):
        self.grid[y][x] = value

    def get_mouse(self, x, y, player):
        if player == "X":
            self.set_cell_value(x, y, "X")
        elif player == "O":
            self.set_cell_value(x, y, "O")
