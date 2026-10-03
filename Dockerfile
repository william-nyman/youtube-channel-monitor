FROM denoland/deno:bin-2.9.4 AS deno

FROM python:3.14-slim

COPY --from=deno /deno /usr/local/bin/deno

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY config.toml ./

RUN pip install --no-cache-dir .

CMD ["ytmonitor", "run"]
