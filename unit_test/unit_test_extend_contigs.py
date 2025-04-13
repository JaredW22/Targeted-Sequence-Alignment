import unittest
import numpy as np
from extend_contigs import reverse_complement, read_tsv, contig_overlap

class TestYourScript(unittest.TestCase):

    def test_reverse_complement(self):
        self.assertEqual(reverse_complement("ATCG"), "CGAT")
        self.assertEqual(reverse_complement("GGCC"), "GGCC")
        self.assertEqual(reverse_complement("AATT"), "AATT")

    def test_read_tsv(self):
        # Create a mock TSV file
        with open('test.tsv', 'w') as file:
            file.write("name1\tATCG\nname2\tGGCC\nname3\tAATT\n")
        
        names, sequences = read_tsv('test.tsv')
        self.assertEqual(names, ["name1", "name2", "name3"])
        np.testing.assert_array_equal(sequences, np.array(["ATCG", "GGCC", "AATT"]))

    def test_contig_overlap(self):
        array = np.array([("name1", "TATATCGTAT"), ("name2", "GGCCATCG"), ("name3", "TACGATGGCC")])
        contig_seq = "ATCGTATCG"
        overlaps = contig_overlap(contig_seq, array, min_overlap_length=6)

        expected_overlaps = [
            "TATATCGTATCG",
            "GGCCATCGTATCG"
        ]

        self.assertEqual(overlaps, expected_overlaps)

if __name__ == "__main__":
    unittest.main()
