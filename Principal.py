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
from Cmd import *
from random import choice

# Lendo parâmetros da linha de comando
cmd = Cmd()

# Número global de loops
numLoops = cmd.var['N']

# Criando o grafo
g = Grafo(cmd.var)
g.carregaGrafo()

for loop in range(numLoops):

	# print ' LOOP: ', loop
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

	caminhos = {} # Dicionário. Chave é relevante	#[Caminho() for i in range(g.getQtdNos())]
	melhoresCaminhos = {}
	melhorCustoTotal = 9999999999

	start = time.time()
	for bli in range(cmd.var['t']):
		
		# Nova formiga
		f = Formiga(g)

		# Carrega cidades
		f.carregaCidades()

		# Para cada cidade restante (disponivel)
		while f.getCidades():

			# Inicia a rota
			if f.iniciaRota():

				# Cidades restantes = X (cidade dos caroneiros) - 1 (cidade do motorista)
				if len(f.getCidades()) > (g.getTamPool() - 1):
					g.setTamCaminho(g.getTamPool() - 1)
				else:
					g.setTamCaminho(len(f.getCidades())) 
				
				# Percorre o caminho pro pool
				for n in range(0,g.getTamCaminho()):
					f.proximaCidade()

				# Adiciona a cidade destino
				f.ultimaCidade()
				
				f.calculaRota() # calcula o custo do caminho e colocar

				strCidadeInicial = str(f.getCidadeInicial())
				
				if strCidadeInicial not in caminhos: # já existe um caminho. Então compara o custo
					caminhos[strCidadeInicial] = Caminho(f.caminho, f.custoAtual, f.getCidadeInicial())
				else:
					if caminhos[strCidadeInicial].getCusto() < f.custoAtual:
						caminhos[strCidadeInicial] = Caminho(f.caminho, f.custoAtual, f.getCidadeInicial())

		if f.getCustoTotal() < melhorCustoTotal:
			melhorCustoTotal = f.getCustoTotal()
			melhoresCaminhos = caminhos.copy()

		# Cleaning caminhos
		# {} instancia um novo dicionario, zerado.
		# clear() limpa o dicionário, que se for uma referência, continua sendo referência
		caminhos = {}
		
	duration = time.time() - start

	strList = []
	for caminho in melhoresCaminhos:
		#print melhoresCaminhos[caminho].getCaminho()
		strList.append(melhoresCaminhos[caminho].getCaminho())
		strList.append('  ')
	# strFinal = ''.join(strList)

	  # for num in xrange(loop_count):	
	  #   str_list.append(`num`)
	  # return ''.join(str_list)
	
	print loop, '  ', melhorCustoTotal, '  ', strList
	
	# print '----------------------------------------'
	# print "Tempo de execução: ", duration
	# print "Melhor custo:      ", melhorCustoTotal
	# print "Melhores caminho:    \n",
	# for caminho in melhoresCaminhos:
	# 	print melhoresCaminhos[caminho].getCusto(),' ',melhoresCaminhos[caminho].getCaminho()
	# print "\n\n"
