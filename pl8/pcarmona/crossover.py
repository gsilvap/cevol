# -*- coding: utf-8 -*-
import random

# Operadores de Recombinação
# Genéricos
def one_point_cross(cromo_1, cromo_2,prob_cross):
	value = random.random()
	if value < prob_cross:
		pos = random.randint(0,len(cromo_1))
		f1 = cromo_1[0:pos] + cromo_2[pos:]
		f2 = cromo_2[0:pos] + cromo_1[pos:]
		return [f1,f2]
	else:
		return [cromo_1,cromo_2]


def two_points_cross(cromo_1, cromo_2,prob_cross):
	print(cromo_1, cromo_2)
	value = random.random()
	if value < prob_cross:
		pc= random.sample(range(len(cromo_1)),2)
		pc.sort()
		pc1,pc2 = pc
		f1= cromo_1[:pc1] + cromo_2[pc1:pc2] + cromo_1[pc2:]
		f2= cromo_2[:pc1] + cromo_1[pc1:pc2] + cromo_2[pc2:]
		return [f1,f2]
	else:
		return [cromo_1,cromo_2]

def uniform_cross(cromo_1, cromo_2,prob_cross):
	value = random.random()
	if value < prob_cross:
		f1=[]
		f2=[]
		for i in range(0,len(cromo_1)):
			if random.random() < 0.5:
				f1.append(cromo_1[i])
				f2.append(cromo_2[i])
			else:
				f1.append(cromo_2[i])
				f2.append(cromo_1[i])

		return [f1,f2]
	else:
		return [cromo_1,cromo_2]

# OX - order crossover

def order_cross(cromo_1,cromo_2,prob_cross):
	size = len(cromo_1)
	value = random.random()
	if value < prob_cross:
		pc= random.sample(range(size),2)
		pc.sort()
		pc1,pc2 = pc
		f1 = [None] * size
		f2 = [None] * size
		f1[pc1:pc2+1] = cromo_1[pc1:pc2+1]
		f2[pc1:pc2+1] = cromo_2[pc1:pc2+1]
		for j in range(size):
			for i in range(size):
				if (cromo_2[j] not in f1) and (f1[i] == None):
					f1[i] = cromo_2[j]
					break
			for k in range(size):
				if (cromo_1[j] not in f2) and (f2[k] == None):
					f2[k] = cromo_1[j]
					break
		return [f1,f2]
	else:
		return [cromo_1,cromo_2]


def pmx_cross(cromo_1,cromo_2,prob_cross):
	size = len(cromo_1)
	value = random.random()
	if value < prob_cross:
		pc= random.sample(range(size),2)
		pc.sort()
		pc1,pc2 = pc
		f1 = [None] * size
		f2 = [None] * size
		f1[pc1:pc2+1] = cromo_1[pc1:pc2+1]
		f2[pc1:pc2+1] = cromo_2[pc1:pc2+1]
		# primeiro filho
		# parte do meio
		for j in range(pc1,pc2+1):
			if cromo_2[j] not in f1:
				pos_2 = j
				g_j_2 = cromo_2[pos_2]
				g_f1 = f1[pos_2]
				index_2 = cromo_2.index(g_f1)
				while f1[index_2] != None:
					index_2 = cromo_2.index(f1[index_2])
				f1[index_2] = g_j_2
		# restantes
		for k in range(size):
			if f1[k] == None:
				f1[k] = cromo_2[k]
		# segundo filho
		# parte do meio
		for j in range(pc1,pc2+1):
			if cromo_1[j] not in f2:
				pos_1 = j
				g_j_1 = cromo_1[pos_1]
				g_f2 = f2[pos_1]
				index_1 = cromo_1.index(g_f2)
				while f2[index_1] != None:
					index_1 = cromo_1.index(f2[index_1])
				f2[index_1] = g_j_1
		# parte restante
		for k in range(size):
			if f2[k] == None:
				f2[k] = cromo_1[k]
		return [f1,f2]
	else:
		return [cromo_1,cromo_2]


# para testar

def cromo_bin(size):
	indiv = [random.randint(0,1) for i in range(size)]
	return indiv

def cromo_int(size):
	indiv = list(range(1,size+1))
	random.shuffle(indiv)
	return indiv


if __name__ =='__main__':
	"""
	c1 = cromo_bin(10)
	c2 = cromo_bin(10)
	print uniform_cross(c1,c2, 1.0)

	c3 = cromo_int(10)
	c4 = cromo_int(10)
	print order_cross(c3,c4,1.0)
	"""
	c5 = [1,2,3,4,5,6,7,8,9]
	c6 = [9,3,7,8,2,6,5,1,4]
	print(uniform_cross(c5,c6,1.0))

