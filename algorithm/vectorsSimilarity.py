"""
cosine_similarity is defined as value between -1 to 1,
cosine_distance is defined as: 1 - cosine_similarity --> hence cosine_distance range is 0 to 2

"""
from math import *


class VectorsSimilarity:

    base_similarity = 0.7

    @staticmethod
    def get_base_similarity():
        return VectorsSimilarity.base_similarity

    @staticmethod
    def set_base_similarity(bs):
        VectorsSimilarity.base_similarity = bs

    @staticmethod
    def square_rooted(x):
        return round(sqrt(sum([a * a for a in x])), 3)

    @staticmethod
    def cosine_similarity(x, y):
        numerator = sum(a * b for a, b in zip(x, y))
        denominator = VectorsSimilarity.square_rooted(x) * VectorsSimilarity.square_rooted(y)
        return round(numerator / float(denominator), 3)

    @staticmethod
    def cosine_distance(x, y):
        return 1 - VectorsSimilarity.cosine_similarity(x, y)

    @staticmethod
    def cosine_distances(x, matrix_dict):
        distances = list()
        for v in matrix_dict.values():
            distances.append(VectorsSimilarity.cosine_distance(x, v))
        return distances


