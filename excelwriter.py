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
    i = 0
    for title in titles:
        worksheet.write(0, i, title, title_format)
        i += 1
    return


def fill_initial_matrix(workbook, matrix):
    # create worksheet
    initial_matrix = workbook.add_worksheet('Main matrix')
    title_format = workbook.add_format()
    title_format.set_bold()
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
    set_movie_titles(empty_matrix, title_format)
    # fill matrix
    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            empty_matrix.write(row+1, column, matrix[row][column])
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
    set_movie_titles(final_matrix, title_format)
    predicted_rating_format = workbook.add_format()
    predicted_rating_format.set_bg_color('yellow')
    # fill matrix
    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            final_matrix.write(row+1, column, matrix[row][column])
    highlight_predicted_ratings(final_matrix, predicted_ratings, predicted_rating_format)
    return


def fill_predicted_ratings(workbook, ratings):
    ordered_predicted_ratings = workbook.add_worksheet('Predicted ratings')
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


def evaluate_rs(workbook, original_matrix, ratings):
    evaluation_results = workbook.add_worksheet('Evaluation')
    prediction_errors = []
    row = 2
    for rating in ratings:
        prediction_error = evalf.prediction_error(rating, original_matrix)
        evaluation_results.write(row, 0, rating.user_id)
        evaluation_results.write(row, 1, titles[rating.movie_id])
        evaluation_results.write(row, 2, original_matrix[rating.user_id][rating.movie_id])
        evaluation_results.write(row, 3, rating.predicted_rating)
        evaluation_results.write(row, 4, prediction_error)
        prediction_errors.append(prediction_error)
        row += 1

    mae = evalf.mae(prediction_errors)
    evaluation_results.write('A1', 'MAE:')
    evaluation_results.write('B1', mae)
    evaluation_results.write('A2', 'User ID')
    evaluation_results.write('B2', 'Movie')
    evaluation_results.write('C2', 'Real rating')
    evaluation_results.write('D2', 'Predicted rating')
    evaluation_results.write('E2', 'Prediction error')
    pass


def generate_results_25(initial_matrix, empty_matrix, pc_matrix, final_matrix, predicted_ratings, k):
    now = datetime.now().microsecond
    workbook_25 = xlsxwriter.Workbook('./results/rating_analysis_25_' + str(k) + '_' + str(now) + '.xlsx')
    fill_initial_matrix(workbook_25, initial_matrix)
    fill_empty_matrix(workbook_25, empty_matrix)
    fill_pc_matrix(workbook_25, pc_matrix)
    fill_final_matrix(workbook_25, final_matrix, predicted_ratings)
    fill_predicted_ratings(workbook_25, predicted_ratings)
    evaluate_rs(workbook_25, initial_matrix, predicted_ratings)
    workbook_25.close()


def generate_results_75(initial_matrix, empty_matrix, pc_matrix, final_matrix, predicted_ratings, n):
    now = datetime.now().microsecond
    workbook_75 = xlsxwriter.Workbook('./results/rating_analysis_75_' + str(n) + '_' + str(now) + '.xlsx')
    fill_initial_matrix(workbook_75, initial_matrix)
    fill_empty_matrix(workbook_75, empty_matrix)
    fill_pc_matrix(workbook_75, pc_matrix)
    fill_final_matrix(workbook_75, final_matrix, predicted_ratings)
    fill_predicted_ratings(workbook_75, predicted_ratings)
    evaluate_rs(workbook_75, initial_matrix, predicted_ratings)
    workbook_75.close()