import sys

import pandas as pd
import matplotlib.pyplot as plt
from textwrap import fill
from scipy.stats import mannwhitneyu


def relative_frequency(output_path, cc_df):
    """
    Converts cell count in cell-count.csv to relative frequency (in percentage) of total cell count for each sample.
    Output saved as 'sample_cell_data.csv'.
    :param output_path: chosen by user, directs where any output files/directories will be stored
    :param cc_df: A pandas dataframe that contains the sample and cell count information from 'cell-count.csv'.
    :return: A pandas dataframe containing sample, total cell count, treatment response, treatment, population, cell count, and relative frequency information.
    """
    
    # calculate total cell counts for each sample
    populations = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']
    cc_df['total_count'] = cc_df[populations].sum(axis=1)
    
    # initialize dataframe we will save sample cell count information in
    sample_df = pd.DataFrame()
    
    # add sample and total_count columns to output df
    sample_df['sample'] = [sample for sample in list(cc_df.loc[:, 'sample']) for _ in range(5)]
    sample_df['total_count'] = [count for count in list(cc_df.loc[:, 'total_count']) for _ in range(5)]
    
    # add these columns for analysis
    columns = ['condition', 'treatment', 'response', 'sample_type']
    for c in columns:
        sample_df[c] = [r for r in list(cc_df.loc[:, c]) for _ in range(5)]
    
    # add populution column to output df
    sample_df['population'] = [pop for _ in range(len(cc_df['sample'])) for pop in populations]
    
    # add cell count column to output df
    sample_df['count'] = [cc_df.loc[sample, pop] for sample in range(len(cc_df.loc[:, 'sample'])) for pop in
                          populations]
    
    # add percentage (relative frequency) column to output df
    sample_df['percentage'] = round(sample_df['count'] / sample_df['total_count'] * 100, 2)
    
    # output sample_df into a .csv file
    # print(output_path + "\\data\\sample_cell_data.csv")
    outf = output_path + "\\sample_cell_data.csv"
    sample_df.to_csv(outf, sep=',', index=False)
    
    del cc_df
    return sample_df
    
    
def make_box_plots(output_path, sample_df):
    """
    Function will receive sample_df and create boxplots comparing the relative frequencies between responders and
    non-responders of tr1 for each population.
    :param output_path: chosen by user, directs where any output files/directories will be stored
    :param sample_df: sample_df containing sample, population, treatment, response, and relative frequency information for all treatments.
    """
    
    populations = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']
    
    # set up a subplot grid for the boxplots
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    axes = axes.flatten()
    plt.subplots_adjust(wspace=0.5, bottom=0.2, hspace=0.5)
    title = fill("Population Relative Frequencies Comparing Responders vs. Non-Responders", width=50)
    fig.suptitle(title, fontsize=14)
    
    # for each population, we want to make two boxplots, one for responders and one for non-responders.
    # Only include melanoma, with tr1 and PBMC blood samples.
    
    sample_df = sample_df[sample_df.loc[:, 'treatment'] == 'tr1']
    sample_df = sample_df[sample_df.loc[:, 'condition'] == "melanoma"]
    sample_df = sample_df[sample_df.loc[:, 'sample_type'] == "PBMC"]
    
    response_freqs = []
    no_response_freqs = []
    with open(output_path + "\\significance_tests.txt", 'w') as outf:
        for p in populations:
            # responders boxplot
            response = sample_df[(sample_df.loc[:, "population"] == p) & (sample_df.loc[:, "response"] == "y")]
            response_freqs.append(list(response.loc[:, 'percentage']))
            
            # non-responders boxplot
            no_response = sample_df[(sample_df.loc[:, "population"] == p) & (sample_df.loc[:, "response"] == "n")]
            no_response_freqs.append(list(no_response.loc[:, 'percentage']))
            
            # use Mann-Whiteny U test to calculate a p-value
            stat, p_value = mannwhitneyu(response.loc[:, 'percentage'], no_response.loc[:, 'percentage'])
            outf.write(f"Population: {p}\n")
            outf.write(f"Mann-Whitney U Test Score: {stat}\n")
            outf.write(f"P-value: {round(p_value, 5)}\n\n")
        
    # graph, format, and shos boxplots
    titles = ["Responders", "Non-Responders"]
    for i in range(len(populations)):
        axes[i].boxplot([response_freqs[i], no_response_freqs[i]], medianprops={"color": 'red', 'linewidth': 1})
        axes[i].set_ylabel("Relative Frequency %")
        axes[i].set_title(populations[i])
        axes[i].set_xticklabels(titles, ha='center')
        
    # remove blank plot and save figure
    axes[-1].axis('off')
    plt.savefig(output_path + "\\Relative_Frequency_Comparisons.png")
    

def main():
    """
    This main method will first attempt to retrieve the cell-count.csv file and stop the program if system arguments are not
    appropriately formated. The relative frequency cell count .csv file wiil
    then be created, followed by the relative
    frequency boxplots, comparisons, and statistics.
    """
    
    cc_file = "cell-count.csv"
    output_directory = input("Enter desired output folder path. Don't include // at the end: \n")
    
    # read file into a dataframe
    try:
        cc_df = pd.read_csv(cc_file)
    except FileNotFoundError:
        # Provide information about error and quit program
        print(f"Could not find the provided file: {cc_file}")
        input("Please check file path and try again.")
        sys.exit()
        
    try:
        # call function to create relative freqeuncy .csv output
        print("Calculating relative frequencies...")
        sample_df = relative_frequency(output_directory, cc_df)
        del cc_df
        
        # Make boxplots showing the population relative frequencies comparing responders vs. non-responders.
        # Run some statistics to see hich cell populations are significantly different in relative frequencies
        # between responders and non-responders.
        print("Creating boxplots and performing statistical analysis...")
        make_box_plots(output_directory, sample_df)
    except BaseException as e:
        input(f"The following error occured: \n{e}")
        sys.exit()


if __name__ == "__main__":
    main()
    print("Finished!")
    input("A data folder was created in your output directory. See contents for output files.")
    