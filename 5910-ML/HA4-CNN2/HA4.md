# Homework Assignment 4

20932780 Zhang Hexiao



All models are loaded with default arguments and correctly predict all test samples. The output probability for the true label is as below.

|                 | True Label  | Resnet50 | VGG16 | InceptionV3 | Densenet121 | EfficientNetB2 | MobileNetV2 |
| --------------- | ----------- | -------- | ----- | ----------- | ----------- | -------------- | ----------- |
| ![1](./1.png)   | rapeseed    | 1.00     | 1.00  | 1.00        | 1.00        | 0.90           | 1.00        |
| ![2](./2.png)   | peacock     | 1.00     | 1.00  | 0.99        | 1.00        | 0.85           | 0.98        |
| ![3](./3.png)   | yurt        | 1.00     | 1.00  | 1.00        | 1.00        | 0.75           | 0.95        |
| ![4](./4.png)   | hourglass   | 1.00     | 1.00  | 1.00        | 1.00        | 0.94           | 0.95        |
| ![5](./5.png)   | water_tower | 1.00     | 1.00  | 0.99        | 1.00        | 0.86           | 0.96        |
| ![6](./6.png)   | zebra       | 1.00     | 1.00  | 0.99        | 1.00        | 0.89           | 0.97        |
| ![7](./7.png)   | school_bus  | 1.00     | 1.00  | 1.00        | 1.00        | 0.90           | 0.99        |
| ![8](./8.png)   | pillow      | 1.00     | 1.00  | 1.00        | 1.00        | 0.95           | 1.00        |
| ![9](./9.png)   | fireboat    | 1.00     | 1.00  | 0.95        | 1.00        | 0.85           | 0.85        |
| ![10](./10.png) | carousel    | 1.00     | 1.00  | 0.97        | 1.00        | 0.88           | 0.99        |

The "fireboat" is a harder sample to classify, which is true even for human.  

The slightly lower prediction probability of correct classification for EfficientNetB2 and MobileNetV2 is reasonable since they have fewer parameters. 
