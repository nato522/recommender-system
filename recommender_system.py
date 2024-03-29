import itertools
import random
from typing import List

import numpy as np
import math
import helper_functions as hf
import excelwriter as ew

# global variables for the number of lines and columns
LINES = 50
COLUMNS = 20


def read_matrix():
    movie_matrix: List[List[int]] = [[0 for x in range(COLUMNS)] for y in range(LINES)]
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

    lines = len(matrix)
    columns = len(matrix[0])
    # generate the same random indexes for every program run
    random.seed(30)
    indexes = list(set(random.sample(list(range(len(flat_list))), int(fraction * columns * lines))));

    # set elements to zero
    for i in indexes:
        flat_list[i] = 0

    # transform the flat list into matrix
    shape = (lines, columns)
    matrix = np.array(flat_list).reshape(shape)
    return matrix


def normalize_matrix(matrix):
    aux_matrix = matrix.copy()
    row = 0
    column = 0
    for row in range(len(matrix)):
        arr = aux_matrix[row]
        avg = hf.get_average(arr)
        for column in range(len(matrix[0])):
            elem = aux_matrix[row][column]
            if elem != 0.0:
                aux_matrix[row][column] = aux_matrix[row][column] - avg
    return aux_matrix


def denormalize_rating_matrix(predicted_rating, matrix, user_index):
    aux_matrix = matrix.copy()
    ratings = aux_matrix[user_index]
    avg = hf.get_average(ratings)
    normalized_rating = predicted_rating + avg
    return normalized_rating


def pearson(x, y):
    x_mean = hf.get_average(x)
    y_mean = hf.get_average(y)

    numerator = 0
    sum_den_x = 0
    sum_den_y = 0
    denominator = 0
    pearson_result = 0
    for ele in range(0, len(x)):
        # we need to ignore the elements that are not rated by both users
        if x[ele] != 0 and y[ele] != 0:
            numerator += (x[ele] - x_mean) * (y[ele] - y_mean)
            sum_den_x += pow((x[ele] - x_mean), 2)
            sum_den_y += pow((y[ele] - y_mean), 2)

        denominator = math.sqrt(sum_den_x * sum_den_y)
    if denominator != 0:
        pearson_result = numerator / denominator
    return pearson_result


def calculate_pearson_matrix(matrix):
    lines = len(matrix)
    pearson_matrix = [[0 for x in range(lines)] for y in range(lines)]
    columns = len(matrix[0])

    # get all the combinations of rows from the matrix
    indexes_list = list(itertools.product(range(lines), repeat=2))
    for ele in range(0, len(indexes_list)):
        i = indexes_list[ele][0]
        j = indexes_list[ele][1]
        pearson_matrix[i][j] = pearson(matrix[i], matrix[j])

    return pearson_matrix


def select_k_neighbours(k, column):
    neighbours = []
    aux_column = column.copy()
    aux_column.sort()

    for index, elem in reversed(list(enumerate(aux_column))):
        if k > 0:
            neighbours.append(elem)
            k -= 1

    return neighbours


def calculate_rating_prediction(k, map_ratings_neighbours):
    rating = 0
    product = 1
    numerator = 0
    denominator = 0
    all_ratings_list = []

    for key in map_ratings_neighbours:
        all_ratings_list.append(map_ratings_neighbours[key][1])
    all_ratings_list.sort(reverse=True)

    ratings_list = []  # the list with all the elements filtered by k

    for element in all_ratings_list:
        if element > k:
            ratings_list.append(element)

    for key in map_ratings_neighbours:
        rating = map_ratings_neighbours[key][0]
        similarity = map_ratings_neighbours[key][1]
        if similarity in ratings_list:
            numerator += rating * similarity
            denominator += abs(similarity)

    if denominator != 0:
        rating = numerator / denominator
    return rating


def get_predicted_ratings(k, pearson_matrix, norm_matrix, movie_matrix):
    # 1st step: determine all the users that have rated the item we want to predict for user u
    # for step 1, we will need the normalized matrix to see where the zeros are
    # 2nd step: choose k users considering the sorted similarities
    # 3rd step: calculate the predicted rating using the formula
    # 4th step: denormalize the result

    list_predicted_info = []
    list_non_rounded_predicted_info = []
    lines_norm = len(norm_matrix)
    columns_norm = len(norm_matrix[0])
    final_matrix = movie_matrix.copy()
    non_rounded_matrix = movie_matrix.copy()

    for i in range(lines_norm):
        # list of column indexes of zero occurrences on every line
        list_zero_col_indexes = np.where(norm_matrix[i] == 0)[0]
        for j in list_zero_col_indexes:
            map_ratings_neighbours = {}
            list_same_column = list(zip(*norm_matrix))[:][j]  # the column of values that includes the 0

            for m in range(lines_norm):
                map_ratings_neighbours[m] = [list_same_column[m]]
            map_ratings_neighbours = dict(filter(lambda elem: elem[1][0] != 0, map_ratings_neighbours.items()))

            for key in map_ratings_neighbours:
                map_ratings_neighbours[key].append(pearson_matrix[key][i])

            # the map will have this structure {index: [rating, pearson_value]}
            # {1: [4.0, 0.143]};  0.143 is the p. value between user 1 and the user we want to calculate the rating for
            rating = calculate_rating_prediction(k, map_ratings_neighbours)
            denormalized_rating = denormalize_rating_matrix(rating, movie_matrix, i)

            non_rounded_matrix[i][j] = denormalized_rating
            non_rounded_predicted_info_obj = hf.PredictedInfo(i, j, non_rounded_matrix[i][j])
            list_non_rounded_predicted_info.append(non_rounded_predicted_info_obj)

            final_matrix[i][j] = hf.round_rating(denormalized_rating)
            predicted_info_obj = hf.PredictedInfo(i, j, final_matrix[i][j])
            list_predicted_info.append(predicted_info_obj)

    return final_matrix, list_predicted_info, list_non_rounded_predicted_info


def main():
    """ Results with the 25% empty cells """
    k_25 = [0, 0.3, 0.6]  # the threshold value based on similarity (the value of pearson)
    initial_matrix = read_matrix()
    movie_matrix_25 = read_matrix()
    movie_matrix_25 = empty_random(movie_matrix_25, 0.25)
    norm_matrix_25 = normalize_matrix(movie_matrix_25)
    pearson_matrix_25 = calculate_pearson_matrix(movie_matrix_25)
    for k in k_25:
        final_matrix_25, list_predicted_info_25, list_non_rounded_info_25 = get_predicted_ratings(k, pearson_matrix_25,
                                                                                                  norm_matrix_25,
                                                                                                  movie_matrix_25)
        ew.generate_results(initial_matrix, movie_matrix_25, norm_matrix_25, pearson_matrix_25, final_matrix_25,
                            list_predicted_info_25, list_non_rounded_info_25, k, hf.EMPTY_25)

    """ Results with the 75% empty cells """
    k_75 = [0, 0.3, 0.6]  # the threshold value based on similarity (the value of pearson)
    movie_matrix_75 = read_matrix()
    movie_matrix_75 = empty_random(movie_matrix_75, 0.75)
    norm_matrix_75 = normalize_matrix(movie_matrix_75)
    pearson_matrix_75 = calculate_pearson_matrix(movie_matrix_75)
    for n in k_75:
        final_matrix_75, list_predicted_info_75, list_non_rounded_info_75 = get_predicted_ratings(n, pearson_matrix_75,
                                                                                                  norm_matrix_75,
                                                                                                  movie_matrix_75)
        ew.generate_results(initial_matrix, movie_matrix_75, norm_matrix_75, pearson_matrix_75, final_matrix_75,
                            list_predicted_info_75, list_non_rounded_info_75, n, hf.EMPTY_75)


main()
