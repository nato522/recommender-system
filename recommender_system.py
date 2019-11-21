def read_matrix():
    # Creates a list containing 5 lists, each of 8 items, all set to 0
    columns, lines = 20, 50
    movie_matrix = [[0 for x in range(columns)] for y in range(lines)]
    filepath = 'matrix.txt'

    fp = open(filepath)
    i = 0
    for index, line in enumerate(fp):
        if index >= 20:
            # we will have an array of ratings for each line
            line_vector = []
            line_vector = line.split()  # split by space
            # print(line_vector)
            j = 0
            for rating in line_vector:
                movie_matrix[i][j] = rating
                j += 1
            i += 1
    fp.close()

    return movie_matrix

def main():
    movie_matrix = read_matrix()
    i_aux = 0
    j_aux = 0
    for i_aux in range(50):
        for j_aux in range(20):
            print(movie_matrix[i_aux][j_aux], end=' ')
        print()

main()
