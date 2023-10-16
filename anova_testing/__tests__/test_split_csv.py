import unittest
from anova_testing.split_csvs import SplitCsvFiles
import pandas as pd
import os

class TestSplitCsv(unittest.TestCase):

    def setUp(self) -> None:
        self.split_csv = SplitCsvFiles(gene_ko_file='./mock_gene_KO.tsv', 
                                       mutation_file='./mock_mutation.tsv')


    def test_gene_file_contains_correct_gene(self):
        self.split_csv.split_genes()
        read_data_in = pd.read_csv('./GeneA_KO.tsv', sep='\t')
        col1= read_data_in.columns[1]
        self.assertEqual(col1, 'GeneA_KO')

    def test_mutation_file_contains_correct_mutation(self):
        self.split_csv.split_mutations()
        read_data_in = pd.read_csv('./Gene1_mut.tsv', sep='\t')
        col1=read_data_in.columns[1]
        self.assertEqual(col1, 'Gene1_mut')


    def test_output_gene_files_are_present(self):
        gene_data = pd.read_csv(self.split_csv.gene_ko_file, sep='\t')
        for gene in gene_data.columns[1:2]:
            file = '{}.tsv'.format(gene)
            pwd_files = os.listdir()
            self.assertIn(file, pwd_files)


    def test_output_mutation_files_are_present(self):
        mutation_data = pd.read_csv(self.split_csv.mutation_file, sep='\t')
        for mut in mutation_data['Mutation']:
            file = '{}.tsv'.format(mut)
            pwd_files = os.listdir()
            self.assertIn(file, pwd_files)

if __name__ == "__main__":
    unittest.main()