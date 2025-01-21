FROM node:22

WORKDIR /usr/src/app/

COPY ./services/relay-service/package.json ./services/relay-service/yarn.lock ./
RUN yarn

COPY ./services/relay-service/tsconfig.json ./

COPY ./services/relay-service/src/ ./src/
COPY ./services/relay-service/nest-cli.json ./
COPY ./services/relay-service/server.js ./

RUN yarn build

CMD ["yarn", "start:prod"]
