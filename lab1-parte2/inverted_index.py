from sortedcontainers import SortedList
from collections import Counter
import operator
import util
import math
import random


inverted_index = dict()
page_tf = dict()
general_tf = dict()


def fill(page_id, text):
    word_counts = Counter(text.split(' '))
    page_tf[page_id] = word_counts

    for word in word_counts:
        if word not in general_tf:
            general_tf[word] = 0

        general_tf[word] += word_counts[word]

        if word not in inverted_index:
            inverted_index[word] = SortedList()

        if page_id not in inverted_index[word]:
            inverted_index[word].add(page_id)


def get_postings(term):
    return inverted_index[term]


def get_tf(term, page_id):
    return page_tf[page_id][term]


def get_general_tf(term):
    return general_tf[term]


def search(sentence, method):
    standardized_sentence = util.standardize_text(sentence)
    words = standardized_sentence.split(' ')

    return {
        'tf': score_search(words, 'tf'),
        'idf': score_search(words, 'idf'),
        'bm25': score_search(words, 'bm25'),
        'binary': binary_search(words)
    }[method]


def merge_results(first_list, second_list):
    results = SortedList()

    i = 0
    j = 0

    while True:
        if first_list[i] == second_list[j]:
            results.add(first_list[i])

        if first_list[i] > second_list[j]:
            j += 1
            if j == len(second_list):
                break

        else:
            i += 1
            if i == len(first_list):
                break

    return results


def calculate_idf(word):
    return math.log((len(inverted_index) + 1)/len(inverted_index[word]))


def calculate_bm25(word,page):
    k = random.random() * 0.8 + 1.2

    return calculate_idf(word) * ((get_tf(word, page) * (k + 1))/(get_tf(word, page) + k))


def binary_search(word_list):
    if len(word_list) == 1:
        return get_postings(word_list[0])

    results = None

    for i in range(1, len(word_list)):
        if i == 1:
            results = merge_results(get_postings(word_list[0]), get_postings(word_list[1]))

        else:
            results = merge_results(results, get_postings(word_list[i]))

    return results


def score_search(word_list, model):
    results = binary_search(word_list)

    sorted_results = []

    for page in results:
        total_score = 0

        for word in word_list:
            if model == 'bm25':
                score = calculate_bm25(word, page)
            else:
                score = get_tf(word, page) * (1 if model == 'tf' else calculate_idf(word))

            total_score += score

        sorted_results.append({'id': page, 'score': total_score})

    sorted_results.sort(key=operator.itemgetter('score'), reverse=True)
    return [e['id'] for e in sorted_results]
