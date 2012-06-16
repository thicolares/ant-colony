#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-;

from random import *
from copy import *
from sys import *
from Grafo import *
from Caminho import *
import time

class Formiga( object ):

	# na inicialização recebe as cidades
	# retira das cidades a inicial
	def __init__( self, grafo, cidadeInicial = 0):
		self.caminho = []
		self.caminhos = []
		self.cidades = []
		self.cidadeAtual = ''
		self.probabilidades = {}
		self.grafo = grafo
		self.cidadeAtual = cidadeInicial
		self.custoAtual = 0
		self.deltaTao2 = 0

	# TODO não conheço sobrecarga em python! hehe
	def setCaminho( self, caminho ):
		self.caminho = caminho
		self.cidadeAtual = self.caminho[0]

	def calculaDivisores( self ):
		alfa = 1
		for i in range(len(self.cidades)): # Para cada cidade atual			
			divisor = 0.0
			cidadeI = self.cidades[i]
			for l in range(len(self.cidades)): # Para cada cidade disponivel
				cidadeL = self.cidades[l]
				if  cidadeI!=cidadeL:
					divisor += pow(self.grafo.feromonio[cidadeI][cidadeL],alfa)*self.grafo.visibilidade_beta[cidadeI][cidadeL]
			self.grafo.divisor[cidadeI] = divisor

	def proximaCidade( self ):		
		"""
		Calcula probabilisticamente qual a proxima cidade a ser visitada pela formiga
		"""
		alfa = self.grafo.alfa
		beta = self.grafo.beta
		i = self.cidadeAtual
		somaPij = 0.0
		rn = random() 
		cidadeI = self.cidadeAtual
		tiraDivisor = 0.0
		
		for j in range(len(self.cidades)):
			cidadeJ = self.cidades[j]
			dividendo = pow(self.grafo.feromonio[cidadeI][cidadeJ],alfa)*self.grafo.visibilidade_beta[cidadeI][cidadeJ]
			divisor = self.grafo.divisor[cidadeI] - tiraDivisor
			if divisor != 0:
				probabilidade = dividendo/divisor
			else:
				probabilidade = 0
			self.probabilidades[cidadeJ] = probabilidade
			somaPij += probabilidade
			if rn <= somaPij:
				break		
		# Move a formiga
		self.cidadeAtual = cidadeJ
		# Adiciona no caminho
		self.caminho.append(cidadeJ)
		# Atualiza a cidade escolhida
		cidadeEscolhida = cidadeJ
		# Remove a cidade do condjunto de cidades disponiveis
		self.cidades.remove(cidadeJ)
		# Diminui o divisor da contribuição pela cidade escolhida - cidade escolhida não entra mais na conta
		tiraDivisor += pow(self.grafo.feromonio[cidadeI][cidadeJ],alfa)*self.grafo.visibilidade_beta[cidadeI][cidadeJ]						
		#self.
		#self.testeEscolha()
		return cidadeEscolhida # cidade escolhida

	def iniciaRota( self ):
		""" Adiciona a cidade atual no comeco do caminho """
		self.caminho = []
		self.cidades = self.grafo.getCidadesDisponiveis()
		
		if not self.cidades:
			return False
		else:
			self.calculaDivisores()
			self.cidades.remove(self.cidadeAtual)
			self.caminho.append(self.cidadeAtual)
			return True

	def finalizaRota( self ):
		""" Adiciona a cidade destino, workplace """
		self.caminho.append(self.caminho)
		self.caminho.append(self.caminho[0])
		self.cidadeAtual = self.caminho[0]

	def calculaRota( self ):
		""" Calcula o custo da rota """
		self.custoAtual = 0
		for i in range(0,self.grafo.tamPool-1):
			self.custoAtual += self.grafo.peso[self.caminho[i]][self.caminho[i+1]]

	def existeAresta( self, i, j ):		
		indexI = self.caminho.index(i)
		if self.caminho[indexI + 1] == j:
			return True 	# Existe a aresta ij
		else:
			return False 	# Não existe a aresta ij

	def calculaDeltaTij( self ):
		Q	= self.grafo.q
		# Para cada aresta do caminho que esta formiga percorreu
		for i in range(len(self.caminho)-1):
			cidadeI = self.caminho[i]
			cidadeJ = self.caminho[i+1]
			# Acrescenta Q/L no deltaTao da aresta
			self.grafo.deltaTao[cidadeI][cidadeJ] += Q/self.custoAtual
			# self.grafo.deltaTao[cidadeI][cidadeJ] += Q/self.custoAtual
