FROM python:3.12-alpine
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
ENV PYTHONUNBUFFERED=1

COPY ./main.py /code/
CMD ["python", "main.py"]