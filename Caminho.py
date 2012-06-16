#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-;

from random import *
from copy import *
from sys import *
import time

class Caminho( object ):

	# na inicialização recebe as cidades
	# retira das cidades a inicial
	def __init__( self, caminho = [], custo = 0):
		self.__caminho = caminho # array de vertices
		self.__custo = custo

	# Caminho / set / property
	def setCaminho( self, caminho ):
		self.__caminho = caminho

	def getCaminho( self ):
		return self.__caminho

	caminho = property(getCaminho, setCaminho)

	# Custo get / set / property
	def setCusto( self, custo ):
		self.__custo = custo

	def getCusto( self ):
		return self.__custo

	custo = property(getCusto, setCusto)

