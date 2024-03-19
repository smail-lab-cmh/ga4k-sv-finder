import argparse
import os
import pandas as pd

def parse_query(query):
    if ':' in query:
        parts = query.split(':')
        chromosome = parts[0]
        start_end = parts[1].split('-')
        start, end = int(start_end[0]), int(start_end[1])
        return chromosome, start, end, None
    else:
        return None, None, None, query.upper()

def search_sv(query, data, accumulated_results):
    chromosome, start, end, gene_name = parse_query(query)
    if gene_name is None:
        filt_data = data[(data['chr'] == chromosome) &
                         (data['start'] <= end) &
                         (data['end'] >= start) &
                         (data['cohort-af'] >= 0.004)]
    else:
        filt_data = data[(data['overlap-gene-name'].str.upper() == gene_name) &
                         (data['cohort-af'] >= 0.004)]
    filt_data = filt_data.drop_duplicates(subset=['chr', 'start', 'end', 'length', 'type', 'overlap-gene-id', 'overlap-gene-name', 'cohort-af', 'amr-af', 'eur-af'])
    accumulated_results = pd.concat([accumulated_results, filt_data]).drop_duplicates().reset_index(drop=True)
    return accumulated_results

def load_data(filepath):
    dtype_spec = {
        'cohort-af': float,
        'amr-af': float,
        'eur-af': float
    }
    column_names = ['chr', 'start', 'end', 'length', 'type', 'overlap-gene-id', 'overlap-gene-name', 'cohort-af', 'amr-af', 'eur-af']
    data = pd.read_csv(filepath, delimiter='\t', names=column_names, dtype=dtype_spec, skiprows=1)
    
    data['start'] = pd.to_numeric(data['start'], errors='coerce').astype('Int64')
    data['end'] = pd.to_numeric(data['end'], errors='coerce').astype('Int64')
    
    return data

def display_results(accumulated_results):
    if not accumulated_results.empty:
        print(accumulated_results.to_string(index=False) + "\n")

def process_file_queries(filepath, data, accumulated_results):
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                accumulated_results = search_sv(line, data, accumulated_results)
    display_results(accumulated_results)

def export_data(accumulated_results):
    filepath = input("Enter the filepath to save the data (default: result.csv): ")
    if not filepath:
        filepath = "result.csv"
    accumulated_results.to_csv(filepath, index=False)
    print(f"Data successfully exported to {filepath}")

def main():
    parser = argparse.ArgumentParser(description='SV Analysis Tool')
    parser.add_argument('-f', '--file', help='Process queries from a file.', type=str)
    parser.add_argument('-e', '--export', help='Export data to a CSV file.', action='store_true')
    args = parser.parse_args()

    dir_path = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(dir_path, '03182024-ga4k-sv.tsv')
    data = load_data(data_file_path)

    accumulated_results = pd.DataFrame()

    if args.file:
        process_file_queries(args.file, data, accumulated_results)
        if args.export:
            export_data(accumulated_results)
    else:
        while True:
            query = input("Enter your query (or type 'exit' to quit): ").strip()
            if query.lower() == 'exit':
                break
            if query:
                accumulated_results = search_sv(query, data, accumulated_results)
                display_results(accumulated_results)
            if args.export:
                export_data(accumulated_results)
                break

if __name__ == "__main__":
    main()
