import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import os
import sys

result_window = None
result_text = None
accum_results = pd.DataFrame()

#packaging the data file with the application (make sure the datafile in same directory as script)
dir_path = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(dir_path, '01082024-ga4k-sv.tsv')

#load it up
column_names = ['chr', 'start', 'end', 'length', 'type', 'overlap-gene-id', 'overlap-gene-name', 'frequency']
data = pd.read_csv(data_file_path, delimiter='\t', names=column_names)

#turn columns 2 and 3 to integers
data['start'] = pd.to_numeric(data['start'], errors='coerce')
data['end'] = pd.to_numeric(data['end'], errors='coerce')

#window
root = tk.Tk()
root.title("GA4K SV Finder")
label = tk.Label(root, text="Enter Query \n (e.g., chr3:179121491-179374301):")
label.pack()
query_input = tk.Entry(root)
query_input.pack()

def parse_query(query):
    if ':' in query:  #coordinate-based query
        parts = query.split(':')
        chromosome = parts[0]
        start, end = map(int, parts[1].split('-'))
        return chromosome, start, end, None
    else:  # Gene name
        return None, None, None, query.upper()

def search_sv(query=None):
    global accum_results
    if query is None:
        query = query_input.get()
    chromosome, start, end, gene_name = parse_query(query)

    if gene_name is None:  #coordinate-based search
        filt_data = data[(data['chr'] == chromosome) &
                         (data['start'] <= end) &
                         (data['end'] >= start) &
                         (data['frequency'] > 0.004)]
    else:  #gene search
        filt_data = data[(data['overlap-gene-name'].str.upper() == gene_name) &
                         (data['frequency'] > 0.004)]
    filt_data = filt_data.drop_duplicates(subset=['chr', 'start', 'end', 'length', 'type', 'overlap-gene-id', 'overlap-gene-name', 'frequency'])
    #appending and accumulating the results
    accum_results = pd.concat([accum_results, filt_data]).drop_duplicates().reset_index(drop=True)

def display_results():
    global result_window, result_text, accum_results
    if not accum_results.empty:
        if not result_window:
            create_results_window()
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, accum_results.to_string(index=False) + "\n\n")
    else:
        messagebox.showinfo("Search Results", "No SV found")

def create_results_window():
    global result_window, result_text
    result_window = tk.Toplevel(root)
    result_window.title("Results")
    scrollbar = tk.Scrollbar(result_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    result_text = tk.Text(result_window, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    result_text.pack(padx=10, pady=10, expand=True, fill='both')
    scrollbar.config(command=result_text.yview)
    export_button = tk.Button(result_window, text="Export", command=lambda: export_data(accum_results))
    export_button.pack(side=tk.LEFT, padx=10, pady=10)
    exit_button = tk.Button(result_window, text="Close", command=lambda: close_results_window())
    exit_button.pack(pady=10)

def close_results_window():
    global result_window, result_text, accum_results
    if result_window:
        result_window.destroy()
        result_window = None
        result_text = None
    accum_results = pd.DataFrame()

def process_file_queries(filepath=None):
    if not filepath:
        filepath = filedialog.askopenfilename(title="Select Query File",
                                              filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not filepath:
            return
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                search_sv(line)
    display_results()

def export_data(accum_data):
    filepath = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
    if filepath:
        accum_data.to_csv(filepath, index=False)
        messagebox.showinfo("Export", f"Data successfully exported to {filepath}")
#buttons!
search_button = tk.Button(root, text="Search", command=lambda: [search_sv(None), display_results()])
search_button.pack()
select_file_button = tk.Button(root, text="Select Query File", command=process_file_queries)
select_file_button.pack()

root.mainloop()