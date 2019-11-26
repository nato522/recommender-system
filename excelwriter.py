import xlsxwriter
import recommender_system as rs

workbook = xlsxwriter.Workbook('./results/rating_analysis.xlsx')

# First sheet for the initial matrix
initial_matrix = workbook.add_worksheet()

# Second sheet for the empty matrix
empty_matrix = workbook.add_worksheet()

# Third sheet for the Pearson correlation
pc_matrix = workbook.add_worksheet()

# Fourth sheet for the final matrix with predicted ratings
final_matrix = workbook.add_worksheet()

# Fifth sheet for the set of predicted ratings per user
ordered_predicted_ratings = workbook.add_worksheet()


#initial_matrix.write('A1', 'Hello world')
#empty_matrix.write('A1', 'Hello world again')


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


def fill_titles():
    titles = get_titles()
    i = 0
    for title in titles:
        initial_matrix.write(0, i, title)
        empty_matrix.write(0, i, title)
        final_matrix.write(0, i, title)
        i += 1
    return

# change name to "generate_results" when finished
def main():
    fill_titles()
    workbook.close()


main()