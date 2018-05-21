import csv
import timeit
import inverted_index
import util

TITLE_INDEX = 1
ID_INDEX = 5
BODY_INDEX = 3

start = timeit.default_timer()

with open('estadao_noticias_eleicao.csv', 'rt', encoding='utf8') as csvfile:
    estadao = csv.reader(csvfile)

    for index, text_row in enumerate(estadao):
        if index == 0:
            continue

        pageId = int(text_row[ID_INDEX])
        content = util.standardize_text(util.join_list(text_row[1:4]))

        inverted_index.fill(pageId, content)

stop = timeit.default_timer()

print('segundo turno')
print('tf')
print(inverted_index.search('segundo turno', 'tf')[0:5])
print('bm25')
print(inverted_index.search('segundo turno', 'bm25')[0:5])
print('idf')
print(inverted_index.search('segundo turno', 'idf')[0:5])

print('lava jato')
print('tf')
print(inverted_index.search('lava jato', 'tf')[0:5])
print('bm25')
print(inverted_index.search('lava jato', 'bm25')[0:5])
print('idf')
print(inverted_index.search('lava jato', 'idf')[0:5])

print('projeto de lei')
print('tf')
print(inverted_index.search('projeto de lei', 'tf')[0:5])
print('bm25')
print(inverted_index.search('projeto de lei', 'bm25')[0:5])
print('idf')
print(inverted_index.search('projeto de lei', 'idf')[0:5])

print('compra de voto')
print('tf')
print(inverted_index.search('compra de voto', 'tf')[0:5])
print('bm25')
print(inverted_index.search('compra de voto', 'bm25')[0:5])
print('idf')
print(inverted_index.search('compra de voto', 'idf')[0:5])

print('ministério público')
print('tf')
print(inverted_index.search('ministério público', 'tf')[0:5])
print('bm25')
print(inverted_index.search('ministério público', 'bm25')[0:5])
print('idf')
print(inverted_index.search('ministério público', 'idf')[0:5])

