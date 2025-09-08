# Define the output file
OUTPUT_FILE="~/de_filtered_id_genotype_date_aln.fasta.timetree.nex"
OUTPUT_FILE=$(eval echo "$OUTPUT_FILE")  # Expands the ~ to the home directory

# Extract the output folder from the output file path
OUTPUT_FOLDER=$(dirname "$OUTPUT_FILE")


INPUT_FILE = 
"/Users/MiladM-Dev/Documents/1PhD/project-1-N450/project-1.1-Data-desc/results.t/mafft-msa-results/de_filtered_id_genotype_date.fasta"


# Check if the output file exists and prevent overwriting
if [[ -f "$OUTPUT_FILE" ]]; then
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    OUTPUT_FILE="output_$TIMESTAMP.log"
    echo "Output file exists. Using new file: $OUTPUT_FILE"
fi


# Your Bash commands go here
echo "Running the script for IQtree and calculating ML" | tee -a "$INPUT_FILE"

# Example Bash commands (replace these with your actual script)
echo "Listing files in the current directory:" | tee -a "$OUTPUT_FILE"

iqtree -s INPUT_FILE -m TEST -bb 1000


echo "Script executed successfully." | tee -a "$OUTPUT_FOLDER"
