# refine tree (takes time) and add traits to the tree
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

# traits
augur traits \
  --tree results/tree.nwk \
  --metadata results/metadata.tsv \
  --output-node-data results/traits.json \
  --column name type date \
  --confidence

# export
augur export v2 \
  --tree results/tree.nwk \
  --metadata results/metadata.tsv \
  --node-data results/branch_lengths.json \
              results/traits.json \
  --color-by-metadata type \
  --output results/auspice/measles-n450.json

# view
nextstrain view results/auspice/measles-n450.json