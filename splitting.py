# Split FASTA file by indexes. I didn't try to improve this one, as it was already pretty fast and I couldn't come up
# with anything that could ake it faster. Perhaps chunk reading would make it faster on old hardware or when reading
# very big sequences (on my computer, it made it slower). Though, if an entire human chromosome is only about 250MB
# at max, one will rarely need more RAM.

import sys

INFILE = sys.argv[1]  # File is taken from first arg

HEADER_START = int(sys.argv[2])  # Index positions taken from following args
HEADER_END = int(sys.argv[3])

SEQ_START = int(sys.argv[4])
SEQ_END = int(sys.argv[5])

infile = open(INFILE, "rb")

infile.seek(HEADER_START)  # Pointer at header start
header = infile.read(HEADER_END - HEADER_START)  # Read chunk with length of header

infile.seek(SEQ_START)  # Pointer at sequence start
seq = infile.read(SEQ_END - SEQ_START)  # Read chunk with length of sequence

infile.close()

if len(seq) < 10 ** 6:
    print(b"".join([header, b"\n", seq]))
else:
    # Write to file if the sequence is large. Large sequences can take hours to print to console.
    outfile = "result.fsa"
    with open(outfile, "wb") as outfile:
        outfile.write(b"".join([header, b"\n", seq]))
    print(f"Writen sequence to {outfile}")
