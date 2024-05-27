FROM python:3.12-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apk add build-base linux-headers
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
ENV PYTHONUNBUFFERED=1


COPY ./main.py /code/
COPY ./controller.py /code/
COPY ./repository.py /code/
ADD ./routes/ /code/routes
CMD ["python", "main.py"]