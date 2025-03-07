import keyboard  
import os
import sys
import heapq
from collections import deque

class EightPuzzle:
    def __init__(self):
        print("Configuração inicial:")
        self.board = self.ler_config("inicial")
        print("\nTabuleiro inicial:\n")
        self.mostrar_tabuleiro()
        
        print("Configuração final (objetivo):")
        self.target_board = self.ler_config("final")
        print("\nTabuleiro final (objetivo):\n")
        self.mostrar_tabuleiro_custom(self.target_board)
        
        if not self.is_solvable(self.board, self.target_board):
            print("O puzzle não é solucionável com a configuração final dada!")
            sys.exit(1)
            
        self.moves = 0  # Contador de movimentos

    def ler_config(self, tipo):
       
        print(f"Introduza 9 números únicos entre 0 e 8 para a configuração {tipo}:")
        numeros_validos = set(range(0, 9))
        numeros_usados = set()
        tabuleiro = []

        for i in range(3):
            while True:
                try:
                    linha = list(map(int, input(f"Linha {i+1}: ").split()))
                    if len(linha) != 3:
                        print("Erro: Deve introduzir exatamente 3 números.")
                        continue

                    if not all(num in numeros_validos for num in linha):
                        print("Erro: Apenas números de 0 a 8 são permitidos.")
                        continue

                    if any(num in numeros_usados for num in linha):
                        print("Erro: Não pode repetir números no tabuleiro.")
                        continue

                    tabuleiro.append(linha)
                    numeros_usados.update(linha)
                    break

                except ValueError:
                    print("Erro: Introduza apenas números inteiros separados por espaço.")

        return tabuleiro

    def mostrar_tabuleiro_custom(self, board):
       
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in board:
            print(" ".join(str(num) if num != 0 else " " for num in row))
        print("\n")
    
    def mostrar_tabuleiro(self):
        
        self.mostrar_tabuleiro_custom(self.board)

    def flatten(self, board):
       
        return [num for row in board for num in row if num != 0]

    def count_inversions(self, board):
       
        flat = self.flatten(board)
        inversions = 0
        for i in range(len(flat)):
            for j in range(i+1, len(flat)):
                if flat[i] > flat[j]:
                    inversions += 1
        return inversions

    def is_solvable(self, initial, target):
       
        return (self.count_inversions(initial) % 2) == (self.count_inversions(target) % 2)

    def find_empty(self, board=None):
        
        if board is None:
            board = self.board
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    return i, j
        return None

    def move(self, direction):
        
        x, y = self.find_empty()
        moved = False

        if direction == 'up' and x < 2:
            self.board[x][y], self.board[x+1][y] = self.board[x+1][y], self.board[x][y]
            moved = True
        elif direction == 'down' and x > 0:
            self.board[x][y], self.board[x-1][y] = self.board[x-1][y], self.board[x][y]
            moved = True
        elif direction == 'left' and y < 2:
            self.board[x][y], self.board[x][y+1] = self.board[x][y+1], self.board[x][y]
            moved = True
        elif direction == 'right' and y > 0:
            self.board[x][y], self.board[x][y-1] = self.board[x][y-1], self.board[x][y]
            moved = True

        if moved:
            self.moves += 1
            self.mostrar_tabuleiro()
            print(f"Movimentos: {self.moves}")

            if self.is_solved():
                print(f"🎉 Parabéns! Atingiu a configuração final em {self.moves} movimentos! 🎉")
                keyboard.unhook_all()

    def is_solved(self):
       
        return self.board == self.target_board

    def board_to_state(self, board):
       
        return tuple(tuple(row) for row in board)

    def get_neighbors(self, state):
        
        board = [list(row) for row in state]
        x, y = self.find_empty(board)
        neighbors = []

        def swap_and_clone(b, i1, j1, i2, j2):
            b_new = [row[:] for row in b]
            b_new[i1][j1], b_new[i2][j2] = b_new[i2][j2], b_new[i1][j1]
            return b_new

        if x < 2:  # pode mover 'up'
            new_board = swap_and_clone(board, x, y, x+1, y)
            neighbors.append(('up', self.board_to_state(new_board)))
        if x > 0:  # pode mover 'down'
            new_board = swap_and_clone(board, x, y, x-1, y)
            neighbors.append(('down', self.board_to_state(new_board)))
        if y < 2:  # pode mover 'left'
            new_board = swap_and_clone(board, x, y, x, y+1)
            neighbors.append(('left', self.board_to_state(new_board)))
        if y > 0:  # pode mover 'right'
            new_board = swap_and_clone(board, x, y, x, y-1)
            neighbors.append(('right', self.board_to_state(new_board)))
        return neighbors

    def heuristic_manhattan(self, state):
        
        board = [list(row) for row in state]
        target = self.target_board
        target_pos = {}
        for i in range(3):
            for j in range(3):
                target_pos[target[i][j]] = (i, j)
        distance = 0
        for i in range(3):
            for j in range(3):
                val = board[i][j]
                if val != 0:
                    ti, tj = target_pos[val]
                    distance += abs(i - ti) + abs(j - tj)
        return distance

    def heuristic_hamming(self, state):
        
        board = [list(row) for row in state]
        distance = 0
        for i in range(3):
            for j in range(3):
                if board[i][j] != 0 and board[i][j] != self.target_board[i][j]:
                    distance += 1
        return distance

    def auto_solve_astar(self, heuristic):
        
        start = self.board_to_state(self.board)
        goal = self.board_to_state(self.target_board)
        open_set = []
        heapq.heappush(open_set, (heuristic(start), 0, start))
        came_from = {}  # state -> (prev_state, move)
        g_score = {start: 0}

        while open_set:
            f, current_cost, current = heapq.heappop(open_set)
            if current == goal:
                moves = []
                while current in came_from:
                    current, move = came_from[current]
                    moves.append(move)
                return list(reversed(moves))
            for move, neighbor in self.get_neighbors(current):
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = (current, move)
                    g_score[neighbor] = tentative_g
                    f_neighbor = tentative_g + heuristic(neighbor)
                    heapq.heappush(open_set, (f_neighbor, tentative_g, neighbor))
        return None

    def auto_solve_bfs(self):
        
        start = self.board_to_state(self.board)
        goal = self.board_to_state(self.target_board)
        queue = deque([(start, [])])
        visited = set([start])

        while queue:
            current, path = queue.popleft()
            if current == goal:
                return path
            for move, neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [move]))
        return None

    def auto_solve(self):
        
        print("Algoritmos disponíveis:")
        print(" 1 - A* com Manhattan")
        print(" 2 - A* com Hamming")
        print(" 3 - BFS")
        alg = input("Escolha o algoritmo (1, 2 ou 3): ").strip()
        if alg == "1":
            solution = self.auto_solve_astar(self.heuristic_manhattan)
        elif alg == "2":
            solution = self.auto_solve_astar(self.heuristic_hamming)
        elif alg == "3":
            solution = self.auto_solve_bfs()
        else:
            print("Opção inválida!")
            return None

        if solution is None:
            print("Não foi encontrada solução!")
            return None

        print(f"Solução encontrada com {len(solution)} movimentos:")
        print(" -> ".join(solution))
        return solution

    def run_all_algorithms_minimal(self):
        
        print("\nExecutando A* com Manhattan:")
        sol_manhattan = self.auto_solve_astar(self.heuristic_manhattan)
        if sol_manhattan is not None:
            print(f"Solução: {' -> '.join(sol_manhattan)}")
            print(f"Número de movimentos: {len(sol_manhattan)}\n")
        else:
            print("Nenhuma solução encontrada.\n")
            
        print("Executando A* com Hamming:")
        sol_hamming = self.auto_solve_astar(self.heuristic_hamming)
        if sol_hamming is not None:
            print(f"Solução: {' -> '.join(sol_hamming)}")
            print(f"Número de movimentos: {len(sol_hamming)}\n")
        else:
            print("Nenhuma solução encontrada.\n")
            
        print("Executando BFS:")
        sol_bfs = self.auto_solve_bfs()
        if sol_bfs is not None:
            print(f"Solução: {' -> '.join(sol_bfs)}")
            print(f"Número de movimentos: {len(sol_bfs)}\n")
        else:
            print("Nenhuma solução encontrada.\n")

    def play(self):
        
        mode = input("Escolha o modo (M para manual, A para automático, C para comparação): ").strip().upper()
        if mode == "M":
            print("Modo manual: Use as SETAS DIRECIONAIS para mover o espaço vazio (0). Pressione ESC para sair.")
            keyboard.on_press_key("up", lambda _: self.move('up'))
            keyboard.on_press_key("down", lambda _: self.move('down'))
            keyboard.on_press_key("left", lambda _: self.move('left'))
            keyboard.on_press_key("right", lambda _: self.move('right'))
            while not self.is_solved():
                if keyboard.is_pressed("esc"):
                    print("Jogo encerrado.")
                    break
            if self.is_solved():
                self.mostrar_tabuleiro()
                print(f"🎉 Parabéns! Atingiu a configuração final em {self.moves} movimentos! 🎉")
        elif mode == "A":
            solution = self.auto_solve()
            if solution is None:
                return
            input("Pressione Enter para começar a solução automática...")
            for move in solution:
                self.move(move)
                input("Pressione Enter para o próximo movimento...")
            print("Resolução automática completa.")
        elif mode == "C":
            self.run_all_algorithms_minimal()
        else:
            print("Modo inválido.")

if __name__ == "__main__":
    game = EightPuzzle()
    game.play()