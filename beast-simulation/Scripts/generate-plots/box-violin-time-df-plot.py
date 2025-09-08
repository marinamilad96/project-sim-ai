import pandas as pd
import glob
import os
import yaml
import matplotlib.pyplot as plt


with open('/Users/MiladM-Dev/Documents/1PhD/project-sim-ai/config-files/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Find all .traj files
traj_files = glob.glob(os.path.join(
    config["FilePath"]["outputFilePath"], "*.traj"))


results = []
for file in traj_files:
    df = pd.read_csv(file, sep='\t')
    results.append({
        "Days": df['t'].max(),
        "File": os.path.basename(file).replace('.traj', '')
    })
Time_df = pd.DataFrame(results).sort_values(by='Days', ascending=True)

Time_df[['name', 'seed']] = Time_df['File'].str.extract(r'^(.*?)-(\d+)$')

Time_df = Time_df[['File', 'name', 'seed', 'Days']]
Time_df.reset_index(drop=True, inplace=True)
print(Time_df)

fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(20, 20))

# Collect unique names
names = Time_df["name"].unique()

for i, (name, group) in enumerate(Time_df.groupby("name")):
    # Violin plot of all Days across all seeds for this name
    axs[0].violinplot(
        dataset=group["Days"].dropna(),
        positions=[i],
        showmeans=False,
        showmedians=True
    )

    # Box plot of all Days across all seeds for this name
    axs[1].boxplot(
        x=group["Days"].dropna(),
        positions=[i]
    )

# Label x-axis with names
axs[0].set_xticks(range(len(names)))
axs[0].set_xticklabels(names, rotation=45, ha="right")

axs[1].set_xticks(range(len(names)))
axs[1].set_xticklabels(names, rotation=45, ha="right")

axs[0].set_title(
    "Violin plots for different scenarios with 20 replicates each")
axs[1].set_title("Box plots for different scenarios with 20 replicates each")

plt.tight_layout()
# plt.show()
plt.savefig(os.path.join(
    config["FilePath"]["outputFilePath"], "Box_Violin_Time_Distribution.png"))
