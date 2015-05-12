import pstats
p = pstats.Stats('restats')
p.sort_stats('calls')
p.print_stats(100)