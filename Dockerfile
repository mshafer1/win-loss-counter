FROM node:22.4-bookworm-slim AS frontend_built

COPY ./frontend/win-loss-counter /app/frontend/win-loss-counter

WORKDIR /app/frontend/win-loss-counter

RUN rm -rf dist node_modules && npm install --no-fund --no-audit

RUN npm run build

FROM python:3.9-bullseye AS python_installed

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y \
# utilities
    tmux \
    nano \
    python-is-python3 \
# envsubst
    gettext-base

RUN python -m pip install -U pip

# setup project venv
RUN mkdir --parent /app/_venv
WORKDIR /app

RUN python -m venv _poetry_venv
RUN /app/_poetry_venv/bin/python -m pip install -U pip wheel poetry==1.8.2

RUN python -m venv _venv
RUN /app/_venv/bin/python -m pip install -U pip wheel

WORKDIR /app/backend

COPY ./backend/pyproject.toml /app/backend/pyproject.toml
COPY ./backend/poetry.lock /app/backend/poetry.lock

RUN . /app/_venv/bin/activate && /app/_poetry_venv/bin/poetry install --no-dev

ENV PATH /app/_venv/bin:$PATH

RUN rm -rf /etc/localtime && ln -s /usr/share/zoneinfo/America/Chicago /etc/localtime


FROM python_installed AS node_installed

# Replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Set debconf to run non-interactively
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# Install base dependencies
RUN apt-get update && apt-get install -y -q --no-install-recommends \
        apt-transport-https \
        build-essential \
        ca-certificates \
        curl \
        git \
        libssl-dev \
        wget \
    && rm -rf /var/lib/apt/lists/*

ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 22.4.0

# Install nvm with node and npm
RUN mkdir ${NVM_DIR} && \
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH      $NVM_DIR/v$NODE_VERSION/bin:$PATH


FROM python_installed AS app_setup

RUN rm -rf /app/frontend

COPY --from=frontend_built /app/frontend/ /app/frontend/

WORKDIR /app/backend

COPY ./backend /app/backend/

COPY ./hosting/config /app/config/

RUN mkdir -p /var/log/uwsgi/
RUN mkdir -p /var/log/uwsgi_socket/
RUN mkdir -p /app/uwsgi

# CMD ["uwsgi", "--ini", "/app/config/wsgi.ini"]
CMD ["python", "-m", "win_loss_counter"]
