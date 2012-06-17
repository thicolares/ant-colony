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
from Caminho import *
from NumerosAleatorios import *
from Cmd import *
from random import choice

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

# Formigas elististas
formigasElitistas = []
QFE = 5
for i in range(QFE):
	fE = Formiga(g)
	formigasElitistas.append(fE)

# Resultados
menorCusto 		= 9999999999
menorCaminho	= []

qwe = time.time()

caminhos = {} # Dicionário. Chave é relevante	#[Caminho() for i in range(g.getQtdNos())]
melhoresCaminhos = {}
melhorCustoTotal = 9999999999
for i in range(0,g.getQtdNos()):
	caminhos[str(i)] = Caminho()
	melhoresCaminhos[str(i)] = Caminho()

for bli in range(cmd.var['t']):
	somaCustos = 0
	c = 0.0
	M = 9999999
	P = 0
	geral = 0
	g.setRestaCidades(g.getQtdNos())
	
	# Nova formiga
	f = Formiga(g)

	# Carrega cidades
	f.carregaCidades()

	# Para cada cidade restante (disponivel)
	for m in range(0,g.getRestaCidades()):
	
		# """ Escolhe aleatoriamente uma cidade como partida """
		# cidadeInicial = randrange(g.getQtdNos())
		# f.setCidadeInicial(cidadeInicial)

		# Exclui a cidade inicial da conta
		g.setRestaCidades(g.getRestaCidades() - 1);
		
		# Inicia a rota
		if f.iniciaRota():

			# Range: Se g.getQtdNos() < 4 --> 4 - g.getQtdNos(), senão --> 4
			if g.getRestaCidades() > g.getTamPool():
				g.setTamCaminho(g.getTamPool())
			else:
				g.setTamCaminho(g.getTamPool() - g.getRestaCidades()) 
			
			# Percorre o caminho pro pool
			for n in range(0,g.getTamCaminho()):
				f.proximaCidade()
			
			f.calculaRota() # calcula o custo do caminho e colocar

			strCidadeInicial = str(f.getCidadeInicial())
			if not caminhos[strCidadeInicial]: # já existe um caminho. Então compara o custo
				caminhos[strCidadeInicial] = Caminho(f.caminho, f.custoAtual, f.getCidadeInicial())
			else:
				if caminhos[strCidadeInicial].getCusto() > f.custoAtual:
					caminhos[strCidadeInicial] = Caminho(f.caminho, f.custoAtual, f.getCidadeInicial())
				else:
					caminhos[strCidadeInicial] = Caminho(f.caminho, f.custoAtual, f.getCidadeInicial())
			print caminhos[strCidadeInicial]

		# f.finalizaRota() # atualiza o caminho em caminhos

		if f.getCustoTotal() < melhorCustoTotal:
			melhorCustoTotal = f.getCustoTotal()
			melhoresCaminhos = caminhos
	



		



	# if formigas[k].custoAtual < menorCusto:
	# 	menorCusto		= formigas[k].custoAtual
	# 	menorCaminho 	= formigas[k].caminho				
	# somaCustos += formigas[k].custoAtual 

		
	
	# for k in range(g.getQtdNos()):
	# 	formigas[k].calculaDeltaTij()
	# g.depositaFeromonio()
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
print "Melhor custo:      ", melhorCustoTotal
print "Melhores caminho:    \n",
for m in range(len(caminhos)):
	print caminhos[str(m)].getCusto(), caminhos[str(m)].getCaminho()
