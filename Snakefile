#Input minimum overlap length here
min_overlap_len = 10


rule all:
    input:
     	"./output/ALLELES.aln"  

rule read_sequences:
	input: 	
		#test = "./input_files/test_READS.fasta",
		R1 = "./input_files/READS.fasta",
		script = "./scripts/read_fasta.py"
	output: 
		#test_out = "./input_files/test_READS.tsv",
		R1_out = "./input_files/READS.tsv"
	shell:
		"""
		python3.8 {input.script} {input.R1} {output.R1_out}
		"""

rule identify_overlap1:
	input:
		#test = "./input_files/test_READS.tsv",
		R1 = "./input_files/READS.tsv",
		query = "./input_files/QUERY.fasta",
		script = "./scripts/initial_overlap.py"
	output:
		overlap_list = "./intermediate_files/overlap_list.tsv",
		contig_list = "./intermediate_files/contig_list.tsv"
	params:
		minimum_overlap_length = min_overlap_len
	shell:
		"""
		python3.8 {input.script} {input.R1} {input.query} {output.overlap_list} {output.contig_list} {params.minimum_overlap_length}
		"""
rule extend_contigs:
	input:
		#test = "./input_files/test_READS.tsv",
	       	R1 = "./input_files/READS.tsv",
		contigs = "./intermediate_files/contig_list.tsv",
		script = "./output/extend_contigs.py"
	output:
		longest_contig = "./output/ALLELES.fasta"
	params: minimum_overlap_length = min_overlap_len
	shell:
		"""
		python3.8 {input.script} {input.R1} {input.contigs} {output.longest_contig} {params.minimum_overlap_length}
		"""

rule contig_overlap:
	input:
		#test = "./input/test_READS.tsv",
                R1 = "./input/READS.tsv",
		contig = "./output/ALLELES.fasta",
		script = "./scripts/overlapping_contig.py"
	output:
		aln = "./output/ALLELES.aln"
	params: minimum_overlap_length = min_overlap_len
	shell:
		"""
		python3.8 {input.script} {input.R1} {input.contig} {output.aln} {params.minimum_overlap_length}
		"""


