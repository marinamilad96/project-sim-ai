import pandas as pd
import glob
import os
import yaml
import matplotlib.pyplot as plt

"""Read configuration file
and load all _trees files to create a dataframe with time distribution data
and extract name and seed from file names
"""

with open('./project-sim-ai/config-files/sconfig.yaml', 'r') as file:
    config = yaml.safe_load(file)

print("Reading files from:", os.path.expandvars(config["Directory"]["Output_Tree_File"]))

print("Creating dataframe with filenames and seeds in seperate columns...")
df = pd.read_csv(os.path.expandvars(config["Directory"]["Output_Tree_File"]))

df = pd.DataFrame(df)


df[['name', 'seed', "tree_type"]] = df['file_name'].str.extract(
    r'^(.*?)-(\d+)\.(.*)$')  # Write regex to extract name and seed

df = df[['file_name', 'name', 'seed', "tree_type", 'tree_height', 'tree_length']]

# ==== Data Cleaning ====
df = df[df["tree_height"] < 1000]  
df.reset_index(drop=True, inplace=True)


df.to_csv(os.path.join(os.path.expandvars(config["FilePath"]["outputFilePath"]), "height_length_DataFrame.csv"), index=False)

print("Final DataFrame is saved:", os.path.join(
    os.path.expandvars(config["FilePath"]["outputFilePath"]), "height_length_DataFrame.csv"))

print("Shape of whole df",df.shape)

"""Splitting the dataframe based on tree type (full vs sampled)"""
full_df = df[df["tree_type"] == "full.trees"]
full_df.reset_index(drop=True, inplace=True)
sampled_df = df[df["tree_type"] == "sampled.trees"]
sampled_df.reset_index(drop=True, inplace=True)

print("Full trees dataframe:", full_df.shape)
print(full_df)

print("Sampled trees dataframe:", sampled_df.shape)
print(sampled_df)

"""Plotting Box plot for time distribution based on different scenarios
with 20 replicates each"""

print("Plotting Box plots for tree height and tree length based on different scenarios...")
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(
    25, 12))  # two subplots: height & length

# Collect unique names
names = df["name"].unique()

# --- FULL TREES ---
# --- Tree Height ---
for i, name in enumerate(names):
    # Group by name only
    group = full_df[full_df["name"] == name]
    if group.empty:
        continue
    axs[0].boxplot(
        x=group["tree_height"].dropna(),
        positions=[i]
    )

# Set x-ticks at each name position
axs[0].set_xticks(range(len(names)))
axs[0].set_xticklabels(names, rotation=45, ha="right")
axs[0].set_title("Box plots of full Tree Height by Name")
axs[0].set_ylabel("Tree Height")


# --- Tree Length ---
for i, name in enumerate(names):
    # Group by name only
    group = full_df[full_df["name"] == name]
    if group.empty:
        continue
    axs[1].boxplot(
        x=group["tree_length"].dropna(),
        positions=[i]
    )

# Set x-ticks at each name position
axs[1].set_xticks(range(len(names)))
axs[1].set_xticklabels(names, rotation=45, ha="right")
axs[1].set_title("Box plots of full Tree length by Name")
axs[1].set_ylabel("Tree length")


plt.tight_layout()
plt.savefig(os.path.join(
    os.path.expandvars(config["FilePath"]["outputFilePath"]), "Box_plot_Full_Tree_Height_Length.png"))
print("Box plots saved:",
      os.path.join(os.path.expandvars(config["FilePath"]["outputFilePath"]), "Box_plot_Full_Tree_Height_Length.png"))
plt.show()


# --- SAMPLED TREES ---
# --- Tree Height ---
for i, name in enumerate(names):
    # Group by name only
    group = sampled_df[sampled_df["name"] == name]
    if group.empty:
        continue
    axs[0].boxplot(
        x=group["tree_height"].dropna(),
        positions=[i]
    )

# Set x-ticks at each name position
axs[0].set_xticks(range(len(names)))
axs[0].set_xticklabels(names, rotation=45, ha="right")
axs[0].set_title("Box plots of sampled Tree Height by Name")
axs[0].set_ylabel("Tree Height")


# --- Tree Length ---
for i, name in enumerate(names):
    # Group by name only
    group = sampled_df[sampled_df["name"] == name]
    if group.empty:
        continue
    axs[1].boxplot(
        x=group["tree_length"].dropna(),
        positions=[i]
    )

# Set x-ticks at each name position
axs[1].set_xticks(range(len(names)))
axs[1].set_xticklabels(names, rotation=45, ha="right")
axs[1].set_title("Box plots of sampled Tree length by Name")
axs[1].set_ylabel("Tree length")


plt.tight_layout()
plt.savefig(os.path.join(
    os.path.expandvars(config["FilePath"]["outputFilePath"]), "Box_plot_sampled_Tree_Height_Length.png"))
print("Box plots saved:",
      os.path.join(os.path.expandvars(config["FilePath"]["outputFilePath"]), "Box_plot_sampled_Tree_Height_Length.png"))
plt.show()