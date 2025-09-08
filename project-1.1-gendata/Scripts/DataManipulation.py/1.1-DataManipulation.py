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
import numpy as np


config_path = '/home/miladm/.vscode-server/data/Machine/Data_curation/config.yaml'
with open(config_path, "r") as config_file:
    config = yaml.safe_load(config_file)

'''
Seq files new
'''
class ManipulateSeqFiles:

    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.df_seq_file = None
        self.df_rep_ID = None
        self.df_files_rep_ID = None

    def create_df_seq_file(self):
        genotypes_seq_folder = self.cfg['Sequence_folder']["genotypes_seq_folder"]
        file_records = []

        # Walk through all subdirectories
        for root, _, files in os.walk(genotypes_seq_folder):
            for file in files:
                if file.endswith(".fasta"):  # Process only FASTA files
                    full_path = os.path.join(root, file)
                    file_records.append((file, full_path))

        # Create a DataFrame
        self.df_seq_file = pd.DataFrame(file_records, columns=['FileName', 'FullPath'])
        
        # Extract the ID
        self.df_seq_file[['ID_seq_prefix', 'ID_seq_Remainder']] = self.df_seq_file['FileName'].str.extract(r'(\d{2}-\d{5})(.*)')
        self.df_seq_file['ID_seq_Remainder'] = self.df_seq_file['ID_seq_Remainder'].str.replace('.fasta', '', regex=False)
        self.df_seq_file['ID_seq_Remainder'] = self.df_seq_file['ID_seq_Remainder'].astype(str)
        self.df_seq_file = self.df_seq_file[~self.df_seq_file['ID_seq_Remainder'].str.startswith('._')]
        return 'Dataframe for IDs and Fullpath created successfully'

    def map_to_key(self, description):
        if not isinstance(description, str):  # Check if it's not a string
            description = str(description) if pd.notna(description) else ""  # Convert to string or empty string if NaN
        for key, values in self.cfg['extraction_abbreviation'].items():
            if any(value in description for value in values):
                return key
        return 'Other'

    def apply_map_to_key(self):
        self.df_seq_file['Material dict'] = self.df_seq_file['ID_seq_Remainder'].apply(self.map_to_key)
        self.df_seq_file.to_csv(self.cfg['Sequence_folder']['seq_output_file'])

    def create_df_duplicated_ID(self):
        if self.df_seq_file is None:
            raise ValueError("DataFrame not created. Call create_df_seq_file() first.")
        
        self.df_rep_ID = self.df_seq_file[self.df_seq_file['ID_seq_prefix'].duplicated(keep=False)]
        self.df_files_rep_ID = self.df_rep_ID.pivot_table(index=['ID_seq_prefix'], aggfunc='size')

        self.df_files_rep_ID = self.df_files_rep_ID.to_frame(name='amount').reset_index()
        self.df_files_rep_ID = self.df_files_rep_ID.sort_values('amount', ascending=False)

        self.df_files_rep_ID.to_csv(self.cfg['Sequence_folder']['rep_IDs_file'])
        return 'Dataframe for replicated ID created successfully'

    def generate_seq_dfs(self):
        self.create_df_seq_file()
        self.apply_map_to_key()
        self.create_df_duplicated_ID()
        return 'Dataframe for IDs, Fullpath, replicated ID created successfully'
#df_fasta_file = ManipulateSeqFiles(config)
#df_fasta_file.generate_seq_dfs()

'''
Excel Sheet
'''
class ManipulateExcel:

    def __init__(self, cfg: dict):
        self.cfg = cfg

    def create_df_xsl(self):
        date_columns = ['EingangsDatum', 'EntnahmeDatum', 'ErkrBeginn', 'EkzBeginn']
        self.df_excel =  pd.read_excel(self.cfg['Excel_folder']['excel_file_path'], engine= "openpyxl", dtype= 'str')
        for col in date_columns:
            self.df_excel[col] = self.df_excel[col].astype(str)
            self.df_excel[col] = self.df_excel[col].apply(lambda x: re.sub(r'(\d{4}-\d{2}-\d{2})\s+\d{1,2}:\d{2}:\d{2}(\.\d+)?', r'\1', x).strip())

        self.df_excel.to_csv(self.cfg['Excel_folder']['excel_file_path_csv'], index= False, encoding='utf-8-sig')

        # Split 'SCount' into two columns
        self.df_excel[['ID_xsl_prefix', 'ID_xsl_Suffix']] = self.df_excel['SCount'].str.extract(r'(\d{2}-\d{5})(.*)')

        # Drop the suffix (.xx)
        del self.df_excel['ID_xsl_Suffix']
        return 'Dataframe for Excel file created successfully'

    def map_to_key(self, description):
        if not isinstance(description, str):  # Check if it's not a string
            description = str(description) if pd.notna(description) else ""  # Convert to string or empty string if NaN
        for key, values in self.cfg['extraction_abbreviation'].items():
            if any(value in description for value in values):
                return key
        return 'Other'

    def apply_map_to_key(self):
        self.df_excel['Material dict'] = self.df_excel["Material"].apply(self.map_to_key)
        self.df_excel.to_csv(self.cfg['Excel_folder']['excel_file_path_output'], index= False, encoding='utf-8-sig')
        return 'Dataframe for Material Mapping in Excel file created successfully'

    def split_df_de_aus(self):
        
        self.df_excel = pd.read_csv(self.cfg['Excel_folder']['excel_file_path_output'])
        print(self.df_excel)
        if 'BLand' not in self.df_excel.columns:
            raise KeyError("Column 'BLand' not found in the DataFrame")
        
        self.df_xsl_ausland = self.df_excel[self.df_excel['BLand'].str.contains('Ausland', na=False)]
        self.df_xsl_de = self.df_excel[~self.df_excel['BLand'].str.contains('Ausland', na=False)]

        self.df_xsl_ausland = pd.DataFrame(self.df_xsl_ausland)
        self.df_xsl_de = pd.DataFrame(self.df_xsl_de)

        self.df_xsl_ausland.to_csv(self.cfg['Excel_folder']['df_xsl_ausland_file'], index= False, encoding='utf-8-sig')
        self.df_xsl_de.to_csv(self.cfg['Excel_folder']['df_xsl_de_file'], index=False, encoding='utf-8-sig')

        return 'Dataframe for Ausland and DE in Excel file created successfully'

    def generate_xsl_dfs(self):
        self.create_df_xsl()
        self.apply_map_to_key()
        self.split_df_de_aus()

        return 'Dataframe for Excel file created successfully'
#df_excel_file = ManipulateExcel(config)
#df_excel_file.generate_xsl_dfs()

'''
Extract Seq to Excel
'''
class ExtractSeqToExcel:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.df_fasta_file = ManipulateSeqFiles(cfg)
        self.df_fasta_file.generate_seq_dfs()

        self.df_excel_file = ManipulateExcel(cfg)
        self.df_excel_file.generate_xsl_dfs()

    def create_df_seq_xsl_file(self):
        self.df_seq_file = self.df_fasta_file.df_seq_file
        self.df_files_rep_ID = self.df_fasta_file.df_files_rep_ID

        self.df_xsl_de = self.df_excel_file.df_xsl_de
        self.df_xsl_ausland = self.df_excel_file.df_xsl_ausland

    def apply_extract(self):
        
        self.merged = self.df_xsl_de.merge(
        self.df_seq_file,
        left_on='ID_xsl_prefix',
        right_on='ID_seq_prefix',
        suffixes=('_xsl', '_seq'),
        how='outer',  # Use 'outer' to include unmatched rows for filtering
        indicator=True )

        # Define conditions for filtering
        #condition1 = ((self.merged['ID_xsl_prefix'] == self.merged['ID_seq_prefix']) &
        #    (self.merged['Material dict_xsl'] == self.merged['Material dict_seq']) & (self.merged['Material dict_seq'] != 'Other') )
        #condition2 =((self.merged['Material dict_xsl'] == self.merged['Material dict_seq'])) # &  (self.merged['Material dict_xsl'] == self.merged['Material dict_seq']))
        #condition3 = ((self.merged['ID_xsl_prefix'] == self.merged['ID_seq_prefix']) & ((self.merged['Material dict_xsl'] == 'Other') | (self.merged['Material dict_seq'] == 'Other')) )

        # Combine conditions
        #combined_condition = condition1 | condition2 #| condition3

        # Filter rows based on the combined condition
        #self.filtered_rows = self.merged[combined_condition & (self.merged['_merge'] == 'both')]

        # Sorting the merged dataframe
        self.de_matched_rows = self.merged[(self.merged['_merge'] == 'both')]
        self.xsl_de_unmatched = self.merged[(self.merged['_merge'] == 'left_only')]
        self.seq_de_unmatched = self.merged[(self.merged['_merge'] == 'right_only')]

        # Drop unnecessary columns
        print("Merged Rows: Done")
        
        print("De Rows extraction: Done")

        # Store or return results as needed
        self.merged.to_csv(self.cfg['Extract_folder']['merged_file_path'], index= False, encoding='utf-8-sig')

        # Extract matched rows in Germany
        self.df_de_matched_rows = pd.DataFrame(self.de_matched_rows)
        self.df_de_matched_rows.to_csv(self.cfg['Extract_folder']['de_matched_rows'], index= False, encoding='utf-8-sig')

        # Extract IDs that doesn't have any match in the merged DataFrame
        self.df_xsl_de_unmatched = pd.DataFrame(self.xsl_de_unmatched)
        self.df_xsl_de_unmatched.to_csv(self.cfg['Extract_folder']['xsl_de_unmatched_file_path_output'], index= False, encoding='utf-8-sig')
        self.df_seq_de_unmatched = pd.DataFrame(self.seq_de_unmatched)
        self.df_seq_de_unmatched.to_csv(self.cfg['Extract_folder']['seq_de_unmatched_file_path_output'], index= False, encoding='utf-8-sig')
        

    def extract_seq_to_excel(self):
        self.create_df_seq_xsl_file()
        self.apply_extract()
        return 'Filtered and other DataFrames created successfully'

    def apply_filter(self):
        """
        Define conditions for filtering and apply them to the merged DataFrame
        """
        is_unique = self.df_de_matched_rows['ID_xsl_prefix'].duplicated(keep=False) == False

        # 1st condition: Material match and ID is unique and more subclassification
        condition1 = (self.df_de_matched_rows['Material dict_xsl'] == self.df_de_matched_rows['Material dict_seq']) & is_unique
        condition2 = (self.df_de_matched_rows['Material dict_xsl'] != self.df_de_matched_rows['Material dict_seq']) & is_unique

        # 2nd condition: Non-unique ID and Material match but not 'Other'
        condition3 = (~is_unique) & (self.df_de_matched_rows['Material dict_xsl'] == self.df_de_matched_rows['Material dict_seq']) #& \
             #(self.df_de_matched_rows['Material dict_xsl'] != 'Other')

        # 3rd condition: If 2nd condition is False, check only material match for non-unique
        condition4 = (~condition2) & (~is_unique) & (self.df_de_matched_rows['Material dict_xsl'] == self.df_de_matched_rows['Material dict_seq'])

        # Combine into final conditions if needed
        combined_condition = condition1 | condition2 | condition3 | condition4

        self.filtered_rows = self.df_de_matched_rows[combined_condition ]
        self.remained_rows = self.df_de_matched_rows[~combined_condition]

        self.df_xsl_de_filtered = pd.DataFrame(self.filtered_rows)
        self.df_xsl_de_filtered.to_csv(self.cfg['Extract_folder']['de_filtered_material'], index= False, encoding='utf-8-sig')

        self.df_remained_rows = pd.DataFrame(self.remained_rows)
        self.df_remained_rows.to_csv(self.cfg['Extract_folder']['de_remained_rows'], index= False, encoding='utf-8-sig')

        # Extract IDs from filtered_rows for comparison
        filtered_ids = set(self.df_xsl_de_filtered['ID_xsl_prefix'])

        # Identify remained rows not present in filtered_rows
        post_remained_rows = self.remained_rows[~self.remained_rows['ID_xsl_prefix'].isin(filtered_ids)]
        post_remained_rows.to_csv(self.cfg['Extract_folder']['de_post_remained_rows'], index=False, encoding='utf-8-sig')
        return 'Filtered, remained, and post-remained DataFrames created successfully'
    
    def create_df_duplicated_ID_final(self):
        if self.de_matched_rows is None:
            raise ValueError("DataFrame not created. Call crde_matched_rows() first.")
            
        self.df_de_matched_rows = self.de_matched_rows[self.de_matched_rows['ID_seq_prefix'].duplicated(keep=False)]
        self.df_de_matched = self.df_de_matched_rows.pivot_table(index=['ID_seq_prefix'], aggfunc='size')

        self.df_de_matched_rep_ID = self.df_de_matched.to_frame(name='amount').reset_index()
        self.df_de_matched_rep_ID = self.df_de_matched_rep_ID.sort_values('amount', ascending=False)

        self.df_de_matched_rep_ID.to_csv(self.cfg['Extract_folder']['rep_IDs_file'])
        return 'Dataframe for replicated ID created successfully'
    
    def apply_seq_to_excel(self):
        self.extract_seq_to_excel()
        self.apply_filter()
        self.create_df_duplicated_ID_final()
        return 'Filtered and other DataFrames created successfully'
extractor = ExtractSeqToExcel(config)
extractor.apply_seq_to_excel()


'''
Extract Seq to Excel
'''