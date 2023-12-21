#!/bin/bash

# CICD Script to check if there is a new push to github and auto deploy it

echo "**** fetching the master branch from github ****"
cd /home/tompi/github/UCL-tombola/
git fetch origin master
echo "**** checking if a newer version of the app is available in github ****"
UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

if [ $LOCAL = $REMOTE ]; then
    echo "**** app is up-to-date so nothing to do - exiting ****"
elif [ $LOCAL = $BASE ]; then
    echo "newer version in github so I will update the app"
    git pull origin master
    cd /home/tompi
    echo "**** stopping gunicorn and python app ****"
    sudo systemctl stop gunicorn.service
    echo "**** gunicorn and python stopped ****"
    echo "**** copying files from cloned github repo ****"
    cp -r /home/tompi/github/UCL-tombola/*  /home/tompi/
    echo "**** all files copied ****"
    echo "**** setting flags on bin folder ****"
    chmod 755 /home/tompi/bin/*.sh
    echo "**** restarting gunicorn and python ****"
    sudo systemctl start gunicorn.service
    echo "**** gunicorn started ****"
    echo "******** new deployment has completed - please test ********"
else
    echo "There was a problem so please check and manually update"
fi

