FROM python:3.12-alpine AS production

WORKDIR /code

RUN apk add --no-cache \
  build-base \
  gcc \
  g++ \
  musl-dev \
  linux-headers

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY . /code/

RUN uv sync --frozen --no-cache

EXPOSE 8080

# Run both FastAPI and cron jobs
CMD ["/bin/sh", "-c", "(/code/.venv/bin/python -u /code/cron_jobs.py 2>&1 | sed 's/^/[CRON] /' &) && (/code/.venv/bin/fastapi run --host 0.0.0.0 --port 8080 /code/src/main.py 2>&1 | sed 's/^/[API] /' &) && wait"]
