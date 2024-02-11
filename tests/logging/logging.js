import { sleep, check } from 'k6';
import http from 'k6/http';

export let options = {
    duration: '30m',
    vus: 500,
};

export default function () {
    
    let response = "response"
    //let response = http.get('http://test.k6.io');
    console.log(`VU: ${__VU} - Iteration: ${__ITER} - Response time: ${response.timings.duration}ms`);

    sleep(0.05);
}

export function teardown() {
    console.log('Cleanup tasks are now being performed.');
    console.log(__VU)
    if(__VU == 0){
        console.log("logging from v0")
    }
}
