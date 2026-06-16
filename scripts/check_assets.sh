#!/usr/bin/env bash
# Guard against the two asset failure modes this repo has actually hit:
# saved-HTML-as-image files and uncompressed multi-MB photos.
set -euo pipefail
cd "$(dirname "$0")/.."

MAX_BYTES=400000        # images: keep photos lean
MAX_VIDEO_BYTES=3000000 # short muted clips: a few seconds at ~720p
fail=0

while IFS= read -r -d '' img; do
  size=$(wc -c < "$img" | tr -d ' ')
  mime=$(file --brief --mime-type "$img")
  case "$img" in
    *.jpg|*.jpeg) want="image/jpeg"; cap=$MAX_BYTES ;;
    *.png)        want="image/png";  cap=$MAX_BYTES ;;
    *.webp)       want="image/webp"; cap=$MAX_BYTES ;;
    *.svg)        want="image/svg+xml"; cap=$MAX_BYTES ;;
    *.mp4)        want="video/mp4";  cap=$MAX_VIDEO_BYTES ;;
    *.webm)       want="video/webm"; cap=$MAX_VIDEO_BYTES ;;
    *)            want="";           cap=$MAX_BYTES ;;
  esac
  if [ "$size" -gt "$cap" ]; then
    echo "FAIL: $img is ${size} bytes (limit ${cap})"
    fail=1
  fi
  # webm sometimes reports as video/x-matroska; accept both
  if [ -n "$want" ] && [ "$mime" != "$want" ]; then
    if ! { [ "$want" = "video/webm" ] && [ "$mime" = "video/x-matroska" ]; }; then
      echo "FAIL: $img claims to be $want but is $mime"
      fail=1
    fi
  fi
done < <(find images -type f \( -name '*.jpg' -o -name '*.jpeg' -o -name '*.png' -o -name '*.webp' -o -name '*.svg' -o -name '*.mp4' -o -name '*.webm' \) -print0)

if [ "$fail" -ne 0 ]; then
  echo "Asset check failed."
  exit 1
fi
echo "Asset check passed."
