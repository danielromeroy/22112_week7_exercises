# Second method to index FASTA file. Pretty fast, indexes the human genome in under 1.5 seconds on my computer.

import time as t
import re

INFILE = "path/to/human.fsa"
CHUNKSIZE = 2 ** 25

start = t.time()

infile = open(INFILE, "rb")

position_before_chunk = 0  # Save position before reading the chunk
chunk = infile.read(CHUNKSIZE)
header_starts = []
while True:
    matches = re.finditer(b">", chunk)  # Find init positions of fasta headers
    positions = [pos.start() for pos in matches]  # Convert iterator into list of positions
    if len(positions) > 0:
        # Save found positions as the position in the current chunk plus all previously read chunks
        header_starts.extend([pos + position_before_chunk for pos in positions])
    position_before_chunk += len(chunk)  # Add current chunk length to cumulative position
    if len(chunk) < CHUNKSIZE:
        break  # Break out of the while loop if finished reading in entire file
    chunk = infile.read(CHUNKSIZE)

# Sequence ends will be the previous position to the header starts (to account for the newline)
seq_ends = [pos - 1 for pos in header_starts][1:]  # Delete first element (will always be -1, before the first header)
seq_ends.append(position_before_chunk - 1)  # Add ending position (-1 to account for newline)


# Header ends and sequence starts are a bit trickier. I read a 300 char chunk starting from the header start and find
# the position of the first newline. The header end will be the position of the newline in the chunk plus the position
# from which I started reading the chunk. The sequence start will be that plus 1 (skipping the newline).
header_ends = []
seq_starts = []
for h_start in header_starts:
    infile.seek(h_start)
    chunk = infile.read(300)
    nl_pos = chunk.find(b"\n")
    header_ends.append(h_start + nl_pos)
    seq_starts.append(h_start + nl_pos + 1)

# Print with the desired format
for i in range(len(header_starts)):
    print(f"{header_starts[i]} {header_ends[i]} {seq_starts[i]} {seq_ends[i]}")

end = t.time()

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
# Finished in 1.472s
