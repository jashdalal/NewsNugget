FROM node:20.12.2

WORKDIR /usr/src/app/frontend

RUN npm install -g http-server

COPY . .

EXPOSE 8080

CMD [ "http-server", "-c-1" ]

