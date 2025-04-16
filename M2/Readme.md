# Jogo do Galo Algoritmos Min-Max e Alpha Beta (Python)

## Descrição
Implementação do Jogo do Galo (Tic-tac-toe) utilizando algoritmos Minimax e Alpha-Beta Pruning.

## Estrutura do Projeto
```
    jogo_galo.py          # Arquivo principal do jogo
    README.md             # Esta documentação
    comparacao_algoritmos.png
    Gráficos de desempenho gerados
    Relatorio.docx
    Si_Trabalho2.pdf
```

## Algoritmos Implementados

### Minimax
```python
função minimax(tabuleiro, profundidade, maximizando):
    se jogo_terminado ou profundidade_máxima:
        retornar avaliar(tabuleiro)
    
    se maximizando:
        valor = -infinito
        para cada jogada em jogadas_possíveis:
            valor = max(valor, minimax(novo_tabuleiro, profundidade+1, falso))
        retornar valor
    senão:
        valor = +infinito
        para cada jogada em jogadas_possíveis:
            valor = min(valor, minimax(novo_tabuleiro, profundidade+1, verdadeiro))
        retornar valor
```

### Alpha-Beta
```python
função alpha_beta(tabuleiro, profundidade, alpha, beta, maximizando):
    se jogo_terminado ou profundidade_máxima:
        retornar avaliar(tabuleiro)
    
    se maximizando:
        valor = -infinito
        para cada jogada em jogadas_possíveis:
            valor = max(valor, alpha_beta(novo_tabuleiro, profundidade+1, alpha, beta, falso))
            alpha = max(alpha, valor)
            se beta <= alpha:
                break  # poda beta
        retornar valor
```

## Resultados de Desempenho

### Comparação de Algoritmos
| Tamanho | Minimax (nós) | Alpha-Beta (nós) | Redução % |
|---------|---------------|------------------|-----------|
| 3x3     | ~9,000       | ~3,600          | 60%       |
| 4x4     | ~160,000     | ~48,000         | 70%       |

### Tempos de Execução
- Minimax: ~0.85 segundos
- Alpha-Beta: ~0.32 segundos
- Redução média de nós explorados: ~60%

## Como Jogar

1. Execute o jogo:
```bash
python jogo_galo.py
```

2. Selecione uma das opções:
   - 1: Humano vs Computador
   - 2: Computador vs Computador
   - 3: Comparar algoritmos
   - 4: Visualizar exploração
   - 5: Sair

3. Para jogar, use o teclado numérico:
```
1 | 2 | 3
---------
4 | 5 | 6
---------
7 | 8 | 9
```

## Requisitos
- Python 3.6+
- Bibliotecas:
  - numpy
  - matplotlib
  - random
  - time

## Exemplos de Jogadas

### Jogada Inicial do Computador
```
Antes:          Depois:
  |   |          |   |   
---------      ---------
  |   |          | X |   
---------      ---------
  |   |          |   |   
```

## Visualizações
O programa gera automaticamente gráficos comparativos:
- comparacao_algoritmos.png
- desempenho_jogo.png

## Dicas
- Modo computador vs computador para análise de desempenho
- Compara os algoritmos em diferentes estados do jogo
- Observa os tempos de execução após cada jogada
