
print("""
      
      This script computes the distance matrix from a multiple sequence alignment (MSA) using the BioPython library.
It uses the identity model to calculate distances, which is suitable for nucleotide sequences.
It reads a FASTA file containing the MSA, computes the distance matrix, and prints it.
      
      
      """)

import pandas as pd
import numpy as np
import os
import glob
import seaborn as sns
import yaml
import matplotlib.pyplot as plt
from Bio import AlignIO
from Bio import Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator


with open("/Users/MiladM-Dev/Documents/1PhD/project-1-N450/project-1.1-gendata/Nextstrain/trial-1/results/clusters/analysis/config.yaml") as f:
    config = yaml.safe_load(f)

#path ='/Users/MiladM-Dev/Documents/1PhD/project-1-N450/project-1.1-gendata/Nextstrain/trial-1/results/clusters/data/aligned_'
# Load your MSA

def calculate_dm_heatmap(fasta_file):

      filename = os.path.basename(fasta_file)

      alignment = AlignIO.read(fasta_file, "fasta")

      # Create a DistanceCalculator object using the "identity" model, which is essentially p-distance
      calculator = DistanceCalculator("identity")

      # Compute the distance matrix
      dm = calculator.get_distance(alignment)

      print( """
            
            The distance matrix is a square matrix where the element at (i, j) represents the distance between sequences i and j.
      The names of the sequences are stored in the 'names' attribute of the distance matrix object.
            
            """
      )# Print the distance matrix



      """Converting the distance matrix to a lower triangular matrix.
      This is useful for visualizing the distances in a heatmap format, where only the lower triangle is filled with values."""

      # Extract labels from the distance matrix
      labels = dm.names  

      # Build lower triangular matrix from the above dictionary
      n = len(labels)
      mat = np.zeros((n, n))

      # Fill lower triangle with your data
      for col_idx, label in enumerate(labels):
            vals = dm[label]
            for row_idx, val in enumerate(vals):
                  if row_idx <= col_idx:  # Ensure only lower triangle is filled
                        mat[col_idx, row_idx] = val
                  else:
                        mat[col_idx, row_idx] = np.nan  # Fill upper triangle with NaN or zeros


      # Create pandas DataFrame with row and column labels
      df_matrix = pd.DataFrame(mat, index=labels, columns=labels)
      df_matrix.to_csv(config['paths']['output_path'] + f"{filename}_distance_matrix.csv")

      print("""
            
            Visualizing the distance matrix as a heatmap using seaborn.
      This provides a graphical representation of the distances between sequences, where colors indicate the distance values.
            Saving it as PNG file.
            
            """
      )
      # Show the matrix as a heatmap
      plt.figure(figsize=(10, 8))
      sns.heatmap(df_matrix, cmap="viridis", xticklabels=True, yticklabels=True)
      plt.title("Distance Matrix Heatmap"+ f" {filename}")
      plt.tight_layout()
      plt.savefig(config['paths']['output_path'] + f"{filename}_distance_matrix_plot.png")
      #plt.show()

for fasta_file in glob.glob(config['paths']['input_path'] + "*.fasta"):
    calculate_dm_heatmap(fasta_file)
    print(f"Processed {fasta_file}")
print("All files processed successfully.")