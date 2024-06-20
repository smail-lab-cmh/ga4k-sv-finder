import argparse
import os
import pandas as pd

def load_data(filepath):
    data = pd.read_csv(filepath, delimiter='\t', skiprows=1, na_values='.')
    data.columns = ['Chrom', 'Start', 'End', 'Length', 'Type', 'CohortAlleleFreq', 'Homozygotes', 'VariantCount','CohortVariantFreq','GeneID', 'GeneName']
    numeric_cols = ['Start', 'End', 'CohortAlleleFreq', 'CohortVariantFreq']
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
    if gene_name == '':
        filt_data = data[(data['Chrom'] == chromosome) &
                         (data['Start'].astype('Int64') <= end) &
                         (data['End'].astype('Int64') >= start) &
                         (data['CohortVariantFreq'] >= 0.004)]
    else:
        filt_data = data[data['GeneName'].apply(lambda x: gene_name in [gene.strip().upper() for gene in x.split(',')] if isinstance(x, str) else False) &
                         (data['CohortVariantFreq'] >= 0.004)]

    filt_data = filt_data.drop_duplicates(subset=['Chrom', 'Start', 'End', 'Length', 'Type', 'GeneID', 'GeneName', 'CohortVariantFreq'])
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

def export_data(accumulated_results, export_filename, export_extension):
    if export_filename is not None:
        filepath = export_filename
        if export_extension is not None:
            filepath += f"{export_extension}"
        accumulated_results.to_csv(filepath, index=False)
        print(f"Data successfully exported to {filepath}")
    else:
        print("Export filename is missing. Results will not be exported.")


def main():
    parser = argparse.ArgumentParser(description='SV Analysis Tool')
    parser.add_argument('-f', '--file', help='Data file path.', required=True)
    parser.add_argument('-q', '--query', help='Single query string.')
    parser.add_argument('-qf', '--query-file', help='File containing queries, one per line.')
    parser.add_argument('-e', '--export-filename', help='Export filename (with or without extension).', default=None)
    args = parser.parse_args()

    if args.export_filename:
        export_filename, export_extension = os.path.splitext(args.export_filename)
    else:
        export_filename, export_extension = None, None
    
    data = load_data(args.file)
    accumulated_results = pd.DataFrame()

    if args.query:
        accumulated_results = search_sv(args.query, data, accumulated_results)
        print("Results for query:")
        display_results(accumulated_results)
        export_data(accumulated_results, export_filename, export_extension)
    elif args.query_file:
        process_file_queries(args.query_file, data, accumulated_results)
        print("Results for queries in file:")
        display_results(accumulated_results)
        export_data(accumulated_results, export_filename, export_extension)


if __name__ == "__main__":
    main()
