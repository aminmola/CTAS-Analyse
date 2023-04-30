#
FROM python:3.9-slim-buster
#
WORKDIR /code
RUN apt-get update
#
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#
EXPOSE 4030

COPY ./ /code/
#
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "2468"]
CMD ["python","main.py"]