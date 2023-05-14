# Lec17 Exercise

20932780 Zhang Hexiao

### 4

##### C1

Strategy: Select by clustering index on rDate.

Page IO cost: The result will contain $100000/1000=100$ tuples, and occupy $100/10=10$ pages.

the cost is $2+10=12$ pages.

Page IO cost to write: 10.

Minimum cost for C1: 22

##### C2

Strategy: block nested-loop join with Temp1 as outer relation.

Page IO cost: $10 + 100\times\lceil10/98\rceil=110$.

Page IO cost to write: The result will contain $100\times10\%=10$ tuples, which takes up  $10/5=2$ pages. The IO cost is 2.

Minimum cost for C1: 112

##### C3

Strategy: indexed nested-loop join

Page IO cost: For each tuple in Temp2, select the sailor with the same sailorId takes 2 Page IOs. The overall cost is $10\times2+2=22$.

Minimum cost for C3: 22



Query processing IO cost: $22+112+22=156$.

### 5

#### a)

SC(salary >= 100000, Employee) = 20000 * (110000 - 100000) / (110000 - 10000) = 2000

SC(budget > 20000, Project) = 2000 * (500 + 300) / 2000 = 800

`deptId` is the key of `Department`.

SC(salary >= 100000, Employee $\Join$ Department) = 2000

SC(salary >= 100000, Employee $\Join$ Department $\Join$ DeptProject) = 2000 * 4000 = 8000000

`projectId` is the key of `Project`.

SC(budget > 20000 $\and$ salary >= 100000,  Employee $\Join$ Department $\Join$ DeptProject $\Join$ Project) = 8,000,000

For the output, the record size is 12 bytes. $bf=[4000/12]=333$. $\lceil 8000000/333 \rceil=24025$ pages are needed.

#### b)

##### Step1

Strategy: use the clustering index on sarlay with pipelining.

Page IO cost: 

To search for the first page that satisfies salary >= 100000, read 3 pages. Then read $2000\times 50/4000=25$ pages of Employee records. 

We only need `empId` and `deptId`. The result size is $2000\times 8 / 4000=4$ pages.

minimum page IO cost: 28

result size: 4

##### Step2

Strategy: block nested-loop join with Department as the outer relation.

Page IO cost: we don't need to read Employee because they have been given by Step1. We just need to read 1 department page.

minimum page IO cost: 1

result size: 4

##### Step3

Strategy: block nested-loop join with DeptProject as the outer relation.

Page IO cost: we don't need to read Result B because they have been given by Step2. We only need to read 8 DeptProject pages.

minimum page IO cost: 8

result size: 24025

##### Step4

Stretegy: linear scan with pipelining.

Page IO cost: 500 pages.

We only need `peojectId` for results. The result size is $\lceil 800\times4/4000 \rceil=1$ page.

minimum page IO cost: 500

result size: 1

##### Step5

Strategy: block nested-loop join with Result D as the outer relation.

Page IO cost: Result C and Result D are given by Step3 and Step4. No page io needed here.

minimum page IO cost: 0

result size: 24025



Query processing IO cost: 28 + 1 + 8 + 500 =  537

result size: 24025