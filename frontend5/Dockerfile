FROM nginx:alpine

WORKDIR /usr/share/nginx/html

RUN rm -rf ./*

COPY ./dist .

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY ssl/fullchain.pem /etc/ssl/certs/fullchain.pem
COPY ssl/privkey.pem /etc/ssl/private/privkey.pem

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
