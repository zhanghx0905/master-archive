import os
import re

os.system("python main.py > output.txt")

# Sample input text
with open("output.txt", "r", encoding="utf16") as f:
    text = f.read()

# Define regex pattern to match the desired fields
pattern = r"====== Testcase (\d+) ======\nGot (\d+) objects\nbrute-force algo traversed (\d+) objects\nmin/max/avg time: ([\d.]+)s ([\d.]+)s ([\d.]+)s\nRtree traversed (\d+) objects\nmin/max/avg time: ([\d.]+)s ([\d.]+)s ([\d.]+)s"

# Find all matches in the input text
matches = re.findall(pattern, text)

# Generate Markdown table header
table = "| Testcase | Retrieved Objects | BF Traversed Objects | BF Time  | R-Tree Traversed Objects | R-tree Time |\n"
table += "| --- | --- | --- | --- | --- | --- |\n"

# Process each match and add a row to the table
for match in matches:
    testcase = match[0]
    objects = match[1]
    bf_traversal = match[2]
    bf_time_min = match[3]
    bf_time_max = match[4]
    bf_time_avg = match[5]
    rt_traversal = match[6]
    rt_time_min = match[7]
    rt_time_max = match[8]
    rt_time_avg = match[9]

    # Format time with 2 decimal places
    bf_time = (
        f"{float(bf_time_max):.2f}/{float(bf_time_min):.2f}/{float(bf_time_avg):.2f} s"
    )
    rt_time = (
        f"{float(rt_time_max):.2f}/{float(rt_time_min):.2f}/{float(rt_time_avg):.2f} s"
    )

    # Add a row to the table
    table += f"| {testcase} | {objects} | {bf_traversal} | {bf_time} | {rt_traversal} | {rt_time} |\n"

# Print the final Markdown table
print(table)
