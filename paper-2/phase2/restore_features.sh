#!/bin/bash
# Reassemble feature files that exceed GitHub's 100 MB limit and are stored as split parts (*.npz.part-NN).
cd "$(dirname "$(readlink -f "$0")")"
for parts0 in features/*/*.npz.part-00; do
  f="${parts0%.part-00}"
  if [ ! -f "$f" ]; then cat "$f".part-* > "$f" && echo "restored $f"; else echo "exists $f"; fi
done
