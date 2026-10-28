FROM node:24-bookworm-slim AS node

FROM python:3.14-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       git ca-certificates libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=node /usr/local/ /usr/local/

RUN npm install --global pnpm@11 --ignore-scripts

RUN useradd --create-home --shell /bin/bash developer

USER developer

RUN python -m venv /home/developer/.venv

ENV PATH="/home/developer/.venv/bin:${PATH}"

WORKDIR /workspace
