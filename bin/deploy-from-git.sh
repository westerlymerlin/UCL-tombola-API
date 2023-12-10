#!/bin/bash

# copy the code from the cloned got repo to the working folders of the raspbery pi

echo "
**** stopping gunicorn and python app ****
"

sudo systemctl stop gunicorn.service
echo "
**** gunicorn and python stopped ****"

echo "**** copying files from cloned github repo ****
"
cp -r /home/tompi/github/UCL-tombola/*  /home/tompi/
echo "**** all files copied ****"
echo "**** setting flags on bin folder ****"
chmod 755 /home/tompi/bin/*.sh

echo "
**** restarting Gunicorn and python ****
"
sudo systemctl start gunicorn.service
echo "
**** gunicorn started ****"

echo "
******** deployment has completed - please test ********"

