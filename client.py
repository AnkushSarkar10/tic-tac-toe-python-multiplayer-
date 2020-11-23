import pygame
from grid import Grid
import os

#threading 
import threading

def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True #this makes is so that these thread will auto quit before the code ends running
    thread.start()


#socket
import socket

# HOST = "127.0.0.1"
HOST = "192.168.0.7"
PORT = 65432

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #sock stream is used for TCP protocols
sock.connect((HOST,PORT))

def receive_data():
    global turn, grid, player
    while True:
        data = sock.recv(1024).decode()
        data = data.split("-")
        x , y = int(data[0]) , int(data[1])
        if data[2] == "yourturn":
            turn = True
        if data[3]  == "False":
            grid.winner = "X"
            grid.game_over = True 
        if grid.get_cell_value(x, y) == 0:
            grid.set_cell_value(x, y, "X")

        print(data)


create_thread(receive_data)


os.environ['SDL_VIDEO_WINDOW_POS'] = "500, 150"

width = 600
height = 600

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic-tac-toe")


# set some variables
running = True
player = "O"
grid = Grid()  # making the grid object
turn = False
playing = "True"
clock = pygame.time.Clock()
    
def main() :
    global running, turn, grid, player, playing, clock
     
    while running: 
        clock.tick(60) # frames i think
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:
                if pygame.mouse.get_pressed()[0]:
                    if turn and not(grid.game_over):

                        pos = pygame.mouse.get_pos()
                        Cell_X, Cell_Y = pos[0]//200, pos[1]//200 #this gets me the cell being clicked

                        grid.get_mouse(Cell_X, Cell_Y, player)
                        if grid.game_over:
                            playing  = "False"
                        #client sending data
                        send_data = "{}-{}-{}-{}".format(Cell_X, Cell_Y, 'yourturn', playing).encode()
                        sock.send(send_data)

                        turn = False
                    
                    # grid.print_grid()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and grid.game_over:                     
                    grid.clear_grid()
                    player = "O"
                    grid.game_over = False
                    playing = "True"

                elif event.key == pygame.K_ESCAPE:
                    running = False
 
        
        grid.draw(win)

        pygame.display.flip()

main()