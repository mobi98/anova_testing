import unittest
from anova_testing.run_anova import RunAnovaTests
import pandas as pd
import os

class TestRunAnovaTests(unittest.TestCase):

    def setUp(self) -> None:
        self.anova_test= RunAnovaTests(mutation_file='./mock_mutation.tsv', 
                                        genes_file='./mock_gene_KO.tsv',
                                        file_type='non-split')
        
        self.anova_test_split = RunAnovaTests(mutation_file='./mock_split_mutation.tsv', 
                                        genes_file='./mock_split_gene.tsv',
                                        file_type='split')
        
    def test_mutation_formatting(self):
        dat = self.anova_test.mutation
        self.assertIsInstance(dat, pd.DataFrame)
        row3 = list(dat.iloc[3,:])
        self.assertEqual(row3, [0,0,0])

    def test_mutation_formatting_for_split_files(self):
        dat = self.anova_test_split.mutation
        self.assertIsInstance(dat, pd.DataFrame)
        row7 = list(dat.iloc[7,:])[0]
        self.assertEqual(row7, 1)

    def test_gene_ko_formatting(self):
        dat = self.anova_test.genes
        self.assertIsInstance(dat, pd.DataFrame)

    def test_anova_files_are_written(self):
        self.anova_test.run_anova()
        pwd_files = os.listdir()
        self.assertIn('GeneA_KO_Gene2_mut_anova.tsv', pwd_files)


if __name__ == "__main__":
    unittest.main()