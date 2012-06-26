#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-;

class Pool( object ):

	# na inicialização recebe as cidades
	# retira das cidades a inicial
	def __init__( self, caminhos = {}, custo = 99999999, pool = []):
		self.__caminhos = caminhos # array de vertices
		self.__custo = custo
		self.__pool = pool
		self.__poolFinal = list(self.__pool)
		self.__poolFinal.append(0)
		self.__indexDoMelhorCaminho = 0
		self.__indexDoPiorCaminho = 0

	# Caminho / set / property
	def setCaminhos( self, caminhos ):
		self.__caminhos = caminhos

	def getCaminhos( self ):
		return self.__caminhos

	def calculeMelhorCaminho( self ):
		melhorCusto = 999999999
		piorCusto = 0
		melhorIndex = 0
		for index in self.__caminhos:
			# print self.__caminhos[index].getCusto(), ' < ', melhorCusto
			if self.__caminhos[index].getCusto() < melhorCusto:
				melhorIndex = index
				melhorCusto = self.__caminhos[index].getCusto()

			if self.__caminhos[index].getCusto() > piorCusto:
				melhorIndex = index
				melhorCusto = self.__caminhos[index].getCusto()
		self.__indexDoMelhorCaminho = melhorIndex

	def getMelhorCaminho( self ):
		if self.__indexDoMelhorCaminho == 0:
			return False
		return self.__caminhos[self.__indexDoMelhorCaminho]

	# Custo get / set / property
	def setCusto( self, custo ):
		self.__custo = custo

	def getCusto( self ):
		return self.__custo

	# Custo get / set / property
	def setPool( self, pool ):
		self.__pool = pool
		self.__poolFinal = list(self.__pool)
		self.__poolFinal.append(0)

	def getPool( self ):
		return self.__pool

	def getPoolFinal( self ):
		return self.__poolFinal