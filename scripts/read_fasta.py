#reading 

import numpy as np
import sys
def read_fasta(filename):  # read fasta and output numpy array
    with open(filename, 'r') as file:
        sequences = []
        current_sequence = []
        read_names = []

        for line in file:
            line = line.strip()  # removes extra spaces
            if line.startswith('>'):  # only looking at the read names
                read_names.append(line[1:])
                if current_sequence:  # ensures the line is not empty
                    sequences.append(''.join(current_sequence))
                    current_sequence = []  # logs the sequence
            else:
                current_sequence.append(line)  # logs the name of the read

        if current_sequence:  # appends the last sequence
            sequences.append(''.join(current_sequence))

    return read_names, np.array(sequences)


def save_as_tsv(read_names, sequences, output_filename):
    with open(output_filename, 'w') as tsv_file: #ensures that the the file is closed properly
        for read_name, sequence in zip(read_names, sequences):
            tsv_file.write(f"{read_name}\t{sequence}\n")

if __name__ == "__main__": #makes sure this is not reassigned accidentally 
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    read_names, sequences_array = read_fasta(input_file)
    save_as_tsv(read_names, sequences_array, output_file)
	


