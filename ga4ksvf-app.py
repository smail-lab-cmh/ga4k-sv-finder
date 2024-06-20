import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import os

# Initialize
root = tk.Tk()
root.title("GA4K SV Finder")
root.geometry("1200x800")

data = None
accum_results = pd.DataFrame()

def load_data_file():
    global data
    filepath = filedialog.askopenfilename(title="Select Data File", filetypes=[("TSV Files", "*.tsv"), ("All Files", "*.*")])
    if filepath:
        dtype_spec = {
            'Start': 'Int64',
            'End': 'Int64',
            'CohortAlleleFreq': float,
            'Homozygotes': 'Int64',
            'VariantCount': 'Int64',
            'CohortVariantFreq': float
        }
        data = pd.read_csv(filepath, delimiter='\t', dtype=dtype_spec)
        data.columns = ['Chrom', 'Start', 'End', 'Length', 'Type', 'CohortAlleleFreq', 'Homozygotes', 'VariantCount', 'CohortVariantFreq', 'GeneID', 'GeneName']
        numeric_cols = ['Start', 'End', 'CohortAlleleFreq', 'CohortVariantFreq']
        data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors='coerce')
        data['GeneID'] = data['GeneID'].astype(str)
        data['GeneName'] = data['GeneName'].astype(str)
        data['CohortVariantFreq'] = pd.to_numeric(data['CohortVariantFreq'], errors='coerce').fillna(0)

        messagebox.showinfo("Data File", f"Data file loaded successfully: {os.path.basename(filepath)}")
        print(data.head())  # Print first few rows to verify data

def parse_query(query):
    if ':' in query:
        parts = query.split(':')
        chromosome = parts[0]
        start, end = map(int, parts[1].split('-'))
        return chromosome, start, end, None
    else:  # Gene name or Gene ID
        return None, None, None, query.upper()

def search_sv(query=None):
    global accum_results
    accum_results = pd.DataFrame()  # Reset accum_results to empty DataFrame
    if data is None:
        messagebox.showwarning("Warning", "Please load a data file first.")
        return
    if not query:
        query = query_input.get().strip()
    if not query:
        messagebox.showwarning("Warning", "Please enter a query.")
        return

    chromosome, start, end, gene_name = parse_query(query)
    
    print(f"Searching for query: {query}")
    print(f"Parsed query - Chromosome: {chromosome}, Start: {start}, End: {end}, Gene name/ID: {gene_name}")

    if gene_name is None:
        filt_data = data[(data['Chrom'] == chromosome) & 
                         (data['Start'] <= end) & 
                         (data['End'] >= start) & 
                         (data['CohortVariantFreq'] >= 0.004)]
        print(f"Filtering by chromosomal range - Rows found: {len(filt_data)}")
    else:
        filt_data = data[(data['GeneName'].str.split(', ').apply(lambda x: gene_name in x) | 
                          data['GeneID'].str.split(', ').apply(lambda x: gene_name in x)) & 
                         (data['CohortVariantFreq'] >= 0.004)]
        print(f"Filtering by gene name/ID - Rows found: {len(filt_data)}")

    accum_results = pd.concat([accum_results, filt_data]).reset_index(drop=True)
    display_results()

def display_results():
    if not accum_results.empty:
        results_text.delete(1.0, tk.END)
        results_text.insert(tk.END, accum_results.to_string(index=False) + "\n\n")
    else:
        messagebox.showinfo("Search Results", "No SV found.")

def process_file_queries():
    if data is None:
        messagebox.showwarning("Warning", "Please load a data file first.")
        return
    filepath = filedialog.askopenfilename(title="Select Query File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    search_sv(line)

def export_data():
    filepath = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
    if filepath:
        accum_results.to_csv(filepath, index=False)
        messagebox.showinfo("Export", f"Data successfully exported to {filepath}")

load_data_button = tk.Button(root, text="Load Data File", command=load_data_file)
load_data_button.pack(pady=(10, 10))

query_label = tk.Label(root, text="Enter Query (e.g., chr3:179121491-179374301 or ASTN1):")
query_label.pack(pady=(10, 0))

query_input = tk.Entry(root)
query_input.pack(padx=20, pady=10, fill=tk.X)

search_button = tk.Button(root, text="Search", command=lambda: search_sv())
search_button.pack(pady=(0, 10))

file_query_button = tk.Button(root, text="Select Query File", command=process_file_queries)
file_query_button.pack(pady=(0, 10))

export_button = tk.Button(root, text="Export Results", command=export_data)
export_button.pack(pady=(0, 20))

results_label = tk.Label(root, text="Results:")
results_label.pack(pady=(10, 0))

results_text = tk.Text(root, height=10)
results_text.pack(padx=20, pady=(0, 10), fill=tk.BOTH, expand=True)

root.mainloop()
