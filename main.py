import tkinter
import random

def check_nul():
    if win is False:
        count = 0
        for col in range(3):
            for row in range(3):
                current_button = buttons[col][row]
                if current_button['text'] in ['X', 'O']:
                    count += 1
        if count == 9:
            print("Match nul")

def print_winner():
    global win
    if win is False:
        win = True
        print(f"Le joueur {current_player} a gagné la partie.")

def switch_player():
    global current_player
    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"

def check_win(clicked_row, clicked_col):
    # Détection victoire horizontale
    count = sum(buttons[i][clicked_row]['text'] == current_player for i in range(3))
    if count == 3: print_winner()

    # Détection victoire verticale
    count = sum(buttons[clicked_col][i]['text'] == current_player for i in range(3))
    if count == 3: print_winner()

    # Détection victoire diagonale
    count = sum(buttons[i][i]['text'] == current_player for i in range(3))
    if count == 3: print_winner()

    # Détection victoire diagonale inversée
    count = sum(buttons[2 - i][i]['text'] == current_player for i in range(3))
    if count == 3: print_winner()

    check_nul()

def place_symbol(row, column):
    global vs_ai
    clicked_button = buttons[column][row]
    if clicked_button['text'] == "":
        clicked_button.config(text=current_player)

        check_win(row, column)
        switch_player()

        # Si on joue contre l'IA et que c'est son tour
        if vs_ai and current_player == "O" and not win:
            ia_move_advanced()

def reset_game():
    global win, current_player
    for col in range(3):
        for row in range(3):
            buttons[col][row].config(text="")
    win = False
    current_player = "X"

def draw_grid():
    for column in range(3):
        buttons_in_cols = []
        for row in range(3):
            button = tkinter.Button(
                root, font=("Arial", 50),
                width=5, height=2,
                command=lambda r=row, c=column: place_symbol(r, c)
            )
            button.grid(row=row, column=column)
            buttons_in_cols.append(button)
        buttons.append(buttons_in_cols)

def ia_move():
    global win
    if win:  # Si le jeu est terminé, l'IA ne joue pas
        return
    empty_cells = [
        (row, col) for col in range(3) for row in range(3)
        if buttons[col][row]['text'] == ""
    ]
    if empty_cells:
        row, col = random.choice(empty_cells)
        place_symbol(row, col)

def evaluate(board):
    # Vérifie si l'ordinateur gagne
    if any(all(buttons[i][j]['text'] == "O" for j in range(3)) for i in range(3)) or \
       any(all(buttons[j][i]['text'] == "O" for j in range(3)) for i in range(3)) or \
       all(buttons[i][i]['text'] == "O" for i in range(3)) or \
       all(buttons[i][2 - i]['text'] == "O" for i in range(3)):
        return 10
    
    # Vérifie si l'humain gagne
    if any(all(buttons[i][j]['text'] == "X" for j in range(3)) for i in range(3)) or \
       any(all(buttons[j][i]['text'] == "X" for j in range(3)) for i in range(3)) or \
       all(buttons[i][i]['text'] == "X" for i in range(3)) or \
       all(buttons[i][2 - i]['text'] == "X" for i in range(3)):
        return -10

    # Aucun gagnant
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

def ia_move_advanced():
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


def toggle_mode():
    global vs_ai
    vs_ai = not vs_ai
    mode_label.config(text="Mode: Contre IA" if vs_ai else "Mode: Joueur vs Joueur")
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

reset_button = tkinter.Button(root, text="Réinitialiser", command=reset_game)
reset_button.grid(row=3, column=1)

mode_label = tkinter.Label(root, text="Mode: Contre IA" if vs_ai else "Mode: Joueur vs Joueur")
mode_label.grid(row=4, column=1)

toggle_mode_button = tkinter.Button(root, text="Changer de mode", command=toggle_mode)
toggle_mode_button.grid(row=5, column=1)

draw_grid()
root.mainloop()
