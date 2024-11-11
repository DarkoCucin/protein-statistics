from flask import Flask, render_template, request
from basic_statistics import unique_means,protein_domains,domain_statistics
from pars_args import parse_args

args = parse_args()

# Variable for new object that inherits from the class Flask
app = Flask(__name__)

def calculate_A1(file, separator, col_name):
    results = unique_means(file, separator, col_name)
    return results[0]

def calculate_A2(file, separator, col_name):
    results = unique_means(file, separator, col_name)
    return results[1].to_html(index=False)

def calculate_A3(file, separator, col_name):
    results = unique_means(file, separator, col_name)
    return results[2].to_html(index=False)

def calculate_B1(file, separator, domain_col):
    results = protein_domains(file, separator, domain_col)
    return results

def calculate_B2(abund_file, domain_file, separator, merging_column, eval_column, avg_abundance_column, column_domain_name):
    results = domain_statistics(abund_file, domain_file, separator, merging_column, eval_column , avg_abundance_column, column_domain_name)
    return (results[0].to_html(index=False),results[1].to_html(index=False))

@app.route('/')

def home():
    return render_template('index.html')

# Define the button which will be used to calculate results 
@app.route('/calculate', methods=['POST'])

def calculate():
    # Determine which button was clicked based on the button name
    question = request.form.get('question')

    # Call the appropriate function based on the question
    if question == 'A1':
        answer = calculate_A1(args.abundance_file, args.separator, args.column_avg_abdn_name)
    elif question == 'A2':
        answer = calculate_A2(args.abundance_file, args.separator, args.column_avg_abdn_name)
    elif question == 'A3':
        answer = calculate_A3(args.abundance_file, args.separator, args.column_avg_abdn_name)
    elif question == 'B1':
        answer = calculate_B1(args.domain_file, args.separator, args.column_domain_name)
    elif question == 'B2':
        answer = calculate_B2(args.abundance_file, args.domain_file, args.separator, args.merging_column, args.eval_column, args.column_avg_abdn_name, args.column_domain_name)
    else:
        answer = "Invalid question"

    # Return the main page with the result displayed
    return render_template('index.html', question=question, answer=answer)

if __name__ == '__main__':
    app.run(debug=True)