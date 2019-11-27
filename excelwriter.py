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
        initial_matrix_25.write(0, i, title)
        empty_matrix_25.write(0, i, title)
        final_matrix_25.write(0, i, title)

        initial_matrix_75.write(0, i, title)
        empty_matrix_75.write(0, i, title)
        final_matrix_75.write(0, i, title)
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


def generate_results_25(initial_matrix, empty_matrix, pc_matrix, final_matrix):
    set_movie_titles()
    fill_initial_matrix(initial_matrix, EMPTY_25)
    fill_empty_matrix(empty_matrix, EMPTY_25)
    fill_pc_matrix(pc_matrix, EMPTY_25)
    fill_final_matrix(final_matrix, EMPTY_25)
    workbook_25.close()


def generate_results_75(initial_matrix, empty_matrix, pc_matrix, final_matrix):
    set_movie_titles()
    fill_initial_matrix(initial_matrix, EMPTY_75)
    fill_empty_matrix(empty_matrix, EMPTY_75)
    fill_pc_matrix(pc_matrix, EMPTY_75)
    fill_final_matrix(final_matrix, EMPTY_75)
    workbook_75.close()