import os
from misc.new_directory import new_directory
from misc.get_MPDE_columns_from_file import get_MPDE_columns_from_file
from misc.hypergeometric_test import hypergeometric_test

def undirectional_overlaps(mpde_file_path, out_path, pde_IDs, overlap_statistics_list):

    # stores overlap stats
    overlap_statistics_dict = {}

    # infile
    mpde_file = open(mpde_file_path).readlines()

    # iterates through the pairwise combinations of PDEs
    for pde1_id in pde_IDs:
        for pde2_id in pde_IDs:

            # excludes self comparing
            if pde1_id != pde2_id:

                pde1_id_parsed = pde1_id.replace(" ","_")
                pde2_id_parsed = pde2_id.replace(" ","_")

                # makes the directory
                new_directory(os.path.join(out_path,"undirectional",pde1_id_parsed,pde2_id_parsed))

                # gets the fold and significance columns for the PDEs
                pde1_log2fold,pde1_p,pde1_padj,pde1_sig,pde1_valid = get_MPDE_columns_from_file(mpde_file, pde1_id)
                pde2_log2fold, pde2_p, pde2_padj, pde2_sig, pde2_valid = get_MPDE_columns_from_file(mpde_file, pde2_id)

                # stores the genes in each group
                pde1_unique_genes_IDs = []
                pde1_unique_genes_symbols = []
                pde2_unique_genes_IDs = []
                pde2_unique_genes_symbols = []
                overlapping_genes_IDs = []
                overlapping_genes_symbols = []

                # gets the genes in each group
                header = True
                for line in mpde_file:
                    if header:
                        header = False
                    else:
                        line_split = line.rstrip().split("\t")

                        # pde1 unique
                        if line_split[pde1_sig] == "True" and line_split[pde2_sig] == "False":
                            pde1_unique_genes_IDs.append(line_split[0])
                            pde1_unique_genes_symbols.append(line_split[1])
                        # pde2 unique
                        elif line_split[pde1_sig] == "False" and line_split[pde2_sig] == "True":
                            pde2_unique_genes_IDs.append(line_split[0])
                            pde2_unique_genes_symbols.append(line_split[1])
                        # overlapping
                        elif line_split[pde1_sig] == "True" and line_split[pde2_sig] == "True":
                            overlapping_genes_IDs.append(line_split[0])
                            overlapping_genes_symbols.append(line_split[1])


                # outputs the gene lists
                pde1_unique_genes_IDs_file = open(os.path.join(out_path,"undirectional",pde1_id_parsed,pde2_id_parsed,"IDs_" + pde1_id_parsed + "_unique_genes.txt"),"w")
                pde1_unique_genes_symbols_file = open(os.path.join(out_path,"undirectional",pde1_id_parsed,pde2_id_parsed,"symbols_" + pde1_id_parsed + "_unique_genes.txt"),"w")
                pde2_unique_genes_IDs_file = open(os.path.join(out_path,"undirectional",pde1_id_parsed,pde2_id_parsed,"IDs_" + pde2_id_parsed + "_unique_genes.txt"),"w")
                pde2_unique_genes_symbols_file = open(os.path.join(out_path,"undirectional",pde1_id_parsed,pde2_id_parsed,"symbols_" + pde2_id_parsed + "_unique_genes.txt"),"w")
                overlapping_genes_IDs_file = open(os.path.join(out_path,"undirectional",pde1_id_parsed,pde2_id_parsed,"IDs_overlapping_genes.txt"),"w")
                overlapping_genes_symbols_file = open(os.path.join(out_path,"undirectional",pde1_id_parsed,pde2_id_parsed,"symbols_overlapping_genes.txt"),"w")

                pde1_unique_genes_IDs_file.write("\n".join(pde1_unique_genes_IDs))
                pde1_unique_genes_symbols_file.write("\n".join(pde1_unique_genes_symbols))
                pde2_unique_genes_IDs_file.write("\n".join(pde2_unique_genes_IDs))
                pde2_unique_genes_symbols_file.write("\n".join(pde2_unique_genes_symbols))
                overlapping_genes_IDs_file.write("\n".join(overlapping_genes_IDs))
                overlapping_genes_symbols_file.write("\n".join(overlapping_genes_symbols))


                # gets the overlap stats
                background_size = len(mpde_file) -1
                candidate_size = len(pde1_unique_genes_IDs) + len(overlapping_genes_IDs)
                gene_set_size = len(pde2_unique_genes_IDs) + len(overlapping_genes_IDs)
                overlap_size = len(overlapping_genes_IDs)
                obs_vs_exp, p_Pos, p_Neg = hypergeometric_test(background_size, candidate_size, gene_set_size, overlap_size)

                # updates the overlap stats (considers A vs B the same as B vs A)
                sorted_pde = "\t".join(sorted([pde1_id,pde2_id]))
                if sorted_pde not in overlap_statistics_dict:
                    overlap_statistics_list.append([pde1_id,pde2_id,background_size, candidate_size, gene_set_size,len(pde1_unique_genes_IDs),len(pde2_unique_genes_IDs),overlap_size,obs_vs_exp,p_Neg])
                overlap_statistics_dict[sorted_pde] = True


    return overlap_statistics_list


