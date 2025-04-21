import random
import time
import matplotlib.pyplot as plt
import numpy as np

def mostrar_tabuleiro(tabuleiro):#  """Mostra o tabuleiro do jogo"""
    """Mostra o estado atual do tabuleiro""" #  
    print("-------------") # 
    for linha in tabuleiro:#
        print("| " + " | ".join(linha) + " |")
        print("-------------")

def verificar_vencedor(tabuleiro, jogador):
    """Verifica se o jogador especificado venceu"""
    # Verificar linhas
    for linha in tabuleiro:
        if all(celula == jogador for celula in linha):
            return True
    
    # Verificar colunas
    for col in range(3):
        if all(tabuleiro[linha][col] == jogador for linha in range(3)):
            return True
    
    # Verificar diagonais
    if all(tabuleiro[i][i] == jogador for i in range(3)):
        return True
    if all(tabuleiro[i][2-i] == jogador for i in range(3)):
        return True
    
    return False

def tabuleiro_cheio(tabuleiro):
    """Verifica se o tabuleiro está cheio (empate)"""
    return all(celula != " " for linha in tabuleiro for celula in linha)

def obter_jogadas_possiveis(tabuleiro):
    """Retorna uma lista de jogadas disponíveis como tuplos (linha, coluna)"""
    jogadas = []
    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j] == " ":
                jogadas.append((i, j))
    return jogadas

def minimax(tabuleiro, profundidade, e_maximizador, jogador, oponente):

    # Casos base: verificar estados terminais
    if verificar_vencedor(tabuleiro, jogador):
        return 10 - profundidade  # Vitória, pontuação maior para vitórias mais rápidas
    if verificar_vencedor(tabuleiro, oponente):
        return profundidade - 10  # Derrota, pontuação maior para derrotas mais lentas
    if tabuleiro_cheio(tabuleiro):
        return 0  # Empate
    
    # Casos recursivos
    if e_maximizador:
        melhor_pontuacao = float('-inf')
        for jogada in obter_jogadas_possiveis(tabuleiro):
            tabuleiro[jogada[0]][jogada[1]] = jogador
            pontuacao = minimax(tabuleiro, profundidade + 1, False, jogador, oponente)
            tabuleiro[jogada[0]][jogada[1]] = " "  # Desfazer jogada
            melhor_pontuacao = max(pontuacao, melhor_pontuacao)
        return melhor_pontuacao
    else:
        melhor_pontuacao = float('inf')
        for jogada in obter_jogadas_possiveis(tabuleiro):
            tabuleiro[jogada[0]][jogada[1]] = oponente
            pontuacao = minimax(tabuleiro, profundidade + 1, True, jogador, oponente)
            tabuleiro[jogada[0]][jogada[1]] = " "  # Desfazer jogada
            melhor_pontuacao = min(pontuacao, melhor_pontuacao)
        return melhor_pontuacao

def alpha_beta(tabuleiro, profundidade, e_maximizador, jogador, oponente, alpha, beta):
   
    # Casos base: verificar estados terminais
    if verificar_vencedor(tabuleiro, jogador):
        return 10 - profundidade
    if verificar_vencedor(tabuleiro, oponente):
        return profundidade - 10
    if tabuleiro_cheio(tabuleiro):
        return 0

    # Casos recursivos com poda alpha-beta
    if e_maximizador:
        melhor_pontuacao = float('-inf')
        for jogada in obter_jogadas_possiveis(tabuleiro):
            tabuleiro[jogada[0]][jogada[1]] = jogador
            pontuacao = alpha_beta(tabuleiro, profundidade + 1, False, jogador, oponente, alpha, beta)
            tabuleiro[jogada[0]][jogada[1]] = " "  # Desfazer jogada
            melhor_pontuacao = max(pontuacao, melhor_pontuacao)
            alpha = max(alpha, pontuacao)
            if beta <= alpha:
                break  # Corte beta
        return melhor_pontuacao
    else:
        melhor_pontuacao = float('inf')
        for jogada in obter_jogadas_possiveis(tabuleiro):
            tabuleiro[jogada[0]][jogada[1]] = oponente
            pontuacao = alpha_beta(tabuleiro, profundidade + 1, True, jogador, oponente, alpha, beta)
            tabuleiro[jogada[0]][jogada[1]] = " "  # Desfazer jogada
            melhor_pontuacao = min(pontuacao, melhor_pontuacao)
            beta = min(beta, pontuacao)
            if beta <= alpha:
                break  # Corte alpha
        return melhor_pontuacao

def obter_jogada_computador(tabuleiro, computador, humano, usar_alpha_beta=False):
    
    melhor_pontuacao = float('-inf')
    melhor_jogada = None
    jogadas_possiveis = obter_jogadas_possiveis(tabuleiro)

    # Para a primeira jogada, escolher aleatoriamente por eficiência
    if len(jogadas_possiveis) == 9:
        return random.choice(jogadas_possiveis), 0.0

    # Medir tempo de execução
    tempo_inicio = time.time()
    
    # Avaliar cada jogada possível
    for jogada in jogadas_possiveis:
        tabuleiro[jogada[0]][jogada[1]] = computador
        if usar_alpha_beta:
            pontuacao = alpha_beta(tabuleiro, 0, False, computador, humano, float('-inf'), float('inf'))
        else:
            pontuacao = minimax(tabuleiro, 0, False, computador, humano)
        tabuleiro[jogada[0]][jogada[1]] = " "  # Desfazer jogada

        if pontuacao > melhor_pontuacao:
            melhor_pontuacao = pontuacao
            melhor_jogada = jogada
            
    tempo_fim = time.time()
    tempo_execucao = tempo_fim - tempo_inicio
    
    return melhor_jogada, tempo_execucao

def contar_nos_visitados(tabuleiro, e_maximizador, jogador, oponente, usar_alpha_beta=False, alpha=float('-inf'), beta=float('inf')):
   
    # Casos base: verificar estados terminais
    if verificar_vencedor(tabuleiro, jogador) or verificar_vencedor(tabuleiro, oponente) or tabuleiro_cheio(tabuleiro):
        return 1  # Nó terminal conta como 1
    
    nos = 1  # Contar nó atual
    
    # Casos recursivos
    for jogada in obter_jogadas_possiveis(tabuleiro):
        tabuleiro[jogada[0]][jogada[1]] = jogador if e_maximizador else oponente
        
        if usar_alpha_beta:
            proxima_pontuacao = alpha_beta(tabuleiro, 0, not e_maximizador, jogador, oponente, alpha, beta)
            if e_maximizador:
                alpha = max(alpha, proxima_pontuacao)
                if beta <= alpha:
                    tabuleiro[jogada[0]][jogada[1]] = " "  # Desfazer jogada
                    break  # Poda
            else:
                beta = min(beta, proxima_pontuacao)
                if beta <= alpha:
                    tabuleiro[jogada[0]][jogada[1]] = " "  # Desfazer jogada
                    break  # Poda
        
        nos += contar_nos_visitados(
            tabuleiro, 
            not e_maximizador, 
            jogador, 
            oponente, 
            usar_alpha_beta,
            alpha,
            beta
        )
        
        tabuleiro[jogada[0]][jogada[1]] = " "  # Desfazer jogada
    
    return nos

def comparar_desempenho_algoritmos():
    
    tamanhos_tabuleiro = [(i, i) for i in range(3, 5)]  # Testaremos com tabuleiros 3x3 e 4x4
    tempos_minimax = []
    tempos_alpha_beta = []
    nos_minimax = []
    nos_alpha_beta = []
    
    for n, m in tamanhos_tabuleiro:
        # Criar tabuleiro vazio
        tabuleiro = [[" " for _ in range(m)] for _ in range(n)]
        
        # Colocar algumas jogadas aleatórias para criar um estado de meio-jogo
        jogadas = [(i, j) for i in range(n) for j in range(m)]
        random.shuffle(jogadas)
        for i, jogada in enumerate(jogadas[:n]):
            tabuleiro[jogada[0]][jogada[1]] = "X" if i % 2 == 0 else "O"
        
        # Medir desempenho Minimax
        tempo_inicio = time.time()
        _, _ = obter_jogada_computador(tabuleiro, "X", "O", usar_alpha_beta=False)
        tempos_minimax.append(time.time() - tempo_inicio)
        
        # Contar nós para Minimax
        contador_nos = contar_nos_visitados(tabuleiro, True, "X", "O", usar_alpha_beta=False)
        nos_minimax.append(contador_nos)
        
        # Medir desempenho Alpha-Beta
        tempo_inicio = time.time()
        _, _ = obter_jogada_computador(tabuleiro, "X", "O", usar_alpha_beta=True)
        tempos_alpha_beta.append(time.time() - tempo_inicio)
        
        # Contar nós para Alpha-Beta
        contador_nos = contar_nos_visitados(tabuleiro, True, "X", "O", usar_alpha_beta=True)
        nos_alpha_beta.append(contador_nos)
    
    # Plotar os resultados
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    etiquetas_tabuleiro = [f"{n}x{m}" for n, m in tamanhos_tabuleiro]
    
    ax1.bar(np.arange(len(tamanhos_tabuleiro)) - 0.2, tempos_minimax, width=0.4, label='Minimax')
    ax1.bar(np.arange(len(tamanhos_tabuleiro)) + 0.2, tempos_alpha_beta, width=0.4, label='Alpha-Beta')
    ax1.set_xticks(np.arange(len(tamanhos_tabuleiro)))
    ax1.set_xticklabels(etiquetas_tabuleiro)
    ax1.set_ylabel('Tempo de Execução (segundos)')
    ax1.set_title('Tempo de Execução dos Algoritmos')
    ax1.legend()
    
    ax2.bar(np.arange(len(tamanhos_tabuleiro)) - 0.2, nos_minimax, width=0.4, label='Minimax')
    ax2.bar(np.arange(len(tamanhos_tabuleiro)) + 0.2, nos_alpha_beta, width=0.4, label='Alpha-Beta')
    ax2.set_xticks(np.arange(len(tamanhos_tabuleiro)))
    ax2.set_xticklabels(etiquetas_tabuleiro)
    ax2.set_ylabel('Nós Visitados')
    ax2.set_title('Número de Nós Visitados')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('comparacao_algoritmos.png')
    plt.show()

def jogar_humano_vs_computador():
    """Modo de jogo: Humano vs Computador"""
    print("\nModo: Humano vs Computador")
    
    # Escolher algoritmo
    print("Escolha o algoritmo para o computador:")
    print("1. Minimax")
    print("2. Alpha-Beta")
    escolha_algo = input("Escolha (1-2): ")
    usar_alpha_beta = (escolha_algo == "2")
    
    # Escolher quem joga primeiro
    print("\nQuem joga primeiro?")
    print("1. Humano")
    print("2. Computador")
    escolha_primeiro = input("Escolha (1-2): ")
    
    jogador_humano = "X" if escolha_primeiro == "1" else "O"
    jogador_computador = "O" if jogador_humano == "X" else "X"
    jogador_atual = "X"  # X sempre joga primeiro
    
    # Criar tabuleiro vazio
    tabuleiro = [[" " for _ in range(3)] for _ in range(3)]
    
    # Loop de jogo
    while True:
        mostrar_tabuleiro(tabuleiro)
        
        if jogador_atual == jogador_humano:
            # Vez do humano
            print(f"A sua vez! É o jogador {jogador_humano}")
            try:
                jogada = input("Introduza a posição da jogada (1-9) ou 'q' para sair: ").lower()
                
                if jogada == 'q':
                    print("\nJogo terminado pelo jogador!")
                    return
                
                jogada = int(jogada) - 1
                linha, coluna = jogada // 3, jogada % 3
                
                if jogada < 0 or jogada > 8:
                    print("Por favor, escolha um número entre 1 e 9.")
                    continue
                
                if tabuleiro[linha][coluna] != " ":
                    print("Essa posição já está ocupada. Tente outra.")
                    continue
                
                tabuleiro[linha][coluna] = jogador_humano
                
            except ValueError:
                print("Por favor, introduza um número válido ou 'q'.")
                continue
                
        else:
            # Vez do computador
            print(f"Vez do computador ({jogador_computador})")
            
            # Aguardar pressionar Enter para continuar
            input("Prima ENTER para o computador jogar...")
            
            jogada, tempo_execucao = obter_jogada_computador(tabuleiro, jogador_computador, jogador_humano, usar_alpha_beta)
            tabuleiro[jogada[0]][jogada[1]] = jogador_computador
            
            nome_algoritmo = "Alpha-Beta" if usar_alpha_beta else "Minimax"
            print(f"O computador escolheu a posição {jogada[0]*3 + jogada[1] + 1}")
            print(f"Tempo de execução ({nome_algoritmo}): {tempo_execucao:.6f} segundos")
        
        # Verificar vencedor
        if verificar_vencedor(tabuleiro, jogador_atual):
            mostrar_tabuleiro(tabuleiro)
            if jogador_atual == jogador_humano:
                print("\nParabéns! Ganhou o jogo!")
            else:
                print("\nO computador ganhou!")
            break
        
        # Verificar empate
        if tabuleiro_cheio(tabuleiro):
            mostrar_tabuleiro(tabuleiro)
            print("\nEmpate!")
            break
        
        # Trocar jogador
        jogador_atual = "O" if jogador_atual == "X" else "X"

def jogar_computador_vs_computador():
    
    print("\nModo: Computador vs Computador")
    
    # Opção para escolher qual algoritmo começa
    print("Qual algoritmo deve jogar primeiro?")
    print("1. Minimax")
    print("2. Alpha-Beta")
    escolha_primeiro = input("Escolha (1-2): ")
    
    minimax_primeiro = (escolha_primeiro == "1")
    
    # Definir jogadores com base na escolha
    if minimax_primeiro:
        algoritmo_x = "Minimax"
        algoritmo_o = "Alpha-Beta"
        usar_alpha_beta_x = False
        usar_alpha_beta_o = True
    else:
        algoritmo_x = "Alpha-Beta"
        algoritmo_o = "Minimax"
        usar_alpha_beta_x = True
        usar_alpha_beta_o = False
    
    print(f"Jogador X usará {algoritmo_x}")
    print(f"Jogador O usará {algoritmo_o}")
    print("Prima ENTER para avançar para a próxima jogada...")
    
    # Criar tabuleiro vazio
    tabuleiro = [[" " for _ in range(3)] for _ in range(3)]
    
    # Computador X e O já definidos com base na escolha acima
    computador_x = "X"
    computador_o = "O"
    jogador_atual = "X"
    
    # Estatísticas
    tempos_minimax = []
    tempos_alpha_beta = []
    nos_minimax = []
    nos_alpha_beta = []
    jogadas_realizadas = []
    
    # Loop de jogo
    rodada = 1
    while True:
        mostrar_tabuleiro(tabuleiro)
        print(f"Vez do jogador {jogador_atual} ({algoritmo_x if jogador_atual == 'X' else algoritmo_o})")
        
        # Aguardar pressionar Enter para continuar
        input("Prima ENTER para fazer a próxima jogada...")
        
        # Obter jogada do computador
        if jogador_atual == computador_x:
            jogada, tempo_execucao = obter_jogada_computador(tabuleiro, computador_x, computador_o, usar_alpha_beta=usar_alpha_beta_x)
            algoritmo = algoritmo_x
            
            # Armazenar estatísticas no array correto
            if usar_alpha_beta_x:
                tempos_alpha_beta.append(tempo_execucao)
                # Contar nós explorados para esta jogada
                copia_tabuleiro = [linha[:] for linha in tabuleiro]
                nos = contar_nos_visitados(copia_tabuleiro, True, computador_x, computador_o, usar_alpha_beta=True)
                nos_alpha_beta.append(nos)
            else:
                tempos_minimax.append(tempo_execucao)
                # Contar nós explorados para esta jogada
                copia_tabuleiro = [linha[:] for linha in tabuleiro]
                nos = contar_nos_visitados(copia_tabuleiro, True, computador_x, computador_o, usar_alpha_beta=False)
                nos_minimax.append(nos)
            
        else:
            jogada, tempo_execucao = obter_jogada_computador(tabuleiro, computador_o, computador_x, usar_alpha_beta=usar_alpha_beta_o)
            algoritmo = algoritmo_o
            
            # Armazenar estatísticas no array correto
            if usar_alpha_beta_o:
                tempos_alpha_beta.append(tempo_execucao)
                # Contar nós explorados para esta jogada
                copia_tabuleiro = [linha[:] for linha in tabuleiro]
                nos = contar_nos_visitados(copia_tabuleiro, True, computador_o, computador_x, usar_alpha_beta=True)
                nos_alpha_beta.append(nos)
            else:
                tempos_minimax.append(tempo_execucao)
                # Contar nós explorados para esta jogada
                copia_tabuleiro = [linha[:] for linha in tabuleiro]
                nos = contar_nos_visitados(copia_tabuleiro, True, computador_o, computador_x, usar_alpha_beta=False)
                nos_minimax.append(nos)
        
        tabuleiro[jogada[0]][jogada[1]] = jogador_atual
        jogadas_realizadas.append(rodada)
        
        print(f"Computador {jogador_atual} ({algoritmo}) escolheu a posição {jogada[0]*3 + jogada[1] + 1}")
        print(f"Tempo de execução: {tempo_execucao:.6f} segundos")
        
        # Verificar vencedor
        if verificar_vencedor(tabuleiro, jogador_atual):
            mostrar_tabuleiro(tabuleiro)
            print(f"\nComputador {jogador_atual} ({algoritmo}) ganhou!")
            break
        
        # Verificar empate
        if tabuleiro_cheio(tabuleiro):
            mostrar_tabuleiro(tabuleiro)
            print("\nEmpate!")
            break
        
        # Trocar jogador
        jogador_atual = "O" if jogador_atual == "X" else "X"
        rodada += 1
    
    # Mostrar estatísticas de desempenho detalhadas com gráficos
    if tempos_minimax and tempos_alpha_beta:
        print("\nEstatísticas de Desempenho:")
        print(f"Tempo médio Minimax: {sum(tempos_minimax)/len(tempos_minimax):.6f} segundos")
        print(f"Tempo médio Alpha-Beta: {sum(tempos_alpha_beta)/len(tempos_alpha_beta):.6f} segundos")
        print(f"Aceleração Alpha-Beta: {sum(tempos_minimax)/sum(tempos_alpha_beta):.2f}x")
        
        if nos_minimax and nos_alpha_beta:
            print(f"\nNós médios explorados Minimax: {sum(nos_minimax)/len(nos_minimax):.1f}")
            print(f"Nós médios explorados Alpha-Beta: {sum(nos_alpha_beta)/len(nos_alpha_beta):.1f}")
            print(f"Redução de nós com Alpha-Beta: {(1 - sum(nos_alpha_beta)/sum(nos_minimax))*100:.2f}%")
        
        # Criar visualizações
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Gráfico de tempo de execução por jogada
        ax1.plot(jogadas_realizadas[:len(tempos_minimax)], tempos_minimax, 
                 'b-o', label='Minimax')
        ax1.plot(jogadas_realizadas[:len(tempos_alpha_beta)], tempos_alpha_beta, 
                 'r-o', label='Alpha-Beta')
        ax1.set_xlabel('Número da Jogada')
        ax1.set_ylabel('Tempo de Execução (segundos)')
        ax1.set_title('Tempo de Execução por Jogada')
        ax1.legend()
        ax1.grid(True)
        
        # Gráfico de nós visitados por jogada
        if nos_minimax and nos_alpha_beta:
            ax2.plot(jogadas_realizadas[:len(nos_minimax)], nos_minimax, 
                     'b-o', label='Minimax')
            ax2.plot(jogadas_realizadas[:len(nos_alpha_beta)], nos_alpha_beta, 
                     'r-o', label='Alpha-Beta')
            ax2.set_xlabel('Número da Jogada')
            ax2.set_ylabel('Nós Visitados')
            ax2.set_title('Nós Visitados por Jogada')
            ax2.legend()
            ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig('desempenho_jogo.png')
        print("\nGráfico de desempenho guardado como 'desempenho_jogo.png'")
        plt.show()
        
        # Comparação de barras (como na opção 3)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        algoritmos = ['Minimax', 'Alpha-Beta']
        tempos_medios = [sum(tempos_minimax)/len(tempos_minimax), 
                          sum(tempos_alpha_beta)/len(tempos_alpha_beta)]
        
        ax1.bar([0, 1], tempos_medios, width=0.4)
        ax1.set_xticks([0, 1])
        ax1.set_xticklabels(algoritmos)
        ax1.set_ylabel('Tempo Médio (segundos)')
        ax1.set_title('Tempo de Execução Médio')
        
        if nos_minimax and nos_alpha_beta:
            nos_medios = [sum(nos_minimax)/len(nos_minimax), 
                           sum(nos_alpha_beta)/len(nos_alpha_beta)]
            
            ax2.bar([0, 1], nos_medios, width=0.4)
            ax2.set_xticks([0, 1])
            ax2.set_xticklabels(algoritmos)
            ax2.set_ylabel('Nós Visitados (média)')
            ax2.set_title('Nós Visitados Médios')
        
        plt.tight_layout()
        plt.savefig('comparacao_algoritmos_jogo.png')
        print("Comparação de algoritmos guardada como 'comparacao_algoritmos_jogo.png'")
        plt.show()

def visualizar_exploracao_tabuleiro():
 
    print("\nVisualizando a exploração do tabuleiro...")
    
    # Criar um tabuleiro de exemplo de meio-jogo
    tabuleiro = [
        [" ", "X", "O"],
        ["X", "O", " "],
        [" ", " ", " "]
    ]
    
    print("Tabuleiro de exemplo:")
    mostrar_tabuleiro(tabuleiro)
    
    # Contar nós explorados por cada algoritmo
    nos_minimax = contar_nos_visitados(tabuleiro, True, "X", "O", usar_alpha_beta=False)
    nos_alpha_beta = contar_nos_visitados(tabuleiro, True, "X", "O", usar_alpha_beta=True)
    
    print(f"Minimax explora {nos_minimax} nós")
    print(f"Alpha-Beta explora {nos_alpha_beta} nós")
    print(f"Eficácia da poda Alpha-Beta: {(1 - nos_alpha_beta/nos_minimax)*100:.2f}% de redução")

def principal():
    """Função principal para executar o programa"""
    while True:
        print("\nJogo do Galo com Algoritmos de MiniMax e Alpha-Beta")
        print("1. Jogar contra o computador")
        print("2. Ver computador vs computador")
        print("3. Comparar desempenho dos algoritmos")
        print("4. Visualizar exploração do tabuleiro")
        print("5. Sair")
        
        escolha = input("Escolha uma opção (1-5): ")
        
        if escolha == "1":
            jogar_humano_vs_computador()
        elif escolha == "2":
            jogar_computador_vs_computador()
        elif escolha == "3":
            comparar_desempenho_algoritmos()
        elif escolha == "4":
            visualizar_exploracao_tabuleiro()
        elif escolha == "5":
            print("\nObrigado por jogar!")
            break
        else:
            print("Escolha inválida. Tente novamente.")

if __name__ == "__main__":
    principal()