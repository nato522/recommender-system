import numpy as np


def get_all_rated_movies(user_id, list_predicted_info):
    if user_id > 50 or user_id < 0:
        print("Wrong user id!")

    map_all_rated_movies = {}  # hash map with the key = movie_id and value = predicted_rating

    for info in list_predicted_info:
        if user_id == info.user_id:
            map_all_rated_movies[info.movie_id] = info.predicted_rating

    return map_all_rated_movies


def get_average(arr):
    arr_total = sum(arr)
    arr_length = np.count_nonzero(arr)
    return arr_total / arr_length


def round_rating(rating):
    if rating >= 5:
        return 5
    return round(rating * 2) / 2
