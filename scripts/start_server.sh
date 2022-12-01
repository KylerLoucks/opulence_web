#!/bin/bash
cd /home/ec2-user
systemctl start nginx
runuser -l ec2-user -c 'screen -dmS "backend" python3.9 main.py'