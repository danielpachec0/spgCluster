import http from 'k6/http';
import {sleep} from 'k6';
import tracing from 'k6/x/tracing';
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

export const options = {
    vus: 100,
    duration: "30m",
    setupTimeout: '4m', 
};

//const endpoint = "tempo-distributor.tempo.svc.cluster.local:4317"
//const endpoint = "tempo.tempo.svc.cluster.local:4317"
const endpoint = "jaeger-collector.jaeger.svc.cluster.local:4317"

const client = new tracing.Client({
    endpoint,
    exporter: tracing.EXPORTER_OTLP,
    insecure: true,
});

const traceDefaults = {
    attributeSemantics: tracing.SEMANTICS_HTTP,
    attributes: {"one": "three"},
    randomAttributes: {count: 2, cardinality: 5}
}

const traceTemplates = [
    {
        defaults: traceDefaults,
        spans: [
            {service: "shop-backend", name: "list-articles", duration: {min: 200, max: 900}},
            {service: "shop-backend", name: "authenticate", duration: {min: 50, max: 100}},
            {service: "auth-service", name: "authenticate"},
            {service: "shop-backend", name: "fetch-articles", parentIdx: 0},
            {service: "article-service", name: "list-articles"},
            {service: "article-service", name: "select-articles", attributeSemantics: tracing.SEMANTICS_DB},
            {service: "postgres", name: "query-articles", attributeSemantics: tracing.SEMANTICS_DB, randomAttributes: {count: 5}},
        ]
    },
    {
        defaults: {
            attributes: {"numbers": ["one", "two", "three"]},
            attributeSemantics: tracing.SEMANTICS_HTTP,
        },
        spans: [
            {service: "shop-backend", name: "article-to-cart", duration: {min: 400, max: 1200}},
            {service: "shop-backend", name: "authenticate", duration: {min: 70, max: 200}},
            {service: "auth-service", name: "authenticate"},
            {service: "shop-backend", name: "get-article", parentIdx: 0},
            {service: "article-service", name: "get-article"},
            {service: "article-service", name: "select-articles", attributeSemantics: tracing.SEMANTICS_DB},
            {service: "postgres", name: "query-articles", attributeSemantics: tracing.SEMANTICS_DB, randomAttributes: {count: 2}},
            {service: "shop-backend", name: "place-articles", parentIdx: 0},
            {service: "cart-service", name: "place-articles", attributes: {"article.count": 1, "http.status_code": 201}},
            {service: "cart-service", name: "persist-cart"}
        ]
    },
    {
        defaults: traceDefaults,
        spans: [
            {service: "shop-backend", attributes: {"http.status_code": 403}},
            {service: "shop-backend", name: "authenticate", attributes: {"http.request.header.accept": ["application/json"]}},
            {service: "auth-service", name: "authenticate", attributes: {"http.status_code": 403}},
        ]
    },
]

export function setup() {
    console.log('Setup function is running...');
    sleep(60)
    console.log("starting")
    return { startTime: new Date().toISOString() };
}

export default function (data) {
    const templateIndex = randomIntBetween(0, traceTemplates.length-1)
    const gen = new tracing.TemplatedGenerator(traceTemplates[templateIndex])
    client.push(gen.traces())

    sleep(0.3);
}

export function teardown(data) {
    client.shutdown();
    console.log('Cleanup tasks are now being performed.');
    let endTime = new Date().toISOString();
    const testRunId = __ENV.TEST_IDENTIFIER; 
    http.post('http://k6-collector-service.k6.svc.cluster.local:8080/tests', JSON.stringify({
         uuid: testRunId,
         start: data.startTime,
         end: endTime
     }), {
         headers: { 'Content-Type': 'application/json' },
     });}
