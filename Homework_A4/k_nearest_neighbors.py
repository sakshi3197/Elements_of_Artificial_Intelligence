# k_nearest_neighbors.py: Machine learning implementation of a K-Nearest Neighbors classifier from scratch.
#
# Submitted by: Sakshi Sitoot -- [ssitoot@iu.edu]
#
# Based on skeleton code by CSCI-B 551 Fall 2022 Course Staff

import numpy as np
from utils import euclidean_distance, manhattan_distance


class KNearestNeighbors:
    """
    A class representing the machine learning implementation of a K-Nearest Neighbors classifier from scratch.

    Attributes:
        n_neighbors
            An integer representing the number of neighbors a sample is compared with when predicting target class
            values.

        weights
            A string representing the weight function used when predicting target class values. The possible options are
            {'uniform', 'distance'}.

        _X
            A numpy array of shape (n_samples, n_features) representing the input data used when fitting the model and
            predicting target class values.

        _y
            A numpy array of shape (n_samples,) representing the true class values for each sample in the input data
            used when fitting the model and predicting target class values.

        _distance
            An attribute representing which distance metric is used to calculate distances between samples. This is set
            when creating the object to either the euclidean_distance or manhattan_distance functions defined in
            utils.py based on what argument is passed into the metric parameter of the class.

    Methods:
        fit(X, y)
            Fits the model to the provided data matrix X and targets y.

        predict(X)
            Predicts class target values for the given test data matrix X using the fitted classifier model.
    """

    def __init__(self, n_neighbors = 5, weights = 'uniform', metric = 'l2'):
        # Check if the provided arguments are valid
        if weights not in ['uniform', 'distance'] or metric not in ['l1', 'l2'] or not isinstance(n_neighbors, int):
            raise ValueError('The provided class parameter arguments are not recognized.')

        # Define and setup the attributes for the KNearestNeighbors model object
        self.n_neighbors = n_neighbors
        self.weights = weights
        self._X = None
        self._y = None
        self._distance = euclidean_distance if metric == 'l2' else manhattan_distance

    def fit(self, X, y):
        fitting_input_data = X
        true_class_values = y
        """
        Fits the model to the provided data matrix X and targets y.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
        """
        self._X = fitting_input_data
        self._y = true_class_values

    # Reference: https://alexkaiser.dev/2020-06-25-k-Nearest-Neighbors-in-Python-from-Scratch/
    def predict(self, X):
        """
        Predicts class target values for the given test data matrix X using the fitted classifier model.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the test data.

        Returns:
            A numpy array of shape (n_samples,) representing the predicted target class values for the given test data.
        """



        array_of_test_data = X
        outlier_removal_param = 1/10
        list_of_predictions = []
        total_number_comp_points = self.n_neighbors
        fitting_input_data = self._X
        length_fitting_data = len(fitting_input_data)
        true_class_values = self._y
        length_true_class_values = len(true_class_values)
        zeroth = 0
        first = 1
        #euc_or_manh = self._distance
        wt = self.weights

        for single_unit_test_data in array_of_test_data:
            total_target_number = []
            for rv in range(zeroth, length_true_class_values):
                total_target_number.append(zeroth)

            distances_of_ngb_points = []

            for fitting_data_unit in range(zeroth,length_fitting_data):
                # calculating distance from other points
                distance_from_current_point = self._distance(fitting_input_data[fitting_data_unit], single_unit_test_data)
                distances_of_ngb_points.append((distance_from_current_point, true_class_values[fitting_data_unit]))

            distances_of_ngb_points.sort(key=lambda m:m[zeroth])
            # getting k nearest points
            t_closest_points = distances_of_ngb_points[:total_number_comp_points]

            if wt == 'uniform':
                for individual_point in t_closest_points:
                    total_target_number[individual_point[first]] = total_target_number[individual_point[first]] + first
            else:
                for individual_point in t_closest_points:
                    total_target_number[individual_point[first]] = first/(individual_point[zeroth]+outlier_removal_param)  + total_target_number[individual_point[first]]

            highest = max(total_target_number)
            list_of_predictions.append(total_target_number.index(highest))

        final_returnable_np_ar = np.array(list_of_predictions,dtype=None, copy=True, order='K')
        return final_returnable_np_ar
