FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY swarm_desktop_os/ ./swarm_desktop_os/
COPY tests/ ./tests/

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["swarm-desktop-os"]
CMD ["demo"]
