#Input minimum overlap length here
min_overlap_len = 10


rule all:
    input:
     	"/beevol/home/williamj/CPBS/ALLELES.aln"  

rule read_sequences:
	input: 	
		#test = "/beevol/home/williamj/CPBS/test_READS.fasta",
		R1 = "/beevol/home/williamj/CPBS/READS.fasta",
		script = "/beevol/home/williamj/CPBS/read_fasta.py"
	output: 
		#test_out = "/beevol/home/williamj/CPBS/test_READS.tsv",
		R1_out = "/beevol/home/williamj/CPBS/READS.tsv"
	shell:
		"""
		python3.8 {input.script} {input.R1} {output.R1_out}
		"""

rule identify_overlap1:
	input:
		#test = "/beevol/home/williamj/CPBS/test_READS.tsv",
		R1 = "/beevol/home/williamj/CPBS/READS.tsv",
		query = "/beevol/home/williamj/CPBS/QUERY.fasta",
		script = "/beevol/home/williamj/CPBS/initial_overlap.py"
	output:
		overlap_list = "/beevol/home/williamj/CPBS/overlap_list.tsv",
		contig_list = "/beevol/home/williamj/CPBS/contig_list.tsv"
	params:
		minimum_overlap_length = min_overlap_len
	shell:
		"""
		python3.8 {input.script} {input.R1} {input.query} {output.overlap_list} {output.contig_list} {params.minimum_overlap_length}
		"""
rule extend_contigs:
	input:
		#test = "/beevol/home/williamj/CPBS/test_READS.tsv",
	       	R1 = "/beevol/home/williamj/CPBS/READS.tsv",
		contigs = "/beevol/home/williamj/CPBS/contig_list.tsv",
		script = "/beevol/home/williamj/CPBS/extend_contigs.py"
	output:
		longest_contig = "/beevol/home/williamj/CPBS/ALLELES.fasta"
	params: minimum_overlap_length = min_overlap_len
	shell:
		"""
		python3.8 {input.script} {input.R1} {input.contigs} {output.longest_contig} {params.minimum_overlap_length}
		"""

rule contig_overlap:
	input:
		#test = "/beevol/home/williamj/CPBS/test_READS.tsv",
                R1 = "/beevol/home/williamj/CPBS/READS.tsv",
		contig = "/beevol/home/williamj/CPBS/ALLELES.fasta",
		script = "/beevol/home/williamj/CPBS/overlapping_contig.py"
	output:
		aln = "/beevol/home/williamj/CPBS/ALLELES.aln"
	params: minimum_overlap_length = min_overlap_len
	shell:
		"""
		python3.8 {input.script} {input.R1} {input.contig} {output.aln} {params.minimum_overlap_length}
		"""


