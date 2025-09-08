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
        return 'Unknown'

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


df_excel_file = ManipulateExcel(config)
df_excel_file.generate_xsl_dfs()

'''
Xsl file
'''