FROM python:3.12-slim

WORKDIR /usr/srv/app
RUN mkdir logs

COPY src/* ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./__main__.py" ]