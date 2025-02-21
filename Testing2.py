# language: python
# filepath: /D:/Testint code/Sistemas Inteligentes/Projeto/Sistemas-Inteligentes/Projecto.py
import keyboard  # Biblioteca para capturar teclas (para modo manual)
import os
import sys
import heapq

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
        """
        Lê uma configuração do tabuleiro.
        O usuário introduz 8 números únicos entre 1 e 8 (o 0 é adicionado automaticamente).
        """
        print(f"Introduza 8 números únicos entre 1 e 8 para a configuração {tipo} (o 0 será inserido automaticamente):")
        numeros_validos = set(range(1, 9))
        numeros_usados = set()
        tabuleiro = []

        for i in range(3):
            while True:
                try:
                    if i < 2:
                        linha = list(map(int, input(f"Linha {i+1}: ").split()))
                        if len(linha) != 3:
                            print("Erro: Deve introduzir exatamente 3 números.")
                            continue
                    else:
                        linha = list(map(int, input(f"Linha {i+1} (apenas 2 números): ").split()))
                        if len(linha) != 2:
                            print("Erro: Deve introduzir exatamente 2 números na última linha.")
                            continue

                    if not all(num in numeros_validos for num in linha):
                        print("Erro: Apenas números de 1 a 8 são permitidos.")
                        continue

                    if any(num in numeros_usados for num in linha):
                        print("Erro: Não pode repetir números no tabuleiro.")
                        continue

                    tabuleiro.append(linha)
                    numeros_usados.update(linha)
                    break

                except ValueError:
                    print("Erro: Introduza apenas números inteiros separados por espaço.")

        tabuleiro[2].append(0)  # Adiciona o 0 automaticamente
        return tabuleiro

    def mostrar_tabuleiro_custom(self, board):
        """Mostra o tabuleiro dado."""
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in board:
            print(" ".join(str(num) if num != 0 else " " for num in row))
        print("\n")
    
    def mostrar_tabuleiro(self):
        """Mostra o tabuleiro atual."""
        self.mostrar_tabuleiro_custom(self.board)

    def flatten(self, board):
        """Converte o board em uma lista ignorando o 0."""
        return [num for row in board for num in row if num != 0]

    def count_inversions(self, board):
        """Conta inversões na lista do board (usado para checagem de solubilidade)."""
        flat = self.flatten(board)
        inversions = 0
        for i in range(len(flat)):
            for j in range(i+1, len(flat)):
                if flat[i] > flat[j]:
                    inversions += 1
        return inversions

    def is_solvable(self, initial, target):
        """
        Para o 8-puzzle, o estado é solucionável se o número de inversões tiver a mesma paridade.
        """
        return (self.count_inversions(initial) % 2) == (self.count_inversions(target) % 2)

    def find_empty(self, board=None):
        """Encontra a posição do espaço vazio (0)."""
        if board is None:
            board = self.board
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    return i, j
        return None

    def move(self, direction):
        """
        Move uma peça na direção especificada. Nossas regras:
         - 'up': se empty não estiver na última linha, troca com a peça abaixo.
         - 'down': se empty não estiver na primeira linha, troca com a peça acima.
         - 'left': se empty não estiver na última coluna, troca com a peça à direita.
         - 'right': se empty não estiver na primeira coluna, troca com a peça à esquerda.
        """
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
                print(f"🎉 Parabéns! Você atingiu a configuração final em {self.moves} movimentos! 🎉")
                keyboard.unhook_all()

    def is_solved(self):
        """Verifica se o board atual é igual ao board alvo."""
        return self.board == self.target_board

    def board_to_state(self, board):
        """Converte board (lista de listas) em uma tupla de tuplas (hashable)."""
        return tuple(tuple(row) for row in board)

    def get_neighbors(self, state):
        """Retorna uma lista de (move, novo_estado) para o estado dado, seguindo as regras de movimentação."""
        # Converte de estado para lista de listas
        board = [list(row) for row in state]
        x, y = self.find_empty(board)
        neighbors = []

        def swap_and_clone(b, i1, j1, i2, j2):
            b_new = [row[:] for row in b]
            b_new[i1][j1], b_new[i2][j2] = b_new[i2][j2], b_new[i1][j1]
            return b_new

        # Usando as mesmas regras do move():
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

    def heuristic(self, state):
        """
        Heurística (distância Manhattan). Calcula a soma das distâncias
        horizontais e verticais de cada peça até sua posição no tabuleiro alvo.
        """
        board = [list(row) for row in state]
        # Cria um mapa do valor até posição no board alvo.
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

    def auto_solve(self):
        """
        Usa A* para achar a sequência ótima de movimentos partindo do board atual (inicial)
        até o board alvo.
        Retorna uma lista de movimentos (strings).
        """
        start = self.board_to_state(self.board)
        goal = self.board_to_state(self.target_board)
        open_set = []
        heapq.heappush(open_set, (self.heuristic(start), 0, start))
        came_from = {}  # state -> (prev_state, move)
        g_score = {start: 0}

        while open_set:
            f, current_cost, current = heapq.heappop(open_set)
            if current == goal:
                # Reconstruir caminho
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
                    f_neighbor = tentative_g + self.heuristic(neighbor)
                    heapq.heappush(open_set, (f_neighbor, tentative_g, neighbor))
        return None  # Sem solução (teoricamente não deve ocorrer)

    def play(self):
        """
        Permite escolher entre resolução manual ou automática.
         - Manual: usa as setas (keyboard) para mover.
         - Automática: calcula solução ótima e mostra cada movimento com avanço por Enter.
        """
        mode = input("Escolha o modo (M para manual, A para automático): ").strip().upper()
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
                print(f"🎉 Parabéns! Você atingiu a configuração final em {self.moves} movimentos! 🎉")
        elif mode == "A":
            solution = self.auto_solve()
            if solution is None:
                print("Não foi encontrada solução!")
                return
            print(f"Solução encontrada com {len(solution)} movimentos:")
            print(" -> ".join(solution))
            input("Pressione Enter para começar a solução automática...")
            # Agora, executar cada movimento da solução:
            for move in solution:
                self.move(move)
                input("Pressione Enter para o próximo movimento...")
            print("Resolução automática completa.")
        else:
            print("Modo inválido.")

if __name__ == "__main__":
    game = EightPuzzle()
    game.play()