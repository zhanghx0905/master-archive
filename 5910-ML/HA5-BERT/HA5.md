# Homework Assignment 5

20932780 ZHANG Hexiao



The baseline model has the same architecture as that in Tutorial 5, which is `BERT+FC+RELU+DROPOUT+FC+SOFTMAX`. The parameters of the BERT model are fixed in the training, w.r.t

```python
bert = AutoModel.from_pretrained('bert-base-uncased')
# freeze all the parameters
for param in bert.parameters():
    param.requires_grad = False
```

Hyper parameters are listed below.

| Hyper parameter | Value | Explanation                       |
| --------------- | ----- | --------------------------------- |
| max_seq_len     | 256   | The length of all input sequences |
| lr              | 1e-3  | Learning rate for AdamW optimizer |
| drop_rate       | 0.5   | Dropout rate                      |
| batch_size      | 16    |                                   |
| epochs          | 5     | Number of training epochs         |

Experiments are conducted by varying a certain aspect of the baseline model. The parameters for the BERT model are fixed.

| Model           | Accuracy (%) |
| --------------- | ------------ |
| Baseline        | 79           |
| lr = 5e-3       | 76           |
| lr = 5e-4       | 80           |
| epochs = 1      | 78           |
| epochs = 3      | 79           |
| epochs = 10     | 80           |
| batch_size = 32 | 81           |
| batch_size = 64 | 79           |
| drop_rate = 0.7 | 79           |
| drop_rate = 0.3 | 79           |

Changing the hyperparameters has a very limited influence on the model performance, and the effect of increasing the training epochs is not significant. This should be because the network behind the BERT model is simple and easy to converge.

If the learning rate of fine-tuning is too large, the model can be hard to converge.  
