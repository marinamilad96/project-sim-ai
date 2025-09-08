import pandas as pd
import glob
import os
import yaml

"""Read configuration file
and load all .traj files to create a dataframe with time distribution data
and extract name and seed from file names
"""

with open('/Users/MiladM-Dev/Documents/1PhD/project-sim-ai/config-files/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

print("Reading files from:", config["FilePath"]["outputFilePath"])
print("Extracting .traj files...")
traj_files = glob.glob(os.path.join(
    config["FilePath"]["outputFilePath"], "*.traj"))

print("Creating dataframe with filenames and seeds in seperate columns...")
results = []
for file in traj_files:
    df = pd.read_csv(file, sep='\t')
    results.append({
        "Days": df['t'].max(),
        "File": os.path.basename(file).replace('.traj', '')
    })
df = pd.DataFrame(results).sort_values(by='Days', ascending=True)

df[['name', 'seed']] = df['File'].str.extract(
    r'^(.*?)-(\d+)$')  # Write regex to extract name and seed

df = df[['File', 'name', 'seed', 'Days']]
df.reset_index(drop=True, inplace=True)

df.to_csv(os.path.join(
    config["FilePath"]["outputFilePath"], "Time_Distribution_DataFrame.csv"), index=False)
print("Final DataFrame is saved:", config["FilePath"]["outputFilePath"])
