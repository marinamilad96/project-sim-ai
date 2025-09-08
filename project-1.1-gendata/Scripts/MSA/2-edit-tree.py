from ete4 import Tree

# Load your Newick tree
tree = Tree(open("project-1-N450/project-1.1-Data-desc/results.t/mafft-msa-results/trial-8/trial-8.timetree.nwk"))

# Traverse the tree and check for the clade with the given attributes
for node in tree.traverse():
    # Assuming you know how to identify the clade based on the attributes
    # (adjust these attributes according to how your tree stores them)
    if (hasattr(node, 'dist') and node.dist == 1.2055 and  # Branch length
        hasattr(node.up, 'age') and node.up.age == 1.2103 and  # Parent age
        hasattr(node, 'age') and node.age == 0.0048075 and  # Child age
        hasattr(node, 'name') and node.name == "92"):  # Child label
        print(f"Found the clade with label {node.name}")
        node.delete()  # Remove this clade from the tree

tree.explore()

# Save the new tree to a file
#tree.write(outfile="project-1-N450/project-1.1-Data-desc/results.t/mafft-msa-results/trial-8/modified_tree.nwk")

modified_tree = Tree(open("project-1-N450/project-1.1-Data-desc/results.t/mafft-msa-results/trial-8/modified.tree"))
modified_tree.explore()

"""
Done
"""