# Targeted-Sequence-Alignment
This pipeline is designed to identify the longest possible contig surronding an input query sequence using a gzipped fasta file of sequencer reads. 
## Input Files
Input files are fasta files containing the sequencer reads and query sequence. These files are titled READS.fasta (or test_READS.fasta for troubleshooting) and QUERY.fasta. Other files used as inputs are the python scripts read_fasta.py, initial_overlap.py and extend_contigs.py
## Output Files
This pipeline outputs many files. The overlap_list.tsv lists all sequences that overlap with the query, and the contig_list.tsv lists the combined sequence from every overlapping sequence that can extend the contig. These files only apply to the first iteration. ALLELES.fasta is a fasta file of the longest possible contig containing the query sequence. ALLELES.aln is a .txt file that describes the allignment of all overlapping reads to the longest contig. 
## Example Use Cases
Identifying the longest contig surronding a query sequence can be useful when testing to see if genetic manipulation has been sucessful, such as CRISPR-based gene editing, or trying to identify the origin of a contaminating sequence during a PCR reaction. In the CRISPR example, one would select a unique sequence adjacent to the site of targeted manipulation as the query sequence, and then use the longest contig to test whether the desired editing took place. In the case of PCR contamination, one would select the primer as the query sequence and then allign the contigs to various genomes to identify the source of the contamination. Or, if you have a different use case, feel free to see if this pipeline works for you!
# How to Use
Example for running the pipeline:
```bash
bsub < run_snake.bsub
```
or
```bash
module load python/3.8.5
snakemake --snakefile ./Snakefile --cores 1
```
## Installing 
Installing snakemake, which runs all of the scripts in order, with the output files of one script used as inputs into the next scripts
```bash
conda install -c bioconda snakemake
```
Installing numpy
```bash
pip install numpy
```
