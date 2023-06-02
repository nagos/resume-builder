FROM node:18 as build
WORKDIR /src
COPY . .
RUN npm install && npm run build

FROM nginx
EXPOSE 80/tcp
COPY --from=build /src/build/ /usr/share/nginx/html/
