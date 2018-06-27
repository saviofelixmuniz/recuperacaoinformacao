import csv
import re
import timeit
from sortedcontainers import SortedList

TITLE_INDEX = 0
BODY_INDEX = 1
ID_INDEX = 2

start = timeit.default_timer()

def fillInvertedIndex(pageId, text, invertedIndex):
    for word in text.split(' '):
        lowerWord = word.lower()
        if lowerWord not in invertedIndex:
            invertedIndex[lowerWord] = SortedList()

        if pageId not in invertedIndex[lowerWord]:
            invertedIndex[lowerWord].add(pageId)

def search(input):
    terms = input.split(' ')
    if len(terms) == 1:
        return invertedIndex[terms[0]]

    else:
        if (terms[1] == 'AND'):
            return searchAnd(terms[0], terms[2], invertedIndex)

        if (terms[1] == 'OR'):
            return searchOr(terms[0], terms[2], invertedIndex)

def searchOr(firstTerm, secondTerm, invertedIndex):
    results = SortedList()
    for pageId in invertedIndex[firstTerm.lower()]:
        results.add(pageId)

    for pageId in invertedIndex[secondTerm.lower()]:
        if pageId not in results:
            results.add(pageId)

    return results

def searchAnd(firstTerm, secondTerm, invertedIndex):
    results = SortedList()

    firstTermList = invertedIndex[firstTerm.lower()]
    secondTermList = invertedIndex[secondTerm.lower()]

    i = 0
    j = 0

    while True:
        if firstTermList[i] == secondTermList[j]:
            results.add(firstTermList[i])

        if firstTermList[i] > secondTermList[j]:
            j += 1
            if j == len(secondTermList):
                break

        else:
            i += 1
            if i == len(firstTermList):
                break

    return results

with open('estadao.csv', 'rt', encoding='utf8') as csvfile:
    estadao = csv.reader(csvfile)

    invertedIndex = dict()
    pages = dict()

    for index, row in enumerate(estadao):
        if index == 0:
            continue

        pageId = int(row[ID_INDEX])

        title = row[TITLE_INDEX]
        body = row[BODY_INDEX]

        pages[pageId] = {'title': title, 'body': body}

        fillInvertedIndex(pageId, title, invertedIndex)
        fillInvertedIndex(pageId, body, invertedIndex)

stop = timeit.default_timer()

print(len(search('debate OR presidencial')))
print(len(search('debate AND presidencial')))

print(len(search('presidenciáveis OR corruptos')))
print(len(search('presidenciáveis AND corruptos')))

print(len(search('Belo OR Horizonte')))
print(len(search('Belo AND Horizonte')))
