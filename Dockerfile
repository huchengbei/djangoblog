FROM python:3.6.6-alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
RUN apk update && apk add \
        python3-dev \
        zlib-dev \
        libuuid \
        pcre \
        mailcap \
        gcc \
        libc-dev \
        linux-headers \
        pcre-dev
RUN apk add \
        mariadb-dev
RUN apk add \
        libjpeg-turbo-dev

WORKDIR /opt/src
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/  --no-cache-dir uwsgi
COPY . ./
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/  --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic --noinput
ENTRYPOINT ["uwsgi","--ini", "/djangoblog/uwsgi.ini"]