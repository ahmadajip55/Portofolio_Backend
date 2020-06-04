#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&
#cd /ajay-task/www/Portofolio_Backend #helloworld
#git pull

source ~/.profile
echo "$DOCKER_PASSWORD" | docker login --username $DOCKER_USERNAME --password-stdin
sudo docker stop restdemo
sudo docker rm restdemo
sudo docker rmi ahmadajip55/rest-tutorial:latest
sudo docker run -d --name restdemo -p 5000:5000 ahmadajip55/rest-tutorial:latest
