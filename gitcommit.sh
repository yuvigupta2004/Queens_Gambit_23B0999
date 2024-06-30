 #!/bin/bash

 git add .
 git status
 echo $1
 git commit -m $1
 git push origin master