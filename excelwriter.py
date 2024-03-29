import xlsxwriter
import helper_functions as hf
import evaluation_functions as evalf
import operator
import os
from datetime import datetime


titles = []

path = "./results"
try:
    os.mkdir(path)
except OSError:
    print("Creation of the directory %s failed" % path)
else:
    print("Successfully created the directory %s " % path)


def get_titles():
    filepath = 'matrix.txt'

    fp = open(filepath)
    i = 0
    for index, line in enumerate(fp):
        if index < 20:
            titles.append(line)
            i += 1
    fp.close()
    return titles


def set_movie_titles(worksheet, title_format):
    titles = get_titles()
    for title in titles:
        worksheet.write(0, titles.index(title), title, title_format)
    return


def fill_initial_matrix(workbook, matrix):
    # create worksheet
    initial_matrix = workbook.add_worksheet('Main matrix')
    title_format = workbook.add_format()
    title_format.set_bold()
    title_format.set_text_wrap()
    set_movie_titles(initial_matrix, title_format)
    # fill matrix
    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            initial_matrix.write(row+1, column, matrix[row][column])
    return


def fill_empty_matrix(workbook, matrix):
    # create worksheet
    empty_matrix = workbook.add_worksheet('Empty matrix')
    title_format = workbook.add_format()
    title_format.set_bold()
    title_format.set_text_wrap()
    set_movie_titles(empty_matrix, title_format)
    # fill matrix
    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            empty_matrix.write(row+1, column, matrix[row][column])
    return


def fill_normalized_matrix(workbook, matrix):
    # create worksheet
    normalized_matrix = workbook.add_worksheet('Normalized matrix')
    title_format = workbook.add_format()
    title_format.set_bold()
    title_format.set_text_wrap()
    set_movie_titles(normalized_matrix, title_format)
    # fill matrix
    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            normalized_matrix.write(row+1, column, matrix[row][column])
    return


def fill_pc_matrix(workbook, matrix):
    # create worksheet
    pc_matrix = workbook.add_worksheet('Pearson Correlation')
    # fill matrix
    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            pc_matrix.write(row, column, matrix[row][column])
    return


def fill_final_matrix(workbook, matrix, predicted_ratings):
    # create worksheet
    final_matrix = workbook.add_worksheet('Final matrix')
    title_format = workbook.add_format()
    title_format.set_bold()
    title_format.set_text_wrap()
    set_movie_titles(final_matrix, title_format)
    predicted_rating_format = workbook.add_format()
    predicted_rating_format.set_bg_color('#2ECC40')
    predicted_rating_format.set_bold()
    # fill matrix
    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            final_matrix.write(row+1, column, matrix[row][column])
    highlight_predicted_ratings(final_matrix, predicted_ratings, predicted_rating_format)
    return


def fill_predicted_ratings(workbook, ratings):
    ordered_predicted_ratings = workbook.add_worksheet('Predicted ratings')
    column_size = len(max(titles, key=len)) + 5
    ordered_predicted_ratings.set_column('A:T', column_size)
    for user in range(50):
        map_rated_movies = hf.get_all_rated_movies(user, ratings)
        sorted_list_rated_movies = sorted(map_rated_movies.items(), key=operator.itemgetter(1))
        index = 0
        for movie, rating in sorted_list_rated_movies:
            content = titles[movie] + ': ' + str(rating)
            ordered_predicted_ratings.write(user, index, content)
            index += 1
    pass


def highlight_predicted_ratings(worksheet, ratings, rating_format):
    for rating in ratings:
        worksheet.write(rating.user_id + 1, rating.movie_id, rating.predicted_rating, rating_format)
    return


def get_N_ratings(N, non_rounded_info):
    evaluation_ratings = []

    for user in range(50):
        map_rated_movies = hf.get_all_rated_movies(user, non_rounded_info)
        sorted_list_rated_movies = sorted(map_rated_movies.items(), key=operator.itemgetter(1), reverse=1)
        if len(sorted_list_rated_movies) < N:
            no_items = len(sorted_list_rated_movies)
        else:
            no_items = N
        for movie, rating in sorted_list_rated_movies:
            if no_items > 0:
                predicted_eval_obj = hf.PredictedInfo(user, movie, rating)
                evaluation_ratings.append(predicted_eval_obj)
                no_items -= 1

    return evaluation_ratings


def evaluate_rs(workbook, original_matrix, non_rounded_info, N):
    evaluation_results = workbook.add_worksheet('Evaluation')
    title_format = workbook.add_format()
    title_format.set_bold()
    title_format.set_text_wrap()
    prediction_errors = []
    longest_title = max(titles, key=len)
    row = 2
    n_ratings = get_N_ratings(N, non_rounded_info)
    for rating in n_ratings:
        prediction_error = evalf.prediction_error(rating, original_matrix)
        evaluation_results.write(row, 0, rating.user_id + 1)
        evaluation_results.write(row, 1, titles[rating.movie_id])
        evaluation_results.write(row, 2, original_matrix[rating.user_id][rating.movie_id])
        evaluation_results.write(row, 3, rating.predicted_rating)
        evaluation_results.write(row, 4, prediction_error)
        prediction_errors.append(prediction_error)
        row += 1

    mae = evalf.mae(prediction_errors)
    evaluation_results.write('A1', 'MAE:', title_format)
    evaluation_results.write('B1', mae)
    evaluation_results.write('A2', 'User ID', title_format)
    evaluation_results.set_column('A:A', len('User ID'))
    evaluation_results.write('B2', 'Movie title', title_format)
    evaluation_results.set_column('B:B', len(longest_title))
    evaluation_results.write('C2', 'Real rating', title_format)
    evaluation_results.set_column('C:C', len('Real rating'))
    evaluation_results.write('D2', 'Predicted rating', title_format)
    evaluation_results.set_column('D:D', len('Predicted rating'))
    evaluation_results.write('E2', 'Prediction error', title_format)
    evaluation_results.set_column('E:E', len('Prediction error'))
    pass


def generate_results(initial_matrix, empty_matrix, normalized_matrix, pc_matrix, final_matrix, predicted_ratings,
                     non_rounded_info, n, flag):
    now = datetime.now().microsecond
    N = 3
    if flag is hf.EMPTY_25:
        workbook = xlsxwriter.Workbook('./results/rating_analysis_25_' + str(n) + '_' + str(now) + '.xlsx')
    else:
        workbook = xlsxwriter.Workbook('./results/rating_analysis_75_' + str(n) + '_' + str(now) + '.xlsx')
    fill_initial_matrix(workbook, initial_matrix)
    fill_empty_matrix(workbook, empty_matrix)
    fill_normalized_matrix(workbook, normalized_matrix)
    fill_pc_matrix(workbook, pc_matrix)
    fill_final_matrix(workbook, final_matrix, predicted_ratings)
    fill_predicted_ratings(workbook, predicted_ratings)
    evaluate_rs(workbook, initial_matrix, non_rounded_info, N)
    workbook.close()
