from Bio import SeqIO
import os
import glob
import yaml
import shutil
import pandas as pd
import FastaValidator
import subprocess
import csv
from collections import Counter
from marshmallow import fields, ValidationError
import matplotlib.pyplot as plt

config_path = "/Users/MiladM-Dev/Documents/1PhD/Scripts/config.yaml"
with open(config_path, "r") as config_file:
    config = yaml.safe_load(config_file)


class ConvertToFasta:
    def __init__(self, input_folder, output_folder,csv_output):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.genbank_files = glob.glob(os.path.join(self.input_folder, "*.gb"))
        self.text_files = glob.glob(os.path.join(self.input_folder, "*.txt"))
        self.fasta_files = glob.glob(os.path.join(self.input_folder, "*.fasta"))
        self.fasta_file_output = glob.glob(os.path.join(self.output_folder, "*.fasta"))
        self.csv_output = csv_output
        os.makedirs(self.output_folder, exist_ok=True)

    def gb_to_fasta(self):
            for gb_file in self.genbank_files:
                if os.path.getsize(gb_file) == 0:
                    print(f"Skipping empty file: {gb_file}")
                    continue
                base_name = os.path.splitext(os.path.basename(gb_file))[0]
                fasta_file = os.path.join(self.output_folder, f"{base_name}.fasta")
                try:
                    SeqIO.convert(gb_file, "genbank", fasta_file, "fasta")
                    print(f"Converted {gb_file} to {fasta_file}")
                except Exception as e:
                    print(f"Error converting {gb_file}: {e}")

    def txt_to_fasta(self):
        for txt_file in self.text_files:
            base_name = os.path.splitext(os.path.basename(txt_file))[0]  # Get the base file name
            fasta_file_txt = os.path.join(self.output_folder, f"{base_name}.fasta")
            with open(txt_file, "r") as txt_handle, open(fasta_file_txt, "w") as fasta_handle:
                for line in txt_handle:
                    fasta_handle.write(f">{base_name}\n{line.strip()}\n")
            print(f"Converted {txt_file} to {fasta_file_txt}")

    def move_files(self):
        for fasta_file in self.fasta_files:
            shutil.copy(os.path.join(self.input_folder, fasta_file), self.output_folder)
            print(f"Moved {fasta_file} to {self.output_folder}")

    def count_files(self):
        input_count = len(self.genbank_files) + len(self.text_files) + len(self.fasta_files)
        output_count = len(glob.glob(os.path.join(self.output_folder, "*.fasta")))
        print(f"Number of files in input folder: {input_count}")
        print(f"Number of files in output folder: {output_count}")

    def validate_fasta(self):
        with open(os.path.join(self.output_folder, self.csv_output), "w") as out_file, open(self.csv_output, "w", newline="") as csv_file:
            # Create a CSV writer object
            csv_writer = csv.writer(csv_file)
            # Write the CSV header
            csv_writer.writerow(["File Name", "Exit Code"])

            # Iterate over all .fasta files in the directory
            for fasta_file_output in glob.glob(os.path.join(self.output_folder, "*.fasta")):
                out_file.write(f"{fasta_file_output}\n")
                print(f"{fasta_file_output}")

                # Run the py_fasta_validator command
                result = subprocess.run(
                    ["py_fasta_validator", "-f", fasta_file_output],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True)

                # Print and log the validation output (stdout and stderr)
                if result.stdout.strip():
                    out_file.write(f"{result.stdout.strip()}\n")
                    print(result.stdout.strip())
                if result.stderr.strip():
                    out_file.write(f"{result.stderr.strip()}\n")
                    print(result.stderr.strip())

                # Log and print the exit code
                out_file.write(f"Exit code: {result.returncode}\n\n")
                print(f"Exit code: {result.returncode}")

                # Write the file name and exit code to the CSV file
                #csv_writer.writerow([os.path.basename(fasta_file_output), result.returncode])

        print(f"CSV summary created at: {self.csv_output}")

    def convert(self):
        self.gb_to_fasta()
        self.txt_to_fasta()
        self.move_files()
        self.validate_fasta()
        self.count_files()

converter = ConvertToFasta(config["input_folder"], config["output_folder"], config["csv_output"])
converter.convert()
