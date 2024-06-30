 #!/bin/bash

python3 -m cProfile -o profiling/profile_data.prof checktheengine.py 
/bin/python3 /home/yuvigupta/Queens_Gambit/Week_4/profiling/analyze_profile.py > profiling/profile.txt