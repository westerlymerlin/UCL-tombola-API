# /bin/bash
sudo systemctl stop gunicorn.service
sudo systemctl stop nginx
sudo systemctl start nginx
sudo systemctl start gunicorn.service

