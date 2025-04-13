import sys
import numpy as np
import unittest

def reverse_complement(seq):
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


def contig_overlap(contig_seq, array, min_overlap_length=10):  
    contigs = []
    temp_contigs = []
    for row in array:
        if len(row) == 2:
            name, seq = row
        else:
            seq = row 
        rev_seq = reverse_complement(seq)
        if contig_seq[:min_overlap_length] in seq:
            start_index = seq.find(contig_seq[:min_overlap_length])
            combined_sequence = seq[:start_index] + contig_seq
            temp_contigs.append(combined_sequence)
        if contig_seq[-min_overlap_length:] in seq:
            start_index = contig_seq.find(seq[:min_overlap_length])
            combined_sequence = contig_seq[:start_index] + seq
            temp_contigs.append(combined_sequence)
        if contig_seq[:min_overlap_length] in rev_seq:
            start_index = rev_seq.find(contig_seq[:min_overlap_length])
            combined_sequence = rev_seq[:start_index] + contig_seq
            temp_contigs.append(combined_sequence)
        if contig_seq[-min_overlap_length:] in rev_seq:
            start_index = contig_seq.find(rev_seq[:min_overlap_length])
            combined_sequence = contig_seq[:start_index] + rev_seq
            temp_contigs.append(combined_sequence)
    return temp_contigs

if __name__ == "__main__": #pulling the file names in from the Snakemake
    reads = sys.argv[1]
    contig_list = sys.argv[2]
    longest_contig = sys.argv[3]
    read_names, sequences_array = read_tsv(reads)
    with open(contig_list, 'r') as file:
        lines = file.readlines()
    sequences = []
    for line in lines:
        columns = line.split('\t')
        if len(columns) > 2: 
            sequences.append(columns[2])
    contigs_list = []
    for previous_contig in sequences:
        temp_contigs = contig_overlap(previous_contig, sequences_array)
        contigs_list = contigs_list + temp_contigs
    pre_contigs = contigs_list
    while True:
        if contigs_list:
            pre_contigs = contigs_list
            temp_contigs = []
            contigs_list = []
            for term in pre_contigs:
                temp_contigs = contig_overlap(term, reads)
                contigs_list = contigs_list + temp_contigs
        else:
            break

    with open(longest_contig, 'w') as longest_contig_file:
        longest_contig_file.write(f"sequence\n")
        for seq in pre_contigs:
            longest_contig_file.write(f"{seq}\n")



