FROM python:alpine3.19

COPY http_server.py .

RUN pip3 install redis

CMD ["python3","http_server.py"]
