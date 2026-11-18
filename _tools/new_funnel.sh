#!/bin/bash
# Start a new funnel repo from the Magic Words templates.
# Usage (after Kasia created the empty repo on GitHub and you cloned it):
#   bash /path/to/magic-words-repo/_tools/new_funnel.sh /path/to/new-repo
set -e
SRC="$(cd "$(dirname "$0")/.." && pwd)"; DST="$1"
mkdir -p "$DST/thank-you" "$DST/access" "$DST/img" "$DST/audio" "$DST/_tools"
cp "$SRC/index.html" "$DST/index.html"
cp "$SRC/thank-you/index.html" "$DST/thank-you/index.html"
cp "$SRC/access/index.html" "$DST/access/index.html"
cp "$SRC"/_tools/* "$DST/_tools/"
echo "Templates copied. Now: replace copy, images (../img/), links (checkout URL, access URL, Doc), and run snap.js checks."
grep -n "magic-words\|Magic Words\|kasiarutkowiak.com/magic" "$DST/index.html" "$DST/thank-you/index.html" "$DST/access/index.html" | wc -l | xargs echo "Lines still mentioning Magic Words to replace:"
