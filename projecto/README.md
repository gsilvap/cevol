TP2- Operadores de Variação Variáveis

============================================

###Descrição Sumária
Desde sempre foi objecto de discussão a importância relativa dos operadores de variacção, em particular a mutação e a recombinação. Normalmente, escolhidos os valores das probabilidades de recombinação e de mutacção, estas são mantidas constantes ao longo da experiência. No entanto há quem defenda que a recombinação é mais importante no início e a mutação mais importante no final. Vamos procurar tirar isso a limpo. Use um dos problemas de referência para fazer o estudo, justificando a opção que efectuou.

###Objectivos
Faça uns testes preliminares que lhe permita definir valores aceitáveis para os diferentes parâmetros do seu AG. Testes três versões do algoritmo genético para este problema.

- Uma, com probabilidades fixas, por exemplo a probabilidade de cruzamento igual a 0.9 e a de mutação igual a 0.01.

- Outra, com uma probabilidade fixa de cruzamento de 0.8 durante as primeiras 70% de gerações, zero nas seguintes, enquanto a probabilidade de mutação  é zero durante as primeiras 70% gerações, passando para 0.05% nas restantes.

- A terceira versão, com probabilidades variáveis, com a probabilidade de recombinação a descer de 0.9 para 0.7, 0.5 e 0.3, ao mesmo tempo que a de mutação vai subindo de 0.01 para 0.05, 0.1 e 0.2. Neste último caso temos então quatro pares de valores (prob. cruzamento, prob. mutação).

Defina o modo como esta variação  é feita (por exemplo, após um certo número de gerações).

Para cada algoritmo faça 30 testes (runs). Recolha os dados sobre desem- penho de cada algoritmo, medido pela qualidade do resultado e pela rapidez com que foi encontrado o melhor resultado. Analise estatisticamente os resultados e tire conclusões.



##Problema de teste:

8.6 Soma de Subconjuntos de Inteiros
Este problema  é um caso particular do problema da mochila. Dado um conjunto de n inteiros distintos, a1, a2, . . . , an, não necessariamente consecutivos, encontrar um subconjunto desses inteiros, logo sem repetições, cuja soma  é igual a um dado X. Admita que pretende a solução de menor cardinalidade. Por exemplo, se tivermos o conjunto {5, 8, 4, 11, 6, 12} e X = 20 então temos as soluções {8, 12} e {4, 5, 11}, sendo a primeira a que nos interessa.
