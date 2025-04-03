import unittest
import numpy as np
from initial_overlap import reverse_complement, read_tsv, query_overlap

class TestFunctions(unittest.TestCase):

    def test_reverse_complement(self):
        self.assertEqual(reverse_complement("ATGC"), "GCAT")
        self.assertEqual(reverse_complement("AATTCCGG"), "CCGGAATT")
        self.assertEqual(reverse_complement(""), "")
        self.assertEqual(reverse_complement("A"), "T")

    def test_read_tsv(self):
        filename = 'test.tsv'
        with open(filename, 'w') as file:
            file.write("name1\tATGC\n")
            file.write("name2\tAATTCCGG\n")

        names, sequences = read_tsv(filename)
        self.assertEqual(names, ["name1", "name2"])
        np.testing.assert_array_equal(sequences, np.array(["ATGC", "AATTCCGG"]))

    def test_query_overlap(self):
        query_seq = "AGCTTAGCTAGCT"
        query_name = "query1"
        array = [("name1", "AGCTTAGCTAGCTTAGCT"), ("name2", "GCTTAGCTAGCT")]
        overlaps, contigs = query_overlap(query_seq, query_name, array)
        
        expected_overlaps = [
            ("name1", "query1", "AGCTTAGCTAGCTTAGCT", 0, 13, 0, 13, 13),
            ("name2", "query1", "GCTTAGCTAGCT", 1, 13, 0, 12, 12)
        ]
        expected_contigs = [
            ("name1", "query1", "AGCTTAGCTAGCTTAGCT", 0, 13, 0, 13, 13),
            ("name2", "query1", "AGCTTAGCTAGCT", 1, 13, 0, 12, 12)
        ]
        
        self.assertEqual(overlaps, expected_overlaps)
        self.assertEqual(contigs, expected_contigs)


if __name__ == '__main__':
    unittest.main()
