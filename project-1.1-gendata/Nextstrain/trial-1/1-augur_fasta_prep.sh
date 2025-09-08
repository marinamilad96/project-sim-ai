#Extract Metadata from the fasta file
augur parse \
    --sequences de_filtered_id_genotype_date_fixed.fasta \
    --output-sequences results/sequences.fasta \
    --fields  name type date \
    --output-metadata results/metadata.tsv

#Index the sequences
augur index \
    --sequences results/sequences.fasta \
    --output results/sequence_index.tsv

#Filter the sequences
augur filter \
    --sequences results/sequences.fasta \
    --metadata results/metadata.tsv \
    --output results/filtered.fasta
