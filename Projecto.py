import keyboard  # Biblioteca para capturar teclas
import os  # Para limpar o terminal (opcional)

class EightPuzzle:
    def __init__(self):
        self.board = self.ler_config()
        self.moves = 0  # 🔹 Initialize move counter
        print("\nTabuleiro inicial:\n")
        self.mostrar_tabuleiro()

    def ler_config(self):
        """Lê uma configuração do tabuleiro, garantindo que o usuário insira apenas 8 números e o 0 seja adicionado automaticamente."""
        print("Introduza 8 números únicos entre 1 e 8 (o 0 será inserido automaticamente):")
        numeros_validos = set(range(1, 9))  # Números permitidos: 1 a 8 (sem o 0)
        numeros_usados = set()
        tabuleiro = []
        """Ola"""
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

        tabuleiro[2].append(0)  # O 0 é adicionado automaticamente
        return tabuleiro

    def find_empty(self):
        """Encontra a posição do espaço vazio (0)."""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def move(self, direction):
        """Move uma peça na direção especificada se for possível e conta os movimentos."""
        x, y = self.find_empty()
        moved = False  # Para verificar se realmente houve movimento

        if direction == 'up' and x < 2:  # Seta para cima (mover 0 para baixo)
            self.board[x][y], self.board[x+1][y] = self.board[x+1][y], self.board[x][y]
            moved = True
        elif direction == 'down' and x > 0:  # Seta para baixo (mover 0 para cima)
            self.board[x][y], self.board[x-1][y] = self.board[x-1][y], self.board[x][y]
            moved = True
        elif direction == 'left' and y < 2:  # Seta para esquerda (mover 0 para a direita)
            self.board[x][y], self.board[x][y+1] = self.board[x][y+1], self.board[x][y]
            moved = True
        elif direction == 'right' and y > 0:  # Seta para direita (mover 0 para a esquerda)
            self.board[x][y], self.board[x][y-1] = self.board[x][y-1], self.board[x][y]
            moved = True

        if moved:
            self.moves += 1  # 🔹 Increment move counter
            self.mostrar_tabuleiro()  # Atualiza o tabuleiro após o movimento
            print(f"🔢 Movimentos: {self.moves}")  # 🔹 Exibe a contagem de movimentos

            # 🔹 Check if the puzzle is solved
            if self.is_solved():
                print(f"🎉 Parabéns! Você resolveu o puzzle em {self.moves} movimentos! 🎉")
                keyboard.unhook_all()  # Para de capturar teclas

    def is_solved(self):
        """Verifica se o puzzle está resolvido."""
        return self.board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def mostrar_tabuleiro(self):
        """Mostra o estado atual do tabuleiro."""
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela (Windows: cls, Linux/Mac: clear)
        for row in self.board:
            print(" ".join(str(num) if num != 0 else " " for num in row))
        print("\n")

    def play(self):
        """Loop principal do jogo com controle por setas direcionais."""
        print("Use as SETAS DIRECIONAIS para mover o espaço vazio (0). Pressione ESC para sair.")

        # Captura os eventos de tecla para mover
        keyboard.on_press_key("up", lambda _: self.move('up'))
        keyboard.on_press_key("down", lambda _: self.move('down'))
        keyboard.on_press_key("left", lambda _: self.move('left'))
        keyboard.on_press_key("right", lambda _: self.move('right'))

        # Aguarda até o puzzle ser resolvido ou ESC ser pressionado
        while not self.is_solved():
            if keyboard.is_pressed("esc"):
                print("Jogo encerrado.")
                break

        if self.is_solved():
            self.mostrar_tabuleiro()
            print(f"🎉 Parabéns! Você resolveu o puzzle em {self.moves} movimentos! 🎉")

if __name__ == "__main__":
    game = EightPuzzle()
    game.play()
