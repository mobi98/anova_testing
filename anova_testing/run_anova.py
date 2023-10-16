import pandas as pd
import argparse
from scipy.stats import f_oneway

def parse_args():
    parser = argparse.ArgumentParser(
                    description='Splits csv files into genes and mutations')
    parser.add_argument('--mutation-file', dest='mutation_file',
                        help='path of the mutation file', required=True)
    parser.add_argument('--genes-file', dest = 'genes_file', help='path to the genes KO file', required=True)
    parser.add_argument('--file-type', dest='file_type', default='non-split', help='Either split or non-split. Default is non-split')

    return parser.parse_args()


class RunAnovaTests:

    def __init__(self, mutation_file, genes_file, file_type):
        self.mutation_file = mutation_file
        self.genes_file = genes_file
        self.file_type = file_type

    @property
    def mutation(self):
        print('parsing mutation file')
        muts = pd.read_csv(self.mutation_file, sep = '\t')
        if self.file_type == 'split':
            try:
                muts = muts.set_index('Model')
            except KeyError as e:
                print("Model doesn't appear to be a column in your data, try again!")
                raise e
        else:
            muts = muts.T
            muts.columns = muts.iloc[0]
            muts = muts.drop(muts.index[0])

        print('Done parsing mutation file')
        return muts
    
    @property
    def genes(self):
        print('parsing gene file')
        genes = pd.read_csv(self.genes_file, sep = '\t')
        genes = genes.set_index('Model')
        print('Done parsing gene file')
        return genes
    
    @property
    def mods_to_keep(self):
        mod_muts = list(self.mutation.index)
        mod_genes = list(self.genes.index) 
        mods_to_keep = list(set(mod_muts) & set(mod_genes))

        return mods_to_keep
    
    
    def run_anova(self):
        gene_KO = self.genes.loc[self.mods_to_keep, :]
        mut = self.mutation.loc[self.mods_to_keep, :]

        for gene in gene_KO:
    
            for m in mut:
                wt_mods = list(mut[mut[m] == 0].index)
                mnt_mods = list(mut[mut[m] == 1].index)

                data_wt = list(gene_KO.loc[wt_mods, gene])
                data_mnt = list(gene_KO.loc[mnt_mods, gene])

                stat, pval = f_oneway(data_mnt, data_wt)
                with open('{}_{}_anova.tsv'.format(gene, m), 'w') as f:
                    f.write('stat\tpval\n')
                    f.write('{stat}\t{pval}'.format(stat=stat,pval=pval))


    
if __name__ == '__main__':
    args = parse_args()
    test = RunAnovaTests(args.mutation_file, args.genes_file, args.file_type)
    test.run_anova()