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


print("Reading files from:", os.path.expandvars(config["FilePath"]["outputFilePath"]))
print("Extracting .traj files...")
traj_files = glob.glob(os.path.join(
    os.path.expandvars(config["FilePath"]["outputFilePath"]), "*.traj"))  # Find all .traj files

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
    os.path.expandvars(config["FilePath"]["outputFilePath"]), "Time_Distribution_DataFrame.csv"), index=False)
print("Final DataFrame is saved:", os.path.join(
    os.path.expandvars(config["FilePath"]["outputFilePath"]), "Time_Distribution_DataFrame.csv"))


"""Plotting Box plot for time distribution based on different scenarios
with 20 replicates each"""

print("Plotting Box plot for time distribution based on different scenarios with 20 replicates each...")
import matplotlib.pyplot as plt

fig, axs = plt.subplots(figsize=(20, 20))

# Collect unique names
names = df["name"].unique()

for i, (name, group) in enumerate(df.groupby("name")):
    # Filter Days < 400
    filtered_days = group["Days"].dropna()
    filtered_days = filtered_days[filtered_days < 400]

    if len(filtered_days) == 0:
        continue  # skip if no values under 400

    # Box plot of filtered Days
    axs.boxplot(
        x=filtered_days,
        positions=[i]
    )

# Label x-axis with names
axs.set_xticks(range(len(names)))
axs.set_xticklabels(names, rotation=45, ha="right")

axs.set_title("Box plots for different scenarios with 20 replicates each (Days < 400)")

plt.tight_layout()

# plt.show()
plt.savefig(os.path.join(
    os.path.expandvars(config["FilePath"]["outputFilePath"]), "Box_Time_Distribution_below400.png"))

print("Box plot is saved:",
      os.path.join(os.path.expandvars(config["FilePath"]["outputFilePath"]), "Box_Time_Distribution_below400.png"))
