 #!/bin/bash

python3 -m cProfile -o profile_data.prof checktheengine.py 
/bin/python3 /home/yuvigupta/Queens_Gambit/Week_4/analyze_profile.py > profile.txt