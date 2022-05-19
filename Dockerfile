# syntax=docker/dockerfile:1
FROM python:3.9-alpine3.13
LABEL maintainer="saharavsh7192@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./hangmangame /app
COPY ./scripts /scripts

WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev gcc python3-dev musl-dev linux-headers && \
    apk add jpeg-dev zlib-dev libjpeg && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

CMD ["run.sh"]