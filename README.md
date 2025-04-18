# Targeted-Sequence-Alignment
This pipeline is designed to identify the longest possible contig surronding an input query sequence using a gzipped fasta file of sequencer reads. 
## Input Files
Input files are fasta files containing the sequencer reads and query sequence. These files are titled READS.fasta (or test_READS.fasta for troubleshooting) and QUERY.fasta. Other files used as inputs are the python scripts read_fasta.py, initial_overlap.py and extend_contigs.py
## Output Files
This pipeline outputs many files. The overlap_list.tsv lists all sequences that overlap with the query, and the contig_list.tsv lists the combined sequence from every overlapping sequence that can extend the contig. These files only apply to the first iteration. ALLELES.fasta is a fasta file of the longest possible contig containing the query sequence. ALLELES.aln is a .txt file that describes the allignment of all overlapping reads to the longest contig. 
## Example Use Cases
Identifying the longest contig surronding a query sequence can be useful when testing to see if genetic manipulation has been sucessful, such as CRISPR-based gene editing, or trying to identify the origin of a contaminating sequence during a PCR reaction. In the CRISPR example, one would select a unique sequence adjacent to the site of targeted manipulation as the query sequence, and then use the longest contig to test whether the desired editing took place. In the case of PCR contamination, one would select the primer as the query sequence and then allign the contigs to various genomes to identify the source of the contamination. Or, if you have a different use case, feel free to see if this pipeline works for you!
# Installing 
Installing snakemake, which runs all of the scripts in order, with the output files of one script used as inputs into the next scripts. Here is the link to the snakemake package: https://anaconda.org/bioconda/snakemake
```bash
conda install -c bioconda snakemake
```
Installing numpy
```bash
pip install numpy
```

# How to Use
## Cloning the Repository
Open Terminal or Command Prompt
Navigate to the directory where you want to clone
```
cd path/to/your/directory
```
Clone the Repository
```
git clone https://github.com/JaredW22/Targeted-Sequence-Alignment.git
```
Navigate to the cloned repository:
```
cd Targeted-Sequence-Alignment
```
Verify successful cloning by listing the files
```
ls
```

## Example for running the pipeline:
```bash
cd /path/to/cloned/repository
bsub < run_snake.bsub
```
or
```bash
module load python/3.8.5
snakemake --snakefile ./Snakefile --cores 1
```
Inside the run_snake.bsub file is the same as the second code box above. The --snakefile argument tells the snakemake command which file to run. --cores determines the numbers of cores that the job will run on, which depends on the number of cores your computer can access. Another common argument is the --latency-wait argument, which determines how long the job will wait for the output file before spitting out an error. 
## To Change the Minimum Overlap Length
The minimum overlap length is default set to 10bp. To change this, you must change the value at the top of the Snakefile. To do this:
```
vim Snakefile
```
Press i to insert new text, then change the value at the top of the Snakefile assigned to min_overlap_len. To write the file (save) and quit back to the original screen, hit esc, then:
```
:wq
```
# Explanation of Files
## Snakefile
This is the file that can be used to run the entire pipeline in one command. See installation instructions if this file is not running properly.
## log.tsv
This is the log of run times throughout my troubleshooting and optimization process. This is not meant to be used in the pipeline, but only for reference. 
## notes.tsv
This is a log of my notes as I went through the development of the pipeline and integration of different ideas. Mostly included for grading purposes 
## run_snake.bsub
This is a file that allows the running of the snakefile to be assigned to a computing cluster 

## Input Files
QUERY.fasta is an example query sequence
READS.fasta is an example of an output fasta file from sequencing 
READS.tsv is an intermediate file generated for easier processing 
test_READS.fasta and tsv are similar to above, but only a subset to make things faster when troubleshooting 

## Intermediate Files
contig_list.tsv is an intermediate file generated from the initial_overlap.py that is then used in the extend_contigs.py script to have an initial list of contigs to test against the rest of the reads
overlap_list.tsv is a list of all sequences that overlap the initial query, regardless of whether they extend the query 

## Output
ALLELES.fasta is the final longest contig sequence(s)
ALLELES.aln is a list of all reads that overlap the final contig sequence 

## Scripts
read_fasta.py reads in the fasta files and converts them to tsvs for easier processing 
initial_overlap.py finds all sequences that overlap the query and outputs as the overlap_list.tsv. It also finds all sequences that overlap AND extend the query sequence, and outputs these in the contig_list.tsv
extend_contigs.py uses the initial contig_list.tsv and iteratively tests allignments to all of the reads to see if any of the other reads contain at least the minimum overlap and extend the contig. If so, these are then tested in the next iteration until a longest contig is found. 
overlapping_contig.py then goes back and tests for allignment to the longest contig file to list all reads that overlap and where. 

## unit_test
These files are for performing unit tests on the different scripts in the Scripts repository. They can be run similar to above: 
```
bsub < run_unit_test.bsub
```
## Archive
The archive contains older versions of the scripts to show progress in the development of this pipeline. These are not meant to be run. 
