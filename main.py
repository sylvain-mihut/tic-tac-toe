import tkinter as tk
from tkinter import messagebox

# Fonction pour jouer un tour
def play(row, col):
    global current_player
    # Vérifier si la case est vide
    if buttons[row][col]["text"] == "":
        # Marquer la case avec le symbole du joueur courant
        buttons[row][col]["text"] = current_player
        # Vérifier si le joueur courant a gagné
        if check_win():
            messagebox.showinfo("Morpion", f"Le joueur {current_player} a gagné !")
            root.destroy() # Fermer la fenêtre
        # Vérifier si le jeu est un match nul
        elif check_draw():
            messagebox.showinfo("Morpion", "Match nul !")
            root.destroy() # Fermer la fenêtre
        else:
            # Passer le tour au prochain joueur
            if current_player == "X":
                current_player = "O"
            else:
                current_player = "X"

# Fonction pour vérifier si un joueur a gagné
def check_win():
    # Vérifier si un joueur a gagné en parcourant toutes les cases du jeu
    for i in range(3):
        # Vérifier si les trois cases d'une ligne sont occupées par le même joueur
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            return True
    for j in range(3):
        # Vérifier si les trois cases d'une colonne sont occupées par le même joueur
        if buttons[0][j]["text"] == buttons[1][j]["text"] == buttons[2][j]["text"] != "":
            return True
    # Vérifier si les trois cases de la diagonale en haut à gauche vers la diagonale en bas à droite sont occupées par le même joueur
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        return True
    # Vérifier si les trois cases de la diagonale en haut à droite vers la diagonale en bas à gauche sont occupées par le même joueur
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        return True
    # Si aucun joueur n'a gagné, retourner False
    return False

# Fonction pour vérifier si le jeu est un match nul
def check_draw():
    # Vérifier si le jeu est terminé en parcourant toutes les cases du jeu
    for i in range(3):
        for j in range(3):
            # S'il reste au moins une case vide, le jeu n'est pas terminé
            if buttons[i][j]["text"] == "":
                return False
    # Si toutes les cases sont occupées et aucun joueur n'a gagné, le jeu est un match nul
    return True

# Interface graphique
# Création de la fenêtre principale
root = tk.Tk()
# Définition du titre de la fenêtre
root.title("Morpion")

# Création d'un frame pour le placement des boutons
frame = tk.Frame(root)
frame.pack()

# Création de la grille de 3x3 pour les boutons
buttons = []
for i in range(3):
    row = []
    for j in range(3):
        # Création d'un bouton avec le texte vide, une taille et une police spécifiques
        # qui appelle la fonction play avec les arguments row et col lorsqu'il est cliqué
        button = tk.Button(frame, width=10, height=5, font=("Arial", 20, "bold"), command=lambda row=i, col=j: play(row, col))
        # Placement du bouton dans la grille
        button.grid(row=i, column=j)
        row.append(button)
    buttons.append(row)

# Définition du joueur courant
current_player = "X"

# Lancement de la boucle principale de la fenêtre pour l'affichage
root.mainloop()
