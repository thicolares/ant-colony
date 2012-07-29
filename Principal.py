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
import copy
import csv

#Arquivos
from NumerosAleatorios import *
from Grafo import *
from Formiga import *
from Caminho import *
from Pool import *
from PoolSet import *
from Cmd import *
from random import choice

# Lendo parâmetros da linha de comando
cmd = Cmd()

# Número global de loops
numLoops = cmd.var['N']

# Criando o grafo
g = Grafo(cmd.var)
g.carregaGrafo()

# # Estrura que armaneza as formigas
# formigas = []

# # TODO acochambra
# cidadesDisponiveis = []
# for i in range(0,g.getQtdNos()):
# 	cidadesDisponiveis.append(i)

# # Gerador de numeros aleatorios sem repeticao
# num = NumerosAleatorios(g.getQtdNos())

# # Distribuição das formigas - cada um vai para uma cidade diferente
# for i in range(0,g.getQtdNos()):
# 	cidadeInicial = num.numero()
# 	f = Formiga(g,cidadeInicial)
# 	formigas.append(f)

# Criando os arquivos CVS para os resultados
resultadoCSV = csv.writer(open(''.join([cmd.var['GRAFO'],"_",str(numLoops),"_",str(cmd.var['t']),".csv"]), "wb"))

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

	melhoresCaminhos = {}
	
	melhorCustoTotal = 9999999999

	melhoresPools = []
	melhorCustoPoolTotal = 9999999999

	start = time.time()
	for bli in range(cmd.var['t']):

		# Nova formiga
		f = Formiga(g)

		# Carrega cidades
		f.carregaCidades()

		pools = []
		custoPoolTotal = 0
		
		# Para cada cidade restante (disponivel)
		while f.getCidades():

			caminhos = {} # Dicionário. Chave é relevante	#[Caminho() for i in range(g.getQtdNos())]
			caminhosPool = {} # Dicionário. Chave é relevante	#[Caminho() for i in range(g.getQtdNos())]
			
			# ------------------------------------------------------
			# Inicia a rota
			# Primeira iteração monta o pool
			if f.iniciaRota():

				# Cidades restantes = X (cidade dos caroneiros) - 1 (cidade do motorista)
				if len(f.getCidades()) > (g.getTamPool() - 1):
					g.setTamCaminho(g.getTamPool() - 1)
				else:
					g.setTamCaminho(len(f.getCidades())) 
				
				# Percorre o caminho inicial e forma a pool
				for n in range(0,g.getTamCaminho()):
					f.proximaCidade()

				# Adiciona a cidade destino
				f.ultimaCidade()
				
				f.calculaRota() # calcula o custo do caminho e colocar

				strCidadeInicial = str(f.getCidadeInicial())
				
				# Primeiro caminho
				# Formação do pool
				custoPool = 0
				# caminhosPool[strCidadeInicial] = Caminho(f.caminho, f.custoAtual, f.getCidadeInicial())
				# print '=============================='
				# print f.getPool()
				melhoresCaminhosLocais = {}
				melhoresCustosLocais = {}

				matriz = {}

				cDP = f.getPool()

				for c1 in range(5):
					melhorCustoLocal = 99999999
					visitados = []
					visitados.append(c1)
					for c2 in range(5):
						if c2 not in visitados:
							visitados.append(c2)

							for c3 in range(5):
								if c3 not in visitados:
									visitados.append(c3)

									for c4 in range(5):
										if c4 not in visitados:
											visitados.append(c4)

											for c5 in range(5):
												if c5 not in visitados:

													visitados.append(c5)

													custoLocal = g.peso[cDP[c1]][cDP[c2]] + g.peso[cDP[c2]][cDP[c3]] + g.peso[cDP[c3]][cDP[c4]] + g.peso[cDP[c4]][cDP[c5]] + g.peso[cDP[c5]][0]
													
													if custoLocal < melhorCustoLocal:
														melhorCustoLocal = custoLocal
														melhoresCaminhosLocais[cDP[c1]] = Caminho(list([cDP[c1],cDP[c2],cDP[c3],cDP[c4],cDP[c5],0]), custoLocal, cDP[c1])
													visitados.remove(c5)		
											visitados.remove(c4)
									visitados.remove(c3)
							visitados.remove(c2)
					visitados.remove(c1)

				# Calcula os custos locais	
				div = 0
				for key in melhoresCaminhosLocais:
					div += melhoresCaminhosLocais[key].getCusto()
					# print '>>>' , melhoresCaminhosLocais[key].getCusto(), ' ', melhoresCaminhosLocais[key].getCaminho()

				custoPoolLocal = div / (g.getTamCaminho() + 1)

				# print custoPoolLocal

			# Acrescenda ao valor local do conjunto e pulls
			custoPoolTotal += custoPoolLocal	

			# Guarda os pools encontrados
			pools.append(Pool(melhoresCaminhosLocais, custoPoolTotal, f.getPool()))	

		# Calcula os resultados encontados do conjunto de pools
		# print 'custo total: ' , custoPoolTotal

		if custoPoolTotal < melhorCustoPoolTotal:
			melhorCustoPoolTotal = custoPoolTotal
			melhoresPools = list(pools)

		# Deposita feromônios
		# print g.getQtdNos()
		# for k in range(g.getQtdNos()):
		# 	formigas[k].calculaDeltaTij()
		f.calculaDeltaTij()
		g.depositaFeromonio()

	duration = time.time() - start

	# ------------------------------------------
	# ------------------------------------------
	# ORGANIZANDO RESULTADOS
	# ------------------------------------------
	# ------------------------------------------

	melhoresPoolsFinais = []
	# Para cada melhor pool..
	for pool in	melhoresPools:
		# Para listar melhores pools da rodada
		melhoresPoolsFinais.append(pool.getPoolFinal())

		# Pegar os melhores caminhos
		# pool.calculeMelhorCaminho()
		# melhorCaminho = pool.getMelhorCaminho()
		# print 'melhor:', melhorCaminho.getCusto(), ' ', melhorCaminho.getCaminho()
		
	# Melhores pools da rodada
	melhoresPoolsString = ''.join(['[' , ','.join( map( str, melhoresPoolsFinais) ) , ']'])

	
	print ' '.join([str(loop), str(melhorCustoPoolTotal), melhoresPoolsString, str(duration)])
	
	
	resultadoCSV.writerow([str(loop), melhorCustoPoolTotal, melhoresPoolsString, str(duration)])
	
	# strList = []
	# for caminho in melhoresCaminhos:
	# 	#print melhoresCaminhos[caminho].getCaminho()
	# 	strList.append(melhoresCaminhos[caminho].getCaminho())
	# 	strList.append('  ')
	# # strFinal = ''.join(strList)

	#   # for num in xrange(loop_count):	
	#   #   str_list.append(`num`)
	#   # return ''.join(str_list)
	
	# print loop, '  ', melhorCustoTotal, '  ', strList

