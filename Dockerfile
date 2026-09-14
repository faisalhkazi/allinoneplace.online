FROM python:3.12-slim
ENV DEBIAN_FRONTEND=noninteractive PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apt-get update \
    && apt-get install -y --no-install-recommends libreoffice-writer libreoffice-calc libreoffice-impress fonts-liberation fonts-dejavu \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . /app
EXPOSE 8765
CMD ["python", "converter-server.py"]
