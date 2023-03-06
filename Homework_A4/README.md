# a4
Skeleton code for Assignment 4

# Assignment 4 - EAI

# Part 1:
K-Nearest Neighbors Classification:

Description of various important methods used:

predict():
In this method, we first loop over the list of data points to calculate the distance between the input point and all of the data points, sorting them in descending order to obtain the top K data points and their classes.

1. In the predict() method, I first iterate for every data point, and calculate the distance of the given input with all data points, and sort the results by distance in descending order. Next, I get the first k data points along with their class. In a "distance" weighing strategy, each data point is weighted by the reciprocal of its distance from the input, whereas in a "uniform" weighing strategy, all data points are given the same weight. To look for points whose distance might be zero, we are using the outlier_removal_param parameter. Lastly, the class with the greatest majority is finally predicted.


# Part 2:
Multilayer Perceptron Classification:

Description of various important methods used:

_initialize():
The train features are initialized using this method, and one hot encoder is utilized to encode the labels vector. Additionally, weights generated at random from a uniform distribution between 0 and 1 are used to initialize the model.

fit():
This function first calls the initialize() method first. The for loop then repeats, with each iteration involving the initial forward pass of the train data. Next, the for loop runs for a designated number of iterations, wherein each iteration first executes a forward pass of the train data through the network. Following the forward pass, the loss is determined using the loss function, which is then used to get the error gradient. The weights of the hidden and output layers are then updated using this error gradient and the back propagation algorithm. The training loss is stored for every 20th iteration.

predict():
This function just performs a forward pass with the input data using the trained model, returning a list of predictions for the input data.

Challenges faced:
Backpropagation implementation was difficult because there were numerous error gradients that needed to be calculated with complicated formulas.
