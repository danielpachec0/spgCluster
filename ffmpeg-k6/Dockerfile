FROM grafana/k6:latest
LABEL authors="daniel"

# Install ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["top", "-b"]