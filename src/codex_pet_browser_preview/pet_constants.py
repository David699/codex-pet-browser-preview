"""Codex Desktop pet atlas constants."""

WIDTH = 1536
HEIGHT = 1872
FRAME_W = 192
FRAME_H = 208
COLS = 8
ROWS = 9

STATES = [
    {"row": 0, "name": "idle", "frames": 6, "timings": [280, 110, 110, 140, 140, 320]},
    {"row": 1, "name": "running-right", "frames": 8, "timings": [120, 120, 120, 120, 120, 120, 120, 220]},
    {"row": 2, "name": "running-left", "frames": 8, "timings": [120, 120, 120, 120, 120, 120, 120, 220]},
    {"row": 3, "name": "waving", "frames": 4, "timings": [140, 140, 140, 280]},
    {"row": 4, "name": "jumping", "frames": 5, "timings": [140, 140, 140, 140, 280]},
    {"row": 5, "name": "failed", "frames": 8, "timings": [140, 140, 140, 140, 140, 140, 140, 240]},
    {"row": 6, "name": "waiting", "frames": 6, "timings": [150, 150, 150, 150, 150, 260]},
    {"row": 7, "name": "running", "frames": 6, "timings": [120, 120, 120, 120, 120, 220]},
    {"row": 8, "name": "review", "frames": 6, "timings": [150, 150, 150, 150, 150, 280]},
]

BUILTIN_INTERNAL = [
    ("codex", "Codex", "webview/assets/codex-spritesheet-v4-Bl6P89d_.webp"),
    ("dewey", "Dewey", "webview/assets/dewey-spritesheet-v4-gAYk_M9g.webp"),
    ("fireball", "Fireball", "webview/assets/fireball-spritesheet-v4-BtU8R9Qp.webp"),
    ("rocky", "Rocky", "webview/assets/rocky-spritesheet-v4-3RlTi26B.webp"),
    ("seedy", "Seedy", "webview/assets/seedy-spritesheet-v4-CdlE_fn9.webp"),
    ("stacky", "Stacky", "webview/assets/stacky-spritesheet-v4-CaUJd4fY.webp"),
    ("bsod", "BSOD", "webview/assets/bsod-spritesheet-v4-BRrRVy1T.webp"),
    ("null-signal", "Null Signal", "webview/assets/null-signal-spritesheet-v4-CCoTR-8t.webp"),
]

