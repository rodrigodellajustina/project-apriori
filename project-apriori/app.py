from apyori import apriori

lista_transacoes = [
    ['cerveja', 'queijo'],
    ['cerveja', 'fritas'],
    ['cerveja', 'mandioca'],
    ['cerveja', 'mandioca'],
    ['cerveja', 'mandioca'],
    ['cerveja', 'mandioca'],
    ['refrigerante', 'fritas'],
    ['refrigerante', 'fritas'],
    ['refrigerante', 'fritas']
]

result = list(apriori(lista_transacoes))

for ranking in result:
    x = list(ranking.items)
    print(str(x)+'  '+str(ranking.support*100))

