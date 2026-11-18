#!/usr/bin/env bash
# 概念モデルのページ（bizspec-concept-overview.html）を作る
set -euo pipefail
cd "$(dirname "$0")"
python3 ex.py
python3 sysex.py
node gen.js
