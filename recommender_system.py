import random
import numpy as np
import math

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


def pearson(x, y):
    x = [2, 0, 3, 5, 4]
    y = [4, 3, 5, 3, 0]

    non_zero_elements_x = np.count_nonzero(x)
    non_zero_elements_y = np.count_nonzero(y)
    total_x = 0
    total_y = 0
    for ele in range(0, len(x)):
        total_x = total_x + x[ele]

    for ele in range(0, len(y)):
        total_y = total_y + y[ele]

    x_mean = total_x / non_zero_elements_x
    y_mean = total_y / non_zero_elements_y

    product = 0
    numerator = 0
    for ele in range(0, len(x)):
        # we need to ignore the elements that are not rated by both users
        if x[ele] != 0 and y[ele] != 0:
            product = (x[ele] - x_mean) * (y[ele] - y_mean)
            numerator += product

    sum_den_x = 0
    sum_den_y = 0
    for ele in range(0, len(x)):
        # we need to ignore the elements that are not rated by both users
        if x[ele] != 0 and y[ele] != 0:
            sum_den_x += pow((x[ele] - x_mean), 2)
            sum_den_y += pow((y[ele] - y_mean), 2)

    denominator = math.sqrt(sum_den_x * sum_den_y)

    pearson_result = numerator / denominator
    return pearson_result;


def main():
    movie_matrix = read_matrix()
    movie_matrix = empty_random(movie_matrix, 0.25)
    print_matrix(movie_matrix)
    count_zeros(movie_matrix)
    pearson()


main()
