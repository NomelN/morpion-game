import tkinter
import random

difficulty = "facile" # Les valeurs possibles : "facile", "moyen", "difficile"

def check_nul():
    global win
    if win:  # Si la partie est déjà terminée, ne rien faire
        return

    count = 0
    for col in range(3):
        for row in range(3):
            current_button = buttons[col][row]
            if current_button['text'] in ['X', 'O']:
                count += 1

    if count == 9:  # Si toutes les cases sont remplies et pas de gagnant
        win = True  # Marque la fin de la partie
        message_label.config(text="Match nul")


def print_winner():
    global win
    if win is False:
        win = True
        message_label.config(text=f"Le joueur {current_player} a gagné la partie.")

def switch_player():
    global current_player
    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"

def check_win(clicked_row, clicked_col):
    # Vérifie les conditions de victoire
    directions = [
        [(i, clicked_row) for i in range(3)],  # Ligne
        [(clicked_col, i) for i in range(3)],  # Colonne
        [(i, i) for i in range(3)],  # Diagonale principale
        [(2 - i, i) for i in range(3)]  # Diagonale inversée
    ]

    for direction in directions:
        if all(buttons[col][row]['text'] == current_player for col, row in direction):
            print_winner()
            return

    # Vérifie si la partie est nulle
    check_nul()



def place_symbol(row, column):
    global vs_ai
    # Empêche toute action si la partie est terminée
    if win:
        return

    clicked_button = buttons[column][row]
    if clicked_button['text'] == "":
        clicked_button.config(text=current_player)

        check_win(row, column)  # Vérifie si ce coup termine la partie
        switch_player()

        # Si on joue contre l'IA et que c'est son tour
        if vs_ai and current_player == "O" and not win:
            ia_move()



def reset_game():
    global win, current_player
    for col in range(3):
        for row in range(3):
            buttons[col][row].config(text="")
    win = False
    current_player = "X"
    message_label.config(text="")

def draw_grid():
    for column in range(3):
        buttons_in_cols = []
        for row in range(3):
            button = tkinter.Button(
                root, font=("Arial", 50),
                width=5, height=2,
                bg="lightblue", fg="black",
                command=lambda r=row, c=column: place_symbol(r, c)
            )
            button.grid(row=row, column=column)
            buttons_in_cols.append(button)
        buttons.append(buttons_in_cols)

def ia_move_facile():
    global win
    if win:
        return

    empty_cells = [
        (row, col) for col in range(3) for row in range(3)
        if buttons[col][row]['text'] == ""
    ]
    if empty_cells:
        row, col = random.choice(empty_cells)
        place_symbol(row, col)

def ia_move_moyen():
    global win
    if win:
        return

    # Vérifie si l'IA peut gagner en un coup
    for col in range(3):
        for row in range(3):
            if buttons[col][row]['text'] == "":
                buttons[col][row]['text'] = "O"
                if evaluate(buttons) == 10:  # L'IA gagne avec ce coup
                    place_symbol(row, col)
                    check_win(row, col)  # Vérifie la victoire
                    return
                buttons[col][row]['text'] = ""

    # Vérifie si l'humain peut gagner en un coup et bloque
    for col in range(3):
        for row in range(3):
            if buttons[col][row]['text'] == "":
                buttons[col][row]['text'] = "X"
                if evaluate(buttons) == -10:  # L'humain gagne avec ce coup
                    buttons[col][row]['text'] = ""  # Nettoie avant de jouer
                    place_symbol(row, col)
                    check_win(row, col)  # Vérifie la victoire (même après blocage)
                    return
                buttons[col][row]['text'] = ""

    # Sinon, joue aléatoirement
    ia_move_facile()


def ia_move_difficile():
    global win
    if win:
        return

    best_score = float('-inf')
    best_move = None

    for col in range(3):
        for row in range(3):
            if buttons[col][row]['text'] == "":
                buttons[col][row]['text'] = "O"
                score = minimax(buttons, 0, False)
                buttons[col][row]['text'] = ""
                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    if best_move:
        row, col = best_move
        place_symbol(row, col)


def ia_move():
    if win:  # Si la partie est déjà terminée
        return

    if difficulty == "facile":
        ia_move_facile()
    elif difficulty == "moyen":
        ia_move_moyen()
    elif difficulty == "difficile":
        ia_move_difficile()


def evaluate(board):
    if any(all(board[i][j]['text'] == "O" for j in range(3)) for i in range(3)) or \
       any(all(board[j][i]['text'] == "O" for j in range(3)) for i in range(3)) or \
       all(board[i][i]['text'] == "O" for i in range(3)) or \
       all(board[i][2 - i]['text'] == "O" for i in range(3)):
        return 10
    
    if any(all(board[i][j]['text'] == "X" for j in range(3)) for i in range(3)) or \
       any(all(board[j][i]['text'] == "X" for j in range(3)) for i in range(3)) or \
       all(board[i][i]['text'] == "X" for i in range(3)) or \
       all(board[i][2 - i]['text'] == "X" for i in range(3)):
        return -10

    return 0

def minimax(board, depth, is_maximizing):
    score = evaluate(board)
    
    # Si quelqu'un a gagné ou match nul
    if score == 10 or score == -10:
        return score - depth if score > 0 else score + depth
    if all(buttons[col][row]['text'] != "" for col in range(3) for row in range(3)):
        return 0

    if is_maximizing:  # Tour de l'ordinateur (O)
        best_score = float('-inf')
        for col in range(3):
            for row in range(3):
                if buttons[col][row]['text'] == "":
                    buttons[col][row]['text'] = "O"
                    score = minimax(board, depth + 1, False)
                    buttons[col][row]['text'] = ""
                    best_score = max(best_score, score)
        return best_score
    else:  # Tour de l'humain (X)
        best_score = float('inf')
        for col in range(3):
            for row in range(3):
                if buttons[col][row]['text'] == "":
                    buttons[col][row]['text'] = "X"
                    score = minimax(board, depth + 1, True)
                    buttons[col][row]['text'] = ""
                    best_score = min(best_score, score)
        return best_score


def toggle_mode():
    global vs_ai
    vs_ai = not vs_ai
    mode_label.config(text="Mode: Contre IA" if vs_ai else "Mode: Joueur vs Joueur")
    reset_game()

def set_difficulty(new_difficulty):
    global difficulty
    difficulty = new_difficulty
    difficulty_label.config(text=f"Difficulté : {new_difficulty.capitalize()}")
    reset_game()


# Stockages
buttons = []
current_player = "X"
win = False
vs_ai = True  # Mode contre IA activé par défaut

# Création de la fenêtre du jeu
root = tkinter.Tk()
root.title("Jeu du morpion")
root.minsize(500, 500)

# Bouton pour réinitialiser le jeu
reset_button = tkinter.Button(root, text="Réinitialiser", command=reset_game)
reset_button.grid(row=4, column=1)

# Label pour indiquer le mode de jeu
mode_label = tkinter.Label(root, text="Mode: Contre IA" if vs_ai else "Mode: Joueur vs Joueur")
mode_label.grid(row=5, column=1)

# Bouton pour changer le mode
toggle_mode_button = tkinter.Button(root, text="Changer de mode", command=toggle_mode)
toggle_mode_button.grid(row=6, column=1)

# Label pour indiquer la difficulté actuelle
difficulty_label = tkinter.Label(root, text=f"Difficulté : {difficulty.capitalize()}")
difficulty_label.grid(row=7, column=0, columnspan=3)

# Label pour afficher les messages (victoire, match nul, etc.)
message_label = tkinter.Label(root, text="", font=("Arial", 14))
message_label.grid(row=8, column=0, columnspan=3)

# Boutons pour changer la difficulté
tkinter.Button(root, text="Facile", bg="green", fg="white", command=lambda: set_difficulty("facile")).grid(row=9, column=0)
tkinter.Button(root, text="Moyen", bg="orange", fg="white", command=lambda: set_difficulty("moyen")).grid(row=9, column=1)
tkinter.Button(root, text="Difficile", bg="red", fg="white", command=lambda: set_difficulty("difficile")).grid(row=9, column=2)

draw_grid()
root.mainloop()

