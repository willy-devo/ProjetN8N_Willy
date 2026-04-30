FROM python:3.11-slim

LABEL maintainer="Devoteam nexDigital"
LABEL description="Agentic4API — Agent Discovery (Chainlit + LangGraph)"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    CHAINLIT_HOST=0.0.0.0 \
    CHAINLIT_PORT=8080

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements_langgraph.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY agent.py chat.py tools.py ./

RUN useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -fsS http://localhost:8080/ || exit 1

CMD ["chainlit", "run", "chat.py", "--host", "0.0.0.0", "--port", "8080", "--headless"]