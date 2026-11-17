#!/usr/bin/env bash
set -euo pipefail

curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "vilab-qwen", "messages": [{"role": "user", "content": "Hello"}]}'
