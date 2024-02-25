FROM ubuntu:latest
LABEL authors="daniel"
FROM golang:1.22 as builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY main.go .
RUN CGO_ENABLED=1 GOOS=linux go build -a -installsuffix cgo -o  /collector
CMD ["/collector"]
