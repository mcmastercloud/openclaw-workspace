#!/usr/bin/env node
import path from "node:path";
import fs from "node:fs";

/**
 * Direct OpenClaw HTTP Gateway Wrapper (JSON Argument Version)
 * Usage: node llm_invoke_json.js '{"prompt": "...", "payloadFile": "...", "promptFile": "..."}'
 */

// 1. Grab configuration from environment variables
const GATEWAY_URL = process.env.OPENCLAW_URL;
const GATEWAY_TOKEN = process.env.OPENCLAW_TOKEN;
const jsonArg = process.argv[2];

// 2. Fast sanity checks
if (!GATEWAY_URL || !GATEWAY_TOKEN) {
  console.error('\x1b[31mError: OPENCLAW_URL and OPENCLAW_TOKEN environment variables must be set.\x1b[0m');
  process.exit(1);
}

if (!jsonArg) {
  console.error('\x1b[31mError: Please provide a JSON argument string.\x1b[0m');
  process.exit(1);
}

let args;
try {
  args = JSON.parse(jsonArg);
} catch (e) {
  console.error('\x1b[31mError: Invalid JSON argument.\x1b[0m');
  process.exit(1);
}

const { prompt, payloadFile, promptFile, temperature, model } = args;

const targetUrl = `${GATEWAY_URL.replace(/\/$/, '')}/tools/invoke`;

async function getPayload(payloadFile) {
  if (!payloadFile) return {};
  try {
    const resolvedPayloadFile = path.resolve("/home/node/.openclaw/workspace/data/" + payloadFile);
    return JSON.parse(fs.readFileSync(resolvedPayloadFile, "utf8"));
  } catch(error) {
    console.error("Error reading payload file:", error.message);
    process.exit(1);
  }
}

async function getPrompt(prompt, promptFile) {
  if (promptFile) {
    try {
      const resolvedPromptFile = path.resolve("/home/node/.openclaw/workspace/prompts/" + promptFile);
      return fs.readFileSync(resolvedPromptFile, "utf8");
    } catch(error) {
      console.error("Error reading prompt file:", error.message);
      process.exit(1);
    }
  }
  return prompt;
}

async function callOpenClawGateway() {
  try {
    const finalPrompt = await getPrompt(prompt, promptFile);
    const payload = await getPayload(payloadFile);
    
    const body = {
      "tool": "llm-task",
      "args": {
        "prompt": finalPrompt,
        "input": JSON.stringify(payload),
        "provider": "openclaw",
        "model": model || "openrouter/google/gemini-3.1-flash-lite-preview"
      }
    };
    
    if (temperature) {
      body.args.temperature = temperature;
    }
    
    const response = await fetch(targetUrl, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${GATEWAY_TOKEN}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Gateway returned HTTP ${response.status}: ${errorText}`);
    }

    const data = await response.json();
    // The llm-task tool returns the output in data.result
    // We need to extract the actual text response from the result object
    // For llm-task, the output is often in data.result.output or data.result.response
    const result = data.result || data;
    const modelOutput = result.output || result.response || (typeof result === 'string' ? result : JSON.stringify(result, null, 2));
    console.log(modelOutput);

  } catch(error) {
      console.error('\x1b[31mGateway Communication Failed:\x1b[0m', error.message);
      process.exit(1);
  }
}

callOpenClawGateway()
