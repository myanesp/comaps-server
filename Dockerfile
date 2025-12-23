FROM python:3.13-alpine

WORKDIR /app

RUN apk add --no-cache \
        ca-certificates \
        curl \
        nginx \
    && update-ca-certificates

COPY /app/comaps.py .

RUN pip install --no-cache-dir requests

RUN mkdir -p /maps /run/nginx

COPY /app/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD sh -c "python -u comaps.py && nginx -g 'daemon off;'"

VOLUME ["/maps"]





