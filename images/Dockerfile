FROM python:3.12-slim

LABEL MAINTAINER="AkizaShyn"
LABEL Version="1.0"

ARG USER=pydyn

WORKDIR /usr/srv/app

RUN useradd --user-group --system --no-log-init --create-home ${USER}

RUN mkdir -p logs && chown -R ${USER}:${USER} /usr/srv/app

COPY --chown=${USER}:${USER} src/* ./

USER ${USER}

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./__main__.py" ]