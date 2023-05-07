# vim: set filetype=Dockerfile:
FROM python:3.11-slim-buster

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update && apt-get install --no-install-recommends -y curl default-jre-headless \
    && curl -sSL https://install.python-poetry.org | python

# Update poetry to latest version
RUN poetry self update

WORKDIR /app/example

# Install dependencies
COPY . /app
COPY ./example/pyproject.toml ./example/poetry.lock /app/example/
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi


# Copy the rest of the application code
COPY ./example /app/example

# Expose the port that the FastAPI app will listen on
EXPOSE 5001
EXPOSE 5002

CMD ["python"]
