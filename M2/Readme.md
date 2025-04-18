# Jogo do Galo — Algoritmos Minimax e Alpha-Beta (Python)

## Descrição
Implementação do Jogo do Galo (Tic-tac-toe) em Python, utilizando os algoritmos Minimax e Alpha-Beta para tomada de decisão. 
O projeto permite comparar o desempenho dos algoritmos e visualizar estatísticas.

## Estrutura do Projeto
```
jogo_galo.py                # Código principal do jogo
README.md                   # Documentação do projeto
comparacao_algoritmos.png   # Gráficos de desempenho gerados
relatorio.docx              # Relatório detalhado do trabalho
Si_Trabalho2.pdf            # Documento complementar
```

## Algoritmos Implementados

### Minimax
```python
def minimax(tabuleiro, profundidade, e_maximizador, jogador, oponente):
    if verificar_vencedor(tabuleiro, jogador):
        return 10 - profundidade
    if verificar_vencedor(tabuleiro, oponente):
        return profundidade - 10
    if tabuleiro_cheio(tabuleiro):
        return 0
    # ... lógica recursiva para maximizar ou minimizar ...
```

### Alpha-Beta
```python
def alpha_beta(tabuleiro, profundidade, e_maximizador, jogador, oponente, alpha, beta):
    # ... lógica semelhante ao minimax, mas com poda alpha-beta ...
    # alpha = melhor valor para o maximizador até agora
    # beta = melhor valor para o minimizador até agora
```

## Resultados de Desempenho

### Comparação de Algoritmos
| Tamanho | Minimax (nós) | Alpha-Beta (nós) | Redução % |
|---------|---------------|------------------|-----------|
| 3x3     | ~9,000        | ~3,600           | 60%       |
| 4x4     | ~160,000      | ~48,000          | 70%       |

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
O programa gera automaticamente gráficos comparativos, como:
- comparacao_algoritmos.png
- desempenho_jogo.png

## Dicas
- Use o modo computador vs computador para análise de desempenho.
- Compare os algoritmos em diferentes estados do jogo.
- Observe os tempos de execução após cada jogada.

---

Desenvolvido para fins educacionais e estudo de algoritmos de decisão em jogos.
