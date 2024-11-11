import argparse

def parse_args():
    """
    Parser of app for calculating basic statistics about the proteins

    """
    parser = argparse.ArgumentParser(description="Arguments for the app for calculating basic statistics about the proteins")

# Add arguments
    parser.add_argument("abundance_file", type=str, help="Path to the input abundance file")
    parser.add_argument("domain_file", type=str, help="Path to the domain file")
    parser.add_argument("--column_avg_abdn_name", type=str, help="Column where protein average abundances are stored")
    parser.add_argument("--column_domain_name", type=str, default='Domain', help="Column where protein domains are stored")
    parser.add_argument("--prefix", type=str, default='test', help="String value for naming output files")
    parser.add_argument("--eval_column", type=str, default='Eval', help="Column with E values in domains file")
    parser.add_argument("--save_outputs", action='store_true', help="Save output files")
    parser.add_argument("--separator", type=str, default='\t' ,help="Column separator for abundance and domain file. When specyfying separator \
                        values it is mandatory to add quotes")
    parser.add_argument("--merging_column", default='Gn', type=str, help="Column which will be used to merge abundance and domain file")
    args = parser.parse_args()
    return (args)
