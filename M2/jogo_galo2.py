import random
import time
import matplotlib.pyplot as plt
import numpy as np

def print_board(board):
    """Prints the current state of the board"""
    print("-------------")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("-------------")

def check_winner(board, player):
    """Checks if the specified player has won"""
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
    """Checks if the board is full (draw condition)"""
    return all(cell != " " for row in board for cell in row)

def get_available_moves(board):
    """Returns a list of available moves as (row, col) tuples"""
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                moves.append((i, j))
    return moves

def minimax(board, depth, is_maximizing, player, opponent):
    """
    Minimax algorithm implementation
    
    Args:
        board: Current game board
        depth: Current depth in the game tree
        is_maximizing: Whether it's maximizing player's turn
        player: The AI player's symbol
        opponent: The opponent's symbol
        
    Returns:
        Best score for the current board state
    """
    # Base cases: check for terminal states
    if check_winner(board, player):
        return 10 - depth  # Win, higher score for faster wins
    if check_winner(board, opponent):
        return depth - 10  # Loss, higher score for slower losses
    if is_board_full(board):
        return 0  # Draw
    
    # Recursive cases
    if is_maximizing:
        best_score = float('-inf')
        for move in get_available_moves(board):
            board[move[0]][move[1]] = player
            score = minimax(board, depth + 1, False, player, opponent)
            board[move[0]][move[1]] = " "  # Undo move
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for move in get_available_moves(board):
            board[move[0]][move[1]] = opponent
            score = minimax(board, depth + 1, True, player, opponent)
            board[move[0]][move[1]] = " "  # Undo move
            best_score = min(score, best_score)
        return best_score

def alpha_beta(board, depth, is_maximizing, player, opponent, alpha, beta):
    """
    Alpha-Beta pruning algorithm implementation
    
    Args:
        board: Current game board
        depth: Current depth in the game tree
        is_maximizing: Whether it's maximizing player's turn
        player: The AI player's symbol
        opponent: The opponent's symbol
        alpha: Alpha value for pruning
        beta: Beta value for pruning
        
    Returns:
        Best score for the current board state
    """
    # Base cases: check for terminal states
    if check_winner(board, player):
        return 10 - depth
    if check_winner(board, opponent):
        return depth - 10
    if is_board_full(board):
        return 0

    # Recursive cases with alpha-beta pruning
    if is_maximizing:
        best_score = float('-inf')
        for move in get_available_moves(board):
            board[move[0]][move[1]] = player
            score = alpha_beta(board, depth + 1, False, player, opponent, alpha, beta)
            board[move[0]][move[1]] = " "  # Undo move
            best_score = max(score, best_score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break  # Beta cutoff
        return best_score
    else:
        best_score = float('inf')
        for move in get_available_moves(board):
            board[move[0]][move[1]] = opponent
            score = alpha_beta(board, depth + 1, True, player, opponent, alpha, beta)
            board[move[0]][move[1]] = " "  # Undo move
            best_score = min(score, best_score)
            beta = min(beta, score)
            if beta <= alpha:
                break  # Alpha cutoff
        return best_score

def get_computer_move(board, computer, human, use_alpha_beta=False):
    """
    Determines the best move for the computer
    
    Args:
        board: Current game board
        computer: Computer's symbol
        human: Human's symbol
        use_alpha_beta: Whether to use Alpha-Beta pruning
        
    Returns:
        The best move as (row, col) tuple and execution time
    """
    best_score = float('-inf')
    best_move = None
    available_moves = get_available_moves(board)

    # For the first move, choose randomly for efficiency
    if len(available_moves) == 9:
        return random.choice(available_moves), 0.0

    # Measure execution time
    start_time = time.time()
    
    # Evaluate each possible move
    for move in available_moves:
        board[move[0]][move[1]] = computer
        if use_alpha_beta:
            score = alpha_beta(board, 0, False, computer, human, float('-inf'), float('inf'))
        else:
            score = minimax(board, 0, False, computer, human)
        board[move[0]][move[1]] = " "  # Undo move

        if score > best_score:
            best_score = score
            best_move = move
            
    end_time = time.time()
    execution_time = end_time - start_time
    
    return best_move, execution_time

def count_visited_nodes(board, is_maximizing, player, opponent, use_alpha_beta=False, alpha=float('-inf'), beta=float('inf')):
    """
    Counts the number of nodes visited by the algorithm
    
    Args:
        board: Current game board
        is_maximizing: Whether it's maximizing player's turn
        player: The AI player's symbol
        opponent: The opponent's symbol
        use_alpha_beta: Whether to use Alpha-Beta pruning
        alpha: Alpha value for pruning
        beta: Beta value for pruning
        
    Returns:
        Number of nodes visited
    """
    # Base cases: check for terminal states
    if check_winner(board, player) or check_winner(board, opponent) or is_board_full(board):
        return 1  # Terminal node counts as 1
    
    nodes = 1  # Count current node
    
    # Recursive cases
    for move in get_available_moves(board):
        board[move[0]][move[1]] = player if is_maximizing else opponent
        
        if use_alpha_beta:
            next_score = alpha_beta(board, 0, not is_maximizing, player, opponent, alpha, beta)
            if is_maximizing:
                alpha = max(alpha, next_score)
                if beta <= alpha:
                    board[move[0]][move[1]] = " "  # Undo move
                    break  # Pruning
            else:
                beta = min(beta, next_score)
                if beta <= alpha:
                    board[move[0]][move[1]] = " "  # Undo move
                    break  # Pruning
        
        nodes += count_visited_nodes(
            board, 
            not is_maximizing, 
            player, 
            opponent, 
            use_alpha_beta,
            alpha,
            beta
        )
        
        board[move[0]][move[1]] = " "  # Undo move
    
    return nodes

def compare_algorithms_performance():
    """
    Compares the performance of Minimax and Alpha-Beta pruning
    """
    board_sizes = [(i, i) for i in range(3, 5)]  # We'll test with 3x3 and 4x4 boards
    minimax_times = []
    alpha_beta_times = []
    minimax_nodes = []
    alpha_beta_nodes = []
    
    for n, m in board_sizes:
        # Create empty board
        board = [[" " for _ in range(m)] for _ in range(n)]
        
        # Place some random moves to create a mid-game state
        moves = [(i, j) for i in range(n) for j in range(m)]
        random.shuffle(moves)
        for i, move in enumerate(moves[:n]):
            board[move[0]][move[1]] = "X" if i % 2 == 0 else "O"
        
        # Measure Minimax performance
        start_time = time.time()
        _, _ = get_computer_move(board, "X", "O", use_alpha_beta=False)
        minimax_times.append(time.time() - start_time)
        
        # Count nodes for Minimax
        node_count = count_visited_nodes(board, True, "X", "O", use_alpha_beta=False)
        minimax_nodes.append(node_count)
        
        # Measure Alpha-Beta performance
        start_time = time.time()
        _, _ = get_computer_move(board, "X", "O", use_alpha_beta=True)
        alpha_beta_times.append(time.time() - start_time)
        
        # Count nodes for Alpha-Beta
        node_count = count_visited_nodes(board, True, "X", "O", use_alpha_beta=True)
        alpha_beta_nodes.append(node_count)
    
    # Plot the results
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    board_labels = [f"{n}x{m}" for n, m in board_sizes]
    
    ax1.bar(np.arange(len(board_sizes)) - 0.2, minimax_times, width=0.4, label='Minimax')
    ax1.bar(np.arange(len(board_sizes)) + 0.2, alpha_beta_times, width=0.4, label='Alpha-Beta')
    ax1.set_xticks(np.arange(len(board_sizes)))
    ax1.set_xticklabels(board_labels)
    ax1.set_ylabel('Execution Time (seconds)')
    ax1.set_title('Algorithm Execution Time')
    ax1.legend()
    
    ax2.bar(np.arange(len(board_sizes)) - 0.2, minimax_nodes, width=0.4, label='Minimax')
    ax2.bar(np.arange(len(board_sizes)) + 0.2, alpha_beta_nodes, width=0.4, label='Alpha-Beta')
    ax2.set_xticks(np.arange(len(board_sizes)))
    ax2.set_xticklabels(board_labels)
    ax2.set_ylabel('Nodes Visited')
    ax2.set_title('Number of Nodes Visited')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('algorithm_comparison.png')
    plt.show()

def play_human_vs_computer():
    """Game mode: Human vs Computer"""
    print("\nMode: Human vs Computer")
    
    # Choose algorithm
    print("Choose algorithm for the computer:")
    print("1. Minimax")
    print("2. Alpha-Beta")
    algo_choice = input("Choose (1-2): ")
    use_alpha_beta = (algo_choice == "2")
    
    # Choose who goes first
    print("\nWho goes first?")
    print("1. Human")
    print("2. Computer")
    first_choice = input("Choose (1-2): ")
    
    human_player = "X" if first_choice == "1" else "O"
    computer_player = "O" if human_player == "X" else "X"
    current_player = "X"  # X always goes first
    
    # Create empty board
    board = [[" " for _ in range(3)] for _ in range(3)]
    
    # Game loop
    while True:
        print_board(board)
        
        if current_player == human_player:
            # Human's turn
            print(f"Your turn! You are {human_player}")
            try:
                move = input("Enter move position (1-9) or 'q' to quit: ").lower()
                
                if move == 'q':
                    print("\nGame ended by player!")
                    return
                
                move = int(move) - 1
                row, col = move // 3, move % 3
                
                if move < 0 or move > 8:
                    print("Please choose a number between 1 and 9.")
                    continue
                
                if board[row][col] != " ":
                    print("That position is already taken. Try another.")
                    continue
                
                board[row][col] = human_player
                
            except ValueError:
                print("Please enter a valid number or 'q'.")
                continue
                
        else:
            # Computer's turn
            print(f"Computer's turn ({computer_player})")
            move, execution_time = get_computer_move(board, computer_player, human_player, use_alpha_beta)
            board[move[0]][move[1]] = computer_player
            
            algorithm_name = "Alpha-Beta" if use_alpha_beta else "Minimax"
            print(f"Computer chose position {move[0]*3 + move[1] + 1}")
            print(f"Execution time ({algorithm_name}): {execution_time:.6f} seconds")
        
        # Check for winner
        if check_winner(board, current_player):
            print_board(board)
            if current_player == human_player:
                print("\nCongratulations! You won!")
            else:
                print("\nComputer wins!")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("\nIt's a draw!")
            break
        
        # Switch player
        current_player = "O" if current_player == "X" else "X"

def play_computer_vs_computer():
    """Game mode: Computer vs Computer"""
    print("\nMode: Computer vs Computer")
    
    # Create empty board
    board = [[" " for _ in range(3)] for _ in range(3)]
    
    # Computer X uses Minimax, Computer O uses Alpha-Beta
    computer_x = "X"
    computer_o = "O"
    current_player = "X"
    
    # Stats
    minimax_times = []
    alpha_beta_times = []
    
    # Game loop
    while True:
        print_board(board)
        print(f"{current_player}'s turn")
        
        # Get computer move
        if current_player == computer_x:
            move, execution_time = get_computer_move(board, computer_x, computer_o, use_alpha_beta=False)
            minimax_times.append(execution_time)
            algorithm = "Minimax"
        else:
            move, execution_time = get_computer_move(board, computer_o, computer_x, use_alpha_beta=True)
            alpha_beta_times.append(execution_time)
            algorithm = "Alpha-Beta"
        
        board[move[0]][move[1]] = current_player
        
        print(f"Computer {current_player} ({algorithm}) chose position {move[0]*3 + move[1] + 1}")
        print(f"Execution time: {execution_time:.6f} seconds")
        
        # Check for winner
        if check_winner(board, current_player):
            print_board(board)
            print(f"\nComputer {current_player} ({algorithm}) wins!")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("\nIt's a draw!")
            break
        
        # Switch player
        current_player = "O" if current_player == "X" else "X"
    
    # Show performance statistics
    if minimax_times and alpha_beta_times:
        print("\nPerformance Statistics:")
        print(f"Minimax avg time: {sum(minimax_times)/len(minimax_times):.6f} seconds")
        print(f"Alpha-Beta avg time: {sum(alpha_beta_times)/len(alpha_beta_times):.6f} seconds")
        print(f"Alpha-Beta speedup: {sum(minimax_times)/sum(alpha_beta_times):.2f}x")

def visualize_board_exploration():
    """Visualizes how the algorithms explore the game tree"""
    print("\nVisualizing board exploration...")
    
    # Create a sample mid-game board
    board = [
        [" ", "X", "O"],
        ["X", "O", " "],
        [" ", " ", " "]
    ]
    
    print("Sample board:")
    print_board(board)
    
    # Count nodes explored by each algorithm
    minimax_nodes = count_visited_nodes(board, True, "X", "O", use_alpha_beta=False)
    alpha_beta_nodes = count_visited_nodes(board, True, "X", "O", use_alpha_beta=True)
    
    print(f"Minimax explores {minimax_nodes} nodes")
    print(f"Alpha-Beta explores {alpha_beta_nodes} nodes")
    print(f"Alpha-Beta pruning effectiveness: {(1 - alpha_beta_nodes/minimax_nodes)*100:.2f}% reduction")

def main():
    """Main function to run the program"""
    while True:
        print("\nTic-Tac-Toe with AI Algorithms")
        print("1. Play against the computer")
        print("2. Watch computer vs computer")
        print("3. Compare algorithm performance")
        print("4. Visualize board exploration")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ")
        
        if choice == "1":
            play_human_vs_computer()
        elif choice == "2":
            play_computer_vs_computer()
        elif choice == "3":
            compare_algorithms_performance()
        elif choice == "4":
            visualize_board_exploration()
        elif choice == "5":
            print("\nThanks for playing!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()