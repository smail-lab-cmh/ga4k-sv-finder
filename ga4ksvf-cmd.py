import argparse
import os
import pandas as pd

def load_data(filepath):
    data = pd.read_csv(filepath, delimiter='\t', skiprows=1, na_values='.')
    data.columns = ['Chrom', 'Start', 'End', 'Length', 'Type', 'cohort_af', 'Homozygotes', 'GeneID', 'GeneName', 'cohort_freq']
    numeric_cols = ['Start', 'End', 'cohort_af', 'cohort_freq']
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    data[['Start', 'End']] = data[['Start', 'End']].astype('Int64')
    return data

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
        filt_data = data[(data['Chrom'] == chromosome) &
                         (data['Start'].astype('Int64') <= end) &
                         (data['End'].astype('Int64') >= start) &
                         (data['cohort_freq'] >= 0.004)]
    else:
        filt_data = data[data['GeneName'].apply(lambda x: gene_name in [gene.strip().upper() for gene in x.split(',')] if isinstance(x, str) else False) &
                         (data['cohort_freq'] >= 0.004)]

    filt_data = filt_data.drop_duplicates(subset=['Chrom', 'Start', 'End', 'Length', 'Type', 'GeneID', 'GeneName', 'cohort_freq'])
    accumulated_results = pd.concat([accumulated_results, filt_data]).drop_duplicates().reset_index(drop=True)
    return accumulated_results


def display_results(accumulated_results):
    if not accumulated_results.empty:
        print(accumulated_results.to_string(index=False) + "\n")
    else:
        print("No results found.\n")

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
    data_file_path = os.path.join(dir_path, '04042024-ga4k-af.tsv')
    data = load_data(data_file_path)

    if args.file:
        accumulated_results = pd.DataFrame()
        process_file_queries(args.file, data, accumulated_results)
        if args.export:
            export_data(accumulated_results)
    else:
        while True:
            query = input("Enter your query (or type 'exit' to quit): ").strip()
            if query.lower() == 'exit':
                break
            if query:
                accumulated_results = pd.DataFrame()  # Reset for each query
                accumulated_results = search_sv(query, data, accumulated_results)
                display_results(accumulated_results)
            if args.export:
                export_data(accumulated_results)
                break


if __name__ == "__main__":
    main()
