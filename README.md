# GA4K SV Finder
GA4K SV Finder is a tool to search for structural variations (SV) and associated genes from 497 probands in the Genomics Answers for Kids (GA4K) cohort (2023) with HiFi long read genomes processed with PBSV (v2.6.2). Whether you're interested in specific genes, SV coordinates, allele frequencies, or a mix (query file), GA4K SV Finder provides a look into the GA4K rare disease cohort.

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

## Command Line Usage
GA4K SV Finder supports three modes of operation  

### For Genes
To search for a specific gene, use:  

`python3 script.py GENENAME`  

### For Coordinates
To search by genomic coordinates:  

`python3 script.py chr3:179121491-179374301`

### For Query Files
To run multiple queries from a file:  

`python3 script.py -f queries.txt`  

### Example queries.txt content:
chr3:179121491-179374301  
chr16:53841057-53841060  
chr9:121275764-121307053  
MFN1  
FTO  
GSN  
