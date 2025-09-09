# Define the output file
OUTPUT_FILE="./de_filtered_id_genotype_date_aln.fasta.timetree.nex"

# Extract the output folder from the output file path
#OUTPUT_FOLDER="."

# Correct the input file assignment (ensure the path is properly assigned)
INPUT_FILE="./de_filtered_id_genotype_date_aln.fasta"  # Corrected

# Check if the output file exists and prevent overwriting
if [[ -f "$OUTPUT_FILE" ]]; then
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    OUTPUT_FILE="output_$TIMESTAMP.log"
    echo "Output file exists. Using new file: $OUTPUT_FILE"
fi

# Your Bash commands go here
#echo "Running the script for IQtree and calculating ML" | tee -a "$OUTPUT_FOLDER"  # Log output to file

# Example Bash commands (replace these with your actual script)
#echo "Listing files in the current directory:" | tee -a "$OUTPUT_FOLDER"  # Log output to file

# Run IQtree (ensure that $INPUT_FILE is correctly passed)
iqtree -s "$INPUT_FILE" --date TAXNAME -B 1000 -pre "trial-8"

#echo "Script executed successfully." | tee -a "$OUTPUT_FOLDER/$(basename "$OUTPUT_FOLDER")"  # Log completion
