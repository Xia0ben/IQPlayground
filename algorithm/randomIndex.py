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

    '''
    get_random_index_vector() : the result is a context vector
    '''

    @staticmethod
    def get_random_index_vector():

        # Generate random positions :
        positions = random.sample(range(RandomIndex.n), RandomIndex.number_ternary)

        # Sort Random positions :
        positions.sort()

        # Throw positions to there 1 and -1 :
        # print(positions)

        # RandomIndex.number_ternary : the number of apparition for the and -1 in the context vector
        a = [1] * RandomIndex.number_ternary

        # for statement to put 1 in impair position and -1 in pair position for having a mean equal to 0
        for i in range(RandomIndex.number_ternary):
            if i % 2 == 0:
                a[i] = a[i] * -1

        # print(a)

        # generate a vector from 0 to RandomIndex.number_ternary, with size equal to RandomIndex.number_ternary
        # and the vector contain unique values
        b = random.sample(range(RandomIndex.number_ternary), RandomIndex.number_ternary)

        # print(b)

        # initialize the correspondence vector, with maintain the correspondence between 1, -1 and the positions :
        c = [1] * RandomIndex.number_ternary

        for i in range(RandomIndex.number_ternary):
            c[b[i]] = a[i]

        # initialize the result vector with size of n, which contain the 1, -1 in the defined positions
        r = [0] * RandomIndex.n

        for i in range(RandomIndex.n):

            if i in positions:
                index_search = positions.index(i)
                r[i] = c[index_search]

        return r
