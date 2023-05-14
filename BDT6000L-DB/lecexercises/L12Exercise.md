# Lec12 Exercise

20932780 Zhang Hexiao

### 4

a. $bf_{Employee}=1000/20=50$

b. $100000/50=2000$

c. 

IO cost: 12

Explanation: Assume that the records of a certain `departmentId` are on exactly two pages. We need $[\log_22000]=11$ times IO to find the first page, and one more IO to get the second page.  

### 5

a. 100000

Explanation: Data is not sorted by the search key. So we need indexes for each record.

b. $bf_{index}=1000/10=100,100000/100=1000$ pages

c. $\lceil\log_2 1000\rceil+1=11$

d. 3

Explanation: $\lceil \log_{100} 100000\rceil=3$