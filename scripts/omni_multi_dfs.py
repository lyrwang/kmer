import yaml
import pandas as pd
import numpy as np
from kmerprediction import constants

def main():
    num_rows = snakemake.config['reps'] * len(snakemake.input)
    cols = ['Model', 'Datatype', 'Kmer Length', 'Kmer Filter',
            'Selection', 'Prediction', 'Accuracy']
    output_df = pd.DataFrame(columns=cols, index=np.arange(num_rows))

    count = 0
    for yf in snakemake.input:
        info = convert_filepath(yf)
        with open(yf, 'r') as f:
            data = yaml.load(f)
            acc = data['output']['results']
            for a in acc:
                curr_row = [info['model'], info['datatype'], info['k'],
                            info['filter'], info['selection'], info['prediction'], a]
                output_df.loc[count] = curr_row
                count += 1
    output_df.to_csv(snakemake.output[0], index=False, sep=',')

if __name__ == "__main__":
    main()
