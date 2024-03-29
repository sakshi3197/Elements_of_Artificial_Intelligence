# multilayer_perceptron.py: Machine learning implementation of a Multilayer Perceptron classifier from scratch.
#
# Submitted by: Sakshi Sitoot -- ssitoot@iu.edu
#
# Based on skeleton code by CSCI-B 551 Fall 2022 Course Staff

import numpy as np
from utils import identity, sigmoid, tanh, relu, softmax, cross_entropy, one_hot_encoding


class MultilayerPerceptron:
	"""
    A class representing the machine learning implementation of a Multilayer Perceptron classifier from scratch.

    Attributes:
        n_hidden
            An integer representing the number of neurons in the one hidden layer of the neural network.

        hidden_activation
            A string representing the activation function of the hidden layer. The possible options are
            {'identity', 'sigmoid', 'tanh', 'relu'}.

        n_iterations
            An integer representing the number of gradient descent iterations performed by the fit(X, y) method.

        learning_rate
            A float representing the learning rate used when updating neural network weights during gradient descent.

        _output_activation
            An attribute representing the activation function of the output layer. This is set to the softmax function
            defined in utils.py.

        _loss_function
            An attribute representing the loss function used to compute the loss for each iteration. This is set to the
            cross_entropy function defined in utils.py.

        _loss_history
            A Python list of floats representing the history of the loss function for every 20 iterations that the
            algorithm runs for. The first index of the list is the loss function computed at iteration 0, the second
            index is the loss function computed at iteration 20, and so on and so forth. Once all the iterations are
            complete, the _loss_history list should have length n_iterations / 20.

        _X
            A numpy array of shape (n_samples, n_features) representing the input data used when fitting the model. This
            is set in the _initialize(X, y) method.

        _y
            A numpy array of shape (n_samples, n_outputs) representing the one-hot encoded target class values for the
            input data used when fitting the model.

        _h_weights
            A numpy array of shape (n_features, n_hidden) representing the weights applied between the input layer
            features and the hidden layer neurons.

        _h_bias
            A numpy array of shape (1, n_hidden) representing the weights applied between the input layer bias term
            and the hidden layer neurons.

        _o_weights
            A numpy array of shape (n_hidden, n_outputs) representing the weights applied between the hidden layer
            neurons and the output layer neurons.

        _o_bias
            A numpy array of shape (1, n_outputs) representing the weights applied between the hidden layer bias term
            neuron and the output layer neurons.

    Methods:
        _initialize(X, y)
            Function called at the beginning of fit(X, y) that performs one-hot encoding for the target class values and
            initializes the neural network weights (_h_weights, _h_bias, _o_weights, and _o_bias).

        fit(X, y)
            Fits the model to the provided data matrix X and targets y.

        predict(X)
            Predicts class target values for the given test data matrix X using the fitted classifier model.
	"""

	def __init__(self, n_hidden = 16, hidden_activation = 'sigmoid', n_iterations = 1000, learning_rate = 0.01):
		# Create a dictionary linking the hidden_activation strings to the functions defined in utils.py
		activation_functions = {'identity': identity, 'sigmoid': sigmoid, 'tanh': tanh, 'relu': relu}

		# Check if the provided arguments are valid
		if not isinstance(n_hidden, int) \
				or hidden_activation not in activation_functions \
				or not isinstance(n_iterations, int) \
				or not isinstance(learning_rate, float):
			raise ValueError('The provided class parameter arguments are not recognized.')

		# Define and setup the attributes for the MultilayerPerceptron model object
		self.n_hidden = n_hidden
		self.hidden_activation = activation_functions[hidden_activation]
		self.n_iterations = n_iterations
		self.learning_rate = learning_rate
		self._output_activation = softmax
		self._loss_function = cross_entropy
		self._loss_history = []
		self._X = None
		self._y = None
		self._h_weights = None
		self._h_bias = None
		self._o_weights = None
		self._o_bias = None

	def _initialize(self, X, y):
		"""
        Function called at the beginning of fit(X, y) that performs one hot encoding for the target class values and
        initializes the neural network weights (_h_weights, _h_bias, _o_weights, and _o_bias).

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
		"""

		self._X = X
		self._y = one_hot_encoding(y)

		np.random.seed(42)

		hidden_weights = self.n_hidden

		def getNumpyRandom(param1, param2):
			return np.random.rand(param1, param2)


		# initializing hidden weights and hidden bias layer
		self._h_weights = getNumpyRandom(self._X.shape[1],hidden_weights)
		self._h_bias = np.zeros((1, hidden_weights))

		# initializing output layer weights
		self._o_weights = getNumpyRandom(hidden_weights, self._y.shape[1])
		self._o_bias = np.zeros((1, self._y.shape[1]))

	def fit(self, X, y):
		"""
        Fits the model to the provided data matrix X and targets y and stores the cross-entropy loss every 20
        iterations.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
		"""

		self._initialize(X, y)

		# initializing the variables to be used
		array_samples_features = X
		array_samples = y
		total_iterations = self._h_weights
		hidd_neu_w = self._o_weights
		bias = self._o_bias
		global_array_samples_features = self._X
		global_array_samples = self._y

		for individual_rep in range(self.n_iterations):
			perceptron_hidden_weighted_output = np.dot(global_array_samples_features,total_iterations)
			perceptron_hidden_actvn = self.hidden_activation(perceptron_hidden_weighted_output)

			perceptron_output_weighted_input = np.dot(perceptron_hidden_actvn,hidd_neu_w) + bias
			perceptron_output_actvn = self._output_activation(perceptron_output_weighted_input)

			#calculating the cross entropy loss
			crs_ent_ls = self._loss_function(global_array_samples,perceptron_output_actvn)
			if individual_rep % 20 == 0:
				self._loss_history.append(crs_ent_ls)

			ls_actn_arr_sample_features = perceptron_output_actvn - global_array_samples
			dert_hd_atvn = self.hidden_activation(perceptron_hidden_weighted_output,derivative=True)

			dt_crs_ent_ls_op_wt = np.dot(perceptron_hidden_actvn.T,ls_actn_arr_sample_features)
			dt_crs_ent_ls_hd_wt = np.dot(global_array_samples_features.T,np.multiply((np.dot(hidd_neu_w,ls_actn_arr_sample_features.T)).T,dert_hd_atvn))

			ow = self.learning_rate * dt_crs_ent_ls_op_wt
			hw = self.learning_rate * dt_crs_ent_ls_hd_wt
			self._o_weights = hidd_neu_w - ow
			self._h_weights = total_iterations - hw

		#raise NotImplementedError('This function must be implemented by the student.')

# Reference: https://ml-cheatsheet.readthedocs.io/en/latest/forwardpropagation.html

	def predict(self, X):
		"""
        Predicts class target values for the given test data matrix X using the fitted classifier model.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the test data.

        Returns:
            A numpy array of shape (n_samples,) representing the predicted target class values for the given test data.
		"""

		array_samples_features = X
		list_of_predictions_perceptron=[]
		for indv_arr_feature in range(array_samples_features.shape[0]):
			# choosing the class with the highest prob

			arr_smp_ftr_expanded=np.expand_dims(array_samples_features[indv_arr_feature],axis=0)
			perceptron_hidden_weighted_output = np.dot(arr_smp_ftr_expanded,self._h_weights)
			perceptron_hidden_actvn = self.hidden_activation(perceptron_hidden_weighted_output)
			perceptron_output_weighted_input = np.dot(perceptron_hidden_actvn,self._o_weights)
			perceptron_output_actvn = self._output_activation(perceptron_output_weighted_input)
			list_of_predictions_perceptron.append(np.argmax(perceptron_output_actvn))

		result_numpy_arr = np.array(list_of_predictions_perceptron)
		return result_numpy_arr
