import pandas as pd
import glob
import os
import yaml
import matplotlib.pyplot as plt
import os


"""Read configuration file
and load all .traj files to create a dataframe with time distribution data
and extract name and seed from file names
"""

with open('../project-sim-ai/config-files/sconfig.yaml', 'r') as file:
    config = yaml.safe_load(file)


print("Reading file:", os.path.expandvars(config["Directory"]["Output_Tree_File"]))
h_l_csv = pd.read_csv(os.path.expandvars(config["Directory"]["Output_Tree_File"]))
df = pd.DataFrame(h_l_csv).sort_values(by='tree_height', ascending=True)

df[['name', 'seed']] = df['file_name'].str.extract(
    r'^(.*?)-(\d+)$')  # Write regex to extract name and seed

df = df[['file_name', 'name', 'seed', 'tree_height', 'tree_length']]
df.reset_index(drop=True, inplace=True)
print(df.head())
print(df["tree_height"].describe())
#df.to_csv(os.path.join(os.path.expandvars(config["Directory"]["Output_Tree_File"]), "Time_Distribution_DataFrame.csv"), index=False)
#print("Final DataFrame is saved:", os.path.join(os.path.expandvars(config["Directory"]["Output_Tree_File"]), "Time_Distribution_DataFrame.csv"))


"""Plotting Box plot for time distribution based on different scenarios
with 20 replicates each"""

print("Plotting Box plot for time distribution based on different scenarios with 20 replicates each...")
fig, axs = plt.subplots(figsize=(20, 20))

# Collect unique names
names = df["name"].unique()

fig, axs = plt.subplots(figsize=(20, 10))

names = df["name"].unique()

for i, (name, group) in enumerate(df.groupby("name")):
    data = group["tree_height"].dropna()
    if len(data) == 0:
        continue
    axs.boxplot(data, positions=[i])

axs.set_xticks(range(len(names)))
axs.set_xticklabels(names, rotation=45, ha="right")
axs.set_title("Box plots for different scenarios with 20 replicates each")
plt.tight_layout()


# plt.show()
plt.savefig(os.path.join(
    os.path.expandvars(config["FilePath"]["outputFilePath"]), "Box-plot-height.png"))

print("Box plot is saved:",
      os.path.join(os.path.expandvars(config["FilePath"]["outputFilePath"]), "Box-plot-height.png"))
