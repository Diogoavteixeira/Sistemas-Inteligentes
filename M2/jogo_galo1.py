import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board, player):
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True
    
    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    
    # Check diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2-i] == player for i in range(3)):
        return True
    
    return False

def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

def get_available_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                moves.append((i, j))
    return moves

def minimax(board, depth, is_maximizing, player, opponent):
    # Base cases
    if check_winner(board, player):
        return 10 - depth
    if check_winner(board, opponent):
        return depth - 10
    if is_board_full(board):
        return 0
    
    if is_maximizing:
        best_score = float('-inf')
        for move in get_available_moves(board):
            board[move[0]][move[1]] = player
            score = minimax(board, depth + 1, False, player, opponent)
            board[move[0]][move[1]] = " "
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for move in get_available_moves(board):
            board[move[0]][move[1]] = opponent
            score = minimax(board, depth + 1, True, player, opponent)
            board[move[0]][move[1]] = " "
            best_score = min(score, best_score)
        return best_score

def alpha_beta(board, depth, is_maximizing, player, opponent, alpha, beta):
    # Base cases
    if check_winner(board, player):
        return 10 - depth
    if check_winner(board, opponent):
        return depth - 10
    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for move in get_available_moves(board):
            board[move[0]][move[1]] = player
            score = alpha_beta(board, depth + 1, False, player, opponent, alpha, beta)
            board[move[0]][move[1]] = " "
            best_score = max(score, best_score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = float('inf')
        for move in get_available_moves(board):
            board[move[0]][move[1]] = opponent
            score = alpha_beta(board, depth + 1, True, player, opponent, alpha, beta)
            board[move[0]][move[1]] = " "
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_score

def get_computer_move(board, computer_player, human_player, use_alpha_beta=False):
    best_score = float('-inf')
    best_move = None
    available_moves = get_available_moves(board)

    # Se for a primeira jogada do computador, escolhe aleatoriamente
    if len(available_moves) == 9:
        return random.choice(available_moves)

    for move in available_moves:
        board[move[0]][move[1]] = computer_player
        if use_alpha_beta:
            score = alpha_beta(board, 0, False, computer_player, human_player, float('-inf'), float('inf'))
        else:
            score = minimax(board, 0, False, computer_player, human_player)
        board[move[0]][move[1]] = " "

        if score > best_score:
            best_score = score
            best_move = move

    return best_move

def play_computer_vs_computer():
    print("\nModo: Computador vs Computador")
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    computer_x = "X"
    computer_o = "O"

    while True:
        print_board(board)
        print(f"Vez do computador ({current_player})")

        if current_player == computer_x:
            move = get_computer_move(board, computer_x, computer_o, use_alpha_beta=False)
        else:
            move = get_computer_move(board, computer_o, computer_x, use_alpha_beta=True)

        board[move[0]][move[1]] = current_player
        print(f"Computador ({current_player}) escolheu a posição {move[0] * 3 + move[1] + 1}")

        if check_winner(board, current_player):
            print_board(board)
            print(f"\nO computador ({current_player}) venceu!")
            break

        if is_board_full(board):
            print_board(board)
            print("\nEmpate! O jogo acabou.")
            break

        current_player = "O" if current_player == "X" else "X"

def play_game():
    while True:
        print("\nBem-vindo ao Jogo do Galo!")
        print("1. Jogar contra o computador")
        print("2. Computador vs Computador (opcional)")
        print("3. Sair")

        try:
            mode = int(input("Escolha o modo (1-3): "))
            if mode == 1:
                print("\nEscolha o algoritmo para o computador:")
                print("1. Minimax")
                print("2. Alpha-Beta")
                algo_choice = int(input("Escolha (1-2): "))
                if algo_choice not in [1, 2]:
                    print("Escolha inválida. A usar Minimax por padrão.")
                    algo_choice = 1

                human_player = "X"
                computer_player = "O"
                board = [[" " for _ in range(3)] for _ in range(3)]
                current_player = "X"

                while True:
                    print_board(board)

                    if current_player == human_player:
                        print(f"Sua vez! Você é {human_player}")
                        try:
                            move = input("Digite o número da posição (1-9) ou 'q' para sair: ").lower()

                            if move == 'q':
                                print("\nJogo encerrado pelo jogador!")
                                return

                            move = int(move) - 1
                            if move < 0 or move > 8:
                                print("Por favor, escolha um número entre 1 e 9.")
                                continue

                            row = move // 3
                            col = move % 3

                            if board[row][col] != " ":
                                print("Esta posição já está ocupada. Tente outra.")
                                continue

                            board[row][col] = current_player
                        except ValueError:
                            print("Por favor, digite um número válido ou 'q' para sair.")
                            continue
                    else:
                        print(f"Vez do computador ({computer_player})")
                        move = get_computer_move(board, computer_player, human_player, use_alpha_beta=(algo_choice == 2))
                        board[move[0]][move[1]] = current_player
                        print(f"Computador escolheu a posição {move[0] * 3 + move[1] + 1}")

                    if check_winner(board, current_player):
                        print_board(board)
                        if current_player == human_player:
                            print("\nParabéns! Você venceu!")
                        else:
                            print("\nO computador venceu!")
                        break

                    if is_board_full(board):
                        print_board(board)
                        print("\nEmpate! O jogo acabou.")
                        break

                    current_player = "O" if current_player == "X" else "X"

                play_again = input("\nDeseja jogar novamente? (s/n): ").lower()
                if play_again != 's':
                    print("\nObrigado por jogar!")
                    return

            elif mode == 2:
                play_computer_vs_computer()

            elif mode == 3:
                print("\nObrigado por jogar!")
                return

            else:
                print("Escolha inválida. Tente novamente.")
        except ValueError:
            print("Por favor, digite um número válido.")
            continue

if __name__ == "__main__":
    play_game()