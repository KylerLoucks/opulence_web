#!/bin/bash
cd /usr/share/nginx/html
rm -r dist
cd /home/ec2-user/src
sed -i 's,ws://localhost:5000,wss://playopulence.com,1' App.vue
cd /home/ec2-user
npm run build
mv dist /usr/share/nginx/html