import { defineConfig, devices } from '@playwright/test';
import * as path from 'path';
import * as child_process from 'child_process';

const serverScript = `
const http = require('http');
const fs = require('fs');
const path = require('path');
http.createServer((req, res) => {
  fs.readFile('${path.join('/home/hochoy/.openclaw/workspace-coder', 'voicepix.html').replace(/'/g, "'\"'\"'")}', (err, data) => {
    if (err) { res.writeHead(500); res.end(); return; }
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end(data);
  });
}).listen(8765);
`;

export default defineConfig({
  testDir: './tests',
  timeout: 30000,
  expect: { timeout: 10000 },
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  reporter: [['list'], ['html', { open: 'never' }]],
  use: {
    baseURL: 'http://localhost:8765',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: `node -e "${serverScript}"`,
    port: 8765,
    reuseExistingServer: true,
    timeout: 15000,
    stdout: 'ignore',
    stderr: 'ignore',
  },
});
