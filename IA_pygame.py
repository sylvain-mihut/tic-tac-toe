import pygame
import random
import math 
from math import inf as infinity
import sys 
import os
import time

# Initialisation de Pygame
pygame.font.init()

# Définition de la taille de la fenêtre de jeu
Width, Height = 480, 480
win = pygame.display.set_mode((Width,Height))

# Définition des symboles et de leur taille
cross = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cross.png")), (Width//3, Height//3))
circle = pygame.transform.scale(pygame.image.load(os.path.join("assets", "circle.png")), (Width//3, Height//3))

# Définition de la couleur de fond
bg = (255, 255, 255)

# Définition de la fréquence d'images
clock = pygame.time.Clock()

# Définition des joueurs
AI = +1
human = -1

fps = 60 

# Définition des joueurs
def fill(surface, color):
    w,h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x,y))[3]
            surface.set_at((x,y), pygame.Color(r,g,b,a))


# Fonction pour créer un tableau de jeu vide
def create_board():
    new_board = [[0 for i in range(3)] for j in range(3)]
    return new_board


# Fonction pour vérifier si le joueur a gagné
def check_game(board, player):
    for row in board:
        if row[0] == row[1] == row[2] == player:
            print("player", player, "win")
            return True

    for col in range(len(board)):
        check = []
        for row in board:
            check.append(row[col])
        if check.count(player) == len(check) and check[0] !=0:
            print("player", player, "win")
            
            return True
        
    diag = []

    for index in range (len(board)):
        diag.append(board[index][index])
    if diag.count(player) == len(diag) and diag[0] != 0:
        print("player",player, "win")
        
        return True
    
    diag_2 = []

    for index, rev_index in enumerate(reversed(range(len(board)))):
        diag_2.append(board[index][rev_index])
    if diag_2.count(player) == len(diag_2) and diag_2[0] !=0:
        print("player", player, "win")
        return True
    
    if len(empty_cells(board)) == 0:
        print("égalité")
        return True


# Fonction pour récupérer les cellules vides du tableau
def empty_cells(board):
    empty_cells = []
    for y, row in enumerate(board):
        for x, case in enumerate(row):
            if case == 0:
                empty_cells.append([x,y])
    
    return empty_cells


# Vérifie si la case sélectionnée est valide (vide)
def valid_locations(board, x,y, player):
    if [x,y] in empty_cells(board):
        print("good")
        return True
    else:
        return False
    
# Place le symbole du joueur sur le plateau
def set_locations(board, x,y, player):
    # Place le pion du joueur sur la case (x, y) du plateau.
    # Si l'emplacement est valide, la fonction renvoie True,
    # sinon False.
    if valid_locations(board, x,y, player):
        board[y][x] = player
        return True
    else:
        return False

# Vérifie si le jeu est terminé (si un joueur a gagné ou si le plateau est rempli).
def is_terminal_node(board):
    return check_game(board, +1) or check_game(board, -1)


def evaluate(board):
    # Évalue la qualité du plateau pour l'IA. Renvoie un score
    # positif si l'IA a gagné, un score négatif si l'IA a perdu,
    # et zéro sinon.
    if check_game(board, 1):
        score = 1
    elif check_game(board, -1):
        score = -1
    else:
        score = 0
    return score


def minimax(board, depth, alpha, beta , player):
    # Implémente l'algorithme Minimax pour que l'IA choisisse le
    # meilleur coup à jouer.
    if player == AI:
        best = [-1,-1, -infinity]
    else:
        best = [-1,-1, +infinity]

    # Si on atteint la profondeur maximale ou que le jeu est terminé,
    # on renvoie le score du plateau.
    if depth == 0 or is_terminal_node(board):
        print("end")
        score = evaluate(board)
        return [-1,-1, score]
    
    # Pour chaque case vide, on simule un coup et on appelle récursivement
    # minimax pour chercher la meilleure solution.
    for location in empty_cells(board):
        print(location)
        x,y = location[0], location[1]
        board[y][x] = player
        info = minimax(board, depth-1, alpha, beta, -player)
        board[y][x] = 0
        info[0], info[1] = x,y

        # Si c'est à l'IA de jouer, on choisit le coup qui maximise le score.
        # Sinon, on choisit le coup qui minimise le score.
        if player == AI:
            if info[2] > best[2]:
                best = info            
            alpha = max(alpha, best[2])
            if alpha >= beta:
                break

        else:
            if best[2] > info[2]:
                best = info
            beta = min(beta, best[2])
            if alpha >= beta:
                break
    return best


def ai_turn(board, alpha, beta):
    # Tour de l'IA : elle choisit le meilleur coup à jouer
    # en utilisant l'algorithme Minimax.
    depth = len(empty_cells(board))

    if depth == 0 or is_terminal_node(board):
        return 
    
    # Si le plateau est vide, on joue un coup aléatoire.
    if depth == 9:
        x = random.choice([0,1,2])
        y = random.choice([0,1,2])
    else:
        move = minimax(board, depth, alpha, beta, AI)
        x,y =  move[0], move[1]

    set_locations(board, x,y, AI)


def reset_board(board):
    # Réinitialiser le plateau de jeu en mettant toutes les cases à 0 (vide)
    for x, row in enumerate(board):
        for y in range(len(row)):
            board[y][x] = 0


def draw_board(win):
    # Dessiner les lignes du plateau de jeu
    for i in range(1,3):
        pygame.draw.line(win, (0,0,0), (Width*(i/3), 0), (Width*(i/3), Height), 1)

    for j in range(1,3):
        pygame.draw.line(win, (0,0,0), (0, Width*(j/3)), (Width, Width*(j/3)), 1)


def draw_pieces(win, board):
    # Dessiner les pièces (croix et cercle) sur le plateau de jeu en fonction des valeurs de chaque case
    for x in range(len(board)):
        for y in range(len(board)):
            if board[y][x] == -1:
                win.blit(circle, (x*(Width//3), y*(Width//3)))
            elif board[y][x] == 1:
                win.blit(cross, (x*(Width//3), y*(Width//3)))


def redraw_window(win, board, player, game_over, AI_win, player_win):
    # Redessiner la fenêtre de jeu en fonction des événements en cours
    win.fill(bg)
    draw_board(win)
    draw_pieces(win, board)

    pygame.display.update()


game_board = create_board()


def main():
    global game_board
    AI_win = False
    player_win = False
    no_one = False
    turn = random.choice([-1, 1])
    run = True 
    game_over = False


    while run:
        clock.tick(fps)
        redraw_window(win, game_board, turn, game_over, AI_win, player_win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    # Réinitialiser le plateau de jeu, choisir un nouveau joueur aléatoire pour commencer,
                    # et remettre les variables de victoire à False
                    reset_board(game_board)
                    turn = random.choice([-1,1])
                    game_over = False
                    if AI_win:
                        AI_win = False
                    if player_win:
                        player_win = False
                    if no_one:
                        no_one = False

            if event.type == pygame.MOUSEBUTTONDOWN and turn == human and not game_over:
                print("Yes")
                if pygame.mouse.get_pressed()[0] and turn == human and not game_over:
                    print("Yes 2")

                pos = pygame.mouse.get_pos()
                if turn == human and not game_over:
                    if set_locations(game_board, pos[0]//(Width//3), pos[1]//(Width//3), turn):
                        if check_game(game_board, human):
                            # Si le joueur humain a gagné, marquer la fin du jeu
                            print("Terminé")
                            game_over = True
                        turn = AI

        if turn == AI and not game_over:
            alpha = -infinity
            beta = +infinity
            ai_turn(game_board, alpha, beta)
            if check_game(game_board, AI):
                game_over = True

            turn = human

main()