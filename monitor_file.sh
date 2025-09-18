#!/usr/bin/env bash
# monitor_file.sh
# 使い方: bash monitor_file.sh <filepaths>

file="$1"
if [[ -z "$file" ]]; then
  echo "Usage: $0 <file-to-monitor>"
  exit 1
fi

prev=0
while true; do
  # ファイルサイズ取得（存在しなければ0）
  sz=$(stat -c %s "$file" 2>/dev/null || echo 0)
  rate=$((sz - prev))

  # 人間向けの単位に変換
  hsz=$(numfmt --to=iec <<<"$sz")
  hr=$(numfmt --to=iec <<<"$rate")

  # 日付 + サイズ + 直近の増分/秒 を表示
  printf "%(%F %T)T  size=%s  +%s/s\n" -1 "$hsz" "$hr"

  prev=$sz
  sleep 1
done