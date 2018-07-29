import os
import operator
from surprise import Reader
from surprise import KNNBasic
from surprise import Dataset
from surprise.model_selection import cross_validate
import shutil

DEFAULT_USER = "12345"
MAX_GRADE = "5"
DEFAULT_TIMESTAMP = "000000000"


def recommend(movie_list):
    """
    Fornece as notas previstas para um usuário que assistiu uma lista de filmes
    :param movie_list: Lista de filmes assistidos
    """
    add_movie_list(movie_list)

    file_path = os.path.expanduser('./ml-100k/u.data')
    reader = Reader(line_format='user item rating timestamp', sep='\t')
    data = Dataset.load_from_file(file_path, reader=reader)

    trainset = data.build_full_trainset()

    algo = KNNBasic()
    algo.fit(trainset)

    ratings = get_all_ratings(12345, algo, movie_list)
    os.remove('./ml-100k/u.data')
    shutil.copy('./ml-100k/u_backup.data', './ml-100k/u.data')
    return ratings


def add_movie_list(movies):
    """
    Adiciona filmes para a tabela de notas MovieLens
    :param movies: array de id de filmes que o usuário já assistiu e gostou
    :return:
    """
    f = open("./ml-100k/u.data", "a")

    for movie in movies:
        f.write("%s\t%s\t%s\t%s\n" % (DEFAULT_USER, movie, MAX_GRADE, DEFAULT_TIMESTAMP))

    f.close()


def read_all_movies():
    """
    Lê todos os filmes da tabela itens
    :return:
    """
    file = open("./ml-100k/u.item", "r", encoding='ISO-8859-1')
    lines = file.readlines()
    movies = []
    for line in lines:
        columns = line.split('|')
        movie_id = columns[0]
        name = columns[1]
        movies.append({"id": movie_id, "name": name})

    return get_movie_sum_ratings(movies)


def get_movie_sum_ratings(movies):
    """
    Fornece a lista de todos os filmes com a soma de todas as notas que obteve, ordenado de forma decrescente
    :param movies: Lista de filmes da tabela itens
    """
    file = open("./ml-100k/u_backup.data", "r", encoding='ISO-8859-1')
    lines = file.readlines()
    ratings = {}
    for line in lines:
        columns = line.split('\t')
        movie_id = columns[1]
        rating = columns[2]
        if movie_id not in ratings:
            ratings[movie_id] = 0
        ratings[movie_id] += int(rating)

    for movie in movies:
        movie["rating"] = ratings[movie["id"]]

    movies.sort(key=operator.itemgetter('rating'), reverse=True)
    return movies


def get_all_ratings(user, algo, movie_list):
    """
    Retorna a previsão de notas de todos os filmes de um usuário
    :param user: id do usuário
    :param algo: modelo treinado
    :param movie_list: lista de filmes que o usuário assistiu
    :return:
    """
    uid = str(user)
    preds = []
    for movie in read_all_movies():
        if movie["id"] in movie_list:
            continue

        iid = str(movie["id"])
        pred = algo.predict(uid, iid)
        preds.append({"item_id": iid, "rating": pred.est})

    preds.sort(key=operator.itemgetter('rating'), reverse=True)
    return preds

