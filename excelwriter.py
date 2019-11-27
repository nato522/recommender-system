import xlsxwriter
import helpers as help
import operator
import os

EMPTY_25 = 0
EMPTY_75 = 1
titles = []

path = "./results"
try:
    os.mkdir(path)
except OSError:
    print("Creation of the directory %s failed" % path)
else:
    print("Successfully created the directory %s " % path)

workbook_25 = xlsxwriter.Workbook('./results/rating_analysis_25.xlsx')
workbook_75 = xlsxwriter.Workbook('./results/rating_analysis_75.xlsx')

# First sheet for the initial matrix
initial_matrix_25 = workbook_25.add_worksheet('Main matrix')
initial_matrix_75 = workbook_75.add_worksheet('Main matrix')

# Second sheet for the empty matrix
empty_matrix_25 = workbook_25.add_worksheet('Empty matrix')
empty_matrix_75 = workbook_75.add_worksheet('Empty matrix')

# Third sheet for the Pearson correlation
pc_matrix_25 = workbook_25.add_worksheet('Pearson Correlation')
pc_matrix_75 = workbook_75.add_worksheet('Pearson Correlation')

# Fourth sheet for the final matrix with predicted ratings
final_matrix_25 = workbook_25.add_worksheet('Final matrix')
final_matrix_75 = workbook_75.add_worksheet('Final matrix')

# Fifth sheet for the set of predicted ratings per user
ordered_predicted_ratings_25 = workbook_25.add_worksheet('Predicted ratings')
ordered_predicted_ratings_75 = workbook_75.add_worksheet('Predicted ratings')


# Format rules
title_format_25 = workbook_25.add_format()
title_format_75 = workbook_75.add_format()
predicted_rating_format_25 = workbook_25.add_format()
predicted_rating_format_75 = workbook_75.add_format()

title_format_25.set_bold()
title_format_75.set_bold()
predicted_rating_format_25.set_bg_color('yellow')
predicted_rating_format_75.set_bg_color('yellow')

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


def set_movie_titles():
    titles = get_titles()
    i = 0
    for title in titles:
        initial_matrix_25.write(0, i, title, title_format_25)
        empty_matrix_25.write(0, i, title, title_format_25)
        final_matrix_25.write(0, i, title, title_format_25)

        initial_matrix_75.write(0, i, title, title_format_75)
        empty_matrix_75.write(0, i, title, title_format_75)
        final_matrix_75.write(0, i, title, title_format_75)
        i += 1
    return


def fill_initial_matrix(matrix, flag):
    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            if flag is EMPTY_25:
                initial_matrix_25.write(row+1, column, matrix[row][column])
            else:
                initial_matrix_75.write(row+1, column, matrix[row][column])
    return


def fill_empty_matrix(matrix, flag):
    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            if flag is EMPTY_25:
                empty_matrix_25.write(row+1, column, matrix[row][column])
            else:
                empty_matrix_75.write(row+1, column, matrix[row][column])
    return


def fill_pc_matrix(matrix, flag):
    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            if flag is EMPTY_25:
                pc_matrix_25.write(row, column, matrix[row][column])
            else:
                pc_matrix_75.write(row, column, matrix[row][column])
    return


def fill_final_matrix(matrix, flag):
    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            if flag is EMPTY_25:
                final_matrix_25.write(row+1, column, matrix[row][column])
            else:
                final_matrix_75.write(row+1, column, matrix[row][column])
    return


def fill_predicted_ratings(ratings, flag):
    for user in range(50):
        map_rated_movies = help.get_all_rated_movies(user, ratings)
        sorted_list_rated_movies = sorted(map_rated_movies.items(), key=operator.itemgetter(1))
        index = 0
        for movie, rating in sorted_list_rated_movies:
            content = titles[movie] + ': ' + str(rating)
            if flag is EMPTY_25:
                ordered_predicted_ratings_25.write(user, index, content)
            else:
                ordered_predicted_ratings_75.write(user, index, content)
            index += 1
    pass


def highlight_predicted_ratings(ratings, flag):
    if flag is EMPTY_25:
        for rating in ratings:
            final_matrix_25.write(rating.user_id + 1, rating.movie_id, rating.predicted_rating, predicted_rating_format_25)
    else:
        for rating in ratings:
            final_matrix_75.write(rating.user_id + 1, rating.movie_id, rating.predicted_rating, predicted_rating_format_75)
    pass


def generate_results_25(initial_matrix, empty_matrix, pc_matrix, final_matrix, predicted_ratings):
    set_movie_titles()
    fill_initial_matrix(initial_matrix, EMPTY_25)
    fill_empty_matrix(empty_matrix, EMPTY_25)
    fill_pc_matrix(pc_matrix, EMPTY_25)
    fill_final_matrix(final_matrix, EMPTY_25)
    highlight_predicted_ratings(predicted_ratings, EMPTY_25)
    fill_predicted_ratings(predicted_ratings, EMPTY_25)
    workbook_25.close()


def generate_results_75(initial_matrix, empty_matrix, pc_matrix, final_matrix, predicted_ratings):
    set_movie_titles()
    fill_initial_matrix(initial_matrix, EMPTY_75)
    fill_empty_matrix(empty_matrix, EMPTY_75)
    fill_pc_matrix(pc_matrix, EMPTY_75)
    fill_final_matrix(final_matrix, EMPTY_75)
    highlight_predicted_ratings(predicted_ratings, EMPTY_75)
    fill_predicted_ratings(predicted_ratings, EMPTY_75)
    workbook_75.close()