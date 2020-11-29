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

HOST = "127.0.0.1"
PORT = 65432

ADDR = (HOST,PORT)
connection_established = False
conn , addr = None, None

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.bind(ADDR)
except socket.error as e:
    print(str(e))
    
sock.listen(1)

def receive_data():
    global turn, grid, player
    while True:
        data = conn.recv(1024).decode()
        data = data.split("-")
        x , y = int(data[0]) , int(data[1])
        if data[2] == "yourturn":
            turn = True
        if data[3]  == "False":
            if data[4] == "None":
                grid.winner = None
            else:
                grid.winner = data[4]
            grid.game_over = True 
        if grid.get_cell_value(x, y) == 0:
            grid.set_cell_value(x, y, "O")

        print(data)



os.environ['SDL_VIDEO_WINDOW_POS'] = "500, 150"

width = 600
height = 600

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic-tac-toe")

# set variables
running = True
player = "X"
turn = True
playing = "True"
grid = Grid()  # making the grid object
clock = pygame.time.Clock() 


def waiting_for_connection():
    global conn, addr, connection_established, grid

    print("Waiting for connection....")
    grid.waiting_for_conn = True
    
    conn , addr = sock.accept() # it will wait for a connection , also blocks any new threads 
    print("Client is connected!!!")

    grid.waiting_for_conn = False
    connection_established = True

    receive_data()

create_thread(waiting_for_connection)

def main() :
    global running, turn, grid, player, playing, clock

    while running: 
        clock.tick(60) # frames i think

        if turn and not(grid.game_over):
            grid.waiting_for_move = False
        elif ((not turn) and not(grid.game_over)):
            grid.waiting_for_move = True
            print("waiting for oppoents turn")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and (not grid.game_over) and connection_established:
                if pygame.mouse.get_pressed()[0]:
                    if turn and not(grid.game_over):

                        pos = pygame.mouse.get_pos()
                        Cell_X, Cell_Y = pos[0]//200, pos[1]//200 #this gets me the cell being clicked

                        grid.get_mouse(Cell_X, Cell_Y, player)
                        if grid.game_over:
                            playing  = "False"
                        #server sending data
                        send_data = "{}-{}-{}-{}-{}".format(Cell_X, Cell_Y, 'yourturn', playing, str(grid.winner)).encode()
                        conn.send(send_data)

                        turn = False

                    # grid.print_grid()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and grid.game_over:                     
                    grid.clear_grid()
                    player = "X"
                    grid.game_over = False
                    playing = "True"

                elif event.key == pygame.K_ESCAPE:
                    running = False
 

        # rgba(116, 185, 255,1.0)
        # (22,32,101)
        grid.draw(win)

        pygame.display.flip()

main()
