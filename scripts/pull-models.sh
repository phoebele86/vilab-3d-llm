#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# Base chat model and embedding model
ollama pull qwen3:8b
ollama pull bge-m3

# Build the project model used by the backend (LLM_MODEL=vilab-qwen)
ollama create vilab-qwen -f models/Modelfile.qwen

ollama list
