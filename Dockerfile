FROM node:26.13.1-trixie-slim AS frontend-build

WORKDIR /frontend

RUN npm install --global pnpm@12.21.0

COPY frontend/package.json frontend/pnpm-lock.yaml ./

RUN pnpm install --frozen-lockfile

COPY frontend/ ./

RUN pnpm build

FROM python:3.14-slim-trixie

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/
COPY config.toml ./
COPY --from=frontend-build /frontend/dist/ ./frontend/dist/

RUN uv sync --locked --no-dev --no-editable

CMD ["/app/.venv/bin/python", "-m", "youtube_channel_monitor.main"]
