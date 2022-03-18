# First method I came up with for indexing FASTA files. Very slow, takes about 12 minutes to index the human genome.

import time as t

INFILE = "path/to/human.fsa"

start = t.time()

infile = open(INFILE, "r")

all_positions = []
curr_seq_positions = []
is_prev_line_header = False
is_first_sequence = True
beginning_of_line_pos = infile.tell()  # Save position of beginning of the line
line = infile.readline()
while line != "":
    if line[0] == ">":  # If line is a header
        curr_seq_positions.append(beginning_of_line_pos)  # Save beginning of line (header start)
        curr_seq_positions.append(beginning_of_line_pos + len(line))  # Save end of line (header end)
        curr_seq_positions.append(beginning_of_line_pos + len(line) + 1)  # Save beginning of next line (sequence start)
        if not is_first_sequence:  # Unless it's the first sequence
            curr_seq_positions.append(beginning_of_line_pos - 1)  # Save end of previous line (sequence end)
            all_positions.append(tuple(curr_seq_positions))  # Append current sequence positions to list of positions
            curr_seq_positions = []  # Clean current sequence positions
        is_first_sequence = False
    beginning_of_line_pos = infile.tell()  # Save position of beginning of the line
    line = infile.readline()  # Read next line

curr_seq_positions.append(beginning_of_line_pos)  # Add last sequence end
all_positions.append(tuple(curr_seq_positions))  # Append last sequence positions to list of positions
curr_seq_positions = []

end = t.time()

infile.close()

for out_line in all_positions:
    print(*out_line, sep=" ")  # Print in desired format

print(f"Finished in {(end - start).__round__(3)}s")  # Time it took to run

# Output:
# 0 71 72 253105767
# 253105768 253105839 253105840 499335927
# 499335928 499335999 499336000 700936484
# 700936485 700936556 700936557 894321354
# 894321355 894321426 894321427 1078885323
# 1078885324 1078885395 1078885396 1252538141
# 1252538142 1252538213 1252538214 1414539953
# 1414539954 1414540025 1414540026 1562097639
# 1562097640 1562097711 1562097712 1702799007
# 1702799008 1702799080 1702799081 1838826460
# 1838826461 1838826533 1838826534 1976164599
# 1976164600 1976164672 1976164673 2111661237
# 2111661238 2111661310 2111661311 2227931711
# 2227931712 2227931784 2227931785 2336759564
# 2336759565 2336759637 2336759638 2440450680
# 2440450681 2440450753 2440450754 2532294738
# 2532294739 2532294811 2532294812 2616939877
# 2616939878 2616939950 2616939951 2698652790
# 2698652791 2698652863 2698652864 2758247440
# 2758247441 2758247513 2758247514 2823765750
# 2823765751 2823765823 2823765824 2871254306
# 2871254307 2871254379 2871254380 2922919822
# 2922919823 2922919894 2922919895 3081561471
# 3081561472 3081561543 3081561544 3139742749
# Finished in 742,682s
