import pstats

# Load the profiling data
p = pstats.Stats('/home/yuvigupta/Queens_Gambit/Week_4/profiling/profile_data.prof')

# Strip directories, sort by total time per call, and print only functions from engine.py
p.strip_dirs().sort_stats('cumtime').print_stats('ihatebajaj.py')
