import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Tic-Tac-Toe with Minimax AI")

# Global variables
board = [["" for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
current_player = "X"
game_mode = None  # "AI" or "MULTI"

player_symbol = "X"
ai_symbol = "O"


def check_winner(symbol):
    for i in range(3):
        if all(board[i][j] == symbol for j in range(3)):
            return True
        if all(board[j][i] == symbol for j in range(3)):
            return True
    if all(board[i][i] == symbol for i in range(3)):
        return True
    if all(board[i][2 - i] == symbol for i in range(3)):
        return True
    return False


def board_full():
    return all(board[r][c] != "" for r in range(3) for c in range(3))


def minimax(board_state, depth, is_maximizing):
    if check_winner(ai_symbol):
        return 1
    elif check_winner(player_symbol):
        return -1
    elif board_full():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for r in range(3):
            for c in range(3):
                if board_state[r][c] == "":
                    board_state[r][c] = ai_symbol
                    score = minimax(board_state, depth + 1, False)
                    board_state[r][c] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for r in range(3):
            for c in range(3):
                if board_state[r][c] == "":
                    board_state[r][c] = player_symbol
                    score = minimax(board_state, depth + 1, True)
                    board_state[r][c] = ""
                    best_score = min(score, best_score)
        return best_score


def ai_move():
    best_score = -float('inf')
    best_move = None
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                board[r][c] = ai_symbol
                score = minimax(board, 0, False)
                board[r][c] = ""
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
    if best_move:
        row, col = best_move
        board[row][col] = ai_symbol
        buttons[row][col].config(text=ai_symbol, state="disabled")

        if check_winner(ai_symbol):
            game_over("AI (O) wins!")
        elif board_full():
            game_over("It's a tie!")


def on_click(row, col):
    global current_player

    if board[row][col] == "":
        board[row][col] = current_player
        buttons[row][col].config(text=current_player, state="disabled")

        if check_winner(current_player):
            game_over(f"Player {current_player} wins!")
        elif board_full():
            game_over("It's a tie!")
        else:
            if game_mode == "MULTI":
                current_player = "O" if current_player == "X" else "X"
            elif game_mode == "AI":
                root.after(300, ai_move)


def game_over(msg):
    if messagebox.askyesno("Game Over", f"{msg}\n\nPlay Again?"):
        select_mode()
    else:
        root.destroy()


def reset_game():
    global board, current_player
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(text="", state="normal")


def select_mode():
    reset_game()
    mode_win = tk.Toplevel(root)
    mode_win.title("Choose Game Mode")
    mode_win.geometry("300x150")
    mode_win.grab_set()

    tk.Label(mode_win, text="Select Game Mode", font=("Arial", 14)).pack(pady=10)

    def choose_ai():
        global game_mode
        game_mode = "AI"
        mode_win.destroy()

    def choose_multi():
        global game_mode
        game_mode = "MULTI"
        mode_win.destroy()

    btn_ai = tk.Button(mode_win, text="Play vs AI", width=15, command=choose_ai)
    btn_ai.pack(pady=5)

    btn_multi = tk.Button(mode_win, text="Multiplayer", width=15, command=choose_multi)
    btn_multi.pack(pady=5)

    root.wait_window(mode_win)


for r in range(3):
    for c in range(3):
        btn = tk.Button(root, text="", font=("Arial", 40), width=5, height=2,
                        command=lambda row=r, col=c: on_click(row, col))
        btn.grid(row=r, column=c)
        buttons[r][c] = btn

select_mode()
root.mainloop()
