import random
import time
import matplotlib.pyplot as plt
import numpy as np

def mostrar_tabuleiro(tabuleiro):
    """Mostra o estado atual do tabuleiro"""
    print("-------------")  # Imprime a linha superior do tabuleiro
    for linha in tabuleiro:  # Itera por cada linha do tabuleiro
        print("| " + " | ".join(linha) + " |")  # Imprime cada célula da linha com separadores
        print("-------------")  # Imprime linha divisória após cada linha do tabuleiro

def verificar_vencedor(tabuleiro, jogador):
    """Verifica se o jogador especificado venceu"""
    # Verificar linhas - examina se alguma linha está preenchida com o mesmo símbolo
    for linha in tabuleiro:
        if all(celula == jogador for celula in linha):  # Verifica se todas as células da linha têm o símbolo do jogador
            return True
    
    # Verificar colunas - examina se alguma coluna está preenchida com o mesmo símbolo
    for col in range(3):  # Itera pelas 3 colunas do tabuleiro
        if all(tabuleiro[linha][col] == jogador for linha in range(3)):  # Verifica se todas as células da coluna têm o símbolo do jogador
            return True
    
    # Verificar diagonal principal (de cima-esquerda a baixo-direita)
    if all(tabuleiro[i][i] == jogador for i in range(3)):  # Verifica as células [0][0], [1][1], [2][2]
        return True
    
    # Verificar diagonal secundária (de cima-direita a baixo-esquerda)
    if all(tabuleiro[i][2-i] == jogador for i in range(3)):  # Verifica as células [0][2], [1][1], [2][0]
        return True
    
    # Se nenhuma condição de vitória foi satisfeita
    return False

def tabuleiro_cheio(tabuleiro):
    """Verifica se o tabuleiro está cheio (empate)"""
    return all(celula != " " for linha in tabuleiro for celula in linha)  # Retorna True se todas as células estão preenchidas

def obter_jogadas_possiveis(tabuleiro):
    """Retorna uma lista de jogadas disponíveis como tuplos (linha, coluna)"""
    jogadas = []  # Inicializa uma lista vazia para armazenar as jogadas possíveis
    for i in range(3):  # Itera pelas linhas do tabuleiro
        for j in range(3):  # Itera pelas colunas do tabuleiro
            if tabuleiro[i][j] == " ":  # Verifica se a célula está vazia
                jogadas.append((i, j))  # Adiciona a coordenada da célula vazia à lista de jogadas
    return jogadas  # Retorna a lista completa de jogadas possíveis

def minimax(tabuleiro, profundidade, e_maximizador, jogador, oponente):
    """Implementa o algoritmo Minimax para escolher a melhor jogada"""
    # Casos base: verificar estados terminais
    if verificar_vencedor(tabuleiro, jogador):
        return 10 - profundidade  # Vitória, pontuação maior para vitórias mais rápidas
    if verificar_vencedor(tabuleiro, oponente):
        return profundidade - 10  # Derrota, pontuação maior para derrotas mais lentas
    if tabuleiro_cheio(tabuleiro):
        return 0  # Empate
    
    # Casos recursivos - exploração de árvore de possibilidades
    if e_maximizador:  # Se é o turno maximizador (computador)
        melhor_pontuacao = float('-inf')  # Inicializa com o pior valor possível
        for jogada in obter_jogadas_possiveis(tabuleiro):  # Itera por todas as jogadas possíveis
            tabuleiro[jogada[0]][jogada[1]] = jogador  # Simula a jogada do jogador atual
            pontuacao = minimax(tabuleiro, profundidade + 1, False, jogador, oponente)  # Avalia recursivamente o estado resultante
            tabuleiro[jogada[0]][jogada[1]] = " "  # Desfaz a jogada para explorar outras possibilidades
            melhor_pontuacao = max(pontuacao, melhor_pontuacao)  # Atualiza a melhor pontuação encontrada
        return melhor_pontuacao  # Retorna a melhor pontuação possível para o maximizador
    else:  # Se é o turno minimizador (oponente)
        melhor_pontuacao = float('inf')  # Inicializa com o melhor valor possível
        for jogada in obter_jogadas_possiveis(tabuleiro):  # Itera por todas as jogadas possíveis
            tabuleiro[jogada[0]][jogada[1]] = oponente  # Simula a jogada do oponente
            pontuacao = minimax(tabuleiro, profundidade + 1, True, jogador, oponente)  # Avalia recursivamente o estado resultante
            tabuleiro[jogada[0]][jogada[1]] = " "  # Desfaz a jogada para explorar outras possibilidades
            melhor_pontuacao = min(pontuacao, melhor_pontuacao)  # Atualiza a melhor pontuação encontrada
        return melhor_pontuacao  # Retorna a melhor pontuação possível para o minimizador

def alpha_beta(tabuleiro, profundidade, e_maximizador, jogador, oponente, alpha, beta):
    """Implementa o algoritmo Minimax com poda Alpha-Beta para melhorar a eficiência"""
    # Casos base: verificar estados terminais
    if verificar_vencedor(tabuleiro, jogador):
        return 10 - profundidade  # Vitória, pontuação maior para vitórias mais rápidas
    if verificar_vencedor(tabuleiro, oponente):
        return profundidade - 10  # Derrota, pontuação maior para derrotas mais lentas
    if tabuleiro_cheio(tabuleiro):
        return 0  # Empate

    # Casos recursivos com poda alpha-beta
    if e_maximizador:  # Se é o turno maximizador (computador)
        melhor_pontuacao = float('-inf')  # Inicializa com o pior valor possível
        for jogada in obter_jogadas_possiveis(tabuleiro):  # Itera por todas as jogadas possíveis
            tabuleiro[jogada[0]][jogada[1]] = jogador  # Simula a jogada do jogador atual
            pontuacao = alpha_beta(tabuleiro, profundidade + 1, False, jogador, oponente, alpha, beta)  # Avalia recursivamente com poda
            tabuleiro[jogada[0]][jogada[1]] = " "  # Desfaz a jogada
            melhor_pontuacao = max(pontuacao, melhor_pontuacao)  # Atualiza a melhor pontuação
            alpha = max(alpha, pontuacao)  # Atualiza o valor de alpha
            if beta <= alpha:  # Condição de poda - se beta <= alpha, o minimizador nunca escolherá este ramo
                break  # Corte beta - poda o resto da árvore
        return melhor_pontuacao  # Retorna a melhor pontuação possível para o maximizador
    else:  # Se é o turno minimizador (oponente)
        melhor_pontuacao = float('inf')  # Inicializa com o melhor valor possível
        for jogada in obter_jogadas_possiveis(tabuleiro):  # Itera por todas as jogadas possíveis
            tabuleiro[jogada[0]][jogada[1]] = oponente  # Simula a jogada do oponente
            pontuacao = alpha_beta(tabuleiro, profundidade + 1, True, jogador, oponente, alpha, beta)  # Avalia recursivamente com poda
            tabuleiro[jogada[0]][jogada[1]] = " "  # Desfaz a jogada
            melhor_pontuacao = min(pontuacao, melhor_pontuacao)  # Atualiza a melhor pontuação
            beta = min(beta, pontuacao)  # Atualiza o valor de beta
            if beta <= alpha:  # Condição de poda - se beta <= alpha, o maximizador nunca escolherá este ramo
                break  # Corte alpha - poda o resto da árvore
        return melhor_pontuacao  # Retorna a melhor pontuação possível para o minimizador

def obter_jogada_computador(tabuleiro, computador, humano, usar_alpha_beta=False):
    """Determina a melhor jogada para o computador usando Minimax ou Alpha-Beta"""
    
    melhor_pontuacao = float('-inf')  # Inicializa com o pior valor possível
    melhor_jogada = None  # Inicializa a melhor jogada como None
    jogadas_possiveis = obter_jogadas_possiveis(tabuleiro)  # Obtém todas as jogadas possíveis no estado atual

    # Para a primeira jogada, escolher aleatoriamente por eficiência
    if len(jogadas_possiveis) == 9:  # Se todas as 9 células estão vazias (início do jogo)
        return random.choice(jogadas_possiveis), 0.0  # Retorna uma jogada aleatória e tempo zero

    # Medir tempo de execução
    tempo_inicio = time.time()  # Registra o tempo de início
    
    # Avaliar cada jogada possível
    for jogada in jogadas_possiveis:  # Itera por todas as jogadas possíveis
        tabuleiro[jogada[0]][jogada[1]] = computador  # Simula a jogada do computador
        if usar_alpha_beta:  # Se usar Alpha-Beta
            pontuacao = alpha_beta(tabuleiro, 0, False, computador, humano, float('-inf'), float('inf'))  # Avalia com Alpha-Beta
        else:  # Se usar Minimax padrão
            pontuacao = minimax(tabuleiro, 0, False, computador, humano)  # Avalia com Minimax
        tabuleiro[jogada[0]][jogada[1]] = " "  # Desfaz a jogada

        # Atualiza a melhor jogada se encontrar uma pontuação melhor
        if pontuacao > melhor_pontuacao:  # Se a pontuação atual é melhor que a melhor encontrada
            melhor_pontuacao = pontuacao  # Atualiza a melhor pontuação
            melhor_jogada = jogada  # Atualiza a melhor jogada
            
    tempo_fim = time.time()  # Registra o tempo de fim
    tempo_execucao = tempo_fim - tempo_inicio  # Calcula o tempo total de execução
    
    return melhor_jogada, tempo_execucao  # Retorna a melhor jogada e o tempo de execução

def contar_nos_visitados(tabuleiro, e_maximizador, jogador, oponente, usar_alpha_beta=False, alpha=float('-inf'), beta=float('inf')):
    """Conta o número de nós (estados do jogo) explorados pelos algoritmos"""
   
    # Casos base: verificar estados terminais
    if verificar_vencedor(tabuleiro, jogador) or verificar_vencedor(tabuleiro, oponente) or tabuleiro_cheio(tabuleiro):
        return 1  # Nó terminal conta como 1
    
    nos = 1  # Contar nó atual
    
    # Casos recursivos - exploração da árvore de possibilidades
    for jogada in obter_jogadas_possiveis(tabuleiro):  # Para cada jogada possível
        tabuleiro[jogada[0]][jogada[1]] = jogador if e_maximizador else oponente  # Simula jogada do jogador atual
        
        if usar_alpha_beta:  # Se usar Alpha-Beta
            proxima_pontuacao = alpha_beta(tabuleiro, 0, not e_maximizador, jogador, oponente, alpha, beta)  # Calcula pontuação
            if e_maximizador:  # Se é maximizador
                alpha = max(alpha, proxima_pontuacao)  # Atualiza alpha
                if beta <= alpha:  # Condição de poda
                    tabuleiro[jogada[0]][jogada[1]] = " "  # Desfaz jogada
                    break  # Poda - não explora mais nós
            else:  # Se é minimizador
                beta = min(beta, proxima_pontuacao)  # Atualiza beta
                if beta <= alpha:  # Condição de poda
                    tabuleiro[jogada[0]][jogada[1]] = " "  # Desfaz jogada
                    break  # Poda - não explora mais nós
        
        # Chamada recursiva para contar nós de subárvores
        nos += contar_nos_visitados(
            tabuleiro, 
            not e_maximizador,  # Alterna entre maximizador e minimizador
            jogador, 
            oponente, 
            usar_alpha_beta,
            alpha,
            beta
        )
        
        tabuleiro[jogada[0]][jogada[1]] = " "  # Desfaz a jogada
    
    return nos  # Retorna número total de nós visitados

def comparar_desempenho_algoritmos():
    """Compara o desempenho dos algoritmos Minimax e Alpha-Beta em diferentes tamanhos de tabuleiro"""
    
    tamanhos_tabuleiro = [(i, i) for i in range(3, 5)]  # Define tabuleiros 3x3 e 4x4 para teste
    tempos_minimax = []  # Lista para armazenar tempos do Minimax
    tempos_alpha_beta = []  # Lista para armazenar tempos do Alpha-Beta
    nos_minimax = []  # Lista para armazenar nós visitados pelo Minimax
    nos_alpha_beta = []  # Lista para armazenar nós visitados pelo Alpha-Beta
    
    # Para cada tamanho de tabuleiro
    for n, m in tamanhos_tabuleiro:
        # Criar tabuleiro vazio
        tabuleiro = [[" " for _ in range(m)] for _ in range(n)]  # Cria tabuleiro n x m
        
        # Colocar algumas jogadas aleatórias para criar um estado de meio-jogo
        jogadas = [(i, j) for i in range(n) for j in range(m)]  # Lista todas as posições possíveis
        random.shuffle(jogadas)  # Embaralha as posições
        for i, jogada in enumerate(jogadas[:n]):  # Usa as primeiras n posições
            tabuleiro[jogada[0]][jogada[1]] = "X" if i % 2 == 0 else "O"  # Alterna entre X e O
        
        # Medir desempenho Minimax
        tempo_inicio = time.time()  # Registra tempo inicial
        _, _ = obter_jogada_computador(tabuleiro, "X", "O", usar_alpha_beta=False)  # Executa Minimax
        tempos_minimax.append(time.time() - tempo_inicio)  # Registra tempo total
        
        # Contar nós para Minimax
        contador_nos = contar_nos_visitados(tabuleiro, True, "X", "O", usar_alpha_beta=False)  # Conta nós do Minimax
        nos_minimax.append(contador_nos)  # Armazena contagem
        
        # Medir desempenho Alpha-Beta
        tempo_inicio = time.time()  # Registra tempo inicial
        _, _ = obter_jogada_computador(tabuleiro, "X", "O", usar_alpha_beta=True)  # Executa Alpha-Beta
        tempos_alpha_beta.append(time.time() - tempo_inicio)  # Registra tempo total
        
        # Contar nós para Alpha-Beta
        contador_nos = contar_nos_visitados(tabuleiro, True, "X", "O", usar_alpha_beta=True)  # Conta nós do Alpha-Beta
        nos_alpha_beta.append(contador_nos)  # Armazena contagem
    
    # Plotar os resultados
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))  # Cria figura com dois gráficos lado a lado
    
    etiquetas_tabuleiro = [f"{n}x{m}" for n, m in tamanhos_tabuleiro]  # Cria etiquetas para os tamanhos de tabuleiro
    
    # Gráfico de tempos
    ax1.bar(np.arange(len(tamanhos_tabuleiro)) - 0.2, tempos_minimax, width=0.4, label='Minimax')  # Barras de tempo Minimax
    ax1.bar(np.arange(len(tamanhos_tabuleiro)) + 0.2, tempos_alpha_beta, width=0.4, label='Alpha-Beta')  # Barras de tempo Alpha-Beta
    ax1.set_xticks(np.arange(len(tamanhos_tabuleiro)))  # Define posições dos ticks
    ax1.set_xticklabels(etiquetas_tabuleiro)  # Define etiquetas dos ticks
    ax1.set_ylabel('Tempo de Execução (segundos)')  # Define título do eixo Y
    ax1.set_title('Tempo de Execução dos Algoritmos')  # Define título do gráfico
    ax1.legend()  # Adiciona legenda
    
    # Gráfico de nós visitados
    ax2.bar(np.arange(len(tamanhos_tabuleiro)) - 0.2, nos_minimax, width=0.4, label='Minimax')  # Barras de nós Minimax
    ax2.bar(np.arange(len(tamanhos_tabuleiro)) + 0.2, nos_alpha_beta, width=0.4, label='Alpha-Beta')  # Barras de nós Alpha-Beta
    ax2.set_xticks(np.arange(len(tamanhos_tabuleiro)))  # Define posições dos ticks
    ax2.set_xticklabels(etiquetas_tabuleiro)  # Define etiquetas dos ticks
    ax2.set_ylabel('Nós Visitados')  # Define título do eixo Y
    ax2.set_title('Número de Nós Visitados')  # Define título do gráfico
    ax2.legend()  # Adiciona legenda
    
    plt.tight_layout()  # Ajusta layout
    plt.savefig('comparacao_algoritmos.png')  # Salva o gráfico como imagem
    plt.show()  # Mostra o gráfico na tela

def jogar_humano_vs_computador():
    """Modo de jogo: Humano vs Computador"""
    print("\nModo: Humano vs Computador")
    
    # Escolher algoritmo
    print("Escolha o algoritmo para o computador:")
    print("1. Minimax")
    print("2. Alpha-Beta")
    escolha_algo = input("Escolha (1-2): ")  # Obtém escolha do usuário
    usar_alpha_beta = (escolha_algo == "2")  # Define se usar Alpha-Beta baseado na escolha
    
    # Escolher quem joga primeiro
    print("\nQuem joga primeiro?")
    print("1. Humano")
    print("2. Computador")
    escolha_primeiro = input("Escolha (1-2): ")  # Obtém escolha do usuário
    
    jogador_humano = "X" if escolha_primeiro == "1" else "O"  # Define símbolo do humano baseado em quem começa
    jogador_computador = "O" if jogador_humano == "X" else "X"  # Define símbolo do computador (oposto do humano)
    jogador_atual = "X"  # X sempre joga primeiro conforme regras do jogo
    
    # Criar tabuleiro vazio
    tabuleiro = [[" " for _ in range(3)] for _ in range(3)]  # Inicializa tabuleiro 3x3 vazio
    
    # Loop de jogo
    while True:
        mostrar_tabuleiro(tabuleiro)  # Mostra estado atual do tabuleiro
        
        if jogador_atual == jogador_humano:  # Se é vez do humano
            # Vez do humano
            print(f"A sua vez! É o jogador {jogador_humano}")
            try:
                jogada = input("Introduza a posição da jogada (1-9) ou 'q' para sair: ").lower()  # Obtém entrada do usuário
                
                if jogada == 'q':  # Se usuário quer sair
                    print("\nJogo terminado pelo jogador!")
                    return  # Termina o jogo
                
                jogada = int(jogada) - 1  # Converte entrada para índice (0-8)
                linha, coluna = jogada // 3, jogada % 3  # Converte índice para coordenadas de linha/coluna
                
                if jogada < 0 or jogada > 8:  # Verifica se jogada está no intervalo válido
                    print("Por favor, escolha um número entre 1 e 9.")
                    continue  # Pede nova entrada
                
                if tabuleiro[linha][coluna] != " ":  # Verifica se posição já está ocupada
                    print("Essa posição já está ocupada. Tente outra.")
                    continue  # Pede nova entrada
                
                tabuleiro[linha][coluna] = jogador_humano  # Efetua a jogada do humano
                
            except ValueError:  # Se entrada não for válida
                print("Por favor, introduza um número válido ou 'q'.")
                continue  # Pede nova entrada
                
        else:  # Se é vez do computador
            # Vez do computador
            print(f"Vez do computador ({jogador_computador})")
            
            # Aguardar pressionar Enter para continuar
            input("Prima ENTER para o computador jogar...")  # Pausa para o usuário ver o tabuleiro
            
            jogada, tempo_execucao = obter_jogada_computador(tabuleiro, jogador_computador, jogador_humano, usar_alpha_beta)  # Obtém jogada do computador
            tabuleiro[jogada[0]][jogada[1]] = jogador_computador  # Efetua a jogada do computador
            
            nome_algoritmo = "Alpha-Beta" if usar_alpha_beta else "Minimax"  # Nome do algoritmo usado
            print(f"O computador escolheu a posição {jogada[0]*3 + jogada[1] + 1}")  # Mostra posição escolhida
            print(f"Tempo de execução ({nome_algoritmo}): {tempo_execucao:.6f} segundos")  # Mostra tempo de execução
        
        # Verificar vencedor
        if verificar_vencedor(tabuleiro, jogador_atual):  # Se jogador atual venceu
            mostrar_tabuleiro(tabuleiro)  # Mostra estado final do tabuleiro
            if jogador_atual == jogador_humano:  # Se humano venceu
                print("\nParabéns! Ganhou o jogo!")
            else:  # Se computador venceu
                print("\nO computador ganhou!")
            break  # Termina o jogo
        
        # Verificar empate
        if tabuleiro_cheio(tabuleiro):  # Se tabuleiro está cheio sem vencedor
            mostrar_tabuleiro(tabuleiro)  # Mostra estado final do tabuleiro
            print("\nEmpate!")
            break  # Termina o jogo
        
        # Trocar jogador
        jogador_atual = "O" if jogador_atual == "X" else "X"  # Alterna entre X e O

def jogar_computador_vs_computador():
    """Modo de jogo: Computador vs Computador - compara os algoritmos Minimax e Alpha-Beta"""
    
    print("\nModo: Computador vs Computador")
    
    # Opção para escolher qual algoritmo começa
    print("Qual algoritmo deve jogar primeiro?")
    print("1. Minimax")
    print("2. Alpha-Beta")
    escolha_primeiro = input("Escolha (1-2): ")  # Obtém escolha do usuário
    
    minimax_primeiro = (escolha_primeiro == "1")  # Define se Minimax joga primeiro
    
    # Definir jogadores com base na escolha
    if minimax_primeiro:  # Se Minimax joga primeiro
        algoritmo_x = "Minimax"  # X usa Minimax
        algoritmo_o = "Alpha-Beta"  # O usa Alpha-Beta
        usar_alpha_beta_x = False  # X não usa poda Alpha-Beta
        usar_alpha_beta_o = True  # O usa poda Alpha-Beta
    else:  # Se Alpha-Beta joga primeiro
        algoritmo_x = "Alpha-Beta"  # X usa Alpha-Beta
        algoritmo_o = "Minimax"  # O usa Minimax
        usar_alpha_beta_x = True  # X usa poda Alpha-Beta
        usar_alpha_beta_o = False  # O não usa poda Alpha-Beta
    
    print(f"Jogador X usará {algoritmo_x}")
    print(f"Jogador O usará {algoritmo_o}")
    print("Prima ENTER para avançar para a próxima jogada...")
    
    # Criar tabuleiro vazio
    tabuleiro = [[" " for _ in range(3)] for _ in range(3)]  # Inicializa tabuleiro 3x3 vazio
    
    # Computador X e O já definidos com base na escolha acima
    computador_x = "X"
    computador_o = "O"
    jogador_atual = "X"  # X sempre começa
    
    # Estatísticas
    tempos_minimax = []  # Lista para armazenar tempos do Minimax
    tempos_alpha_beta = []  # Lista para armazenar tempos do Alpha-Beta
    nos_minimax = []  # Lista para armazenar nós visitados pelo Minimax
    nos_alpha_beta = []  # Lista para armazenar nós visitados pelo Alpha-Beta
    jogadas_realizadas = []  # Lista para armazenar número das jogadas
    
    # Loop de jogo
    rodada = 1  # Contador de rodadas
    while True:
        mostrar_tabuleiro(tabuleiro)  # Mostra estado atual do tabuleiro
        print(f"Vez do jogador {jogador_atual} ({algoritmo_x if jogador_atual == 'X' else algoritmo_o})")
        
        # Aguardar pressionar Enter para continuar
        input("Prima ENTER para fazer a próxima jogada...")  # Pausa para o usuário ver o tabuleiro
        
        # Obter jogada do computador
        if jogador_atual == computador_x:  # Se é vez do jogador X
            jogada, tempo_execucao = obter_jogada_computador(tabuleiro, computador_x, computador_o, usar_alpha_beta=usar_alpha_beta_x)  # Obtém jogada de X
            algoritmo = algoritmo_x  # Nome do algoritmo usado por X
            
            # Armazenar estatísticas no array correto
            if usar_alpha_beta_x:  # Se X usa Alpha-Beta
                tempos_alpha_beta.append(tempo_execucao)  # Registra tempo de Alpha-Beta
                # Contar nós explorados para esta jogada
                copia_tabuleiro = [linha[:] for linha in tabuleiro]  # Cria cópia do tabuleiro para contagem
                nos = contar_nos_visitados(copia_tabuleiro, True, computador_x, computador_o, usar_alpha_beta=True)  # Conta nós
                nos_alpha_beta.append(nos)  # Registra contagem
            else:  # Se X usa Minimax
                tempos_minimax.append(tempo_execucao)  # Registra tempo de Minimax
                # Contar nós explorados para esta jogada
                copia_tabuleiro = [linha[:] for linha in tabuleiro]  # Cria cópia do tabuleiro para contagem
                nos = contar_nos_visitados(copia_tabuleiro, True, computador_x, computador_o, usar_alpha_beta=False)  # Conta nós
                nos_minimax.append(nos)  # Registra contagem
            
        else:  # Se é vez do jogador O
            jogada, tempo_execucao = obter_jogada_computador(tabuleiro, computador_o, computador_x, usar_alpha_beta=usar_alpha_beta_o)  # Obtém jogada de O
            algoritmo = algoritmo_o  # Nome do algoritmo usado por O
            
            # Armazenar estatísticas no array correto
            if usar_alpha_beta_o:  # Se O usa Alpha-Beta
                tempos_alpha_beta.append(tempo_execucao)  # Registra tempo de Alpha-Beta
                # Contar nós explorados para esta jogada
                copia_tabuleiro = [linha[:] for linha in tabuleiro]  # Cria cópia do tabuleiro para contagem
                nos = contar_nos_visitados(copia_tabuleiro, True, computador_o, computador_x, usar_alpha_beta=True)  # Conta nós
                nos_alpha_beta.append(nos)  # Registra contagem
            else:  # Se O usa Minimax
                tempos_minimax.append(tempo_execucao)  # Registra tempo de Minimax
                # Contar nós explorados para esta jogada
                copia_tabuleiro = [linha[:] for linha in tabuleiro]  # Cria cópia do tabuleiro para contagem
                nos = contar_nos_visitados(copia_tabuleiro, True, computador_o, computador_x, usar_alpha_beta=False)  # Conta nós
                nos_minimax.append(nos)  # Registra contagem
        
        tabuleiro[jogada[0]][jogada[1]] = jogador_atual  # Efetua a jogada
        jogadas_realizadas.append(rodada)  # Registra número da rodada
        
        print(f"Computador {jogador_atual} ({algoritmo}) escolheu a posição {jogada[0]*3 + jogada[1] + 1}")  # Mostra posição escolhida
        print(f"Tempo de execução: {tempo_execucao:.6f} segundos")  # Mostra tempo de execução
        
        # Verificar vencedor
        if verificar_vencedor(tabuleiro, jogador_atual):  # Se jogador atual venceu
            mostrar_tabuleiro(tabuleiro)  # Mostra estado final do tabuleiro
            print(f"\nComputador {jogador_atual} ({algoritmo}) ganhou!")
            break  # Termina o jogo
        
        # Verificar empate
        if tabuleiro_cheio(tabuleiro):  # Se tabuleiro está cheio sem vencedor
            mostrar_tabuleiro(tabuleiro)  # Mostra estado final do tabuleiro
            print("\nEmpate!")
            break  # Termina o jogo
        
        # Trocar jogador
        jogador_atual = "O" if jogador_atual == "X" else "X"  # Alterna entre X e O
        rodada += 1  # Incrementa contador de rodadas
    
    # Mostrar estatísticas de desempenho detalhadas com gráficos
    if tempos_minimax and tempos_alpha_beta:  # Se ambos os algoritmos foram usados
        print("\nEstatísticas de Desempenho:")
        print(f"Tempo médio Minimax: {sum(tempos_minimax)/len(tempos_minimax):.6f} segundos")  # Média de tempo Minimax
        print(f"Tempo médio Alpha-Beta: {sum(tempos_alpha_beta)/len(tempos_alpha_beta):.6f} segundos")  # Média de tempo Alpha-Beta
        print(f"Aceleração Alpha-Beta: {sum(tempos_minimax)/sum(tempos_alpha_beta):.2f}x")  # Razão de tempos
        
        if nos_minimax and nos_alpha_beta:  # Se contagens de nós estão disponíveis
            print(f"\nNós médios explorados Minimax: {sum(nos_minimax)/len(nos_minimax):.1f}")  # Média de nós Minimax
            print(f"Nós médios explorados Alpha-Beta: {sum(nos_alpha_beta)/len(nos_alpha_beta):.1f}")  # Média de nós Alpha-Beta
            print(f"Redução de nós com Alpha-Beta: {(1 - sum(nos_alpha_beta)/sum(nos_minimax))*100:.2f}%")  # Percentual de redução
        
        # Criar visualizações - Gráficos de linha
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))  # Cria figura com dois gráficos lado a lado
        
        # Gráfico de tempo de execução por jogada
        ax1.plot(jogadas_realizadas[:len(tempos_minimax)], tempos_minimax, 
                 'b-o', label='Minimax')  # Linha de tempo Minimax
        ax1.plot(jogadas_realizadas[:len(tempos_alpha_beta)], tempos_alpha_beta, 
                 'r-o', label='Alpha-Beta')  # Linha de tempo Alpha-Beta
        ax1.set_xlabel('Número da Jogada')  # Etiqueta eixo X
        ax1.set_ylabel('Tempo de Execução (segundos)')  # Etiqueta eixo Y
        ax1.set_title('Tempo de Execução por Jogada')  # Título do gráfico
        ax1.legend()  # Adiciona legenda
        ax1.grid(True)  # Adiciona grade
        
        # Gráfico de nós visitados por jogada
        if nos_minimax and nos_alpha_beta:  # Se contagens de nós estão disponíveis
            ax2.plot(jogadas_realizadas[:len(nos_minimax)], nos_minimax, 
                     'b-o', label='Minimax')  # Linha de nós Minimax
            ax2.plot(jogadas_realizadas[:len(nos_alpha_beta)], nos_alpha_beta, 
                     'r-o', label='Alpha-Beta')  # Linha de nós Alpha-Beta
            ax2.set_xlabel('Número da Jogada')  # Etiqueta eixo X
            ax2.set_ylabel('Nós Visitados')  # Etiqueta eixo Y
            ax2.set_title('Nós Visitados por Jogada')  # Título do gráfico
            ax2.legend()  # Adiciona legenda
            ax2.grid(True)  # Adiciona grade
        
        plt.tight_layout()  # Ajusta layout
        plt.savefig('desempenho_jogo.png')  # Salva o gráfico como imagem
        print("\nGráfico de desempenho guardado como 'desempenho_jogo.png'")
        plt.show()  # Mostra o gráfico na tela
        
        # Comparação de barras
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))  # Cria figura com dois gráficos lado a lado
        
        algoritmos = ['Minimax', 'Alpha-Beta']  # Nomes dos algoritmos
        tempos_medios = [sum(tempos_minimax)/len(tempos_minimax), 
                          sum(tempos_alpha_beta)/len(tempos_alpha_beta)]  # Calcula tempos médios
        
        ax1.bar([0, 1], tempos_medios, width=0.4)  # Cria gráfico de barras para tempos médios
        ax1.set_xticks([0, 1])  # Define posições dos ticks
        ax1.set_xticklabels(algoritmos)  # Define etiquetas dos ticks
        ax1.set_ylabel('Tempo Médio (segundos)')  # Etiqueta eixo Y
        ax1.set_title('Tempo de Execução Médio')  # Título do gráfico
        
        if nos_minimax and nos_alpha_beta:  # Se contagens de nós estão disponíveis
            nos_medios = [sum(nos_minimax)/len(nos_minimax), 
                           sum(nos_alpha_beta)/len(nos_alpha_beta)]  # Calcula nós médios
            
            ax2.bar([0, 1], nos_medios, width=0.4)  # Cria gráfico de barras para nós médios
            ax2.set_xticks([0, 1])  # Define posições dos ticks
            ax2.set_xticklabels(algoritmos)  # Define etiquetas dos ticks
            ax2.set_ylabel('Nós Visitados (média)')  # Etiqueta eixo Y
            ax2.set_title('Nós Visitados Médios')  # Título do gráfico
        
        plt.tight_layout()  # Ajusta layout
        plt.savefig('comparacao_algoritmos_jogo.png')  # Salva o gráfico como imagem
        print("Comparação de algoritmos guardada como 'comparacao_algoritmos_jogo.png'")
        plt.show()  # Mostra o gráfico na tela

def visualizar_exploracao_tabuleiro():
    """Visualiza e compara a exploração de nós entre Minimax e Alpha-Beta em um tabuleiro de exemplo"""
 
    print("\nVisualizando a exploração do tabuleiro...")
    
    # Criar um tabuleiro de exemplo de meio-jogo
    tabuleiro = [
        [" ", "X", "O"],  # Primeira linha do tabuleiro
        ["X", "O", " "],  # Segunda linha do tabuleiro 
        [" ", " ", " "]   # Terceira linha do tabuleiro
    ]
    
    print("Tabuleiro de exemplo:")
    mostrar_tabuleiro(tabuleiro)  # Mostra o tabuleiro de exemplo
    
    # Contar nós explorados por cada algoritmo
    nos_minimax = contar_nos_visitados(tabuleiro, True, "X", "O", usar_alpha_beta=False)  # Conta nós para Minimax
    nos_alpha_beta = contar_nos_visitados(tabuleiro, True, "X", "O", usar_alpha_beta=True)  # Conta nós para Alpha-Beta
    
    # Exibe os resultados
    print(f"Minimax explora {nos_minimax} nós")  # Mostra número de nós do Minimax
    print(f"Alpha-Beta explora {nos_alpha_beta} nós")  # Mostra número de nós do Alpha-Beta
    print(f"Eficácia da poda Alpha-Beta: {(1 - nos_alpha_beta/nos_minimax)*100:.2f}% de redução")  # Mostra percentual de redução

def principal():
    """Função principal para executar o programa - Menu principal"""
    while True:
        # Mostra menu principal
        print("\nJogo do Galo com Algoritmos de MiniMax e Alpha-Beta")
        print("1. Jogar contra o computador")
        print("2. Ver computador vs computador")
        print("3. Comparar desempenho dos algoritmos")
        print("4. Visualizar exploração do tabuleiro")
        print("5. Sair")
        
        escolha = input("Escolha uma opção (1-5): ")  # Obtém escolha do usuário
        
        # Executa a opção escolhida
        if escolha == "1":  # Modo jogador vs computador
            jogar_humano_vs_computador()
        elif escolha == "2":  # Modo computador vs computador
            jogar_computador_vs_computador()
        elif escolha == "3":  # Comparação de algoritmos
            comparar_desempenho_algoritmos()
        elif escolha == "4":  # Visualização de exploração
            visualizar_exploracao_tabuleiro()
        elif escolha == "5":  # Sair
            print("\nObrigado por jogar!")
            break  # Encerra o programa
        else:  # Opção inválida
            print("Escolha inválida. Tente novamente.")

if __name__ == "__main__":
    principal()