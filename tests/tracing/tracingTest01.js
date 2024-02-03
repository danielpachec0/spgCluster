import {sleep} from 'k6';
import tracing from 'k6/x/tracing';
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';


export const options = {
    vus: 1,
    duration: "2m",
};

const endpoint = __ENV.ENDPOINT || " jaeger-collector.jaeger.svc.cluster.local:14268/api/traces"
const client = new tracing.Client({
    endpoint,
    exporter: tracing.EXPORTER_OTLP,
    insecure: true,
});


export default function () {
    let pushSizeTraces = randomIntBetween(2,3);
    let pushSizeSpans = 0;
    let t = [];
    for (let i = 0; i < pushSizeTraces; i++) {
        let c = randomIntBetween(5,10)
        pushSizeSpans += c;

        t.push({
            random_service_name: false,
            spans: {
                count: c,
                size: randomIntBetween(300,1000),
                random_name: true,
                fixed_attrs: {
                    "test": "test",
                },
            }
        });
    }

    let gen = new tracing.ParameterizedGenerator(t)
    let traces = gen.traces()
    client.push(traces);

    console.log(`Pushed ${pushSizeSpans} spans from ${pushSizeTraces} different traces. Here is a random traceID: ${t[Math.floor(Math.random() * t.length)].id}`);
    sleep(15);
}

export function teardown() {
    client.shutdown();
}
