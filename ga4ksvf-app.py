import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import os

# Initialize
root = tk.Tk()
root.title("GA4K SV Finder")
root.geometry("600x400")

dir_path = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(dir_path, '03182024-ga4k-sv.tsv')

dtype_spec = {
    'start': 'Int64',
    'end': 'Int64',
    'cohort_af': float,
    'amr_af': float,
    'eur_af': float,
}

data = pd.read_csv(data_file_path, delimiter='\t', dtype=dtype_spec)

accum_results = pd.DataFrame()

def parse_query(query):
    if ':' in query: 
        parts = query.split(':')
        chromosome = parts[0]
        start, end = map(int, parts[1].split('-'))
        return chromosome, start, end, None
    else:  # Gene name
        return None, None, None, query.upper()

def search_sv(query=None):
    global accum_results
    accum_results = pd.DataFrame()
    if not query:
        query = query_input.get().strip()
    if not query:
        messagebox.showwarning("Warning", "Please enter a query.")
        return

    chromosome, start, end, gene_name = parse_query(query)

    if gene_name is None:
        filt_data = data[(data['chrom'] == chromosome) & 
                         (data['start'] <= end) & 
                         (data['end'] >= start) & 
                         (data['cohort_af'] >= 0.004)]
    else:  # Gene search
        filt_data = data[(data['gene_name'].str.upper() == gene_name) & 
                         (data['cohort_af'] >= 0.004)]

    filt_data = filt_data.drop_duplicates()
    accum_results = pd.concat([accum_results, filt_data]).drop_duplicates().reset_index(drop=True)
    display_results()

def display_results():
    if not accum_results.empty:
        results_text.delete(1.0, tk.END)
        results_text.insert(tk.END, accum_results.to_string(index=False) + "\n\n")
    else:
        messagebox.showinfo("Search Results", "No SV found.")

def process_file_queries():
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

# GUI components setup
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
