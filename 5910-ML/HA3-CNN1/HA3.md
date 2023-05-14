# Homework Assignment 3

20932780 Zhang Hexiao



The baseline model and hyper parameters are the same as in Tutorial 3. I take 20% of samples from the training dataset to construct the validation dataset. The training process is stopped when the validation error has not decreased for 10 epochs. The model that gets the lowest validation error will be tested.

| Layer                   | Parameter                                     | Input           |
| ----------------------- | --------------------------------------------- | --------------- |
| Conv2d                  | in_channels=3, out_channels=6, kernel_size=5  | (-, 32, 32, 3)  |
| MaxPool2d + Relu        | kernel_size=2, stride=2                       | (-, 28, 28, 6)  |
| Conv2d                  | in_channels=6, out_channels=16, kernel_size=5 | (-, 14, 14, 6)  |
| MaxPool2d + Relu        | kernel_size=2, stride=2                       | (-, 10, 10, 16) |
| Flatten + Linear + Relu | out_features=120                              | (-, 400)        |
| Linear + Relu           | out_features=84                               | (-, 120)        |
| Linear                  | out_features=10                               | (-, 84)         |

For faster training, the optimizer is the SGD with `momentum=0.9` and `learning rate=0.01` and The batch size is set as 128.

Experiments are conducted by varying a certain aspect of the baseline model. 

1. Remove the second convolution layer.
2. Remove the second fully connected layer.
3. Change the number of filters of convolution layers to 32 and 64, respectively.
4. Change the number of filters of convolution layers to 64 and 128, respectively.
5. Set `lr=0.005`.
6. Set `lr=0.001`
7. Using Adam.
8. Using RMSprop.
9. Using SDG (`lr=0.01`) without momentum.
10. Add a batch normalization layer to each convolution layer.

| Model                            | Test Acc (%) |
| -------------------------------- | ------------ |
| Baseline                         | 64.65        |
| Remove 2nd Conv layer            | 59.00        |
| Remove 2nd FC layer              | 62.11        |
| Filters (32, 64)                 | 70.92        |
| Filters (64, 128)                | 70.89        |
| `lr=0.005`                       | 63.70        |
| `lr=0.001`                       | 63.38        |
| Adam (`lr=0.01`)                 | 63.54        |
| RMSprop (`lr=0.001`)             | 61.20        |
| SDG (`lr=0.01`) without momentum | 63.42        |
| Batch normalization              | 65.62        |

The baseline model is too simple to fit the dataset. More complex models have more expressive power and therefore achieve better results, while simpler models can worsen the underfitting problem. Convolution layers have a greater impact on performance than fully connected layers.

The learning rate is closely related to the convergence of the model, but the optimal choice also depends on other things such as the batch size and the optimizer. Typically, the Adam optimizer is the most stable one. But with proper parameters, SGD with momentum can also achieve equivalent results. RMSprop can only achieve roughly 50% test accuracy with `lr=0.01`.

Batch normalization can accelerate the training process and help the model achieve lower test performance.