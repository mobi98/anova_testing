import pandas as pd
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
                    description='Splits csv files into genes and mutations')
    parser.add_argument('--mutation-file', dest='mutation_file',
                        help='path of the mutation file', required=True)
    parser.add_argument('--genes-file', dest = 'genes_file', help='path to the genes file', required=True)

    return parser.parse_args()

class SplitCsvFiles:
    def __init__(self, mutation_file, gene_ko_file):
        self.mutation_file = mutation_file
        self.gene_ko_file = gene_ko_file


    def split_mutations(self):
        muts = pd.read_csv(self.mutation_file, sep = '\t')
        muts = muts.T
        muts.columns = muts.iloc[0]
        muts = muts.drop(muts.index[0]) 

        for m in muts.columns:
            to_write = muts[m]
            to_write.to_csv('%s.tsv'%m, index =True, index_label='Model', sep='\t')

    def split_genes(self):
        genes = pd.read_csv(self.gene_ko_file, sep = '\t')

        for g in genes:
            to_write = genes.loc[:,['Model', g]]
            to_write.to_csv('%s.tsv'%g, index=False, sep='\t')


if __name__ == '__main__':
    args = parse_args()
    splitter = SplitCsvFiles(args.mutation_file, args.genes_file)
    splitter.split_mutations()
    splitter.split_genes()
            