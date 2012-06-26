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
resultadoCSV = csv.writer(open(''.join([cmd.var['GRAFO'],"_",str(numLoops),".csv"]), "wb"))

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

				# Somatório custo do Pool
				custoPool += f.custoAtual
				# print  caminhosPool[strCidadeInicial].getCusto(), ' ', caminhosPool[strCidadeInicial].getCaminho()
				
				# ------------------------------------------------------
				# Em seguida, testa-se todos os caminhos a partir dos demais pontos do poool
				for inicioPool in f.getIniciosPool():

					if f.iniciaRotaPool(inicioPool):

						# Percorre o caminho pro pool
						for n in range(0,g.getTamCaminho()):
							f.proximaCidadePool()

						# Adiciona a cidade destino
						f.ultimaCidadePool()
						# print 'caminho: ',f.caminhoPool
						f.calculaRotaPool() # calcula o custo do caminho e colocar

						strCidadeInicial = str(inicioPool)
					
						caminhosPool[strCidadeInicial] = Caminho(f.caminhoPool, f.custoAtual, inicioPool)
						# print  caminhosPool[strCidadeInicial].getCusto(), ' ', caminhosPool[strCidadeInicial].getCaminho()

						# Somatório custo do Pool
						custoPool += f.custoAtual

			# Calcula custos após fazer um caminho para cada saída do pool

			# Custo do Pool final
			custoPool = custoPool / (g.getTamCaminho() + 1)
			# print 'custo do pool: ', custoPool

			# Adiciona o pool da lista
			pools.append(Pool(caminhosPool, custoPool, f.getPool()))
			
			# Custo e todos os pools da rodada
			custoPoolTotal += custoPool
		
		if custoPoolTotal < melhorCustoPoolTotal:
			melhorCustoPoolTotal = custoPoolTotal
			melhoresPools = list(pools)
		
		# Cleaning caminhos
		# {} instancia um novo dicionario, zerado.
		# clear() limpa o dicionário, que se for uma referência, continua sendo referência
		caminhos = {}
		
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
	
	resultadoCSV.writerow([str(loop), melhorCustoPoolTotal, melhoresPoolsString, str(duration)])
	print loop, ' [ok!]'
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

