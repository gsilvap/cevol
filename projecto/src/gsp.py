__author__ = 'GonçaloSilva'

# Algoritmo genetico

import random

def init_pop(pop_size, cromo_size):
    """Return a list of individuals, where each indicidual has the forma [chromo, 0]"""
    population = [[cromo_reals(cromo_size),0] for count in range(pop_size)]
    return population

def cromo_reals(size):
    cromo =[random.choice([0,1]) for i in range(size)]
    return cromo

def mutacao():
    pass


def recombinacao():
    pass



"""
    Fazer 30 runs, medir o desempenho com:
    - qualidade do algoritmo
    - rapidez com que foi encontrado o melhor resultado

    Analise estatistica dos resultados e tirar conclusões
"""


# varicao das probabilidades de mutacao e recombinação
# mutação no inicio e recombinação no fim ?
if __name__ == '__main__':
    size = 10
    sequencia =[i for i in range(size)]

    # 1º TESTE FIXO
    # cruzamento = 0.9
    # mutacao = 0.1

    # 2º TESTE PROBABILIDADE INICIAL E FINAL
    # cruzamento = 0.8 durante 70% das gerações, 0 nas seguintes
    # mutacao = 0      durante 70% das gerações, 0.05 nas seguintes

    # 3º TESTE PROBABILIDADES VARIAVEIS
    # cruzamento  a descer de 0.9 a 0.7,  0.5, 0.3
    # mutacao     a descer de 0.01, 0.05, 0.1, 0.2
    # quatro pares de valores
    # definir como é feita a variação

    pass