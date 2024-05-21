FROM node:18.19.0 as build-stage
WORKDIR /app
COPY . .
RUN yarn && yarn run docs:build

FROM nginx
COPY --from=build-stage /app/.vitepress/dist /usr/share/nginx/html
