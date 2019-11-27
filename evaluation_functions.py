import numpy as np


def mae(prediction_errors):
    '''
    :return: Average of the prediction errors for all the users and rated items
    '''
    return np.mean(prediction_errors) or 0


def prediction_error(rating, original_matrix):
    '''
    :return: abs(prediction - real_rating)
    TODO: get rating in original matrix, predicted rating, and get their error
    '''
    return abs(rating.predicted_rating - original_matrix[rating.user_id][rating.movie_id])
