FROM python:3.13-slim

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install git
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
WORKDIR /workspaces/python-wiremock
COPY pyproject.toml uv.lock ./
ENV UV_PROJECT_ENVIRONMENT=/usr/local
RUN uv sync --frozen