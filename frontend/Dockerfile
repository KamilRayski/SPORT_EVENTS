# Etap 1: build aplikacji
FROM node:16-alpine as build

WORKDIR /app
COPY package.json .
COPY package-lock.json .
#RUN npm install
RUN npm install --legacy-peer-deps

COPY . .
RUN npm run build

# Etap 2: serwer Nginx
FROM nginx:alpine
COPY default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
