import pandas as pd
import os
import sys

dir_path = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(dir_path, '01082024-ga4k-sv.tsv')

column_names = ['chr', 'start', 'end', 'length', 'type', 'overlap-gene-id', 'overlap-gene-name', 'frequency']
data = pd.read_csv(data_file_path, delimiter='\t', names=column_names)

data['start'] = pd.to_numeric(data['start'], errors='coerce')
data['end'] = pd.to_numeric(data['end'], errors='coerce')

accumulated_results = pd.DataFrame()

def parse_query(query):
    if ':' in query:
        parts = query.split(':')
        chromosome = parts[0]
        start, end = map(int, parts[1].split('-'))
        return chromosome, start, end, None
    else: 
        return None, None, None, query.upper()

def search_sv(query=None):
    global accumulated_results
    if query is None:
        print("Please provide a query.")
        return
    chromosome, start, end, gene_name = parse_query(query)

    if gene_name is None: 
        filt_data = data[(data['chr'] == chromosome) &
                         (data['start'] <= end) &
                         (data['end'] >= start) &
                         (data['frequency'] > 0.004)]
    else:
        filt_data = data[(data['overlap-gene-name'].str.upper() == gene_name) &
                         (data['frequency'] > 0.004)]
    filt_data = filt_data.drop_duplicates(subset=['chr', 'start', 'end', 'length', 'type', 'overlap-gene-id', 'overlap-gene-name', 'frequency'])
    accumulated_results = pd.concat([accumulated_results, filt_data]).drop_duplicates().reset_index(drop=True)

def display_results():
    global accumulated_results
    if not accumulated_results.empty:
        print(accumulated_results.to_string(index=False) + "\n")

def close_results():
    global accumulated_results
    accumulated_results = pd.DataFrame()

def process_file_queries(filepath=None):
    if not filepath:
        print("Please provide a filepath to a query file.")
        return
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                search_sv(line)
    display_results()

def export_data(accum_data):
    filepath = input("Enter the filepath to save the data (default: result.csv): ")
    if not filepath:
        filepath = "result.csv"
    accum_data.to_csv(filepath, index=False)
    print("Data successfully exported to {}".format(filepath))

if len(sys.argv) > 1:
    query = " ".join(sys.argv[1:])
    search_sv(query)
    display_results()
else:
    print("Usage: python script.py [query] [options]")
    print("Options:")
    print("  -f, --file     Process queries from a file")
    print("  -e, --export   Export data to a CSV file")
