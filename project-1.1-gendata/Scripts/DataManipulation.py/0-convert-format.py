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
import xlrd
import re


config_path = "/home/miladm/.vscode-server/data/Machine/config.yaml"
with open(config_path, "r") as config_file:
    config = yaml.safe_load(config_file)

'''
Convert different format to FASTA format
'''
class ConvertToFasta:
    def __init__(self, cfg):
        self.cfg = cfg
        self.genbank_files = glob.glob(os.path.join(self.cfg['input_folder'], "*.gb"))
        self.text_files = glob.glob(os.path.join(self.cfg['input_folder']))
        self.fasta_files = glob.glob(os.path.join(self.cfg['input_folder'], "*.fasta"))
        self.fasta_file_output = glob.glob(os.path.join(self.cfg['output_folder'], "*.fasta"))
        print(f"Found the following .TXT files: {self.text_files}")
        self.cfg['csv_output'] = cfg['csv_output']
        os.makedirs(self.cfg['output_folder'], exist_ok=True)
        
        # Track folders where files are not converted
        self.failed_folders = []

    def gb_to_fasta(self):
        for gb_file in self.genbank_files:
            if os.path.getsize(gb_file) == 0:
                print(f"Skipping empty file: {gb_file}")
                continue
            base_name = os.path.splitext(os.path.basename(gb_file))[0]
            fasta_file = os.path.join(self.cfg['output_folder'], f"{base_name}.fasta")
            try:
                SeqIO.convert(gb_file, "genbank", fasta_file, "fasta")
                print(f"Converted {gb_file} to {fasta_file}")
            except Exception as e:
                print(f"Error converting {gb_file}: {e}")
                self.failed_folders.append(self.cfg['input_folder'])

    def txt_to_fasta(self):
        input_folder = self.cfg['input_folder']
        print(f"Scanning directory: {input_folder}")
        
        self.text_files = []
        for file in os.listdir(input_folder):
            if file.lower().endswith(".txt"):
                self.text_files.append(os.path.join(input_folder, file))
        
        print(f"Text files found: {self.text_files}")

        if not self.text_files:
            print("No .TXT files found in the input folder.")
            self.failed_folders.append(input_folder)
            return

        for txt_file in self.text_files:
            base_name = os.path.splitext(os.path.basename(txt_file))[0]
            fasta_file_txt = os.path.join(self.cfg['output_folder'], f"{base_name}.fasta")

            try:
                with open(txt_file, "r") as txt_handle, open(fasta_file_txt, "w") as fasta_handle:
                    for line in txt_handle:
                        line = line.strip()
                        if line:
                            fasta_handle.write(f"{line}\n")
                print(f"Converted {txt_file} to {fasta_file_txt}")
            except Exception as e:
                print(f"Error processing {txt_file}: {e}")
                self.failed_folders.append(input_folder)

    def move_files(self):
        for fasta_file in self.fasta_files:
            shutil.copy(os.path.join(self.cfg['input_folder'], fasta_file), self.cfg['output_folder'])
            print(f"Moved {fasta_file} to {self.cfg['output_folder']}")

    def count_files(self):
        input_count = len(self.genbank_files) + len(self.text_files) + len(self.fasta_files)
        output_count = len(glob.glob(os.path.join(self.cfg['output_folder'], "*.fasta")))
        print(f"Number of files in input folder: {input_count}")
        print(f"Number of files in output folder: {output_count}")

    def validate_fasta(self):
        with open(os.path.join(self.cfg['output_folder'], self.cfg['csv_output']), "w") as out_file, open(self.cfg['csv_output'], "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["File Name", "Exit Code"])

            for fasta_file_output in glob.glob(os.path.join(self.cfg['output_folder'], "*.fasta")):
                out_file.write(f"{fasta_file_output}\n")
                print(f"{fasta_file_output}")

                result = subprocess.run(
                    ["py_fasta_validator", "-f", fasta_file_output],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True)

                if result.stdout.strip():
                    out_file.write(f"{result.stdout.strip()}\n")
                    print(result.stdout.strip())
                if result.stderr.strip():
                    out_file.write(f"{result.stderr.strip()}\n")
                    print(result.stderr.strip())

                out_file.write(f"Exit code: {result.returncode}\n\n")
                print(f"Exit code: {result.returncode}")

        print(f"CSV summary created at: {self.cfg['csv_output']}")

    def convert(self):
        self.gb_to_fasta()
        self.txt_to_fasta()
        self.move_files()
        self.validate_fasta()
        self.count_files()

        # Print the list of folders that failed during the conversion process
        if self.failed_folders:
            print("Folders where conversion failed or no files were found:")
            for folder in set(self.failed_folders):  # Use set to avoid duplicates
                print(folder)
converter = ConvertToFasta(config)
converter.convert()

'''
Convert different format to FASTA format
'''