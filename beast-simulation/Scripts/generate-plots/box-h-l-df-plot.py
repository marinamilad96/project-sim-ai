import pandas as pd
import glob
import os
import yaml
import matplotlib.pyplot as plt

"""Read configuration file
and load all _trees files to create a dataframe with time distribution data
and extract name and seed from file names
"""

with open('/Users/MiladM-Dev/Documents/1PhD/project-sim-ai/config-files/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

print("Reading files from:", config["Directory"]["Output_Tree_File"])

print("Creating dataframe with filenames and seeds in seperate columns...")
df = pd.read_csv(config["Directory"]["Output_Tree_File"])

df = pd.DataFrame(df)


df[['name', 'seed', "tree_type"]] = df['file_name'].str.extract(
    r'^(.*?)-(\d+)\.(.*)$')  # Write regex to extract name and seed
print(df)
df = df[['file_name', 'name', 'seed', "tree_type", 'tree_height', 'tree_length']]
df.reset_index(drop=True, inplace=True)

df.to_csv(os.path.join(
    config["FilePath"]["outputFilePath"], "height_length_DataFrame.csv"), index=False)
print("Final DataFrame is saved:", os.path.join(
    config["FilePath"]["outputFilePath"], "height_length_DataFrame.csv"))

print(df)

"""Plotting Box plot for time distribution based on different scenarios
with 20 replicates each"""

print("Plotting Box plots for tree height and tree length based on different scenarios...")
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(
    25, 12))  # two subplots: height & length

# Collect unique names
names = df["name"].unique()
tree_types = ["full.trees", "sampled.trees"]

# --- Tree Height ---
for i, name in enumerate(names):
    for j, tree_type in enumerate(tree_types):
        group = df[(df["name"] == name) & (df["tree_type"] == tree_type)]
        if group.empty:
            continue
        axs[0].boxplot(
            x=group["tree_height"].dropna(),
            # offset so full/sample are side by side
            positions=[i * len(tree_types) + j]
        )

axs[0].set_xticks(
    [i * len(tree_types) + 0.5 for i in range(len(names))],  # center labels
)
axs[0].set_xticklabels(names, rotation=45, ha="right")
axs[0].set_title("Box plots of Tree Height by Scenario (Full vs Sampled)")
axs[0].set_ylabel("Tree Height")

# --- Tree Length ---
for i, name in enumerate(names):
    for j, tree_type in enumerate(tree_types):
        group = df[(df["name"] == name) & (df["tree_type"] == tree_type)]
        if group.empty:
            continue
        axs[1].boxplot(
            x=group["tree_length"].dropna(),
            positions=[i * len(tree_types) + j]
        )

axs[1].set_xticks(
    [i * len(tree_types) + 0.5 for i in range(len(names))],
)
axs[1].set_xticklabels(names, rotation=45, ha="right")
axs[1].set_title("Box plots of Tree Length by Scenario (Full vs Sampled)")
axs[1].set_ylabel("Tree Length")

plt.tight_layout()
plt.savefig(os.path.join(
    config["FilePath"]["outputFilePath"], "Box_TreeHeight_TreeLength.png"))
print("Box plots saved:",
      os.path.join(config["FilePath"]["outputFilePath"], "Box_TreeHeight_TreeLength.png"))
plt.show()
