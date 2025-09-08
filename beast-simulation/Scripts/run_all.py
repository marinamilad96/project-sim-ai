import subprocess

generate_xml_script = """
python3 /home/miladm/scratch/git/measles_simulations/Scripts/generate_SEID_p_m_xml_files.py
"""

BEAST_script = """
cd $TMPDIR/wissdaten/ZKI-PH2_Data/MiladM/trees/

for file in $TMPDIR/wissdaten/ZKI-PH2_Data/MiladM/trees/*.xml; do
    echo "Running BEAST for $file"
    /home/miladm/beast/beast/bin/beast "$file"
done
"""

plot_script = """
python3 /home/miladm/scratch/git/measles_simulations/Scripts/traj_plot.py
python3 /home/miladm/scratch/git/measles_simulations/Scripts/time_distirbution_plot.py
Rscript /home/miladm/scratch/git/TreeStatistics-/scripts/tree-length-height-folder-treefile.r
"""
subprocess.run(generate_xml_script, shell=True, executable="/bin/bash")

for i in range(20):
    print(f"Iteration {i+1}/20")
    subprocess.run(BEAST_script, shell=True, executable="/bin/bash")
print("All iterations completed.")

subprocess.run(plot_script, shell=True, executable="/bin/bash")
print("All tasks completed.")


# python3 /home/miladm/scratch/git/measles_simulations/Scripts/generate_SEID_p_m_xml_files.py
# python3 /home/miladm/scratch/git/measles_simulations/Scripts/time_distirbution_plot.py
# python3 /home/miladm/scratch/git/measles_simulations/Scripts/generate_SEIR_p_m_xml_files.py
