"""Student Name: Zhang Hexiao
Student ID: 20932780
Assignment #: 2
Student Email: 731931282@qq.com
Course Name: ML
"""

"""
         Programming Assignment 2
         
To be submitted via canvas, just as Programming Assignment 1

This program builds a two-layer neural network for the Iris dataset.
The first layer is a relu layer with 10 units, and the second one is 
a softmax layer. The network structure is specified in the "train" function.

The parameters are learned using SGD.  The forward propagation and backward 
propagation are carried out in the "compute_neural_net_loss" function.  The codes
for the propagations are deleted.  Your task is to fill in the missing codes.

"""

# In this exercise, we are going to work with a two-layer neural network
# first layer is a relu layer with 10 units, and second one is a softmax layer.
# randomly initialize parameters


import numpy as np
import os, sys
import math


# Data sets
IRIS_TRAINING = "iris_training.csv"
IRIS_TEST = "iris_test.csv"


def get_data():
    # Load datasets.
    train_data = np.genfromtxt(IRIS_TRAINING, skip_header=1, dtype=float, delimiter=",")
    test_data = np.genfromtxt(IRIS_TEST, skip_header=1, dtype=float, delimiter=",")
    train_x = train_data[:, :4]
    train_y = train_data[:, 4].astype(np.int64)
    test_x = test_data[:, :4]
    test_y = test_data[:, 4].astype(np.int64)

    return train_x, train_y, test_x, test_y


def compute_neural_net_loss(params, X, y, reg=0.0):
    """
    Neural network loss function.
    Inputs:
    - params: dictionary of parameters, including "W1", "b1", "W2", "b2"
    - X: N x D array of training data. Each row is a D-dimensional point.
    - y: 1-d array of shape (N, ) for the training labels.

    Returns:
    - loss: the softmax loss with regularization
    - grads: dictionary of gradients for the parameters in params
    """
    # Unpack variables from the params dictionary
    W1, b1 = params["W1"], params["b1"]  # D * 10, 10
    W2, b2 = params["W2"], params["b2"]  # 10 * K, K
    N, D = X.shape

    loss = 0.0
    grads = {}

    #############################################################################
    # TODO: Finish the forward pass, and compute the loss. This should include  #
    # both the data loss and L2 regularization for W1 and W2. Store the result  #
    # in the variable loss, which should be a scalar. Use the Softmax           #
    # classifier loss. So that your results match ours, multiply the            #
    # regularization loss by 0.5                                                #
    #############################################################################
    EPSILON = 1e-40

    class Relu:
        def forward(self, input):
            self.mask = input > 0
            return self.mask * input

        def backward(self, grad_output):
            return self.mask * grad_output


    class Linear:
        def __init__(self, W, b) -> None:
            self.W, self.b = W, b

        def forward(self, input):
            self.input = input
            return input.dot(self.W) + self.b

        def backward(self, grad_output):
            self.grad_b = np.sum(grad_output, axis=0)
            self.grad_W = np.dot(self.input.T, grad_output)
            return np.dot(grad_output, self.W.T)


    def onehot_encoding(label, max_num_class):
        return np.eye(max_num_class)[label]


    class SoftmaxCE:
        def forward(self, input, target):
            """target is one-hot encoding of y_true"""
            exp = np.exp(input - np.max(input))
            prob = exp / (np.sum(exp, axis=1, keepdims=True) + EPSILON)
            return np.mean(np.sum(-target * np.log(prob + EPSILON), axis=1))

        def backward(self, input, target):
            exp = np.exp(input - np.max(input))
            prob = exp / (np.sum(exp, axis=1, keepdims=True) + EPSILON)
            return (prob - target) / input.shape[0]


    model = [Linear(W1, b1), Relu(), Linear(W2, b2)]
    softmax =  SoftmaxCE()
    y_onehot = onehot_encoding(y, W2.shape[1])

    # forward
    result = X
    for layer in model:
        result = layer.forward(result)
    loss = softmax.forward(result, y_onehot)
    loss += 0.5 * reg * (np.sum(W1 **2) + np.sum(W2 ** 2))

    #############################################################################
    #                              END OF YOUR CODE                             #
    #############################################################################

    #############################################################################
    # TODO: Compute the backward pass, computing the derivatives of the weights #
    # and biases. Store the results in the grads dictionary. For example,       #
    # grads['W1'] should store the gradient on W1, and be a matrix of same size #
    #############################################################################

    grad = softmax.backward(result, y_onehot)
    for layer in reversed(model):
        grad = layer.backward(grad) 
    dW1 = model[0].grad_W + reg * W1
    dW2 = model[-1].grad_W + reg * W2
    db1 = model[0].grad_b
    db2 = model[-1].grad_b

    #############################################################################
    #                          END OF YOUR CODE                                 #
    #############################################################################
    grads["W1"] = dW1
    grads["W2"] = dW2
    grads["b1"] = db1
    grads["b2"] = db2

    return loss, grads


def predict(params, X):
    """
    Use the trained weights of this linear classifier to predict labels for
    data points.

    Inputs:
    - params: dictionary of parameters, including "W1", "b1", "W2", "b2"
    - X: N x D array of training data. Each row is a D-dimensional point.

    Returns:
    - y_pred: Predicted labels for the data in X. y_pred is a 1-dimensional
      array of length N, and each element is an integer giving the predicted
      class.
    """
    # Unpack variables from the params dictionary
    W1, b1 = params["W1"], params["b1"]
    W2, b2 = params["W2"], params["b2"]

    y_pred = np.zeros(X.shape[1])

    relu = lambda x: x * (x > 0)
    z1 = np.dot(X, W1) + b1
    u1 = relu(z1)
    z2 = np.dot(u1, W2) + b2
    y_pred = np.argmax(z2, axis=1)

    return y_pred


def acc(ylabel, y_pred):
    return np.mean(ylabel == y_pred)


def sgd_update(params, grads, learning_rate):
    """
    Perform sgd update for parameters in params.
    """
    for key in params:
        params[key] += -learning_rate * grads[key]


def validate_gradient():
    """
    Function to validate the implementation of gradient computation.
    Should be used together with gradient_check.py.
    This is a useful thing to do when you implement your own gradient
    calculation methods.
    It is not required for this assignment.
    """
    from gradient_check import eval_numerical_gradient, rel_error

    # randomly initialize W
    dim = 4
    num_classes = 4
    num_inputs = 5
    params = {}
    std = 0.001
    params["W1"] = std * np.random.randn(dim, 10)
    params["b1"] = np.zeros(10)
    params["W2"] = std * np.random.randn(10, num_classes)
    params["b2"] = np.zeros(num_classes)

    X = np.random.randn(num_inputs, dim)
    y = np.array([0, 1, 2, 2, 1])

    loss, grads = compute_neural_net_loss(params, X, y, reg=0.1)
    # these should all be less than 1e-8 or so
    for param_name in params:
        f = lambda W: compute_neural_net_loss(params, X, y, reg=0.1)[0]
        param_grad_num = eval_numerical_gradient(f, params[param_name], verbose=False)
        print(
            "%s max relative error: %e"
            % (param_name, rel_error(param_grad_num, grads[param_name]))
        )


def train(X, y, Xtest, ytest, learning_rate=1e-3, reg=1e-5, epochs=100, batch_size=20):
    num_train, dim = X.shape
    num_classes = (
        np.max(y) + 1
    )  # assume y takes values 0...K-1 where K is number of classes
    num_iters_per_epoch = int(math.floor(1.0 * num_train / batch_size))

    # In this exercise, we are going to work with a two-layer neural network
    # first layer is a relu layer with 10 units, and second one is a softmax layer.
    # randomly initialize parameters
    params = {}
    std = 0.001
    params["W1"] = std * np.random.randn(dim, 10)
    params["b1"] = np.zeros(10)
    params["W2"] = std * np.random.randn(10, num_classes)
    params["b2"] = np.zeros(num_classes)

    for epoch in range(max_epochs):
        perm_idx = np.random.permutation(num_train)
        # perform mini-batch SGD update
        for it in range(num_iters_per_epoch):
            idx = perm_idx[it * batch_size : (it + 1) * batch_size]
            batch_x = X[idx]
            batch_y = y[idx]

            # evaluate loss and gradient
            loss, grads = compute_neural_net_loss(params, batch_x, batch_y, reg)

            # update parameters
            sgd_update(params, grads, learning_rate)

        # evaluate and print every 10 steps
        if epoch % 10 == 0:
            train_acc = acc(y, predict(params, X))
            test_acc = acc(ytest, predict(params, Xtest))
            print(
                "Epoch %4d: loss = %.2f, train_acc = %.4f, test_acc = %.4f"
                % (epoch, loss, train_acc, test_acc)
            )

    return params


# validate_gradient()  # don't worry about this.
# sys.exit()

max_epochs = 200
batch_size = 20
learning_rate = 0.1
reg = 0.001

# get training and testing data
train_x, train_y, test_x, test_y = get_data()
params = train(
    train_x, train_y, test_x, test_y, learning_rate, reg, max_epochs, batch_size
)

# Classify two new flower samples.
def new_samples():
    return np.array([[6.4, 3.2, 4.5, 1.5], [5.8, 3.1, 5.0, 1.7]], dtype=np.float32)


new_x = new_samples()
predictions = predict(params, new_x)

print("New Samples, Class Predictions:    {}\n".format(predictions))
validate_gradient()