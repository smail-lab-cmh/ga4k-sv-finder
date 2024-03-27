# GA4K SV Finder
GA4K SV Finder is a tool to search for structural variations (SV) and associated genes from 497 probands in the Genomics Answers for Kids (GA4K) cohort (2023) with HiFi long read genomes processed with PBSV (v2.6.2). Whether you're interested in specific genes, SV coordinates, variant frequencies, or a mix (query file), GA4K SV Finder provides a look into the GA4K rare disease cohort.

Note: SVs were aligned using human genome reference hg38. Cohort alleles with frequencies that would identify a single person have been excluded. Additionally, frequencies for european (eur) and admixed american (amr) ancestries are provided based on somalier probabilities (https://github.com/brentp/somalier).

## Dependencies
- Python 3.7 or higher
- Tkinter (usually comes with Python)
- Pandas

## Installation
## Python Installation
### For Linux (Debian/Ubuntu)
`sudo apt update`  
`sudo apt install python3`

### For Linux (CentOS/Red Hat)
`sudo dnf install python3`  

### For MacOS
`brew install python`  

## Pandas Installation
After installing Python, you can install Pandas using pip:  

`pip install pandas`  

## Application Usage
Navigate the command line to the directory where you have downloaded the raw data tsv and ga4ksvf-app.py (`cd path/to/your/download`)

Execute the following command:
`python3 ga4ksvf-app.py`

## Command Line Usage
GA4K SV Finder supports three modes of operation.
Navigate the command line to the directory where you have downloaded the raw data tsv and ga4ksvf-cmd.py (`cd path/to/your/download`)

### Genes
To search for a specific gene, use:  

`python3 ga4ksvf-cmd.py GENENAME`  

### Coordinates
To search by genomic coordinates:  

`python3 ga4ksvf-cmd.py chr3:179121491-179374301`  

### Query Files (Both)
To run multiple queries from a file:  

`python3 ga4ksvf-cmd.py [options]` 

- `-f FILE`, `--file FILE`: Process queries from a specified file.
- `-e`, `--export`: Export accumulated query results to a CSV file. Prompts for a file name, defaulting to `result.csv`.

### Interactive Mode

If the script is run without any arguments, it enters interactive mode. In this mode, you can input queries directly into the terminal. Type 'exit' to quit the interactive mode.
`python3 ga4ksvf-cmd.py`

### Example queries.txt content:
chr3:179121491-179374301  
chr16:53841057-53841060  
chr9:121275764-121307053  
MFN1  
FTO  
GSN  
