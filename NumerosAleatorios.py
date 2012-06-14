#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

from random import *

class NumerosAleatorios( object ):
	"""
	Dentro de uma faixa de valores , gera números aleatórios sem repetir
	- 'qtd_num'		quantidade de valores
	- 'faixa' 		faixa de valores
	"""
	def __init__( self, qtd_num):
		self.faixa = range(qtd_num)

	def numero( self ):
		if self.faixa != []:
			pos = randrange( len(self.faixa) )
			elem = self.faixa[pos]
			self.faixa[pos] = self.faixa[-1]
			del self.faixa[-1]
			return elem
		else:
			return None
