import pandas as pd
from pars_args import parse_args

pd.set_option('colheader_justify', 'center')
args = parse_args()

def unique_means(abund_file, separator, col_prot_num_values):

    """
    This function will calculate the following things:
        1. The unique protein/copy-number values in the abundance file 
        2. The mean and standard deviation of copy numbers for all unique proteins
        3. The percentile rank for each protein 
    """

    # Load abundance file 
    data_frame = pd.read_csv(abund_file, sep=separator)
    # Filter data frame from rows which do not have numeric column for protein copy number values
    data_frame.columns = data_frame.columns.str.lstrip('#')
    data_frame[col_prot_num_values] = pd.to_numeric(data_frame[col_prot_num_values], errors = 'coerce')
    filtered_na = data_frame.dropna(subset=[col_prot_num_values]) 

    # Get the number of unique copy number values
    unique_copy_number_values = pd.Series.unique(filtered_na[col_prot_num_values])
    number_unique_copy_number_values = f"Number of unique protein/copy-number values is: {len(unique_copy_number_values)}"
    
    # Remove rows which has zero value for protein copy number values. 
    remove_zeros = filtered_na.loc[filtered_na[col_prot_num_values] > 0 ]
    unique_without_zeros = pd.Series.unique(remove_zeros[col_prot_num_values])

    # Calculate the mean and standard deviation for protein which has unique value of protein copy number column
    mean = unique_without_zeros.mean()
    stdev = unique_without_zeros.std()
    table_mean_stdev = pd.DataFrame({'Mean':[mean], 'Standard_deviation': [stdev]})

    # Drop duplicated rows from the data frame 
    df_rank = remove_zeros.drop_duplicates()

    # Sort dataframe according to the values of protein copy number column
    df_rank = df_rank.sort_values(col_prot_num_values)

    # Rank the proteins according to the value in the protein copy number column

    df_rank['Rank'] = df_rank[col_prot_num_values].rank(pct=True)    

    return (number_unique_copy_number_values, table_mean_stdev, df_rank)

def protein_domains (file, separator, domain_col):

    """
    The function which will calculate the most abundant protein domain.
    """
    
    # Load abundance file 
    data_frame = pd.read_csv(file, sep=separator)

    # Discard rows which have the same value for the below-mentioned columns. 
    data_frame.columns = data_frame.columns.str.lstrip('#')
    df_unique = data_frame.drop_duplicates(subset=['Gn', domain_col, 'Start', 'End'], keep='first')

    # Calculate domain with the highest average abundance
    highest_abundance = df_unique[domain_col].mode()
    most_abundant_domain = f"The highest abundant protein domain is: {highest_abundance[0]}"
    return (most_abundant_domain)

def domain_statistics(abund_file, domain_file, separator, merging_column, eval_column, avg_abundance_column, column_domain_name):

    """
    The function which will mean, standard deviation and ranks for the protein domains.
    """

    # Load abundance file 
    abundance_df = pd.read_csv(abund_file, sep=separator)

    # Filter abundance file 
    abundance_df.columns = abundance_df.columns.str.lstrip('#')
    abundance_df['Mean-copy-number'] = pd.to_numeric(abundance_df['Mean-copy-number'], errors = 'coerce')
    dropna_abundance_df = abundance_df.dropna(subset=['Mean-copy-number'])
    remove_zeros_abundance_df = dropna_abundance_df.loc[dropna_abundance_df['Mean-copy-number'] > 0 ]
    remove_duplicates_abundance_df = remove_zeros_abundance_df.drop_duplicates()      

    # Load domain file 
    domain_df = pd.read_csv(domain_file, sep=separator)

    # Filter domain file according to Eval and length of the domain
    domain_df.columns = domain_df.columns.str.lstrip('#')
    domain_df['Score_diff'] = domain_df['End'].sub(domain_df['Start'], axis = 0)
    remove_short_domains = domain_df[(domain_df['Score_diff'] > 20) & (domain_df[eval_column] < 0.001)]

    # Merge data on 'Gn' (gene name) column
    merged_df = pd.merge(remove_short_domains, remove_duplicates_abundance_df, on=merging_column)

    # Calculate mean and standard deviation of domain average abundance for each domain
    domain_stats = merged_df.groupby(column_domain_name)[avg_abundance_column].agg(['mean', 'std']).reset_index()

    # As the stdev value can be NA if the domain is present only in one protein we will replace NA values with 0 
    domain_stats['std'] = domain_stats['std'].fillna(0)
    
    # Calculate percentile rank for each domain abundance within its domain
    domain_stats_ranked = domain_stats.sort_values('mean')
    domain_stats_ranked['Rank'] = domain_stats_ranked['mean'].rank(pct=True) 

    return (domain_stats, domain_stats_ranked)

def save_results(prefix='test'):

    # Call the function and get the tuple
    result_A_task = unique_means(args.abundance_file, args.separator, args.column_avg_abdn_name)
    result_B1_task = protein_domains (args.domain_file, args.separator, args.column_domain_name)
    result_B2_task = domain_statistics(args.abundance_file, args.domain_file, args.separator, args.merging_column, args.eval_column, args.column_avg_abdn_name, args.column_domain_name)
    
    # Extract the results
    number_of_unique = result_A_task[0]
    table_mean_stdev = result_A_task[1]
    ranked_table = result_A_task[2]
    most_abundant_domain = result_B1_task
    table_mean_stdev_domains = result_B2_task[0]
    ranked_table_domains = result_B2_task[1]

    # Write results in CSV (tables) or TXT (single values) file 
    table_mean_stdev.to_csv(prefix + "_table_mean_stdev.csv", index=False)
    ranked_table.to_csv(prefix + "_ranked_table.csv", index=False)
    table_mean_stdev_domains.to_csv(prefix + "_table_mean_stdev_domains.csv", index=False)
    ranked_table_domains.to_csv(prefix + "_ranked_table_domains.csv", index=False)
    
    with open(prefix + "_single_values.txt", "w") as text_file:
        text_file.write(f"{number_of_unique}\n")
        text_file.write(f"{most_abundant_domain}\n")

save_results(args.prefix)