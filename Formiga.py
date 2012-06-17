#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-;

from random import *
from copy import *
from sys import *
from Grafo import *
import time

class Formiga( object ):

	# na inicialização recebe as cidades
	# retira das cidades a inicial
	def __init__( self, grafo, cidadeInicial = 0):
		self.caminho = []
		self.caminhos = []
		self.cidades = []
		self.probabilidades = {}
		self.grafo = grafo
		self.cidadeAtual = cidadeInicial
		self.cidadeInicial = cidadeInicial
		self.custoAtual = 0
		self.custoTotal = 0
		self.deltaTao2 = 0

	# TODO não conheço sobrecarga em python! hehe
	def setCaminho( self, caminho ):
		self.caminho = caminho
		self.cidadeAtual = self.caminho[0]

	def getCidadeAtual( self ):
		return self.cidadeAtual

	def getCidadeInicial( self ):
		return self.cidadeInicial

	def getCidades( self ):
		return self.cidades

	def getCustoTotal( self ):
		return self.custoTotal

	def getCustoAtual( self, custoAtual ):
		self.custoAtual = custoAtual

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
		somaPij = 0.0
		rn = random() 
		cidadeI = self.cidadeAtual
		tiraDivisor = 0.0

		if not self.cidades:
			return False
		# print 'Cidades disponíveis: ',self.cidades
		for cidade in self.cidades:        # Second Example
			cidadeJ = cidade
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
		# print 'cidade escolhida: ', cidadeJ
		# Remove a cidade do condjunto de cidades disponiveis
		self.cidades.remove(cidadeJ)
		# Diminui o divisor da contribuição pela cidade escolhida - cidade escolhida não entra mais na conta
		tiraDivisor += pow(self.grafo.feromonio[cidadeI][cidadeJ],alfa)*self.grafo.visibilidade_beta[cidadeI][cidadeJ]						
		
		return cidadeEscolhida # cidade escolhida

	def ultimaCidade( self ):
		self.caminho.append(0) # ultima cidade

	def carregaCidades( self ):
		""" Adiciona a cidade atual no comeco do caminho """
		self.caminho = []
		self.cidades = self.grafo.getCidadesDisponiveis()
		self.cidades.remove(0) # Remove a cidade final, 0


	def iniciaRota( self ):
		if not self.cidades:
			return False
		else:
			self.caminho = [] # limpa o caminho
			self.calculaDivisores()
			self.cidadeInicial = choice(self.cidades) # pega uma cidade aleatório
			self.cidadeAtual = self.cidadeInicial
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
		for i in range(0,self.grafo.getTamCaminho() + 1): # + 1 é para pegar calcular o destino final
			self.custoAtual += self.grafo.peso[self.caminho[i]][self.caminho[i+1]]
		self.custoTotal += self.custoAtual

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
