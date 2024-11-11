# Basic protein analysis

These scripts will be used to calculate basic protein statistics from the provided files. Also, it can be used to make interactive HTML file where the user can get basic protein statistics metrics.
It is used to calculate the following things:
  1. Number of unique protein/copy-number values in the dataset.
  2. Mean and standard deviation of copy numbers for all unique proteins in the dataset.
  3. Percentile ranks for each protein based of copy number values in the dataset.
  4. Domain with the highest average abundance in the dataset.
  5. Mean and standard deviation of domain average abundance for each protein domain in the dataset.
  6. Percentile ranks for mean of domain average abundance for each protein domain in the dataset.

## Prerequisites

In order to run these scripts you should install the following packages/modules:
* **Python/Python3**
* **pandas**
* **flask**

## Get stared 

The analysis can be run in a two ways:
  1. Only generating results of the analysis
     * `python3 basic_statistics.py 9606_abund.txt 9606_gn_dom.txt --column_avg_abdn_name Mean-copy-number --column_domain_name Domain --separator '\t' --merging_column Gn --eval_column Eval --prefix test_1`
  2. Generating interactive HTML file where the user can get basic protein statistics metrics
     * `python3 html_flask_calculate.py 9606_abund.txt 9606_gn_dom.txt --column_avg_abdn_name Mean-copy-number --column_domain_name Domain --separator '\t' --merging_column Gn --eval_column Eval --prefix test_2`

* `basic_statistics.py` - Script that is used to calculate the basic protein statistics metrics for the dataset
* `html_flask_calculate.py` - Script that is used to make interactive HTML where the user can get basic protein statistics metrics.
* `9606_abund.txt` - A file which contains a roughly measures of the average amount of each protein in a typical human cell.
* `9606_gn_dom.txt` - A file which specifies, for each protein (Gn column) each domain (Domain column) that is present inside it. It is important to mention that file has to contain **Start** and **End** columns which marks the position of the domains in proteins.
* `--column_avg_abdn_name` - A name of column in abundance file which specifies for the average amount of each protein in a typical human cell.
* `--column_domain_name` - A name of column which specifies protein domain names in domain file (default: Domen).
* `--separator` - A value which is used in abundance and domain files to separate columns (default: '\t').
* `--merging_column` - A name of column common for both files and which will be used to merge files. The merging is performed in order to calculate values for domain average abundance for each protein domain (default:Gn).
* `--eval_column` - A name of column in domain file where E values for protein domains are specified. This column is important for filtering protein domains according to E values (defaul:Eval).
* `--prefix` - A string value that will be used to name output files (default: test).

## Outputs

The outputs of these scripts are as follows:
* **Single values** - a TXT file which contains number of unique protein/copy-number values and domain with the highest average abundance in the dataset.
* **Mean and stdev table** - a CSV file which contains mean and standard deviation of copy numbers for all unique proteins in the dataset.
* **Ranked table** - a CSV file which contains percentile ranks for each protein based of copy number values in the dataset.
* **Mean and stdev table for domains** - a CSV file which contains mean and standard deviation of domain average abundance for each protein domain in the dataset.
* **Ranked table for domains** - a CSV file which contains percentile ranks for mean of domain average abundance for each protein domain in the dataset.
