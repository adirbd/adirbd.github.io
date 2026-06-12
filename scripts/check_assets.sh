#!/usr/bin/env bash
# Guard against the two asset failure modes this repo has actually hit:
# saved-HTML-as-image files and uncompressed multi-MB photos.
set -euo pipefail
cd "$(dirname "$0")/.."

MAX_BYTES=400000
fail=0

while IFS= read -r -d '' img; do
  size=$(wc -c < "$img" | tr -d ' ')
  if [ "$size" -gt "$MAX_BYTES" ]; then
    echo "FAIL: $img is ${size} bytes (limit ${MAX_BYTES})"
    fail=1
  fi
  mime=$(file --brief --mime-type "$img")
  case "$img" in
    *.jpg|*.jpeg) want="image/jpeg" ;;
    *.png)        want="image/png" ;;
    *.webp)       want="image/webp" ;;
    *.svg)        want="image/svg+xml" ;;
    *)            want="" ;;
  esac
  if [ -n "$want" ] && [ "$mime" != "$want" ]; then
    echo "FAIL: $img claims to be $want but is $mime"
    fail=1
  fi
done < <(find images -type f \( -name '*.jpg' -o -name '*.jpeg' -o -name '*.png' -o -name '*.webp' -o -name '*.svg' \) -print0)

if [ "$fail" -ne 0 ]; then
  echo "Asset check failed."
  exit 1
fi
echo "Asset check passed."
