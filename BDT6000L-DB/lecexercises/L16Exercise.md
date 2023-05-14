# Lec16 Exercise

20932780 Zhang Hexiao

### 4

a)

Sort: We remove unwanted attributes after sorting. $bf_{sName}=[800/10]=80$, $B_{sName}=500$ pages. The IO cost is $500+2000=2500$.

Merge: We need $\lceil\log_{499}{500/100}\rceil=1$ pass. The IO cost is $500$.

Projection: $2500+500=3000$.

Result: $500\times (1-5\%)=475$

b)

Partitioning: For each partition, read $2000/40=50$ pages but write $\lceil 50\times bf_{Sailor}\times10/800 \rceil=13$ pages. The cost is $2000+13\times40=2520$ pages.

Duplicate elimination: To read each partition, the cost is $520$ pages.

Projection:$2520+520=3040$

Result: $475$

### 5

Assume the minimum buffer size (3 pages). $bf=10$

Base Strategy: block nested-loop join

Page IO cost: $5000\times 1000+1000=5001000$

a) Strategy: check the condition in the buffer (on-the-fly) after the join. 

Page IO cost: 0

b) Strategy: Search on the clustering index.

Page IO cost: The number of pages per department is $400/10=40$. The cost is $3+40=43$.

c) Strategy: indexed nested-loop join on `sid`

Page IO cost: There are 400 students in a department. For each student, we use the non-clustering index on `sid` to find all matched records in EnrollsIn. We further assume that it takes 1 more page IO to read the indirection page. We need to read in a total of  $(3 + 1 + 2.5)\times 400 = 2600$ pages. 

d) Strategy: do in the buffer (on-the-fly) during the join.

Page IO cost: 0



Query Page IO cost: 2643.