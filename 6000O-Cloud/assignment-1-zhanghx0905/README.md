[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=10144252&assignment_repo_type=AssignmentRepo)

# CSIT6000O Assignment-1: EC2 Measurement (2 questions, 4 marks)

### Deadline: 23:59, Feb 27, Monday

---

### Name: Zhang Hexiao
### Student Id: 20932780
### Email: hzhangea@connect.ust.hk

---

## Question 1: Measure the EC2 CPU and Memory performance

1. (1 mark) Report the name of measurement tool used in your measurements (you are free to choose *any* open source measurement software as long as it can measure CPU and memory performance). Please describe your configuration of the measurement tool, and explain why you set such a value for each parameter. Explain what the values obtained from measurement results represent (e.g., the value of your measurement result can be the execution time for a scientific computing task, a score given by the measurement tools or something else).

    > I tested with Phoronix Test Suite, using `compress-7zip` for CPU performance and `ramspeed` for memory performance respectively.
    >
    > `compress-7zip` has no parameters to set. For `ramspeed`, the task I selected is Average and Floating Point Calculation. Because it contains multiple operations, while floating point number are more common in scientific computing.**
    >
    > For`compress-7zip`, MIPS (million instructions per second) of Compression and Decompression is performance metric. For `ramspeed`, the software will test the memory throughput in MB/s.

2. (1 mark) Run your measurement tool on general purpose `t3.medium`, `m5.large`, and `c5d.large` Linux instances, respectively, and find the performance differences among these instances. Launch all the instances in the **US East (N. Virginia)** region. Does the performance of EC2 instances increase commensurate with the increase of the number of vCPUs and memory resource?

    In order to answer this question, you need to complete the following table by filling out blanks with the measurement results corresponding to each instance type.

    | Size        | CPU performance (MIPS) | Memory performance (MB/s) |
    | ----------- | ---------------------- | ------------------------- |
    | `t3.medium` | 6668/ 4447             | 12893.36                  |
    | `m5.large`  | 7143/ 4540             | 13607.89                  |
    | `c5d.large` | 8074/ 5272             | 14418.08                  |

    `c5d.large` has the best performance, while `t3.medium` has the worst.
    
    > Region: US East (N. Virginia). Use `Ubuntu Server 22.04 LTS (HVM)` as AMI.

## Question 2: Measure the EC2 Network performance

1. (1 mark) The metrics of network performance include **TCP bandwidth** and **round-trip time (RTT)**. Within the same region, what network performance is experienced between instances of the same type and different types? In order to answer this question, you need to complete the following table.

    | Type                      | TCP b/w (Gbps) | RTT (ms) |
    | ------------------------- | -------------- | -------- |
    | `t3.medium` - `t3.medium` | 4.80           | 0.219    |
    | `m5.large` - `m5.large`   | 9.72           | 0.118    |
    | `c5n.large` - `c5n.large` | 24.5           | 0.087    |
    | `t3.medium` - `c5n.large` | 4.80           | 0.144    |
    | `m5.large` - `c5n.large`  | 9.72           | 0.094    |
    | `m5.large` - `t3.medium`  | 4.80           | 0.176    |

    > Region: US East (N. Virginia). Use `Ubuntu Server 22.04 LTS (HVM)` as AMI.

2. (1 mark) What about the network performance for instances deployed in different regions? In order to answer this question, you need to complete the following table.

    | Connection                | TCP b/w   | RTT (ms) |
    | ------------------------- | --------- | -------- |
    | N. Virginia - Oregon      | 26.0 Mbps | 63.474   |
    | N. Virginia - N. Virginia | 9.74 Gbps | 0.124    |
    | Oregon - Oregon           | 9.74 Gbps | 0.104    |

    > Region: US East (N. Virginia), US West (Oregon). Use `Ubuntu Server 22.04 LTS (HVM)` as AMI. All instances are `c5.large`.
