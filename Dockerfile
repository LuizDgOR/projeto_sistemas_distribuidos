FROM python:3.12.3-alpine3.20

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./application /application

WORKDIR /application
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers python3-dev && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home application && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R root:root /vol && \
    chmod -R 755 /vol

ENV PATH="/py/bin:$PATH"

