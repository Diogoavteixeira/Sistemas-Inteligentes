import keyboard  # Biblioteca para capturar teclas (para modo manual)
import os  # Usado para limpar o terminal
import sys  # Usado para saída do programa
import heapq  # Estrutura de heap para a busca A*
from collections import deque  # Fila dupla usada no BFS

class EightPuzzle:
    def __init__(self):
        print("Configuração inicial:")
        self.board = self.ler_config("inicial")  # Lê a configuração inicial do tabuleiro
        print("\nTabuleiro inicial:\n")
        self.mostrar_tabuleiro()
        
        print("Configuração final (objetivo):")
        self.target_board = self.ler_config("final")  # Lê a configuração final do tabuleiro
        print("\nTabuleiro final (objetivo):\n")
        self.mostrar_tabuleiro_custom(self.target_board)
        
        # Verifica se o puzzle é solucionável
        if not self.is_solvable(self.board, self.target_board):
            print("O puzzle não é solucionável com a configuração final dada!")
            sys.exit(1)  # Encerra o programa se o puzzle não puder ser resolvido
            
        self.moves = 0  # Contador de movimentos

    def ler_config(self, tipo):
        """
        Lê uma configuração do tabuleiro.
        O utilizador introduz 9 números únicos entre 0 e 8, onde 0 representa o espaço vazio.
        """
        print(f"Introduza 9 números únicos entre 0 e 8 para a configuração {tipo}:")
        numeros_validos = set(range(0, 9))  # Conjunto de números permitidos
        numeros_usados = set()  # Conjunto para evitar repetição de números
        tabuleiro = []

        for i in range(3):
            while True:
                try:
                    linha = list(map(int, input(f"Linha {i+1}: ").split()))  # Lê e converte a entrada em lista de inteiros
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
        """Mostra um tabuleiro fornecido."""
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela
        for row in board:
            print(" ".join(str(num) if num != 0 else " " for num in row))  # Exibe o tabuleiro
        print("\n")
    
    def mostrar_tabuleiro(self):
        """Mostra o tabuleiro atual."""
        self.mostrar_tabuleiro_custom(self.board)

    def flatten(self, board):
        """Converte o tabuleiro numa lista ignorando o 0."""
        return [num for row in board for num in row if num != 0]

    def count_inversions(self, board):
        """Conta inversões no tabuleiro (usado para verificar se é solucionável)."""
        flat = self.flatten(board)
        inversions = 0
        for i in range(len(flat)):
            for j in range(i+1, len(flat)):
                if flat[i] > flat[j]:
                    inversions += 1
        return inversions

    def is_solvable(self, initial, target):
        """Verifica se o tabuleiro inicial pode ser resolvido para o estado final."""
        return (self.count_inversions(initial) % 2) == (self.count_inversions(target) % 2)

    def find_empty(self, board=None):
        """Encontra a posição do espaço vazio (0) no tabuleiro."""
        if board is None:
            board = self.board
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    return i, j
        return None

    def move(self, direction):
        """Move uma peça na direção especificada."""
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
        """Verifica se o tabuleiro atual é igual ao tabuleiro alvo."""
        return self.board == self.target_board
    
    def play(self):
        """Permite jogar no modo manual ou automático."""
        mode = input("Escolha o modo (M para manual, A para automático): ").strip().upper()
        if mode == "M":
            print("Modo manual: Use as setas direcionais para mover o espaço vazio (0). Pressione ESC para sair.")
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
        else:
            print("Modo inválido.")

if __name__ == "__main__":
    game = EightPuzzle()
    game.play()
