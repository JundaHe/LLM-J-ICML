#!/bin/bash
# Public preference datasets for paper 4 (not committed: size and licences — MultiPref ODC/CC per its card; PRISM CC-BY-4.0 human text / CC-BY-NC-4.0 model responses).
set -e; cd "$(dirname "$0")"; mkdir -p data/prism data/multipref
for f in utterances.jsonl survey.jsonl conversations.jsonl README.md; do curl -sL -o data/prism/$f "https://huggingface.co/datasets/HannahRoseKirk/prism-alignment/resolve/main/$f"; done
for f in MultiPref-Train.jsonl README.md; do curl -sL -o data/multipref/$f "https://huggingface.co/datasets/allenai/multipref/resolve/main/$f"; done
echo done
