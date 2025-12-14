#!/usr/bin/env bash
pip install -r requirements.txt
set -e
if ! command -v ollama >/dev/null 2>&1; then
  curl -fsSL https://ollama.com/install.sh | sh
fi
#export OLLAMA_HOST=0.0.0.0:11434
#export OLLAMA_MODELS="$HOME/.ollama/models"
mkdir -p ~/.ollama

# curl -fsSL https://ollama.com/install.sh | sh
# sudo systemctl daemon-reload
# sudo systemctl enable ollama
if ! pgrep -x ollama >/dev/null; then
  nohup ollama serve > ~/ollama.log 2>&1 &
fi

ps aux | grep ollama
ollama list
#curl http://localhost:11434/api/tags
ollama pull deepseek-v3.1:671b-cloud
ollama pull gemini-3-pro-preview:latest
ollama pull qwen3-vl:235b-cloud
#ollama run gemini-3-pro-preview:latest --prompt "$(cat secure_prompt.txt)"


#nohup  ollama run deepseek-v3.2:cloud 2>&1 &
#https://github.com/copyleftdev/ai-testing-prompts
ollama run nomic-embed-text:latest