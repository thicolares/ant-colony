ant-colony
==========

An ant colony optimization in Python for the long-term car pooling problem.

(Portuguese)

### Uso
<code>python Principal.py \<grafo> \<t> \<alfa> \<beta> \<rô> \<Q> \<tau_0></code>

Onde:

  	<grafo> Arquivo com um grafo completo
		<t> Número de iterações a ser executado
		<alfa> Expoente da importância do feromônio
		<beta> Expoente da importância do tamanho da aresta
		<rô> Parâmetro de evaporação de feromônio
		<Q> Parâmetro para quantidade de feromônio depositada por formiga
		<tau_0> Quantidade inicial de feromônio nas arestas (tal_0)

### Exemplo:
			python Principal.py grafo.txt 10000 1 5 0.5 100 0.000001

**Dica:** <code>bavaria</code> é um exemplo de grafo completo