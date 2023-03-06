# utils.py: Utility file for implementing helpful utility functions used by the ML algorithms.
#
# Submitted by: Sakshi Sitoot -- ssitoot@iu.edu
#
# Based on skeleton code by CSCI-B 551 Fall 2022 Course Staff

import numpy as np

def getmatvectnorm(param1):
    matvectnorm = np.linalg.norm(param1,ord=None, axis=None, keepdims=False)
    return matvectnorm

def getAbsoluteValue(param1):
    result = np.absolute(param1,casting='same_kind', order='K', dtype=None)
    return result

def getNumpySum(param1):
    result = np.sum(param1,dtype=None, out=None)
    return result

def getLimitedValues(param1, param2 = -1e100, param3 = 1e100):
    result = np.clip(param1, param2, param3, out=None)
    return result

def getNumpyOnes(param1):
    result = np.ones(param1, dtype=None)
    return result

def getExponential(param1):
    result = np.exp(param1, where=True, casting='same_kind')
    return result

def getTanH(param1):
    result = np.tanh(param1, where=True, casting='same_kind')
    return result

def getNumpyMaximum(param1, param2):
    result = np.maximum(param1, param2, where=True, casting='same_kind')
    return result

def getNumpyGreater(param1, param2):
    result = np.greater(param1, param2, where=True, casting='same_kind').astype(int)
    return result

def getNumpyLogarithm(param1):
    result = np.log(param1, casting='same_kind', order='K')
    return result

def getNumpyZeroes(param1, param2):
    result = np.zeros((param1, param2), dtype=float, order='C')
    return result

def getNumpyAranged(param1):
    result = np.arange(param1)
    return result


def euclidean_distance(x1, x2):
    """
    Computes and returns the Euclidean distance between two vectors.

    Args:
        x1: A numpy array of shape (n_features,).
        x2: A numpy array of shape (n_features,).
    """
    ecld_d = x1 - x2
    result = getmatvectnorm(ecld_d)
    return result
    #raise NotImplementedError('This function must be implemented by the student.')

def manhattan_distance(x1, x2):
    """
    Computes and returns the Manhattan distance between two vectors.

    Args:
        x1: A numpy array of shape (n_features,).
        x2: A numpy array of shape (n_features,).
    """
    dis = x1 - x2
    result = getNumpySum(getAbsoluteValue(dis))
    return result
    #raise NotImplementedError('This function must be implemented by the student.')


def identity(x, derivative = False):
    """
    Computes and returns the identity activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """

    limited_values_in_arr = getLimitedValues(x)
    if derivative == False:
        return limited_values_in_arr
    else:
        result = getNumpyOnes(limited_values_in_arr.shape)
        return result
    #raise NotImplementedError('This function must be implemented by the student.')

#reference: https://www.v7labs.com/blog/neural-networks-activation-functions
def sigmoid(x, derivative = False):
    """
    Computes and returns the sigmoid (logistic) activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """

    # x = np.clip(x, -1e100, 1e100)
    limited_values_in_arr = getLimitedValues(x)
    calc_s = 1 + getExponential(-limited_values_in_arr)
    inverse = 1 / calc_s
    # sig = 1 / (1 + np.exp(-x))
    if derivative == False:
        return inverse
    else:
        return (1 - inverse) * inverse
    # raise NotImplementedError('This function must be implemented by the student.')

def tanh(x, derivative = False):
    """
    Computes and returns the hyperbolic tangent activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    limited_values_in_arr = getLimitedValues(x)
    values_tan_h = getTanH(limited_values_in_arr)
    if derivative == False:
        return values_tan_h
    else:
        return (3-2) - values_tan_h ** (5-3)
    # raise NotImplementedError('This function must be implemented by the student.')

def relu(x, derivative = False):
    """
    Computes and returns the rectified linear unit activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """

    limited_values_in_arr = getLimitedValues(x)
    valmax = getNumpyMaximum(limited_values_in_arr, 0)
    if derivative == False:
        return valmax
    else:
        result = getNumpyGreater(limited_values_in_arr, 0)
        return result
    # raise NotImplementedError('This function must be implemented by the student.')

def softmax(x, derivative = False):
    x = np.clip(x, -1e100, 1e100)
    if not derivative:
        c = np.max(x, axis = 1, keepdims = True)
        return np.exp(x - c - np.log(np.sum(np.exp(x - c), axis = 1, keepdims = True)))
    else:
        return softmax(x) * (1 - softmax(x))
    # raise NotImplementedError('This function must be implemented by the student.')

# Reference: https://deepnotes.io/softmax-crossentropy#cross-entropy-loss
def cross_entropy(y, p):
    """
    Computes and returns the cross-entropy loss, defined as the negative log-likelihood of a logistic model that returns
    p probabilities for its true class labels y.

    Args:
        y:
            A numpy array of shape (n_samples, n_outputs) representing the one-hot encoded target class values for the
            input data used when fitting the model.
        p:
            A numpy array of shape (n_samples, n_outputs) representing the predicted probabilities from the softmax
            output activation function.
    """
    values = p
    numpy_array = y
    limited_values_in_arr = getLimitedValues(values, 1e-5, 1 - 1e-5)
    values_with_log = numpy_array * getNumpyLogarithm(limited_values_in_arr)
    cross_entropy = -getNumpySum(values_with_log) / limited_values_in_arr.shape[0]
    return cross_entropy
    # raise NotImplementedError('This function must be implemented by the student.')


#reference: https://machinelearningmastery.com/how-to-one-hot-encode-sequence-data-in-python/
def one_hot_encoding(y):
    """
    Converts a vector y of categorical target class values into a one-hot numeric array using one-hot encoding: one-hot
    encoding creates new binary-valued columns, each of which indicate the presence of each possible value from the
    original data.

    Args:
        y: A numpy array of shape (n_samples,) representing the target class values for each sample in the input data.

    Returns:
        A numpy array of shape (n_samples, n_outputs) representing the one-hot encoded target class values for the input
        data. n_outputs is equal to the number of unique categorical class values in the numpy array y.
    """

    numpy_array = y
    numpy_zeros = getNumpyZeroes(numpy_array.shape[0],numpy_array.max()+1)
    numpy_zeros[getNumpyAranged(numpy_array.shape[0]),numpy_array] = 1
    return numpy_zeros
    # raise NotImplementedError('This function must be implemented by the student.')
