from Bio import Phylo

tree = Phylo.read(
    "/Users/MiladM-Dev/Documents/1PhD/project-1-N450/git_trial/SEID_p_m1_LI_1.full.trees", "nexus")

# Tree length (sum of all branches)
tree_length = tree.total_branch_length()

# Tree height (max root-to-tip distance)


def get_height(clade, dist=0):
    if clade.is_terminal():
        return dist
    return max(get_height(c, dist + c.branch_length) for c in clade.clades)


tree_height = get_height(tree.root)

print("Tree length:", tree_length)
print("Tree height:", tree_height)
