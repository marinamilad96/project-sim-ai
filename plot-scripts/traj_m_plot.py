import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os
import yaml

# Path to your directory
with open('/Users/MiladM-Dev/Documents/1PhD/project-1-N450/git_trial/Scripts/xml_config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Find all .traj files
traj_files = glob.glob(os.path.join(
    config["FilePath"]["outputFilePath"], "*.traj"))


# Loop over each .traj file
for file in traj_files:
    # Read the data
    df = pd.read_csv(file, sep='\t')

    # Convert 'Sample' to categorical (like factor in R)
    df['population types'] = df['population'] + '_' + df['index'].astype('str')
    df['population types'] = df['population types'].astype('category')

    # Plot
    plt.figure(figsize=(10, 6))
    sns.lineplot(
        data=df,
        x='t',
        y='value',
        hue='population types',
        style='index',
        estimator=None,
        alpha=0.5,
        drawstyle='steps-post'
    )

    plt.xlabel('t')
    plt.ylabel('value')
    plt.title(f'Trajectory Plot: {os.path.basename(file)}')
    plt.legend(title='Population', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Save plot
    plot_filename = f"{os.path.splitext(file)[0]}_plot.png"
    plt.savefig(plot_filename, dpi=300)
    plt.close()

    print(f"Plot saved for {file}")

print("All plots generated.")
