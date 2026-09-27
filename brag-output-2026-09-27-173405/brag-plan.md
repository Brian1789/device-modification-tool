# Brag plan — Android Device Modification Tool

## Angle

An emulator-first Android workflow: Android Studio provides the AVD, virtualization keeps it fast, and `device-tool` turns the running emulator into a focused diagnostics and backup surface.

## Storyboard (32.0s, 1920x1080, 30fps)

| # | Time | Scene | On screen |
|---|------|-------|-----------|
| 1 | 0.0-3.5s | Hook | Android Studio. A virtual device. One focused workflow. |
| 2 | 3.5-8.5s | Reveal | `device-tool`; AVD, ADB, diagnostics, and emulator control. |
| 3 | 8.5-14.5s | Devices | `device-tool devices` and `status`; `emulator-5554` appears as ready. |
| 4 | 14.5-21.0s | Inspect | `info --json` reveals emulator properties, architecture, and security state. |
| 5 | 21.0-26.5s | Protect | Backup and verify show explicit, non-destructive state handling. |
| 6 | 26.5-32.0s | Outro | Android Studio + AVD + VM acceleration; `device-tool` on `emulator-5554`. |

## Tone

Polished technical demo with a calm terminal rhythm and longer holds for the emulator workflow to read clearly.

## Deliverables

- `brag.mp4` — 1920x1080, 30fps, 32 seconds
- `brag.jpg` — settled outro poster
- `share-copy.txt` — emulator-focused caption
