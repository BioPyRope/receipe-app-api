#拉image
FROM python:3.9-alpine3.13
LABEL maintainer="bill0704"
#緩存
ENV PYTHONBUFFERED 1
#將檔案送到image並到app資料夾
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000
#開起虛擬環境並安裝我想要的東西
#移除tmp資料夾
#新的liunx增加一個使用者
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user