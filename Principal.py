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
				caminhosPool[strCidadeInicial] = Caminho(f.caminho, f.custoAtual, f.getCidadeInicial())
				# print '=============================='
				# print f.getPool()
				melhoresCaminhosLocais = {}
				# print '------------------------------------------'
				for bli2 in range(100):#cmd.var['t']):
					# ------------------------------------------------------
					# Em seguida, encontra o melhor caminho a partir de CADA vertice do pool
					# print 'inicios', f.getIniciosPool()
					for inicioPool in f.getIniciosPool():
						if f.iniciaRotaPool(inicioPool):

							# Percorre o caminho pro pool
							for n in range(0,g.getTamCaminho()):
								# print 'cidade atual: ', f.getCidadeAtual()
								f.proximaCidadePool()

							# Adiciona a cidade destino
							f.ultimaCidadePool()
							# print 'caminho: ',f.caminhoPool
							f.calculaRotaPool() # calcula o custo do caminho e colocar

							strInicioPool = str(inicioPool)
							# print f.custoAtual, ' < ', f.melhoresCaminhosLocais[strInicioPool]
							if f.custoAtual < f.melhoresCaminhosLocais[strInicioPool]:
								f.melhoresCaminhosLocais[strInicioPool] =  f.custoAtual
								melhoresCaminhosLocais[strInicioPool] = Caminho(f.caminhoPool, f.custoAtual, inicioPool)
				
				# Calcula os custos locais	
				div = 0
				for key in melhoresCaminhosLocais:
					div += melhoresCaminhosLocais[key].getCusto()
					# print melhoresCaminhosLocais[key].getCusto(), ' ', melhoresCaminhosLocais[key].getCaminho()

				custoPoolLocal = div / (g.getTamCaminho() + 1)

			# Acrescenda ao valor local do conjunto e pulls
			custoPoolTotal += custoPoolLocal	

			# Guarda os pools encontrados
			pools.append(Pool(melhoresCaminhosLocais[strInicioPool], custoPoolTotal, f.getPool()))	

		# Calcula os resultados encontados do conjunto de pools
		# print 'custo total: ' , custoPoolTotal

		if custoPoolTotal < melhorCustoPoolTotal:
			melhorCustoPoolTotal = custoPoolTotal
			melhoresPools = list(pools)

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
	
	
	#resultadoCSV.writerow([str(loop), melhorCustoPoolTotal, melhoresPoolsString, str(duration)])
	
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

