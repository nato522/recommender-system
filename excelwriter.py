import xlsxwriter

EMPTY_25 = 0
EMPTY_75 = 1

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
ordered_predicted_ratings_25 = workbook_25.add_worksheet()
ordered_predicted_ratings_75 = workbook_75.add_worksheet()


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
    titles = []
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
                initial_matrix_75.write(row + 1, column, matrix[row][column])
    return


def fill_empty_matrix(matrix, flag):
    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            if flag is EMPTY_25:
                empty_matrix_25.write(row+1, column, matrix[row][column])
            else:
                empty_matrix_75.write(row + 1, column, matrix[row][column])
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
                final_matrix_75.write(row + 1, column, matrix[row][column])
    return


def fill_predicted_ratings(ratings, flag):
    '''
    TODO: iterate the list of object to show predicted ratings in order
    :param ratings: list of objects with userId, movieId, and predicted rating
    :param flag: file identifier
    :return: nothing, just writes the predicted ratings in descending order in the corresponding sheet
    '''
    if flag is EMPTY_25:
        ordered_predicted_ratings_25.write()
    else:
        ordered_predicted_ratings_75.write()
    pass

def highlight_predicted_ratings(ratings, flag):
    '''
    TODO: iterate the list of object to identify cell location
    :param ratings: list of objects with userId, movieId, and predicted rating
    :param flag: file identifier
    :return: nothing, just adds format to the predicted ratings' cells
    '''
    if flag is EMPTY_25:
        final_matrix_25.write(user, movie, predicted_rating_format_25)
    else:
        final_matrix_75.write(user, movie, predicted_rating_format_75)
    pass


def generate_results_25(initial_matrix, empty_matrix, pc_matrix, final_matrix, predicted_ratings):
    set_movie_titles()
    fill_initial_matrix(initial_matrix, EMPTY_25)
    fill_empty_matrix(empty_matrix, EMPTY_25)
    fill_pc_matrix(pc_matrix, EMPTY_25)
    fill_final_matrix(final_matrix, EMPTY_25)
    # highlight_predicted_ratings(predicted_ratings, EMPTY_25)
    # fill_predicted_ratings(predicted_ratings, EMPTY_25)
    workbook_25.close()


def generate_results_75(initial_matrix, empty_matrix, pc_matrix, final_matrix, predicted_ratings):
    set_movie_titles()
    fill_initial_matrix(initial_matrix, EMPTY_75)
    fill_empty_matrix(empty_matrix, EMPTY_75)
    fill_pc_matrix(pc_matrix, EMPTY_75)
    fill_final_matrix(final_matrix, EMPTY_75)
    # highlight_predicted_ratings(predicted_ratings, EMPTY_75)
    # fill_predicted_ratings(predicted_ratings, EMPTY_75)
    workbook_75.close()