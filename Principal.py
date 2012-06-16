#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

#Importando pyco se tiver
#psyco e um compilador JIT (just-in-time) para python. Isto faz melhor a peformance do código intepretado
# aptitude install python-psyco :)

try:
	import psyco
	psyco.log()
	psyco.full(memory=100)
	psyco.profile(0.09, memory=100)
	psyco.profile(0.09)
except ImportError:
	pass

import random
from random import *
from sys import *
import pdb
import timeit
import time

#Arquivos
from Grafo import *
from Formiga import *
from NumerosAleatorios import *
from Cmd import *

# Lendo parâmetros da linha de comando
cmd = Cmd()

# Variáveis
"""
var = {}
var['ALFA']	= 1.0 
var['BETA']	= 5.0
var['RO']	= 0.5
var['Q']	= 100.0
var['T0']	= 0.000001
var['E']	= 5	
"""
# Criando o grafo
g = Grafo(cmd.var)
g.carregaGrafo()


# Estrura que armaneza as formigas
formigas = []

# TODO acochambra
cidadesDisponiveis = []
for i in range(0,g.getQtdNos()):
	cidadesDisponiveis.append(i)

# Gerador de numeros aleatorios sem repeticao
num = NumerosAleatorios(g.getQtdNos())

# Distribuição das formigas - cada um vai para uma cidade diferente
for i in range(0,g.getQtdNos()):
	cidadeInicial = num.numero()
	f = Formiga(g,cidadeInicial)
	formigas.append(f)


# Formigas elististas
formigasElitistas = []
QFE = 5
for i in range(QFE):
	fE = Formiga(g)
	formigasElitistas.append(fE)

tamPool 		= 5		# Tamanho do pool 1 + 4

# Resultados
menorCusto 		= 9999999999
menorCaminho	= []
qwe = time.time()
for bli in range(cmd.var['t']):
	somaCustos = 0
	c = 0.0
	M = 9999999
	P = 0
	geral = 0
	restaCidades = g.getQtdNos() # Total de Cidades - Cidade Inicial
	
	for k in range(g.getQtdNos()):

		restaCidades--1; # Exclui a cidade atual
		for m in range(0,restaCidades):
			
			formigas[k].iniciaRota() # TODO Pega um aleatório, diferente de algum nó presente em caminhos

			# Range: Se g.getQtdNos() < 4 --> 4 - g.getQtdNos(), senão --> 4
			if restaCidades > tamPool:
				tamCaminho = tamPool
			else:
				tamCaminho = tamPool - restaCidades
			
			# Percorre o caminho pro pool
			for n in range(0,tamCaminho):
				formigas[k].proximaCidade()

		formigas[k].finalizaRota()
		formigas[k].calculaRota()
		if formigas[k].custoAtual < menorCusto:
			menorCusto		= formigas[k].custoAtual
			menorCaminho 	= formigas[k].caminho				
		somaCustos += formigas[k].custoAtual 
	
	for k in range(g.getQtdNos()):
		formigas[k].calculaDeltaTij()
	g.depositaFeromonio()
	"""
	for e in range(QFE):
		formigasElitistas[e].setCaminho(menorCaminho)
		formigas.append(formigasElitistas[e])
	"""
	"""
	for e in range(QFE):
		formigas.pop()
	"""
	"""
	print ('[%7d] %5d %10f') % (bli,menorCusto,somaCustos/(float)(g.getQtdNos()))
	"""

asd = time.time()
asd = asd-qwe
print '\n\n----------------------------------------'
print "Tempo de execução: ", asd
print "Melhor custo:      ", menorCusto
print "Melhor caminho:    ", menorCaminho
