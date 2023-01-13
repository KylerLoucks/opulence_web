# Multistage build
FROM node:latest as build-stage
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
RUN npm run build

FROM nginx as production-stage
# Copy 'dist' folder into prod-stage /app directory
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy 'nginx.conf' to the default server block location, which gets 'included' in /etc/nginx/nginx.conf file
COPY nginx.conf /etc/nginx/conf.d
