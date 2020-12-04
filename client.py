import pygame
from grid import Grid
import time
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "500, 150"

width = 600
height = 600

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic-tac-toe")


#threading 
import threading

def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True #this makes is so that these thread will auto quit before the code ends running
    thread.start()


#socket
import socket


HOST = "2.tcp.ngrok.io"
PORT = 17333



# set some variables
running = True
player = "O"
grid = Grid()  # making the grid object
turn = False
playing = "True"
clock = pygame.time.Clock()
time_delta = clock.tick(60)/1000.0


click = False
host_text = ""
port_text = ""

active_host = False
active_port = False

def input_screen():
    global running, clock, host_text, port_text, active_host, active_port

    while running:

        win.fill((9, 132, 227))

        mx, my = pygame.mouse.get_pos()

        button_text = "Submit"
        font = pygame.font.Font("Fonts/Nunito-Black.ttf", 30)
        input_color_active = pygame.Color('lightskyblue3')
        input_color_passive = pygame.Color('gray15')
        button_color = (255, 0, 0)
        
        
    
        click = False

        # rects
        
        button_rect = pygame.Rect(200, 400, 200, 50)
        host_rect = pygame.Rect(200,200, 240, 52)
        port_rect = pygame.Rect(200,300, 240, 52)

        if button_rect.collidepoint((mx, my)):
            if click:
                main()

        # text surfaces
        text_surface_button = font.render(button_text,True,(255,255,255))
        text_surface_host = font.render(host_text,True,(0,0,0))
        text_surface_port = font.render(port_text,True,(0,0,0))

        # cursor
        cursor_color = (211,211,211)
        cursor_host = pygame.Rect((host_rect.x + 5,host_rect.y + 5), (2, host_rect.height - 10))
        cursor_port = pygame.Rect((port_rect.x + 5,port_rect.y + 5), (2, port_rect.height - 10))

        cursor_host.x += text_surface_host.get_width()
        cursor_port.x += text_surface_port.get_width()

        if active_host:
            if time.time() % 1 > 0.5:
                pygame.draw.rect(win, cursor_color, cursor_host)

        if active_port:
            if time.time() % 1 > 0.5:
                pygame.draw.rect(win, cursor_color, cursor_port)
    
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if active_host:
                    if event.key == pygame.K_BACKSPACE:
                        host_text = host_text[0:-1]
                    else:
                        host_text += event.unicode

                    

                
                if active_port:
                    if event.key == pygame.K_BACKSPACE:
                        port_text = port_text[0:-1]
                    else:
                        port_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if host_rect.collidepoint((mx, my)):
                    active_host = True
                else: 
                    active_host = False
                if port_rect.collidepoint((mx, my)):
                    active_port = True
                else:
                    active_port = False

                if event.button == 1:
                    click = True
        
        
        
        # dynamic width
        host_rect.width = max(240, text_surface_host.get_width()+ 20)
        port_rect.width = max(240, text_surface_port.get_width()+ 20)

        

        # drawing all the things here
        pygame.draw.rect(win, button_color, button_rect)
        if active_host:
            pygame.draw.rect(win, input_color_active, host_rect, 3)
        else:
            pygame.draw.rect(win, input_color_passive, host_rect, 3)
        if active_port:
            pygame.draw.rect(win, input_color_active, port_rect, 3)
        else:
            pygame.draw.rect(win, input_color_passive, port_rect, 3)

        win.blit(text_surface_host, (host_rect.x + 5,host_rect.y + 5))
        win.blit(text_surface_port, (port_rect.x + 5, port_rect.y + 5))
        win.blit(text_surface_button, (button_rect.x + 46,button_rect.y + 5))
        

        pygame.display.flip()
        clock.tick(60) 

def main() :
    global running, turn, grid, player, playing, clock, font

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
                if data[4] == "None":
                    grid.winner = None
                else:
                    grid.winner = data[4]
                grid.game_over = True
            if grid.get_cell_value(x, y) == 0:
                grid.set_cell_value(x, y, "X")

            print(data)


    create_thread(receive_data)

    while running: 
        clock.tick(60) # frames i think

        if turn and not(grid.game_over):
            grid.waiting_for_move = False
        elif ((not turn) and not(grid.game_over)):
            grid.waiting_for_move = True

        for event in pygame.event.get():


            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:
                if pygame.mouse.get_pressed()[0]:
                    if turn and not(grid.game_over):
                        

                        pos = pygame.mouse.get_pos()
                        Cell_X, Cell_Y = pos[0]//200, pos[1]//200 #this gets me the cell being clicked
                        if grid.get_cell_value(Cell_X,Cell_Y) == 0:
                            grid.get_mouse(Cell_X, Cell_Y, player)
                            if grid.game_over:
                                playing  = "False"
                            #client sending data
                            send_data = "{}-{}-{}-{}-{}".format(Cell_X, Cell_Y, 'yourturn', playing, str(grid.winner)).encode()
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

input_screen()
