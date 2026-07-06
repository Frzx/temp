FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir uv \
    && uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:${PATH}"

EXPOSE 3000

CMD ["sh", "-c", "doris-mcp-server --transport http --host ${MCP_HOST:-0.0.0.0} --port ${MCP_PORT:-3000} --doris-host ${DORIS_HOST} --doris-port ${DORIS_PORT:-9030} --doris-user ${DORIS_USER} ${DORIS_PASSWORD:+--doris-password \\\"$DORIS_PASSWORD\\\"}"]
