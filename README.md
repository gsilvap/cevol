cevol
=====


#Enunciado do projeto
__________________

TP2- Operadores de Varia��o Vari�veis
- Descri��o Sumaria

Desde sempre foi objecto de discuss�o a import�ncia relativa dos operadores
de varia��o, em particular a muta��o e a recombina��o. Normalmente, escolhidos
os valores das probabilidades de recombina��o e de muta��o, estas s�o
mantidas constantes ao longo da experi�ncia. No entanto h� quem defenda
que a recombinac�o e mais importante no inicio e a muta��o mais importante
no final. Vamos procurar tirar isso a limpo. Use um dos problemas de
refer�ncia para fazer o estudo, justi�ando a op��o que efectuou.

- Objectivos

Faca uns testes preliminares que lhe permita definir valores aceit�veis para os
diferentes par�metros do seu AG. Testes tr�s vers�es do algoritmo gen�tico
para este problema. Uma, com probabilidades fixas, por exemplo a probabilidade
de cruzamento igual a 0.9 e a de mutac�o igual a 0.01. Outra, com
uma probabilidade fixa de cruzamento de 0.8 durante as primeiras 70% de
gera��es, zero nas seguintes, enquanto a probabilidade de muta��o e zero
durante as primeiras 70% gera��es, passando para 0.05% nas restantes. A terceira vers�o, com probabilidades vari�veis, com a probabilidade de recombina��o a descer de 0.9 para 0.7, 0.5 e 0.3, ao mesmo tempo que a de muta��o
vai subindo de 0.01 para 0.05, 0.1 e 0.2. Neste ultimo caso temos ent�o quatro
pares de valores (prob. cruzamento, prob. muta��o). Defina o modo como
esta varia��o e feita (por exemplo, ap�s um certo numero de gera��es).
Para cada algoritmo faca 30 testes (runs). Recolha os dados sobre desempenho
de cada algoritmo, medido pela qualidade do resultado e pela rapidez
com que foi encontrado o melhor resultado. Analise estatisticamente os resultados
e tire conclus�es.