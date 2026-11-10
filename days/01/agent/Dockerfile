FROM python:3.13-slim
WORKDIR /app
COPY days/01/agent/src/ ./src/
COPY days/01/agent/tests/ ./tests/
RUN python -m unittest discover -s tests
USER 65532:65532
ENTRYPOINT ["python", "src/solve.py"]
