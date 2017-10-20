# import numpy
import random

class RandomIndex:

    n = 100
    number_ternary = 20

    @staticmethod
    def get_n():
        return RandomIndex.n

    @staticmethod
    def get_number_ternary():
        return RandomIndex.n

    @staticmethod
    def set_n(n):
        RandomIndex.n = n

    @staticmethod
    def set_number_ternary(number_ternary):
        RandomIndex.number_ternary = number_ternary

    @staticmethod
    def get_random_index_vector():

        """
        print(numpy.random.randint(fin, size=8))
        """

        # Generate random positions :
        positions = random.sample(range(RandomIndex.n), RandomIndex.number_ternary)

        # Sort Random positions :
        positions.sort()

        # Throw positions to there 1 and -1 :
        # print(positions)

        a = [1] * RandomIndex.number_ternary

        for i in range(RandomIndex.number_ternary):
            if i % 2 == 0:
                a[i] = a[i] * -1

        # print(a)

        b = random.sample(range(RandomIndex.number_ternary), RandomIndex.number_ternary)

        # print(b)

        c = [1] * RandomIndex.number_ternary

        for i in range(RandomIndex.number_ternary):
            c[b[i]] = a[i]

        # print(c)

        r = [0] * RandomIndex.n

        for i in range(RandomIndex.n):

            if i in positions:
                index_search = positions.index(i)
                r[i] = c[index_search]

        return r
