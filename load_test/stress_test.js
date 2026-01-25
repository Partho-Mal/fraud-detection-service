// RUN:
// docker run --rm -i \
//   -v "$PWD/load_test:/src" \
//   --add-host=host.docker.internal:host-gateway \
//   grafana/k6 run /src/stress_test.js

import http from 'k6/http';
import { check, sleep } from 'k6';

// 1. Configuration: Load pattern and Success Criteria
export const options = {
  stages: [
    { duration: '30s', target: 10 },  // Warm up: Ramp to 10 users
    { duration: '1m', target: 50 },   // Normal Load: Hold at 50 users
    { duration: '30s', target: 100 }, // Stress Spike: Jump to 100 users
    { duration: '30s', target: 0 },   // Cool down
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'],   // Error rate must be < 1%
    http_req_duration: ['p(95)<200'],   // 95% of requests must complete in <200ms
  },
};

export default function () {
  // NOTE: 'host.docker.internal' allows the container to talk to your machine
  const url = 'http://host.docker.internal:8000/predict';

  // 2. Data Generation: Randomize amount to prevent caching
  const amount = Math.floor(Math.random() * 100000) + 100;
  
  const payload = JSON.stringify({
    amount_cents: amount,
    transaction_country: "NG",
    channel: "ONLINE",
    entry_mode: "APP"
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  // 3. Execution
  const res = http.post(url, payload, params);

  // 4. Verification
  check(res, {
    'is status 200': (r) => r.status === 200,
  });

  // 5. Pacing: Wait between 0.1s and 1s (simulating real user speed)
  sleep(Math.random() * 0.9 + 0.1);
}