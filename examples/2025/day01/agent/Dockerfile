FROM python:3.13-slim
WORKDIR /app
COPY examples/2025/day01/agent/src/ ./src/
COPY examples/2025/day01/agent/tests/ ./tests/
RUN python -m unittest discover -s tests
USER 65532:65532
ENTRYPOINT ["python", "src/solve.py"]
