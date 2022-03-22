FROM python:3.7.13-slim-bullseye
LABEL maintainer="r.talalaeva@innopolis.university"

ENV VENV_PATH=/opt/venv \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
ENV PATH="$VENV_PATH/bin:$PATH"
RUN python -m venv $VENV_PATH && \
    useradd -u 42069 --create-home --shell /bin/bash app

WORKDIR /home/app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

USER app

RUN mkdir app

WORKDIR /home/app/app

COPY --chown=app:app . .

EXPOSE 8000
