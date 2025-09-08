from Bio import SeqIO
import os
import glob
import yaml
import shutil
import pandas as pd
import subprocess
import csv
from collections import Counter

config_path = "/Users/MiladM-Dev/Documents/1PhD/Scripts/config.yaml"
with open(config_path, "r") as config_file:
    config = yaml.safe_load(config_file)

'''
Seq files
'''

class ManipulateSeqFiles:

    def __init__(self, cfg: dict):
        self.cfg = cfg
        
    def create_df_seq_file(self):    
        # Get the list of filenames in the folder
        seq_file_names = os.listdir(self.cfg['Sequence_folder']["seq_file"])

        # Create a DataFrame
        self.df_seq_file = pd.DataFrame(seq_file_names, columns=['FileName'])

        # Add a column with the full path for each file
        self.df_seq_file['FullPath'] = [os.path.abspath(os.path.join(self.cfg['Sequence_folder']["seq_file"], file)) for file in seq_file_names]

        # extract the ID
        self.df_seq_file[['ID_seq_prefix', 'ID_seq_Remainder']] = self.df_seq_file['FileName'].str.extract(r'(\d{2}-\d{5})(.*)')
        self.df_seq_file['ID_seq_Remainder'] = self.df_seq_file['ID_seq_Remainder'].str.replace('.fasta', '')

        # Make the full path column always at the end
        columns_order = [col for col in self.df_seq_file.columns if col != 'FullPath'] + ['FullPath']
        self.df_seq_file = self.df_seq_file[columns_order]

        
        return 'Dataframe for IDs and Fullpath created successfully'

    def map_to_key(self, description):
        if not isinstance(description, str):  # Check if it's not a string
            description = str(description) if pd.notna(description) else ""  # Convert to string or empty string if NaN
        for key, values in self.cfg['extraction_abbreviation'].items():
            if any(value in description for value in values):
                return key
        return 'Unknown'

    def apply_map_to_key(self):
        self.df_seq_file['Material dict'] = self.df_seq_file['ID_seq_Remainder'].apply(self.map_to_key)
        self.df_seq_file.to_csv(self.cfg['Sequence_folder']['seq_output_file'], sep=';')

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
        self.df_excel = pd.read_csv(self.cfg['Excel_folder']['excel_file_path'], encoding='utf-8', sep=';')

        # Split 'SCount' into two columns
        self.df_excel[['ID_xsl_prefix', 'ID_xsl_Suffix']] = self.df_excel['SCount'].str.extract(r'(\d{2}-\d{5})(.*)')

        # Drop the suffix (.xx)
        del self.df_excel['ID_xsl_Suffix']
        #self.df_excel.to_csv(self.cfg['Excel_folder']['excel_file_path_output'], sep=';')
        return 'Dataframe for Excel file created successfully'

    def map_to_key(self, description):
        if not isinstance(description, str):  # Check if it's not a string
            description = str(description) if pd.notna(description) else ""  # Convert to string or empty string if NaN
        for key, values in self.cfg['extraction_abbreviation'].items():
            if any(value in description for value in values):
                return key
        return 'Unknown'

    def apply_map_to_key(self):
        #self.df_excel = pd.read_csv(self.cfg['Excel_folder']['excel_file_path_output'], encoding='utf-8', sep=';')
        self.df_excel['Material dict'] = self.df_excel["Material"].apply(self.map_to_key)
        self.df_excel.to_csv(self.cfg['Excel_folder']['excel_file_path_output'], sep=';')
        return 'Dataframe for Material Mapping in Excel file created successfully'

    def split_df_de_aus(self):
        
        self.df_excel = pd.read_csv(self.cfg['Excel_folder']['excel_file_path_output'], encoding='utf-8', sep=';')
        print(self.df_excel)
        if 'BLand' not in self.df_excel.columns:
            raise KeyError("Column 'BLand' not found in the DataFrame")
        
        self.df_xsl_ausland = self.df_excel[self.df_excel['BLand'].str.contains('Ausland', na=False)]
        self.df_xsl_de = self.df_excel[~self.df_excel['BLand'].str.contains('Ausland', na=False)]

        self.df_xsl_ausland = pd.DataFrame(self.df_xsl_ausland)
        self.df_xsl_de = pd.DataFrame(self.df_xsl_de)

        self.df_xsl_ausland.to_csv(self.cfg['Excel_folder']['df_xsl_ausland_file'], index=False)
        self.df_xsl_de.to_csv(self.cfg['Excel_folder']['df_xsl_de_file'], index=False)

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

    def extract_and_filter(self):
        
        merged = self.df_xsl_de.merge(
        self.df_seq_file,
        left_on='ID_xsl_prefix',
        right_on='ID_seq_prefix',
        suffixes=('_xsl', '_seq'),
        how='outer',  # Use 'outer' to include unmatched rows for filtering
        indicator=True
    )

        # Define conditions for filtering
        condition1 = ((merged['ID_xsl_prefix'] == merged['ID_seq_prefix']) &
            (merged['Material dict_xsl'] == merged['Material dict_seq']))
        condition2 = ((merged['ID_xsl_prefix'] == merged['ID_seq_prefix']) &
            ((merged['Material dict_xsl'] == 'Unknown') |
                (merged['Material dict_seq'] == 'Unknown')) )

        # Combine conditions
        combined_condition = condition1 | condition2

        # Filter rows based on the combined condition
        filtered_rows = merged[combined_condition]
        unmatched_rows = merged[~combined_condition & (merged['_merge'] == 'left_only')]

        # Drop unnecessary columns
        filtered_rows = filtered_rows.drop(columns=['_merge'])
        unmatched_rows = unmatched_rows.drop(columns=['_merge'])

        print("Filtered Rows:")
        print(filtered_rows)

        print("Unmatched Rows:")
        print(unmatched_rows)

        # Store or return results as needed
        self.filtered_rows = filtered_rows
        self.unmatched_rows = unmatched_rows
        
        self.df_xsl_de_filtered = pd.DataFrame(filtered_rows)
        self.df_xsl_de_filtered.to_csv(self.cfg['Extract_folder']['extract_file_path_output'], index=True)

        self.df_xsl_de_unmatched = pd.DataFrame(unmatched_rows)
        self.df_xsl_de_unmatched.to_csv(self.cfg['Extract_folder']['unmatched_file_path_output'], index=True)
        
    def extract_seq_to_excel(self):
        self.create_df_seq_xsl_file()
        self.extract_and_filter()
        return 'Filtered and other DataFrames created successfully'



extractor = ExtractSeqToExcel(config)
extractor.extract_seq_to_excel()


