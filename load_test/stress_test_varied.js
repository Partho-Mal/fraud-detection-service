import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },  // Ramp to 50 users
    { duration: '1m', target: 50 },   // Hold
    { duration: '30s', target: 0 },   // Cool down
  ],
  thresholds: {
    http_req_duration: ['p(95)<100'],
  },
};

export default function () {
  const url = 'http://host.docker.internal:8000/predict';
  
  // 1. Determine User Type (80% Safe, 20% Fraud)
  const isSafeUser = Math.random() < 0.8;

  let payload;

  if (isSafeUser) {
    // SCENARIO A: Normal User (US, Low Amount, Chip Card)
    // The model should PASS this. Legacy rules might pass or fail it.
    payload = JSON.stringify({
      amount_cents: Math.floor(Math.random() * 5000) + 100, // $1 - $50
      transaction_country: "IN",
      channel: "POS",
      entry_mode: "CHIP"
    });
  } else {
    // SCENARIO B: Fraudster (NG, High Amount, Online)
    // The model should BLOCK this.
    payload = JSON.stringify({
      amount_cents: Math.floor(Math.random() * 50000) + 10000, // $100 - $600
      transaction_country: "NG",
      channel: "ONLINE",
      entry_mode: "APP"
    });
  }

  const params = { headers: { 'Content-Type': 'application/json' } };
  const res = http.post(url, payload, params);

  check(res, { 'is status 200': (r) => r.status === 200 });
  sleep(0.1);
}