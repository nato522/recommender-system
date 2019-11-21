import random
import numpy as np

# global variables for the number of lines and columns
LINES = 50
COLUMNS = 20


def read_matrix():
    movie_matrix = [[0 for x in range(COLUMNS)] for y in range(LINES)]
    filepath = 'matrix.txt'

    fp = open(filepath)
    i = 0
    for index, line in enumerate(fp):
        if index >= 20:
            # we will have an array of ratings for each line
            line_vector = []
            line_vector = line.split()  # split by space
            j = 0
            for rating in line_vector:
                movie_matrix[i][j] = float(rating)
                j += 1
            i += 1
    fp.close()
    return movie_matrix


def empty_random(matrix, fraction):

    # the matrix transformed into a list
    flat_list = []
    for sublist in matrix:
        for item in sublist:
            flat_list.append(item)

    # generate the same random indexes for every program run
    random.seed(30)
    indexes = list(set(random.sample(list(range(len(flat_list))), int(fraction * COLUMNS * LINES))));

    # set elements to zero
    for i in indexes:
        flat_list[i] = 0

    # transform the flat list into matrix
    shape = (LINES, COLUMNS)
    matrix = np.array(flat_list).reshape(shape)
    return matrix


# helper function
def print_matrix(matrix):
    i_aux = 0
    j_aux = 0
    for i_aux in range(LINES):
        for j_aux in range(COLUMNS):
            print(matrix[i_aux][j_aux], end=' ')
        print()


# helper function to check that 25% of the matrix is with the value 0
def count_zeros(matrix):
    i_aux = 0
    j_aux = 0
    count = 0
    for i_aux in range(LINES):
        for j_aux in range(COLUMNS):
            if matrix[i_aux][j_aux] == 0:
                count += 1
    print(count)


def main():
    movie_matrix = read_matrix()
    movie_matrix = empty_random(movie_matrix, 0.25)
    print_matrix(movie_matrix)
    count_zeros(movie_matrix)

main()
