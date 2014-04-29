READ ME
=====


#Representação

- cadeia binária de tamanho N, inde é possivel ver se o elemento está na mochila ou nao

#Qualidade

- soma dos valores, porem se o peso excede a capacidade o fitness = 0

#Algoritmo

##Perturbacao


#Apontamentos

Sem correlacao

- P[i] -> Peso do item -> uniforme (1..N)

- V[i] -> Valor do item -> uniforme (1..N)

- C = sum(P)/2 -> capacidade, por exemplo metade dos pesos

Fortemente Correlacionado

- P[i] -> Peso do item -> uniforme (1..N)

- V[i] -> Valor do item -> P[i] + r

- C = sum(P)/2 -> capacidade, por exemplo metade dos pesos

Média correlação

- P[i] -> Peso do item -> uniforme (1..N)

- V[i] -> Valor do item -> P[i] + uniforme(-r,r)

- C = sum(P)/2 -> capacidade, por exemplo metade dos pesos
