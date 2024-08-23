#### Associated pre-print:
Mapping structural variants to rare disease genes using long-read whole genome sequencing and trait-relevant polygenic scores
Cas LeMaster, Carl Schwendinger-Schreck, Bing Ge, Warren A. Cheung, Rebecca McLennan, Jeffrey J. Johnston, Tomi Pastinen, Craig Smail
medRxiv 2024.03.15.24304216; doi: https://doi.org/10.1101/2024.03.15.24304216
### Changelog:
#### 08/23/2024 - 
Demographics have been added to the Additional Information section.  
We identified an issue with VariantCount and CohortVariantFreq in the SURVIVOR merged tsv where some counts were inflated due to parsing issues. We have replaced values in these columns with "NA" for the time being.  
#### 07/17/2024 -  
CohortAlleleFreq now reflects 4 decimal places instead of 3.
#### 06/20/2024 -  
Updated cohort size 497 samples > 1,566 samples.  
New tsv file offers SURVIVOR merged SV data as an optional input.  
Apps now have option to select data file for query (ie merged or unmerged).  
Command line tool has additional option flags (see below).  
Cohort information has been updated.  
#### 05/03/2024 -  
Amended end coordinate of insertion calls and overlapping gene IDs.  
#### 04/04/2024 -  
Re-uploaded raw data tsv.  
Included homozygote count.  
Updated cohort allele frequency (cohort_af) accuracy for observed genotypes.  
Removed frequencies for european (eur) and admixed american (amr) ancestries based on somalier probabilities.  
#### 04/01/2024 -  
We identified some issues with calculations in the tsv file and have removed the file until fixed. We will update with the corrected file soon.  

# GA4K SV Finder  
GA4K SV Finder is a tool to search for structural variants (SV) and associated genes from 1,566 individuals in the Genomics Answers for Kids (GA4K) cohort (2024) with HiFi long read genomes processed with PBSV (v2.6.2). Whether you're interested in specific genes, SV coordinates, variant frequencies, or a mix (query file), GA4K SV Finder provides a look into the GA4K rare disease cohort.


## File contents  
Column Names  
------------  
Chr - Chromosome location of the SV  
Start - Start coordinate of the SV  
End - End coordinate of the SV  
Length - Length of the SV  
Type - Type of the SV (DEL, DUP, INS, INV)  
CohortAlleleFreq - Allele frequency of SV in cohort population  
Homozygotes - Number of homozygotes for SV  
VariantCount - Count of individuals with SV  
CohortVariantFreq - Population frequency of SV (VariantCount / Cohort)  
GeneID - Ensemble gene ID for SV intersected genes  
GeneName - Gene name for SV intersected genes  

Additional information  
----------------------  
This data reflects long read HiFi WGS for 1,566 individuals in the Genomic Answers for Kids (GA4K) study.  
Sample sex summary: 777 males, 745 females, 17 unknowns  
Sample ancestry (somalier) summary: 1234 European, 239 Admixed American, 53 African, 23 South Asian, and 17 East Asian.  
All Structural variants were called with PBSV (v2.6.2) using reference genome GRCh38.  
Gene intersects were tested against all 19,291 protein coding genes from Gencode release v26 (GRCh38).  
The unmerged tsv only collapses identically called variants across individuals.  
The merged tsv data comes from a single merged VCF from all individuals using SURVIVOR (v1.0.7) merge options 1000 1 1 1 0 50 (max dist, callers, type specific, strand specific, disabled, min bp).  

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

### Example queries.txt content
chr3:179121491-179374301  
chr16:53841057-53841060  
chr9:121275764-121307053  
MFN1  
FTO  
GSN  

### Options
`python3 ga4ksvf-cmd.py [options]` 

- `-f FILE`, `--file FILE`: Process queries from a specified file.
- `-q`, `--query`: Query string. Either coordinate (chr:star-end), gene name (GENE1), or Ensembl gene ID (ENSG000).
- `-qf`, `--query-file`: File containing queries, one per line (see example in README).
- `-e`, `--export`: Export accumulated query results to a specified filename.ext.


