import itertools
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


def get_average(arr):
    arr_total = sum(arr)
    arr_length = np.count_nonzero(arr)
    return arr_total / arr_length


def normalize_matrix(matrix):
    aux_matrix = matrix.copy()
    row = 0
    column = 0
    for row in range(LINES):
        arr = aux_matrix[row]
        avg = get_average(arr)
        for column in range(COLUMNS):
            elem = aux_matrix[row][column]
            if elem != 0.0:
                aux_matrix[row][column] = aux_matrix[row][column] - avg
    return aux_matrix


def pearson(x, y):

    x_mean = get_average(x)
    y_mean = get_average(y)

    numerator = 0
    sum_den_x = 0
    sum_den_y = 0
    for ele in range(0, len(x)):
        # we need to ignore the elements that are not rated by both users
        if x[ele] != 0 and y[ele] != 0:
            numerator += (x[ele] - x_mean) * (y[ele] - y_mean)
            sum_den_x += pow((x[ele] - x_mean), 2)
            sum_den_y += pow((y[ele] - y_mean), 2)

    denominator = math.sqrt(sum_den_x * sum_den_y)

    pearson_result = numerator / denominator
    return pearson_result


def calculate_pearson_matrix(matrix):
    pearson_matrix = [[0 for x in range(LINES)] for y in range(LINES)]

    lines = len(matrix)
    columns = len(matrix[0])

    # get all the combinations of rows from the matrix
    indexes_list = list(itertools.product(range(lines), repeat=2))
    for ele in range(0, len(indexes_list)):
        i = indexes_list[ele][0]
        j = indexes_list[ele][1]
        pearson_matrix[i][j] = pearson(matrix[i], matrix[j])

    return pearson_matrix


# helper function
def print_matrix(matrix):
    i_aux = 0
    j_aux = 0
    for i_aux in range(len(matrix)):
        for j_aux in range(len(matrix[0])):
            print(matrix[i_aux][j_aux], end=" ")
        print()


# helper function to check that 25% of the matrix is with the value 0
def count_zeros(matrix):
    i_aux = 0
    j_aux = 0
    count = 0
    for i_aux in range(len(matrix)):
        for j_aux in range(len(matrix[0])):
            if matrix[i_aux][j_aux] == 1.0:
                count += 1
    return count


def select_k_neighbours(k, column):
    aux_column = column.copy()
    # for i in range(k):
    #   print(aux_column[i], end=" \n")
    print(aux_column)


def predicted_value(matrix):
    print('My matrix:')
    print(matrix)
    print('----------------------')
    columns = np.size(matrix, 1)
    for i in range(columns-1):
        col = matrix[:, i]
        print(col)
        select_k_neighbours(2, col)
        print('----------------------')


def main():
    movie_matrix = read_matrix()
    movie_matrix = empty_random(movie_matrix, 0.25)
    norm_matrix = normalize_matrix(movie_matrix)

    pearson_matrix = calculate_pearson_matrix(norm_matrix)
    print_matrix(pearson_matrix)
    print(count_zeros(pearson_matrix))
    my_matrix = np.matrix('0 1 2 3 4 5 6 7 8 9; 25 12 4 35 6 663 12 34 99 109; 8 8 9 0 1 2 7 8 9 0; 11 22 33 44 55 66 77 88 99 189')
    predicted_value(my_matrix)

main()
