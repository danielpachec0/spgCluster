import http from 'k6/http';
import { sleep, check } from 'k6';
//import http from 'k6/http';
import { randomString } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

export let options = {
    duration: '30m',
    vus: 100,
    setupTimeout: '4m',
};

const n = randomIntBetween(5000, 5500)
const s = randomString(n);

export function setup() {
    console.log('Setup function is running...');
    sleep(90)
    console.log("starting")
    return { startTime: new Date().toISOString() };
}

export default function(data) {
    
    let response = "response"
    console.log(`VU: ${__VU} - Iteration: ${__ITER} - msg: ${s}`);
    sleep(0.3)
}

export function teardown(data) {
    console.log('Cleanup tasks are now being performed.');
    let endTime = new Date().toISOString();
    const testRunId = __ENV.TEST_IDENTIFIER; 
    http.post('http://k6-collector-service.k6.svc.cluster.local:8080/tests', JSON.stringify({
         uuid: testRunId,
         start: data.startTime,
         end: endTime
     }), {
         headers: { 'Content-Type': 'application/json' },
     });
}
