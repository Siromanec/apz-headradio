FROM node:16-alpine

WORKDIR /code

RUN apk add --no-cache python3

COPY ./package.json /code/package.json
COPY ./package-lock.json /code/package-lock.json


COPY ./src /code/src
COPY ./public /code/public
COPY ./react-fix.py /code/react-fix.py
RUN npm install

RUN python react-fix.py

CMD ["npm", "start", "--host", "0.0.0.0:3000"]

