#   *----- Global variables -----*
ARG APP_USER=pushup
ARG APP_DIR=/opt/pushupclub

#   *----- Python base -----*
# Stage for setting up base python image
FROM python:3.11.6-slim as python-base
ENV \
    # Keeps Python from generating .pyc files in the container
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    DEBIAN_FRONTEND=noninteractive

#   *----- Dependencies -----*
# Stage for installing deps
FROM python-base as deps

# Installing project dependencies
RUN apt-get update && apt-get -y install -y curl libpq-dev build-essential python3-dev jq
RUN curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64
RUN chmod +x /usr/local/bin/dbmate
RUN python -m pip install --upgrade pip
RUN python -m pip install poetry
RUN python -m poetry self update
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry config virtualenvs.create false
RUN python -m poetry install


#   *----- Backend base -----*
# Stage for setting up project files and directories
FROM deps as pushup
ARG APP_USER
ARG APP_DIR

# Create a group and user
# NOTE: switching to non-root takes place in derived images
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}
# Switch to non-root
USER ${APP_USER}:${APP_USER}

# Create project directory and copy files
WORKDIR /${APP_DIR}
COPY . .


#   *----- Backend image -----*
# Image for development
# dbmate -d "./src/db/migrations" -e DB__MIGRATION_URL --wait migrate &&
FROM pushup as pushup-backend
CMD uvicorn main:app --reload --host 0.0.0.0 --port 8000
