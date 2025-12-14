#!/usr/bin/env bash
set -e

# Install Ollama only if not present
if ! command -v ollama >/dev/null 2>&1; then
  curl -fsSL https://ollama.com/install.sh | sh
fi

# Create persistent directories
mkdir -p ~/.ollama

# Optional: pull a small model so it’s ready
# ollama pull llama3.2:3b || true

# curl -fsSL https://ollama.com/install.sh | sh
# sudo systemctl daemon-reload
# sudo systemctl enable ollama

nohup ollama serve > ~/ollama.log 2>&1 &
ollama run gemini-3-pro-preview:latest --prompt "$(cat secure_prompt.txt)"