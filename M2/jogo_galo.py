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

def get_computer_move(board, computer_player, human_player):
    best_score = float('-inf')
    best_move = None
    available_moves = get_available_moves(board)
    
    # Se for a primeira jogada do computador, escolhe aleatoriamente
    if len(available_moves) == 9:
        return random.choice(available_moves)
    
    for move in available_moves:
        board[move[0]][move[1]] = computer_player
        score = minimax(board, 0, False, computer_player, human_player)
        board[move[0]][move[1]] = " "
        
        if score > best_score:
            best_score = score
            best_move = move
    
    return best_move

def play_game():
    while True:
        print("\nBem-vindo ao Jogo do Galo contra o Computador!")
        print("Use números de 1 a 9 para fazer sua jogada:")
        print("1 | 2 | 3")
        print("---------")
        print("4 | 5 | 6")
        print("---------")
        print("7 | 8 | 9")
        print("\nEscolha seu símbolo:")
        print("1. X (joga primeiro)")
        print("2. O (joga segundo)")
        
        try:
            choice = int(input("Escolha (1-2): "))
            if choice not in [1, 2]:
                print("Por favor, escolha 1 ou 2.")
                continue
                
            human_player = "X" if choice == 1 else "O"
            computer_player = "O" if choice == 1 else "X"
            
            # Initialize empty board
            board = [[" " for _ in range(3)] for _ in range(3)]
            current_player = "X"  # X sempre começa
            
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
                    move = get_computer_move(board, computer_player, human_player)
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
                
        except ValueError:
            print("Por favor, digite um número válido.")
            continue

if __name__ == "__main__":
    play_game() 