FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && \
    apt-get install -y gcc python3-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

ENV PYTHONUNBUFFERED=1

COPY ./main.py /code/
COPY ./controller.py /code/
COPY ./service.py /code/
COPY ./repository.py /code/

CMD ["python", "main.py"]
