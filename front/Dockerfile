FROM node:16-alpine

WORKDIR /code

COPY ./package.json /code/package.json
COPY ./package-lock.json /code/package-lock.json

COPY ./src /code/src
COPY ./public /code/public
COPY ./react-fix.py /code/react-fix.py
RUN npm install

RUN apk add --no-cache python3
RUN python react-fix.py

CMD ["npm", "start"]

