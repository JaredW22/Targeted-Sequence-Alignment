import sys
import numpy as np


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


def query_overlap(query_seq, query_name, array, min_overlap_length=10):
    overlaps = []
    contigs = []
    for name, seq in array:
        temp_overlaps = []
        temp_contigs = []
        for i in range(len(query_seq)):
            for j in range(i + min_overlap_length, len(query_seq) + 1):
                substring = query_seq[i:j]
                if substring in seq:
                    start_index = seq.find(substring)
                    end_index = start_index + len(substring)
                    length = j - i
                    temp_overlaps.append((name, query_name, seq, i, j, start_index, end_index, length))
                    if query_seq[0:min_overlap_length] in seq or query_seq[-1*min_overlap_length:-1] in seq:
                        combined_sequence = query_seq[:i] + seq[start_index:end_index] + query_seq[j:]
                        temp_contigs.append((name, query_name, combined_sequence, i, j, start_index, end_index, length))
        if temp_overlaps:
            add = max(temp_overlaps, key=lambda x: x[-1])
            overlaps.append(add)
            if temp_contigs:
                add = max(temp_contigs, key=lambda x: x[-1])
                contigs.append(add)
    return overlaps, contigs

#def write_tsv_overlap(read_names, overlap_seq, output_name):
#	with open(output_name, 'w') as tsv_file:
#		for read_names, sequence in zip(read_names, sequences):
#			tsv_file.write(f"{read_name}\t{sequence}\n")

if __name__ == "__main__": #pulling the file names in from the Snakemake
    array = sys.argv[1]
    query = sys.argv[2]
    overlap_list = sys.argv[3]
    contig_list = sys.argv[4]

    with open(query, 'r') as file:
        lines = file.readlines()
        query_name = lines[0].strip()[1:] #to get rid of the carrot
        query_seq = lines[1].strip() #only pulls the second line from the query file
    read_names, sequences_array = read_tsv(array)
    overlaps, contigs = query_overlap(query_seq, query_name, zip(read_names, sequences_array))
    
    with open(overlap_list, 'w') as overlap_file:
        overlap_file.write(f"sseqid\tqseqid\tsequence\tquery_start\tquery_end\tseq_start\tseq_end\tlength\n")
        for name, query_name, sequence, query_start, query_end, seq_start, seq_end, length in overlaps:
            overlap_file.write(f"{name}\t{query_name}\t{sequence}\t{query_start}\t{query_end}\t{seq_start}\t{seq_end}\t{length}\n")

    with open(contig_list, 'w') as contig_file:
        contig_file.write(f"name\tqseqid\tsequence\tquery_start\tquery_end\tseq_start\tseq_end\tlength\n")
        for name, query_name, sequence, query_start, query_end, seq_start, seq_end, length in contigs:
            contig_file.write(f"{name}\t{query_name}\t{sequence}\t{query_start}\t{query_end}\t{seq_start}\t{seq_end}\t{length}\n")
#then compare each sequence to the query and list the sequences that match and with how muh overlap
#count each of these sequences as contigs only if they extend the query, maybe shorten to only compare against the first and last ten bp of the query 
#compare all sequences against the contigs iteravily until no longer generating new contigs of longer lengths (this should probably be a different script) 
