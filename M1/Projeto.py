import keyboard  # Importa a biblioteca keyboard
import os # Importa a biblioteca os
import sys # Importa a biblioteca sys
import heapq # Importa a biblioteca heapq
from collections import deque # Importa a biblioteca deque

class EightPuzzle: # Classe que representa o jogo do puzzle de 8 peças
    def __init__(self): # Construtor da classe
        print("Configuração inicial:") # Mostra a configuração inicial
        self.board = self.ler_config("inicial") # Lê a configuração inicial do tabuleiro
        print("\nTabuleiro inicial:\n") # Mostra o tabuleiro inicial
        self.mostrar_tabuleiro() # Mostra o tabuleiro
        
        print("Configuração final (objetivo):") # Mostra a configuração final
        self.target_board = self.ler_config("final") # Lê a configuração final do tabuleiro
        print("\nTabuleiro final (objetivo):\n") # Mostra o tabuleiro final
        self.mostrar_tabuleiro_custom(self.target_board) # Mostra o tabuleiro final
        
        if not self.is_solvable(self.board, self.target_board): # Verifica se o puzzle é solucionável
            print("O puzzle não é solucionável com a configuração final dada!") # Mostra a mensagem de erro, se não o for solucionável.
            sys.exit(1) # Sai do programa com código de erro 1
            
        self.moves = 0  # Contador de movimentos

    def ler_config(self, tipo): # Método para ler a configuração do tabuleiro
       
        print(f"Introduza 9 números únicos entre 0 e 8 para a configuração {tipo}:") # Mostra a mensagem para introduzir os números
        numeros_validos = set(range(0, 9)) # Define os números válidos
        numeros_usados = set() # Define os números usados
        tabuleiro = [] # Define o tabuleiro

        for i in range(3): # Loop para ler as linhas do tabuleiro
            while True: # Enquanto verdade/loop verifica se os números são válidos
                try: # Tenta ler os números
                    linha = list(map(int, input(f"Linha {i+1}: ").split())) # Lê os números da linha
                    if len(linha) != 3: # Verifica se a linha tem 3 números
                        print("Erro: Deve introduzir exatamente 3 números.") # Mostra a mensagem de erro se não tiver 3 números
                        continue # Continua o loop se preencher os requisitos

                    if not all(num in numeros_validos for num in linha): # Verifica se não há mais de 8 números introduzidos
                        print("Erro: Apenas números de 0 a 8 são permitidos.") # Mostra a mensagem de erro se houver mais de 8 números
                        continue # Continua o loop se preencher os requisitos

                    if any(num in numeros_usados for num in linha): # Verifica se não há números repetidos
                        print("Erro: Não pode repetir números no tabuleiro.") # Mostra a mensagem de erro se houver números repetidos
                        continue# Continua o loop se preencher os requisitos

                    tabuleiro.append(linha) # Adiciona a linha ao tabuleiro
                    numeros_usados.update(linha) # Atualiza os números usados
                    break # Sai do loop

                except ValueError: # Trata o erro de valor inválido
                    print("Erro: Introduza apenas números inteiros separados por espaço.") # Mostra a mensagem de erro se o valor for inválido

        return tabuleiro # Retorna o tabuleiro

    def mostrar_tabuleiro_custom(self, board): # Método para mostrar o tabuleiro
       
        os.system('cls' if os.name == 'nt' else 'clear') # Limpa a tela
        for row in board: # Loop para mostrar as linhas do tabuleiro 
            print(" ".join(str(num) if num != 0 else " " for num in row)) # Conversão dos números para string e se for 0, mostra um espaço
        print("\n") # Espaço de uma linha em branco
    
    def mostrar_tabuleiro(self): # Método para mostrar o tabuleiro
        
        self.mostrar_tabuleiro_custom(self.board) # Mostra o tabuleiro

    def flatten(self, board): # Método para achatar o tabuleiro
       
        return [num for row in board for num in row if num != 0] # Converte o tabuleiro 3x3 em uma lista de 9 elementos

    def count_inversions(self, board): # Método para contar as inversões
       
        flat = self.flatten(board) # Achata o tabuleiro
        inversions = 0 # Contador de inversões começa a 0
        for i in range(len(flat)): # Loop para percorrer a lista achada
            for j in range(i+1, len(flat)): # Loop para percorrer a lista achada a partir do próximo elemento
                if flat[i] > flat[j]: # Sempre que um número for maior que o outro(i > j), incrementa o contador de inversões
                    inversions += 1 # Incrementa o contador de inversões
        return inversions # Retorna o contador de inversões

    def is_solvable(self, initial, target): # Método para verificar se o puzzle é solucionável
       
        return (self.count_inversions(initial) % 2) == (self.count_inversions(target) % 2) # Retorna True se o número de inversões for par, False se for ímpar

    def find_empty(self, board=None): # Método para encontrar o espaço vazio
        
        if board is None: # Verifica se o tabuleiro é nulo
            board = self.board # Se nenhum tabuleiro for passado, usa o tabuleiro atual (self.board)
        for i in range(3): # Loop para percorrer as linhas do tabuleiro
            for j in range(3):  # Loop para percorrer as colunas do tabuleiro
                if board[i][j] == 0: # Verifica se o número é 0
                    return i, j     # Retorna a posição do espaço vazio
        return None # Retorna nulo se não encontrar o espaço vazio

    def move(self, direction): # Método para mover o espaço vazio
        
        x, y = self.find_empty() # Usa método find_empty para encontrar a posição do espaço vazio
        moved = False # Verifica se o movimento foi realizado com sucesso

        if direction == 'up' and x < 2: # Troca o espaço vazio com o número acima dele
            self.board[x][y], self.board[x+1][y] = self.board[x+1][y], self.board[x][y] # Não deixa exceder o limite do tabuleiro
            moved = True
        elif direction == 'down' and x > 0: # Troca o espaço vazio com o número abaixo dele
            self.board[x][y], self.board[x-1][y] = self.board[x-1][y], self.board[x][y] # Não deixa exceder o limite do tabuleiro
            moved = True
        elif direction == 'left' and y < 2: # Troca o espaço vazio com o número à esquerda dele
            self.board[x][y], self.board[x][y+1] = self.board[x][y+1], self.board[x][y] # Não deixa exceder o limite do tabuleiro
            moved = True
        elif direction == 'right' and y > 0: # Troca o espaço vazio com o número à direita dele
            self.board[x][y], self.board[x][y-1] = self.board[x][y-1], self.board[x][y] # Não deixa exceder o limite do tabuleiro
            moved = True

        if moved: # Se o movimento foi realizado com sucesso
            self.moves += 1 # Incrementa o contador de movimentos
            self.mostrar_tabuleiro() # Mostra o tabuleiro
            print(f"Movimentos: {self.moves}") # Exibe o número de movimentos

            if self.is_solved(): # Verifica se o tabuleiro está resolvido
                print(f"🎉 Parabéns! Atingiu a configuração final em {self.moves} movimentos! 🎉") 
                keyboard.unhook_all() # Desliga o hook/import do teclado

    def is_solved(self): # Método para verificar se o tabuleiro está resolvido
       
        return self.board == self.target_board # Comparação do tabuleiro atual com o tabuleiro final
 
    def board_to_state(self, board): # Método para converter o tabuleiro em estado
       
        return tuple(tuple(row) for row in board) # Converte o tabuleiro em uma tupla que é imutável (inalterável)

    def get_neighbors(self, state): # Método para obter os numeros vizinhos
        
        board = [list(row) for row in state] # Converte o tabuleiro em uma lista mutavel (alterável)
        x, y = self.find_empty(board) # Localiza o espaço vazio
        neighbors = [] # Armazena os movimentos possíveis e os estados resultantes

        def swap_and_clone(b, i1, j1, i2, j2): # Método para trocar e clonar o tabuleiro
            b_new = [row[:] for row in b] # Clona o tabuleiro para não alterar o original
            b_new[i1][j1], b_new[i2][j2] = b_new[i2][j2], b_new[i1][j1] # Troca os valores das posições
            return b_new # Retorna o tabuleiro clonado

        if x < 2:  # pode mover 'up' 
            new_board = swap_and_clone(board, x, y, x+1, y) # Troca o espaço vazio com o número acima dele (imutável)
            neighbors.append(('up', self.board_to_state(new_board))) # Adiciona o movimento e o estado resultante
        if x > 0:  # pode mover 'down'
            new_board = swap_and_clone(board, x, y, x-1, y) # Troca o espaço vazio com o número abaixo dele (imutável)
            neighbors.append(('down', self.board_to_state(new_board))) # Adiciona o movimento e o estado resultante
        if y < 2:  # pode mover 'left'
            new_board = swap_and_clone(board, x, y, x, y+1) # Troca o espaço vazio com o número à esquerda dele (imutável)
            neighbors.append(('left', self.board_to_state(new_board))) # Adiciona o movimento e o estado resultante
        if y > 0:  # pode mover 'right'
            new_board = swap_and_clone(board, x, y, x, y-1) # Troca o espaço vazio com o número à direita dele (imutável)
            neighbors.append(('right', self.board_to_state(new_board))) # Adiciona o movimento e o estado resultante
        return neighbors # Retorna os movimentos possíveis e os estados resultantes

    def heuristic_manhattan(self, state): # Método para calcular a heurística de Manhattan
        
        board = [list(row) for row in state] # Converte o tabuleiro em uma lista mutável (alterável)
        target = self.target_board # Define o tabuleiro final como o alvo
        target_pos = {} # Dicionário para armazenar as posições dos números no tabuleiro final
        for i in range(3): # Loop para percorrer as linhas do tabuleiro
            for j in range(3): # Loop para percorrer as colunas do tabuleiro
                target_pos[target[i][j]] = (i, j) # Armazena no dicionário as posições dos números no tabuleiro final
        distance = 0 # Distância começa em 0
        for i in range(3): # Loop para percorrer as linhas do tabuleiro
            for j in range(3): # Loop para percorrer as colunas do tabuleiro
                val = board[i][j] # Verifica se o valor é diferente de 0
                if val != 0:    # Ignora o espaço vazio

                    ti, tj = target_pos[val] #### Verifica a posição do número no tabuleiro final ????
                    
                    distance += abs(i - ti) + abs(j - tj) # Calcula a distância de Manhattan
        return distance # Retorna a distância de Manhattan

    def heuristic_hamming(self, state): # Método para calcular a heurística de Hamming
        
        board = [list(row) for row in state] # Converte o tabuleiro em uma lista mutável (alterável)
        distance = 0 # Distância começa em 0
        for i in range(3): # Loop para percorrer as linhas do tabuleiro
            for j in range(3): # Loop para percorrer as colunas do tabuleiro
                if board[i][j] != 0 and board[i][j] != self.target_board[i][j]: # Verifica se o número é diferente de 0 e se está na posição correta
                    distance += 1 # Incrementa a distância
        return distance # Retorna a distância

    def auto_solve_astar(self, heuristic): # Método para resolver o puzzle automaticamente
        
        start = self.board_to_state(self.board) # Converte o tabuleiro inicial em estado
        goal = self.board_to_state(self.target_board) # Verifica se o tabuleiro final é o objetivo
        open_set = [] # Filas de prioridade para armazenar os estados para explorar
        heapq.heappush(open_set, (heuristic(start), 0, start)) # Adiciona o estado inicial à fila de prioridade
        came_from = {}  # Dicionário para armazenar o movimento e o estado anterior
        g_score = {start: 0} # Dicionário para armazenar o custo do caminho (inicialmente 0)

        while open_set: # Enquanto a fila de prioridade não estiver vazia
            f, current_cost, current = heapq.heappop(open_set) # Remove o estado com menor custo da fila de prioridade
            if current == goal: # Verifica se o estado atual é o objetivo
                moves = [] # 

                while current in came_from: # Enquanto o estado atual estiver no dicionário came_from
                    current, move = came_from[current] # Atualiza o estado atual e o movimento
                    moves.append(move) # Adiciona o movimento à lista de movimentos
                return list(reversed(moves)) # Retorna a lista de movimentos invertida
            
            for move, neighbor in self.get_neighbors(current): # Para cada movimento e vizinho no estado atual
                tentative_g = g_score[current] + 1 # Custo acumulado = custo atual + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]: # Se o vizinho não estiver no dicionário ou o custo acumulado for menor
                    came_from[neighbor] = (current, move) # Atualiza o dicionário came_from
                    g_score[neighbor] = tentative_g # Atualiza o dicionário g_score
                    f_neighbor = tentative_g + heuristic(neighbor) # Calcula a heurística do vizinho
                    heapq.heappush(open_set, (f_neighbor, tentative_g, neighbor)) # Adiciona o vizinho à fila de prioridade
        return None # Retorna nulo se não encontrar solução

    def auto_solve_bfs(self): # Método para resolver o puzzle automaticamente
        
        start = self.board_to_state(self.board) # Converte o tabuleiro inicial em estado
        goal = self.board_to_state(self.target_board) # Verifica se o tabuleiro final é o objetivo
        queue = deque([(start, [])]) # Fila para armazenar o estado e o caminho
        visited = set([start]) # Conjunto para armazenar os estados visitados

        while queue: # Enquanto a fila não estiver vazia
            current, path = queue.popleft() # Remove o estado mais antigo da fila (FIFO)
            if current == goal: # Verifica se o estado atual é o objetivo
                return path # Retorna o caminho
            for move, neighbor in self.get_neighbors(current): # Usa o método get_neighbors para obter os vizinhos
                if neighbor not in visited: # Se o vizinho não foi visitado
                    visited.add(neighbor) # Adiciona ao estado visitado
                    queue.append((neighbor, path + [move])) # Adiciona o vizinho e o movimento à fila
        return None # Retorna nulo se não encontrar solução

    def auto_solve(self): # Método para resolver o puzzle automaticamente
        
        print("Algoritmos disponíveis:")
        print(" 1 - A* com Manhattan")
        print(" 2 - A* com Hamming")
        print(" 3 - BFS")
        alg = input("Escolha o algoritmo (1, 2 ou 3): ").strip() # Escolha do algoritmo
        if alg == "1": # Se escolher o algoritmo 1
            solution = self.auto_solve_astar(self.heuristic_manhattan) # Resolve o puzzle com a heurística de Manhattan
        elif alg == "2":    # Se escolher o algoritmo 2
            solution = self.auto_solve_astar(self.heuristic_hamming) # Resolve o puzzle com a heurística de Hamming
        elif alg == "3":    # Se escolher o algoritmo 3
            solution = self.auto_solve_bfs()    # Resolve o puzzle com o BFS
        else:  # Se escolher um algoritmo inválido
            print("Opção inválida!")
            return None

        if solution is None: # Se não encontrar solução
            print("Não foi encontrada solução!") # Mostra a mensagem de erro
            return None

        print(f"Solução encontrada com {len(solution)} movimentos:") # Mostra a solução encontrada
        print(" -> ".join(solution)) # Mostra os movimentos
        return solution

    def run_all_algorithms_minimal(self):   # Método para executar todos os algoritmos minimamente
        
        print("\nExecutando A* com Manhattan:") 
        sol_manhattan = self.auto_solve_astar(self.heuristic_manhattan) # Resolve o puzzle com a heurística de Manhattan
        if sol_manhattan is not None: # Se encontrar solução
            print(f"Solução: {' -> '.join(sol_manhattan)}") # Mostra a solução
            print(f"Número de movimentos: {len(sol_manhattan)}\n") # Mostra o número de movimentos
        else: #
            print("Nenhuma solução encontrada.\n") # Mostra a mensagem de erro
            
        print("Executando A* com Hamming:") # Mostra a execução do A* com Hamming
        sol_hamming = self.auto_solve_astar(self.heuristic_hamming) # Resolve o puzzle com a heurística de Hamming
        if sol_hamming is not None: # Se encontrar solução
            print(f"Solução: {' -> '.join(sol_hamming)}") # Mostra a solução
            print(f"Número de movimentos: {len(sol_hamming)}\n") # Mostra o número de movimentos
        else:
            print("Nenhuma solução encontrada.\n") # Mostra a mensagem de erro
            
        print("Executando BFS:") # Mostra a execução do BFS
        sol_bfs = self.auto_solve_bfs() # Resolve o puzzle com o BFS
        if sol_bfs is not None: # Se encontrar solução
            print(f"Solução: {' -> '.join(sol_bfs)}") # Mostra a solução
            print(f"Número de movimentos: {len(sol_bfs)}\n") # Mostra o número de movimentos
        else:
            print("Nenhuma solução encontrada.\n")

    def play(self): # Método para jogar o puzzle
        
        mode = input("Escolha o modo (M para manual, A para automático, C para comparação): ").strip().upper() # Escolha do modo
        if mode == "M": 
            print("Modo manual: Use as SETAS DIRECIONAIS para mover o espaço vazio (0). Pressione ESC para sair.")
            keyboard.on_press_key("up", lambda _: self.move('up')) # Usa a tecla de seta para cima para mover o espaço vazio para cima
            keyboard.on_press_key("down", lambda _: self.move('down')) # Usa a tecla de seta para baixo para mover o espaço vazio para baixo
            keyboard.on_press_key("left", lambda _: self.move('left')) # Usa a tecla de seta para a esquerda para mover o espaço vazio para a esquerda 
            keyboard.on_press_key("right", lambda _: self.move('right')) # Usa a tecla de seta para a direita para mover o espaço vazio para a direita
            while not self.is_solved(): # Enquanto o tabuleiro não estiver resolvido
                if keyboard.is_pressed("esc"): # Se a tecla ESC for pressionada
                    print("Jogo encerrado.") # Mostra a mensagem de encerramento
                    break 
            if self.is_solved(): # Se o tabuleiro estiver resolvido
                self.mostrar_tabuleiro() # Mostra o tab
                print(f"🎉 Parabéns! Atingiu a configuração final em {self.moves} movimentos! 🎉") # 
        elif mode == "A": # Se escolher o modo automático
            solution = self.auto_solve() # Resolve o puzzle automaticamente 
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

if __name__ == "__main__": # Executa o jogo
    game = EightPuzzle() # Instancia a classe EightPuzzle
    game.play() # Inicia o jogo