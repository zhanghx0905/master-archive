# Lec14 Exercise

20932780 ZhangHexiao

### 4

a).

i. We use the index to scan the leaf pages of the index sequentially finding pointers to records, until the first entry where `sailorId = 50000`.

Since search key values are uniformly distributed in $[1, 100000]$, there are roughly $1/2$ of them lower than 50000.

IO for Index Pages: $50/2=25$

IO for reading records: $80\times 500/2=20000$

The overall IO cost is $20025$.

Linear search will be much faster, in which case the overall IO cost is $500$.

ii. The IO cost is $5 +1=6$.

b).

i. We need to sequentially scan the index to find all possible pointers.

IO for Index Pages: 50

IO for reading records: $80\times 500/2=20000$

The overall IO cost is $20050$.

Linear search will be much faster, in which case the overall IO cost is $500$.

ii. The IO cost is $1 +1=2$

### 5

The number of passes is $1+\lceil \log_{99}{600000/100}\rceil=3$

The IO cost is $2\times 600000\times3=3,600,000$

#### 6

$$
1+\lceil log_{M-1}{B/M}\rceil =2\\
0<log_{M-1}{B/M}\le1\\
1<B/M\le M-1\\
\lceil\frac{1}{2}(\sqrt{4B+1}+1)\rceil \le M <B
$$

