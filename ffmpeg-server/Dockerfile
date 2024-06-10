FROM ubuntu:latest
LABEL authors="daniel"
FROM golang:1.22 as builder
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY go.mod ./
RUN go mod download
COPY main.go .
RUN CGO_ENABLED=1 GOOS=linux go build -a -installsuffix cgo -o /go-ffmpeg
EXPOSE 8080
CMD ["/go-ffmpeg"]