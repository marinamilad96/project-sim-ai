import pandas as pd
import glob
import os
import yaml
import matplotlib.pyplot as plt

with open('/home/miladm/scratch/git/measles_simulations/Scripts/xml_config.yaml', 'r') as file:
    config = yaml.safe_load(file)


config["FilePath"]["outputFilePath"] = os.path.expandvars(config["FilePath"]["outputFilePath"])
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


plt.figure(figsize=(12, 6))
plt.bar(Time_df['File'], Time_df['Days'], color='skyblue')
plt.xlabel('File Name')
plt.ylabel('Days')
plt.title('Days from Trajectory Files')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save plot
plot_filename = config["FilePath"]["outputFilePath"]+"Bar_timeseries_plot.png"
plt.savefig(plot_filename, dpi=300)
plt.close()


# Save the DataFrame to a CSV file
# Time_df.to_csv(os.path.join(config["outputFilePath"], "time_df.csv"), index
plt.figure(figsize=(12, 6))
plt.hist(Time_df['Days'].dropna(), bins=10, color='skyblue', edgecolor='black')
plt.xlabel('Days')
plt.ylabel('Frequency')
plt.title('Histogram of Days from Trajectory Files')
plt.tight_layout()

plot_filename = config["FilePath"]["outputFilePath"]+"Hist_timeseries_plot.png"
plt.savefig(plot_filename, dpi=300)
plt.close()
