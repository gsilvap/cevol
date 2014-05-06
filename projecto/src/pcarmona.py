__author__ = 'PedroCarmona'


#imports

import time
from pcarmona.sum_sub_int_see import *

# Algoritmo genetico

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

    file_name = 'out/'
    file_name =file_name + str(int(time.time()))
    file_name = file_name + '.csv'
    run_parents_selection(30,file_name, 150, 10, rastrigin, 0.8, 0.01,tournament_sel, muta_reals_rastrigin, [one_point_cross,uniform_cross], survivors_steady_state, 500)

    pass
