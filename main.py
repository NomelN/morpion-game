import tkinter


def check_nul():
    if win is False:
        count = 0
        for col in range(3):
            for row in range(3):
                current_button = buttons[col][row]
                if current_button['text'] == 'X' or current_button['text'] == 'O':
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
    # detection victoire horizontale
    count = 0
    for i in range(3):
        current_button = buttons[i][clicked_row]

        if current_button['text'] == current_player:
            count += 1

    if count == 3:
        print_winner()

    # detection victoire verticale
    count = 0
    for i in range(3):
        current_button = buttons[clicked_col][i]

        if current_button['text'] == current_player:
            count += 1
    if count == 3:
        print_winner()

    # detection victoire diagonale
    count = 0
    for i in range(3):
        current_button = buttons[i][i]

        if current_button['text'] == current_player:
            count += 1
    if count == 3:
        print_winner()

    # detection victoire diagonale inversée
    count = 0
    for i in range(3):
        current_button = buttons[2-i][i]

        if current_button['text'] == current_player:
            count += 1
    if count == 3:
        print_winner()
    check_nul()


def place_symbol(row, column):
    clicked_button = buttons[column][row]
    if clicked_button['text'] == "":
        clicked_button.config(text=current_player)

        check_win(row, column)
        switch_player()


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
                command=lambda r=row, c=column: place_symbol(r, c)  # utilisé ici pour sauvegarder l'état de selection
            )
            button.grid(row=row, column=column)
            buttons_in_cols.append(button)
        buttons.append(buttons_in_cols)


# stockages
buttons = []
current_player = "X"
win = False

# création de la fenêtre du jeu
root = tkinter.Tk()

# personnalisation de la fenetre
root.title("Jeu du morpion")
root.minsize(500, 500)

reset_button = tkinter.Button(root, text="Réinitialiser", command=reset_game)
reset_button.grid(row=3, column=1)

draw_grid()

root.mainloop()
