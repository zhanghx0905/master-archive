# Assignment 2

20932780 Zhang Hexiao

### Task 1

My R-tree implementation is modified from [rtreelib: Pluggable R-tree implementation in pure Python. (github.com)](https://github.com/lukas-shawford/rtreelib).  This repository implements the insertion algorithm of R-tree, to which I added functionalities include height calculation, number of nodes calculation and window query.

#### R-tree Algorithm

The algorithm is derived from its original paper: [R-trees: a dynamic index structure for spatial searching](https://dl.acm.org/doi/10.1145/971697.602266). Since our dataset is static, we do not have to consider update and delete operations and only need to implement the insertion algorithm.

When inserting a new item into an R-tree, the algorithm 

1. first traverses the tree to **find the most appropriate leaf node** based on the item's MBR. 
2. If the node has enough space, the item is added to it. Otherwise, the node is **split into two and the item is inserted into the appropriate new node**. 
3. The split may propagate up the tree, causing parent nodes to split as well. The root node may be split, resulting in a new root. 

I will explain more details below.

For the 1st step, we traverse the tree from the root node to the leaf node. In every decision, we select the child of current node whose MBR **needs least enlargement** to include the MBR of the new data.

For the 2nd step, I use **the quadratic-cost algorithm** to implement node splitting. To split a full leaf node, the following steps are taken:

1. Choose two items from the full node that will act as the seeds for the two new nodes. The area of the union of their MBRs minus both MBRs should be the maximum.
2. Calculate the increase in area or volume of the bounding boxes of the two new nodes that would result from adding each remaining item to each of the two new nodes.
3. Choose the item that results in the maximum difference in the increase in area or volume between the two new nodes.
4. Add this item to the new node with the smaller bounding box increase.
5. Repeat steps 2-4 until all remaining items have been added to one of the two new nodes.

The 3rd step of the insertion algorithm is basically the same as the B-tree. So I'm not going to discuss its details.

#### Experiments

For different parameters, the tree height and the number of nodes are as below. As fanout increases, the number of nodes and the height of the tree decrease accordingly.

| d    | n    |             | First Half Dataset |                    |             | Entire Dataset |                    |
| ---- | ---- | ----------- | ------------------ | ------------------ | ----------- | -------------- | ------------------ |
|      |      | Tree height | Leaf nodes No.     | Internal nodes No. | Tree height | leaf nodes No. | internal nodes No. |
| 8    | 64   | 6           | 930                | 277                | 7           | 1871           | 591                |
| 8    | 256  | 5           | 277                | 61                 | 5           | 466            | 131                |
| 32   | 64   | 4           | 956                | 58                 | 4           | 1891           | 206                |
| 32   | 256  | 3           | 229                | 14                 | 3           | 446            | 32                 |

### Task 2

The brute force algorithm traverses the entire dataset to determine whether each polygon is covered by the query window.

The window query algorithm in R-trees works by recursively traversing from the root node to the leaf nodes while checking if the MBR of the node intersects with the query window. If so, the algorithm will check all the children of this node. Otherwise there is no need to check children whose polygons must not be in the query window.

#### Experiments

The results of the brute-force algorithm and the R-tree are the same, verifying the correctness of the implementation. For each randomly generated query window, we run it 20 times. In the table, the runtime for each measurement is in the format `max/min/avg`.

| Testcase | Retrieved Objects | BF Traversed Objects | BF Time          | R-Tree Traversed Objects | R-tree Time      |
| -------- | ----------------- | -------------------- | ---------------- | ------------------------ | ---------------- |
| 0        | 0                 | 76718                | 0.51/0.49/0.50 s | 2555                     | 0.03/0.03/0.03 s |
| 1        | 3                 | 76718                | 0.51/0.49/0.50 s | 8350                     | 0.08/0.08/0.08 s |
| 2        | 0                 | 76718                | 0.53/0.50/0.51 s | 2214                     | 0.02/0.02/0.02 s |
| 3        | 612               | 76718                | 0.49/0.48/0.49 s | 16945                    | 0.14/0.14/0.14 s |
| 4        | 24                | 76718                | 0.50/0.49/0.49 s | 1917                     | 0.03/0.02/0.02 s |
| 5        | 4                 | 76718                | 0.52/0.50/0.50 s | 7714                     | 0.07/0.07/0.07 s |
| 6        | 1                 | 76718                | 0.52/0.48/0.49 s | 304                      | 0.00/0.00/0.00 s |
| 7        | 0                 | 76718                | 0.53/0.49/0.50 s | 894                      | 0.01/0.01/0.01 s |
| 8        | 763               | 76718                | 0.52/0.49/0.50 s | 9835                     | 0.11/0.09/0.09 s |
| 9        | 259               | 76718                | 0.52/0.48/0.49 s | 8060                     | 0.09/0.08/0.08 s |
| 10       | 0                 | 76718                | 0.50/0.48/0.49 s | 183                      | 0.00/0.00/0.00 s |
| 11       | 0                 | 76718                | 0.50/0.49/0.49 s | 600                      | 0.01/0.01/0.01 s |
| 12       | 0                 | 76718                | 0.51/0.49/0.50 s | 13430                    | 0.13/0.12/0.12 s |
| 13       | 0                 | 76718                | 0.50/0.48/0.49 s | 5692                     | 0.06/0.06/0.06 s |
| 14       | 20                | 76718                | 0.50/0.49/0.49 s | 2014                     | 0.02/0.02/0.02 s |
| 15       | 0                 | 76718                | 0.51/0.49/0.50 s | 8808                     | 0.10/0.08/0.09 s |
| 16       | 1                 | 76718                | 0.49/0.48/0.49 s | 6154                     | 0.06/0.06/0.06 s |
| 17       | 612               | 76718                | 0.49/0.48/0.49 s | 10048                    | 0.09/0.09/0.09 s |
| 18       | 7                 | 76718                | 0.51/0.49/0.50 s | 14100                    | 0.15/0.13/0.13 s |
| 19       | 62                | 76718                | 0.50/0.48/0.49 s | 10972                    | 0.12/0.10/0.10 s |
| 20       | 599               | 76718                | 0.57/0.49/0.51 s | 13502                    | 0.14/0.11/0.12 s |
| 21       | 1                 | 76718                | 0.54/0.49/0.51 s | 7373                     | 0.08/0.07/0.08 s |
| 22       | 0                 | 76718                | 0.54/0.48/0.50 s | 0                        | 0.00/0.00/0.00 s |
| 23       | 0                 | 76718                | 0.51/0.48/0.49 s | 1098                     | 0.02/0.02/0.02 s |
| 24       | 0                 | 76718                | 0.53/0.49/0.51 s | 1136                     | 0.03/0.01/0.02 s |
| 25       | 0                 | 76718                | 0.54/0.49/0.50 s | 626                      | 0.00/0.00/0.00 s |
| 26       | 0                 | 76718                | 0.54/0.49/0.50 s | 18049                    | 0.17/0.16/0.16 s |
| 27       | 0                 | 76718                | 0.51/0.49/0.50 s | 1024                     | 0.01/0.01/0.01 s |
| 28       | 0                 | 76718                | 0.53/0.49/0.50 s | 18162                    | 0.18/0.16/0.16 s |
| 29       | 0                 | 76718                | 0.50/0.48/0.49 s | 10403                    | 0.10/0.09/0.09 s |
