cevol
=====


#Enunciado do projeto
__________________

TP2- Operadores de Variação Variáveis
- Descrição Sumaria

Desde sempre foi objecto de discussão a importância relativa dos operadores
de variação, em particular a mutação e a recombinação. Normalmente, escolhidos
os valores das probabilidades de recombinação e de mutação, estas são
mantidas constantes ao longo da experiência. No entanto há quem defenda
que a recombinacão e mais importante no inicio e a mutação mais importante
no final. Vamos procurar tirar isso a limpo. Use um dos problemas de
referência para fazer o estudo, justiçando a opção que efectuou.

- Objectivos

Faca uns testes preliminares que lhe permita definir valores aceitáveis para os
diferentes parâmetros do seu AG. Testes três versões do algoritmo genético
para este problema. Uma, com probabilidades fixas, por exemplo a probabilidade
de cruzamento igual a 0.9 e a de mutacão igual a 0.01. Outra, com
uma probabilidade fixa de cruzamento de 0.8 durante as primeiras 70% de
gerações, zero nas seguintes, enquanto a probabilidade de mutação e zero
durante as primeiras 70% gerações, passando para 0.05% nas restantes. A terceira versão, com probabilidades variáveis, com a probabilidade de recombinação a descer de 0.9 para 0.7, 0.5 e 0.3, ao mesmo tempo que a de mutação
vai subindo de 0.01 para 0.05, 0.1 e 0.2. Neste ultimo caso temos então quatro
pares de valores (prob. cruzamento, prob. mutação). Defina o modo como
esta variação e feita (por exemplo, após um certo numero de gerações).
Para cada algoritmo faca 30 testes (runs). Recolha os dados sobre desempenho
de cada algoritmo, medido pela qualidade do resultado e pela rapidez
com que foi encontrado o melhor resultado. Analise estatisticamente os resultados
e tire conclusões.