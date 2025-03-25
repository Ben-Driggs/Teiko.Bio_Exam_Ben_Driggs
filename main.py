import sys
print(sys.executable)
import pandas as pd
import matplotlib.pyplot as plt


def relative_frequency(cc_df):
    """
    Converts cell count in cell-count.csv to relative frequency (in percentage) of total cell count for each sample.
    Output saved as 'sample_cell_data.csv'.
    :param cc_df: A pandas dataframe that contatins the sample and cell count information from 'cell-count.csv'.
    """
    
    # calculate total cell counts for each sample
    populations = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']
    cc_df['total_count'] = cc_df[populations].sum(axis=1)
    
    # initialize dataframe we will save sample cell count information in
    sample_df = pd.DataFrame()
    
    # add sample and total_count columns to output df
    sample_df['sample'] = [sample for sample in list(cc_df.loc[:, 'sample']) for _ in range(5)]
    sample_df['total_count'] = [count for count in list(cc_df.loc[:, 'total_count']) for _ in range(5)]
    
    # add response column for boxplots
    sample_df['response'] = [r for r in list(cc_df.loc[:, 'response']) for _ in range(5)]
    
    # add populution column to output df
    sample_df['population'] = [pop for _ in range(len(cc_df['sample'])) for pop in populations]
    
    # add cell count column to output df
    sample_df['count'] = [cc_df.loc[sample, pop] for sample in range(len(cc_df.loc[:, 'sample'])) for pop in
                          populations]
    
    # add percentage (relative frequency) column to output df
    sample_df['percentage'] = round(sample_df['count'] / sample_df['total_count'] * 100, 2)
    
    # output sample_df into a .csv file
    outf = "sample_cell_data.csv"
    sample_df.to_csv(outf, sep=',', index=False)
    
    return cc_df, sample_df
    
    
def make_box_plots(cc_df, sample_df):
    populations = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']
    
    # for each population, we want to make two boxplots, one for responders and one for non-responders.
    # We won't include any data with samples that have nan for the response
    plt.boxplot([1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 3, 4, 5, 2, 3])
    plt.show()
    
    print()


def main():
    """
    This main method will first attempt to retrieve the cell-count.csv file and stop the program if system arguments are not
    appropriately formated. The relative frequency cell count .csv file wiil then be created, followed by the relative
    frequency boxplots, comparisons, and statistics.
    """
    
    # save cell-count input file
    if len(sys.argv) != 2:
        # check for correct number of system arguments and quit if too few or too many are found.
        cc_file = input("Expected one file name as a system argument, but none was provided.")
        sys.exit()
    else:
        # save file path
        cc_file = sys.argv[1]
    
    # read file into a dataframe
    try:
        cc_df = pd.read_csv(cc_file)
    except FileNotFoundError as e:
        # Provide information about error and quit program
        print(f"Could not find the provided file: {cc_file}")
        print("Please check file path and try again.")
        sys.exit()
        
    # call function to create relative freqeuncy .csv output
    cc_df, sample_df = relative_frequency(cc_df)
    
    # make boxplots showing the population relative frequencies comparing responders vs. non-responders
    make_box_plots(cc_df, sample_df)


if __name__ == "__main__":
    main()
    