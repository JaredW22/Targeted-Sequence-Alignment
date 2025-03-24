# Targeted-Sequence-Alignment
This pipeline is designed to identify the longest possible contig surronding an input query sequence using a gzipped fasta file of sequencer reads. 
## Input Files
Input files are fasta files containing the sequencer reads and query sequence. these files are titled ...
## Example Use Cases
Identifying the longest contig surronding a query sequence can be useful when testing to see if genetic manipulation has been sucessful, such as CRISPR-based gene editing, or trying to identify the origin of a contaminating sequence during a PCR reaction. In the CRISPR example, one would select a unique sequence adjacent to the site of targeted manipulation as the query sequence, and then use the longest contig to test whether the desired editing took place. In the case of PCR contamination, one would select the primer as the query sequence and then allign the contigs to various genomes to identify the source of the contamination. Or, if you have a different use case, feel free to see if this pipeline works for you!
