rule all:
    input:
     	"/beevol/home/williamj/CPBS/longest_contig.tsv"  


#rule read_sequences:
#	input: 	
#		test = "/beevol/home/williamj/CPBS/test_READS.fasta",
		#R1 = "/beevol/home/williamj/CPBS/test_READS.fasta",
#		script = "/beevol/home/williamj/CPBS/read_fasta.py"
#	output: 
#		test_out = "/beevol/home/williamj/CPBS/test_READS.tsv",
		#R1_out = "/beevol/home/williamj/CPBS/READS.tsv"
#	shell:
#		"""
#		python3.8 {input.script} {input.test} {output.test_out}
#		"""

#rule identify_overlap1:
#	input:
#		test = "/beevol/home/williamj/CPBS/test_READS.tsv",
		#R1 = "/beevol/home/williamj/CPBS/READS.bed",
#		query = "/beevol/home/williamj/CPBS/QUERY.fasta",
#		script = "/beevol/home/williamj/CPBS/initial_overlap.py"
#	output:
#		overlap_list = "/beevol/home/williamj/CPBS/overlap_list.tsv",
#		contig_list = "/beevol/home/williamj/CPBS/contig_list.tsv"
#	shell:
#		"""
#		python3.8 {input.script} {input.test} {input.query} {output.overlap_list} {output.contig_list}
#		"""
rule extend_contigs:
	input:
		test = "/beevol/home/williamj/CPBS/test_READS.tsv",
	       	#R1 = "/beevol/home/williamj/CPBS/READS.bed",
		contigs = "/beevol/home/williamj/CPBS/contig_list.tsv",
		script = "/beevol/home/williamj/CPBS/extend_contigs.py"
	output:
		longest_contig = "/beevol/home/williamj/CPBS/longest_contig.tsv"
	shell:
		"""
		python3.8 {input.script} {input.test} {input.contigs} {output.longest_contig}
		"""



