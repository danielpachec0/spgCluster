FROM grafana/k6:latest

WORKDIR /k6

COPY test.js .
COPY input.gif .

ENTRYPOINT ["k6", "run", "/k6/test.js"]