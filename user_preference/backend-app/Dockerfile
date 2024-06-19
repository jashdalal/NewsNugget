FROM node:20.12.2

WORKDIR /usr/src/app/backend

COPY package*.json /usr/src/app/backend/

RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]