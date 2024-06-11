import http from 'k6/http';
import { sleep } from 'k6';
import { check } from 'k6';

export let options = {
    vus: 1,
    iterations: 15,
};

const url = 'http://localhost:8080/upload';
const videoFile = open('input.gif', 'b');
const formData = {
    video: http.file(videoFile, 'input.gif', 'image/gif'),
    command: "-movflags faststart -pix_fmt yuv420p"
};

export function setup() {
    console.log('Setup function is running...');
    console.log("starting")
}

export default function () {
    console.log(__ITER)

    let res = http.post(url, formData);

    check(res, {
        'status is 200': (r) => r.status === 200,
        'response is a video': (r) => r.headers['Content-Type'] === 'video/mp4',
    });

    if (__ITER < 5) {
        sleep(15);
    } else if (__ITER < 10) {
        sleep(10);
    } else {
        sleep(5);
    }
}

export function teardown(data) {
    console.log('Cleanup tasks are now being performed.');
    let endTime = new Date().toISOString();
    const testRunId = __ENV.TEST_IDENTIFIER;
    console.log(testRunId)
    console.log(endTime)
}