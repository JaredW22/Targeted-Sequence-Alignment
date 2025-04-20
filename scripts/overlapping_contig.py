import sys
import numpy as np


def reverse_complement(seq): #generates the complimentary strand in the correct orientation
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    try:
        return ''.join(complement[base] for base in reversed(seq) if base in complement)
    except KeyError as e:
        print(f"Invalid character {e} found in sequence.")
        return None

def read_tsv(filename):  # read tsv and output lists of names and sequences
    names = []
    sequences = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                names.append(parts[0])
                sequences.append(parts[1])
    return names, np.array(sequences)

def contig_overlap(query_seq, query_name, array, min_overlap_length): #input is the query sequence, query name, read file and minimum overlap parameter. The function then looks for all reads that ovoerlap this contig and outputs details about this overlap
    overlaps = []
    contigs = []
    for name, seq in array:
        temp_overlaps_fwd = []
        temp_overlaps_rev = []
        for i in range(len(query_seq)):
            for j in range(i + min_overlap_length, len(query_seq)+1): #interating through the query sequence and checking for allignment with the read, taking the longest allignment found 
                substring = query_seq[i:j]
                rev_comp_substring = reverse_complement(substring) #doing the same for the reverse direction 
                if substring in seq:
                    start_index = seq.find(substring) #finds where in the read there is overlap (overlap in the contig is already found w i and j)
                    end_index = start_index + len(substring)
                    length = abs(j - i)
                    temp_overlaps_fwd.append((name, query_name, seq, i, j, start_index, end_index, length))
                if rev_comp_substring in seq:
                    seq.find(rev_comp_substring)
                    start_index = seq.find(rev_comp_substring)
                    end_index = start_index - len(rev_comp_substring)
                    length = abs(i-j)
                    temp_overlaps_rev.append((name, query_name, seq, i, j, start_index, end_index, length))
                else:
                    break
        if temp_overlaps_fwd:
            add = max(temp_overlaps_fwd, key=lambda x: x[-1])
            name = add[0]
            query_name = add[1]
            seq = add[2]
            i = add[3]
            j = add[4]
            start_index = add[5]
            end_index = add[6]
            length = add[7]
            overlaps.append(add)
        if temp_overlaps_rev:
            add = max(temp_overlaps_rev, key=lambda x: x[-1])
            overlaps.append(add)
            name = add[0]
            query_name = add[1]
            seq = add[2]
            i = add[3]
            j = add[4]
            start_index = add[5]
            end_index = add[6]
            length = add[7]                    
    return overlaps


if __name__ == "__main__": #pulling the file names in from the Snakemake
    array = sys.argv[1]
    query = sys.argv[2]
    overlap_list = sys.argv[3]
    min_overlap_len = sys.argv[4]

with open(query, 'r') as file: #writing the output file
    lines = file.readlines()
    i = 1
    with open(overlap_list, 'w') as overlap_file:
        overlap_file.write(f"sseqid\tqseqid\tsequence\tqstart\tqend\tsstart\tsend\tlength\n")
        for line in lines[1:]:
            query_name = "sequence" + str(i)
            query_seq = line
            read_names, sequences_array = read_tsv(array)
            i += 1
            overlaps = contig_overlap(query_seq, query_name, zip(read_names, sequences_array), int(min_overlap_len))
            for name, query_name, sequence, query_start, query_end, seq_start, seq_end, length in overlaps:
                overlap_file.write(f"{name}\t{query_name}\t{sequence}\t{query_start}\t{query_end}\t{seq_start}\t{seq_end}\t{length}\n")

