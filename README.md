ant-colony
==========

An ant colony optimization in Python for the long-term car pooling problem.

(Portuguese)

### Uso
<code>python Principal.py \<grafo> \<t> \<alfa> \<beta> \<rô> \<Q> \<tau_0></code>

Onde:

  	<grafo> Nome da pasta com os arquivos <grafo>_03_weight_graphs.txt
		Exemplo, <grafo> = UFBA11:
		GRAPHS/UFBA11/UFBA11_03_weight_graphs.txt
	<t> Número de iterações a ser executado
	<alfa> Expoente da importância do feromônio
	<beta> Expoente da importância do tamanho da aresta
	<rô> Parâmetro de evaporação de feromônio
	<Q> Parâmetro para quantidade de feromônio depositada por formiga
	<tau_0> Quantidade inicial de feromônio nas arestas (tal_0)

###Exemplos:
	python Principal.py UFBA11 10000 1 5 0.5 100 0.000001 1
	python Principal.py UFBA11 10000 1 10 0.5 100 0.000001 20

Para melhor performance, execute com pypy (<http://pypy.org/>):

    pypy Principal.py UFBA11 10000 1 5 0.5 100 0.000001 1
    pypy Principal.py UFBA11 10000 1 10 0.5 100 0.000001 20