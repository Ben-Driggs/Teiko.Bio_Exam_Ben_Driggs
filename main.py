"""
"""

import os
import sys
import pandas as pd


def main():
    # save cell-count input file
    if len(sys.argv) != 2:
        cc_file = input("Expected one file name as a system argument, but none was provided.")
        sys.exit()
    else:
        cc_file = sys.argv[1]
    
    # read file into a dataframe
    try:
        cc_df = pd.read_csv(cc_file)
    except FileNotFoundError as e:
        print(f"Could not find the provided file: {cc_file}")
        print("Please check file path and try again.")
        sys.exit()
        
    # calculate total cell counts for each sample
    populations = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']
    cc_df['total_count'] = cc_df[populations].sum(axis=1)
    
    # initialize dataframe we will save sample cell count information in
    sample_df = pd.DataFrame()
    
    # add sample and total_count columns to output df
    sample_df['sample'] = [sample for sample in list(cc_df.loc[:, 'sample']) for _ in range(5)]
    sample_df['total_count'] = [count for count in list(cc_df.loc[:, 'total_count']) for _ in range(5)]
    
    # add populution column to output df
    sample_df['population'] = [pop for _ in range(len(cc_df['sample'])) for pop in populations]
    
    # add cell count column to output df
    sample_df['count'] = [cc_df.loc[sample, pop] for sample in range(len(cc_df.loc[:, 'sample'])) for pop in populations]
    
    # add percentage (relative frequency) column to output df
    sample_df['percentage'] = round(sample_df['count'] / sample_df['total_count'] * 100, 2)
    
    # output sample_df into a .csv file
    sample_df.to_csv("sample_cell_data.csv", sep=',', index=False)
    
    print(sample_df.head())


if __name__ == "__main__":
    main()
    