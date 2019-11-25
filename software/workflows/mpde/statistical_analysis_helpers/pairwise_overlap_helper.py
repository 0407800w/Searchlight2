import os
from statistical_analysis_tools.pairwise_overlap.pairwise_overlap import pairwise_overlap

def pairwise_overlap_helper(out_path, pde_IDs):

    mpde_file_path = os.path.join(out_path, "data", "all_genes_annotated.csv")
    pairwise_overlap_out_path = os.path.join(out_path, "data", "statistical_analysis", "pairwise_overlap")
    pairwise_overlap(mpde_file_path, pairwise_overlap_out_path, pde_IDs)