import time
import random
import pygame
from sys import exit

from game_board import board_class, move_class
from minimaxbot import get_move_by_bot

pygame.init()
screen = pygame.display.set_mode((900,750))
pygame.display.set_caption("Baghchal")
clock = pygame.time.Clock()
test_font = pygame.font.Font('./font/Jetbrainsmono.ttf',23)
test_font2 = pygame.font.Font('./font/Jetbrainsmono.ttf',20)
bg_surface = pygame.Surface((900,750))
bg_surface.fill('white')

board_surface = pygame.image.load('pics/board.png') 
tiger_surface = pygame.transform.smoothscale(pygame.image.load('pics/TP.png').convert_alpha(),(50,50))
goat_surface = pygame.transform.smoothscale(pygame.image.load('pics/GP.png').convert_alpha(),(50,50))

def show_board(board:board_class, selected):
    if selected : pygame.draw.ellipse(screen, 'lightgreen', (27+160*selected[-1], 27+160*selected[0], 56, 56),width=3)
    for i in range(5) :
        for j in range(5) :
            if board.board_details[i][j]==1 : screen.blit(tiger_surface, (30+160*j,30+160*i))
            elif board.board_details[i][j]==-1 : screen.blit(goat_surface, (30+160*j,30+160*i))


def select_piece(board:board_class, position):
    for i in range(5) :
        for j in range(5) :
            if board.turn ==-1 and board.board_details[i][j]==-1 and pygame.Rect(30+160*j,30+160*i,50,50).collidepoint(position) : return (i,j)
            if board.turn ==1 and board.board_details[i][j]==1 and pygame.Rect(30+160*j,30+160*i,50,50).collidepoint(position) : return (i,j)
    return None


def get_move(board:board_class, position, selected) :
    available_moves = board.get_possible_moves()
    mv: move_class
    for mv in available_moves['P']:
        if pygame.Rect(30+160*mv.final_pos[-1],30+160*mv.final_pos[0],50,50).collidepoint(position) : return mv
    for mv in available_moves['M']:
        if selected==mv.initial_pos and pygame.Rect(30+160*mv.final_pos[-1],30+160*mv.final_pos[0],50,50).collidepoint(position) : return mv
    for mv in available_moves['C']:
        if selected==mv.initial_pos and pygame.Rect(30+160*mv.final_pos[-1],30+160*mv.final_pos[0],50,50).collidepoint(position) : return mv
    return None


new_game_surface = test_font.render('New Game',False,(64,64,64))
new_game_rect = new_game_surface.get_rect(center = (800, 450))
new_game = True
undo_move_surface= test_font.render('Undo Move',False,(64,64,64))
undo_move_rect= undo_move_surface.get_rect(center = (800, 350))
while True :
    for event in pygame.event.get():
        if event.type == pygame.QUIT : 
            pygame.quit()
            exit()

    if pygame.mouse.get_pressed()[0] : 
        mouse_pre_pos = pygame.mouse.get_pos()
        time.sleep(0.2) 
    else : mouse_pre_pos = None

    if new_game:
        player= None
        two_players= None
        screen.blit(bg_surface,(0,0))
        screen.blit(test_font.render('Choose Side',False,(64,64,64)),(350,100))
        if pygame.Rect(250,250,150,150).collidepoint(pygame.mouse.get_pos()) : pygame.draw.ellipse(screen,'lightgreen',(250,250,150,150))
        if pygame.Rect(450,250,150,150).collidepoint(pygame.mouse.get_pos()) : pygame.draw.ellipse(screen,'lightgreen',(450,250,150,150))
        if pygame.Rect(385,445,95,40).collidepoint(pygame.mouse.get_pos()) : pygame.draw.ellipse(screen,'lightgreen',(385,445,115,40))
        if pygame.Rect(390,495,135,40).collidepoint(pygame.mouse.get_pos()) : pygame.draw.ellipse(screen,'lightgreen',(370,495,160,40))
        screen.blit(pygame.transform.smoothscale(pygame.image.load('pics/TP.png').convert_alpha(),(150,150)),(250,250))
        screen.blit(pygame.transform.smoothscale(pygame.image.load('pics/GP.png').convert_alpha(),(150,150)),(450,250))
        screen.blit(test_font2.render('Random',False,(64,64,64)),(400,450))
        screen.blit(test_font2.render('Two Players',False,(64,64,64)),(380,500))
        if mouse_pre_pos and pygame.Rect(250,250,150,150).collidepoint(mouse_pre_pos) : player = 1
        if mouse_pre_pos and pygame.Rect(450,250,150,150).collidepoint(mouse_pre_pos) : player = -1
        if mouse_pre_pos and pygame.Rect(385,445,95,30).collidepoint(mouse_pre_pos) : player = random.choice([-1,1]) 
        if mouse_pre_pos and pygame.Rect(390,500,135,30).collidepoint(mouse_pre_pos) : two_players = True
        board= board_class()
        winner = None
        mouse_pre_pos = None
        selected = None
        if two_players or player : new_game = False

    elif not winner:
        move= None
        if mouse_pre_pos and (board.turn == player or two_players) :
            if not selected : selected = select_piece(board, mouse_pre_pos)
            elif pygame.Rect(30+160*selected[1],30+160*selected[0],50,50).collidepoint(mouse_pre_pos) : selected= None
            move = get_move(board, mouse_pre_pos, selected)
        elif board.turn!=player and not two_players:
            move= get_move_by_bot(board)
        if move:
            board.update_board(move)
            winner = board.check_winner()
            selected = None

    if not new_game :
        screen.blit(bg_surface,(0,0))
        screen.blit(board_surface,(50,50))
        screen.blit(test_font2.render('You are',False,(64,64,64)),(760,20))
        screen.blit(tiger_surface if player==1 else goat_surface,(780,50))
        show_board(board, selected)
        if undo_move_rect.collidepoint(pygame.mouse.get_pos()) : pygame.draw.rect(screen,'lightgreen',undo_move_rect)
        screen.blit(undo_move_surface, undo_move_rect)
        if mouse_pre_pos and undo_move_rect.collidepoint(mouse_pre_pos) :
            board.undo_last_move()
            board.undo_last_move()
            winner= None
            selected= None
        if winner:
            screen.blit(test_font2.render('Winner',False,(64,64,64)),(760,220))
            screen.blit(tiger_surface if winner=='T' else goat_surface,(780,250))
            if new_game_rect.collidepoint(pygame.mouse.get_pos()) : pygame.draw.rect(screen,'lightgreen',new_game_rect)
            screen.blit(new_game_surface, new_game_rect)
            if mouse_pre_pos and new_game_rect.collidepoint(mouse_pre_pos) : new_game = True

    pygame.display.update()
    clock.tick(60)
