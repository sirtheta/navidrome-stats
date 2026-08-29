FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_DEV=1

WORKDIR /app

# Copy only dependency files first (for better caching)
COPY pyproject.toml uv.lock ./

# Install dependencies in a separate layer (cached unless dependencies change)
RUN uv sync --frozen

# Copy the rest of the application code
COPY . .

EXPOSE 5000

ENTRYPOINT ["sh", "./entrypoint.sh"]
