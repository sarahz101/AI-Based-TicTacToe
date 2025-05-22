#core logic of tic-tac-toe
def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]
    return None

def is_full(board):
    return all(cell != ' ' for row in board for cell in row)

#minimax algorithm
def minimax(board, is_maximizing):
    winner = check_winner(board)
    if winner == 'X': return 1
    if winner == 'O': return -1
    if is_full(board): return 0

    best = -float('inf') if is_maximizing else float('inf')

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'X' if is_maximizing else 'O'
                score = minimax(board, not is_maximizing)
                board[i][j] = ' '
                best = max(best, score) if is_maximizing else min(best, score)
    return best

def best_move_minimax(board):
    best_score = -float('inf')
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                score = minimax(board, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

#alpha-beta pruning algorithm optimization
def alpha_beta(board, is_maximizing, alpha, beta):
    winner = check_winner(board)
    if winner == 'X': return 1
    if winner == 'O': return -1
    if is_full(board): return 0

    if is_maximizing:
        max_eval = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = alpha_beta(board, False, alpha, beta)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = alpha_beta(board, True, alpha, beta)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def best_move_alpha_beta(board):
    best_score = -float('inf')
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                score = alpha_beta(board, False, -float('inf'), float('inf'))
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

#gameplay and comparison
import time

def play_ai(ai_func, label):
    board = [[' ' for _ in range(3)] for _ in range(3)]
    turn = 'X'

    print(f"\n--- Playing with {label} ---")
    start = time.time()
    while not check_winner(board) and not is_full(board):
        print_board(board)
        if turn == 'X':
            i, j = ai_func(board)
        else:
            empty = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ' ']
            i, j = empty[0]
        board[i][j] = turn
        turn = 'O' if turn == 'X' else 'X'
    print_board(board)
    print("Winner:", check_winner(board) or "Draw")
    print("Time:", round(time.time() - start, 4), "seconds")

play_ai(best_move_minimax, "Minimax")
play_ai(best_move_alpha_beta, "Alpha-Beta Pruning")
