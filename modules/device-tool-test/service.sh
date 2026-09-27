#!/system/bin/sh
MODDIR=${0%/*}
MARKER=/data/local/tmp/device-tool-test-module.txt
printf '%s module active\n' "$(date -u)" > "$MARKER"
printf '%s module active\n' "$(date -u)" >> "$MODDIR/service.log"
