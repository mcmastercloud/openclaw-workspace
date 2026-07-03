#!/usr/bin/env node
import path from "node:path";
import fs from "node:fs";

/**
 * Direct OpenClaw HTTP Gateway Wrapper
 * Usage: node ask-gateway.js "Your prompt here"
 */

// 1. Grab configuration from environment variables
const GATEWAY_URL = process.env.OPENCLAW_URL;
const GATEWAY_TOKEN = process.env.OPENCLAW_TOKEN;

// 2. Fast sanity checks
if (!GATEWAY_URL || !GATEWAY_TOKEN) {
  console.error('\x1b[31mError: OPENCLAW_URL and OPENCLAW_TOKEN environment variables must be set.\x1b[0m');
  process.exit(1);
}

const targetUrl = `${GATEWAY_URL.replace(/\/$/, '')}/tools/invoke`;

async function callOpenClawGateway() {
  try {
    const response = await fetch(targetUrl, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${GATEWAY_TOKEN}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "tool": "lobster",
         "args": {
          "action": "run",
          "pipeline": "/home/node/.openclaw/workspace/flows/morning_brief/morning-brief.lobster",
	  "timeoutMs": 120000
        }
      })
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Gateway returned HTTP ${response.status}: ${errorText}`);
    }

    const data = await response.json();

    // 4. Output the raw text response from the agent/model object
    // OpenClaw standard output typically maps to data.output or data.response
    const modelOutput = data.output || data.response || JSON.stringify(data.result.details, null, 2);
    console.log(modelOutput);

  } catch(error) {
      console.error('\x1b[31mGateway Communication Failed:\x1b[0m', error.message);
      process.exit(1);
  }
}

callOpenClawGateway()
