import pandas as pd
import yaml
import subprocess
from Bio import SeqIO

config_path = "/Users/MiladM-Dev/Documents/1PhD/project-1-N450/project-1.1-Data-desc/MSA/config.yaml"
with open(config_path, "r") as config_file:
    config = yaml.safe_load(config_file)

# Input file paths
csv_file = config['input_folder_path']['de_filtered']  # Path to your CSV file
output_file = config['output_folder_path']['de_filtered_sampling_date']  # Output merged file

metadata = pd.read_csv(csv_file)

nan_count = metadata["EntnahmeDatum"].isna().sum()

print(f"Number of NaN values in 'EntnahmeDatum': {nan_count}")


# Open output FASTA file
with open(output_file, "w") as out_fasta:
    for _, row in metadata.iterrows():
        seq_name = row["ID_seq_prefix"]
        sampling_date = row["EntnahmeDatum"]
        Genotype = row["Genotyp"]
        fasta_path = row["FullPath"]

        # Skip if sampling_date is NaN
        if pd.isna(sampling_date):
            continue

        # Read the sequence from the current FASTA file
        try:
            for record in SeqIO.parse(fasta_path, "fasta"):
                # Update the header to include the sampling date
                record.id = f"{seq_name}_{Genotype}|{sampling_date}"
                record.description = ""
                SeqIO.write(record, out_fasta, "fasta")
        except FileNotFoundError:
            print(f"Error: File '{fasta_path}' not found.")
        except Exception as e:
            print(f"Error processing '{fasta_path}': {e}")

print(f"FASTA sequences merged and saved as '{output_file}'.")
"""
Done with sampling dates
"""

"""
RUN MAFFT
"""