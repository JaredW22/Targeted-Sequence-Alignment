import sys
import numpy as np
import unittest

def reverse_complement(seq): #Generates the corresponding read on the complimentary strand, input is a strand and output is the expected complimetary strand
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


def contig_overlap(contig_seq, array, min_overlap_length): #tests for overlap with a contig sequence and the list of reads. Input contig sequence, read array and the minimum overlap length parameter, output is the list of extended contigs (containing the original contig and part of the read)
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
    min_overlap_length = sys.argv[4]
    read_names, sequences_array = read_tsv(reads)
    with open(contig_list, 'r') as file:
        lines = file.readlines()
    #print("lines:", lines)
    sequences = []
    for line in lines:
        columns = line.split('\t')
        if len(columns) > 2: 
            sequences.append(columns[2])
    #print("sequences", sequences)
    contigs_list = []
    all_contigs = []
    for previous_contig in sequences:
        temp_contigs = contig_overlap(previous_contig, sequences_array, int(min_overlap_length))
        contigs_list = contigs_list + temp_contigs
        #print("checking contigs_list", contigs_list)
    pre_contigs = contigs_list
    all_contigs = contigs_list
    #print("this is pre_contigs", pre_contigs, "this is the first contigs_list:", contigs_list)
    while len(contigs_list) > 0:
        #print("this is the next contigs_list:", contigs_list)
        pre_contigs = contigs_list
        temp_contigs = []
        contigs_list = []
        for term in pre_contigs: #iterates through the previous contigs
            temp_contigs = contig_overlap(term, reads, int(min_overlap_length))
            contigs_list = contigs_list + temp_contigs
        all_contigs = all_contigs + contigs_list
    #print("outside the loop, pre_contigs:", pre_contigs)
    longest = [term for term in all_contigs if len(term) == max(len(term) for term in all_contigs)]
    with open(longest_contig, 'w') as longest_contig_file: #writes the longest contig file
        i = 1
        for seq in longest:
            name = "sequence" + str(i)
            i = i+1
            longest_contig_file.write(f"{name}\n")
            longest_contig_file.write(f">{seq}\n")



