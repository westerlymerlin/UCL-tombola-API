#!/bin/bash

# Script to pull the master branch from github
echo "
**** pulling the master branch from github ****
"
cd /home/tompi/github/UCL-tombola/
git pull origin master
cd /home/tompi/

echo "
******** git pull completed ********
"
