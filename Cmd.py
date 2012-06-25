#!/usr/bin/env python 
# -*- coding: iso-8859-1 -*-
from sys import *

class Cmd( object ):
	"""
	Lê parâmetros a partir da linha de comando para executar o programa
	"""
	def __init__( self ):
		self.ajuda = """
		USO: python Principal.py <grafo> <t> <alfa> <beta> <rô> <Q> <tau_0>\n
		<grafo> Arquivo com um grafo completo
		<t> Número de iterações a ser executado
		<alfa> Expoente da importância do feromônio
		<beta> Expoente da importância do tamanho da aresta
		<rô> Parâmetro de evaporação de feromônio
		<Q> Parâmetro para quantidade de feromônio depositada por formiga
		<tau_0> Quantidade inicial de feromônio nas arestas (tal_0)
		<N> Número global de iterações a serem feitas
		Exemplos:
			python Principal.py grafo.txt 10000 1 5 0.5 100 0.000001 1
			python Principal.py grafo.txt 10000 1 10 0.5 100 0.000001 20
		"""
		try:
			self.var = {}
			self.var['GRAFO']= argv[1]
			self.var['t'] 	=  int(argv[2])
			self.var['ALFA'] = float(argv[3])
			self.var['BETA'] = float(argv[4])
			self.var['RO']   = float(argv[5])
			self.var['Q']    = float(argv[6])
			self.var['T0']   = float(argv[7])
			self.var['N']   = int(argv[8])
		except:
			print self.ajuda
			exit()
