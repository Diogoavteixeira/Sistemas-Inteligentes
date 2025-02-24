# Relatório – Resolução do 8-Puzzle

## Descrição do Puzzle

O 8-Puzzle é um quebra-cabeça deslizante composto por 8 peças numeradas (de 1 a 8) distribuídas em um tabuleiro 3x3, onde uma posição é deixada vazia (representada por 0 ou espaço em branco). O objetivo do jogo é transformar uma configuração inicial em uma configuração final (objetivo) através de movimentos válidos, deslizando as peças para ocupar a posição vazia. Este problema é clássico na área de inteligência artificial, devido à sua complexidade combinatória e ao espaço de estados finito.

## Descrição dos Algoritmos Implementados

O código contempla diferentes abordagens para a resolução do puzzle:

### Modo Manual
Permite que o usuário mova as peças utilizando as setas do teclado. Cada movimento é executado interativamente e o número de movimentos é contabilizado.

### Modo Automático
O usuário pode escolher entre três algoritmos para resolver o puzzle automaticamente:

- **A* com Heurística Manhattan**: Utiliza a soma das distâncias horizontais e verticais de cada peça até sua posição correta na configuração alvo. Esta heurística é admissível e consistente, oferecendo uma boa orientação e gerando a solução ótima com eficiência.
  
- **A* com Heurística Hamming**: Calcula o número de peças fora de posição (desconsiderando o espaço vazio). Embora admissível, esta heurística é menos informativa que a Manhattan, o que pode levar a uma expansão maior de nós durante a busca.

- **Busca em Largura (BFS)**: Explora os estados do puzzle de forma nivelada, garantindo a solução ótima em termos de número de movimentos, mas com um custo elevado em tempo e memória para estados com maior profundidade.

## Principais Características de Cada Algoritmo

### A* com Manhattan
- **Optimalidade**: Garante encontrar a solução ótima, desde que a heurística seja admissível e consistente.
- **Completude**: Completo para espaços finitos.
- **Complexidade**: Exponencial no pior caso, mas eficiente na prática devido à heurística informativa.

### A* com Hamming
- **Optimalidade**: Garante a solução ótima.
- **Completude**: Completo para espaços finitos.
- **Complexidade**: Pode ser menos eficiente que a Manhattan, devido à heurística menos informativa.

### Busca em Largura (BFS)
- **Optimalidade**: Garante a solução ótima em termos de número de movimentos.
- **Completude**: Completo para espaços finitos.
- **Complexidade**: Exponencial, o que torna inviável para instâncias com profundidade maior.

## Combinações Testadas e Respectivas Respostas

Foram realizados testes com diferentes configurações do puzzle. Abaixo estão alguns exemplos ilustrativos:

### Exemplo 1
**Configuração Inicial**:

1 2 3 4 5 6 7 0

**Configuração Final**:

1 2 3 4 5 6 7 8

**Output Esperado**: Solução simples com um movimento ("right").

### Exemplo 2
**Configuração Inicial**:


**Configuração Final**:

**Configuração Final**:

**Output Esperado**: Teste de maior complexidade que evidencia diferenças entre heurísticas e abordagem BFS.

## Estudo de Custo de Tempo e Memória

- **BFS**: Embora garantido para encontrar a solução ótima, possui alto custo de tempo e memória devido à explosão combinatória.
  
- **A* com Hamming**: Menos eficiente que a Manhattan, levando a maior expansão de nós.
  
- **A* com Manhattan**: A heurística mais informada permite um tempo de execução mais rápido e menor consumo de memória.

## Discussão dos Resultados

### Eficiência e Otimalidade
Todos os algoritmos garantem a solução ótima, mas com diferentes eficiências em termos de tempo e memória. O A* com Manhattan se destaca pela boa orientação da heurística, enquanto o BFS se torna inviável para estados mais profundos devido ao uso intensivo de memória.

### Escalabilidade
Os algoritmos A* demonstram melhor escalabilidade em comparação com o BFS, especialmente para puzzles mais complexos.

### Aplicabilidade
O A* com Manhattan é geralmente a melhor escolha, especialmente para puzzles mais complexos. Para puzzles simples ou fins didáticos, a BFS pode ser suficiente.

## Conclusões Principais

- **Versatilidade do Código**: O sistema oferece modos interativos (manual) e automáticos, permitindo ao usuário experimentar o puzzle e analisar os algoritmos de busca.
  
- **Importância da Heurística**: A heurística Manhattan reduz significativamente o espaço de busca, levando a soluções mais rápidas e com menor consumo de memória.
  
- **Trade-off entre Simplicidade e Desempenho**: A BFS, embora simples e ótima, possui alto custo computacional. Heurísticas eficientes em algoritmos como A* são fundamentais.

- **Aplicação em Problemas Reais**: O estudo pode ser aplicado a outros problemas de busca e planejamento em inteligência artificial, destacando a importância da escolha de heurísticas adequadas.

## Como Rodar

1. Clone o repositório:
   ```bash
   git clone https://github.com/Diogoavteixeira/Sistemas-Inteligentes8-puzzle.git

