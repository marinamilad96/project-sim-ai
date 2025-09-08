augur parse \
    --sequences de_filtered_id_genotype_date_fixed.fasta \
    --output-sequences results/sequences.fasta \
    --fields  name type date \
    --output-metadata results/metadata.tsv

augur index \
    --sequences results/sequences.fasta \
    --output results/sequence_index.tsv

augur filter \
    --sequences results/sequences.fasta \
    --metadata results/metadata.tsv \
    --output results/filtered.fasta

augur align \
    --sequences results/filtered.fasta \
    --method mafft \
    --output results/aligned.fasta \
    --debug

augur tree \
  --alignment results/aligned.fasta \
  --output results/tree_raw.nwk

augur refine \
  --tree results/tree_raw.nwk \
  --alignment results/aligned.fasta \
  --metadata results/metadata.tsv \
  --output-tree results/tree.nwk \
  --output-node-data results/branch_lengths.json \
  --timetree \
  --coalescent opt \
  --date-confidence \
  --date-inference marginal \
  --clock-filter-iqd 4 \
  --stochastic-resolve True

augur traits \
  --tree results/tree.nwk \
  --metadata results/metadata.tsv \
  --output-node-data results/traits.json \
  --column name type date \
  --confidence

augur export v2 \
  --tree results/tree.nwk \
  --metadata results/metadata.tsv \
  --node-data results/branch_lengths.json \
              results/traits.json \
  --color-by-metadata type \
  --output results/auspice/measles-n450.json

nextstrain view results/auspice/measles-n450.json
