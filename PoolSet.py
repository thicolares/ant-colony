#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-;

class PoolSet( object ):

	# na inicialização recebe as cidades
	# retira das cidades a inicial
	def __init__( self, pools = [], custo = 0):
		self.__pools = pools # array de vertices
		self.__custo = custo

	# Caminho / set / property
	def addPool( self, pool ):
		self.__pools.append(pool)
		self.__custo += pool.getCusto()

	def getPools( self ):
		return self.__pools


	def getCusto( self ):
		return self.__custo

	def kill(self):
		del self

