#!/bin/bash
cd /home/seu_usuario/regulus
git pull origin main
sudo docker compose pull
sudo docker compose up -d --build
echo "Deploy Docker concluído: $(date)" >> deploy.log
