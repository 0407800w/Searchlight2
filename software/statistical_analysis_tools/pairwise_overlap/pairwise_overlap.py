from statistical_analysis_tools.pairwise_overlap.undirectional_overlaps import undirectional_overlaps
from statistical_analysis_tools.pairwise_overlap.directional_overlaps import directional_overlaps
from statistical_analysis_tools.pairwise_overlap.overlap_stats_table import overlap_stats_table


def pairwise_overlap(mpde_file_path, out_path, pde_IDs):

    # stores the overlap stats
    overlap_statistics_list = []

    # gets the undirectional overlaps
    overlap_statistics_list = undirectional_overlaps(mpde_file_path, out_path, pde_IDs, overlap_statistics_list)

    # gets the directional overlaps
    overlap_statistics_list = directional_overlaps(mpde_file_path, out_path, pde_IDs, overlap_statistics_list)

    # outputs the overlap stats
    overlap_stats_table(out_path, overlap_statistics_list)














