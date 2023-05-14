## Install Dependencies

```
pip install -r requirements.txt
```

To visualize the results of the run, you should log in to `wandb` in the current environment.

```
wandb login
```

Please extract the data to the dataset folder.

```python
TASK1_TRAINING_DATA_PATH = "./dataset/part1_bballs_training.npz"
TASK1_TEST_DATA_PATH = "./dataset/part1_bballs_test.npz"
TASK2_DATA_PATH = "./dataset/part2_bballs_sequence.npz"
```

## Task1 & Task2 & Task3

```
python part1.py ./config/task1.json
```

The trained model will be in the `wandb/run-*` directory.

## Task4

```
python part1.py ./config/task4.json
```

## Task 6

```
python part2_train.py ./config/task6.json
```

The trained model and pictures will be in the `wandb/run-*` directory.

## Task 7

```bash
python part2_train.py ./config/task7.json
```

