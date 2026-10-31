FROM node:24-alpine AS frontend-build

WORKDIR /frontend

RUN corepack enable

COPY frontend/package.json frontend/pnpm-lock.yaml ./

RUN pnpm install --frozen-lockfile

COPY frontend/ ./

RUN pnpm build

FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY config.toml ./
COPY --from=frontend-build /frontend/dist/ ./frontend/dist/

RUN pip install --no-cache-dir .

CMD ["ytmonitor", "run"]
