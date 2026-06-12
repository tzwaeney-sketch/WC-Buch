#!/usr/bin/env python3
"""
Lädt Fotos aus Google Drive und erstellt eine Slideshow mit ffmpeg.

Benötigte Umgebungsvariablen:
  GOOGLE_SERVICE_ACCOUNT_JSON  – Service-Account-JSON als String
  GOOGLE_DRIVE_FOLDER_ID       – Ordner-ID in Google Drive
Optionale Umgebungsvariablen:
  OUTPUT_VIDEO    – Ausgabedatei       (default: slideshow.mp4)
  VIDEO_TITLE     – Titeltext          (default: WC Gästebuch)
  PHOTO_DURATION  – Sekunden pro Foto  (default: 4)
  MUSIC_FILE      – Pfad zur Musikdatei (default: music.mp3)
"""

import io
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# ── Konfiguration ────────────────────────────────────────────────────────────
FOLDER_ID = os.environ["GOOGLE_DRIVE_FOLDER_ID"]
SA_JSON   = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
OUTPUT    = os.environ.get("OUTPUT_VIDEO",   "slideshow.mp4")
TITLE     = os.environ.get("VIDEO_TITLE",    "WC Gästebuch")
DURATION  = int(os.environ.get("PHOTO_DURATION", "4"))
MUSIC     = os.environ.get("MUSIC_FILE",     "music.mp3")

WIDTH, HEIGHT = 1920, 1080
FPS           = 25
FADE          = 0.5   # Überblend-Dauer in Sekunden

FONT_BOLD   = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_NORMAL = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

IMAGE_MIMES = {
    "image/jpeg", "image/jpg", "image/png",
    "image/gif",  "image/webp", "image/heic",
}


# ── Google Drive ─────────────────────────────────────────────────────────────
def drive_service():
    info  = json.loads(SA_JSON)
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/drive.readonly"]
    )
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def download_photos(svc, dest: str) -> list[tuple[str, str]]:
    mime_filter = " or ".join(f"mimeType='{m}'" for m in IMAGE_MIMES)
    q = f"'{FOLDER_ID}' in parents and ({mime_filter}) and trashed=false"

    all_files: list[dict] = []
    page_token = None
    while True:
        resp = svc.files().list(
            q=q,
            orderBy="createdTime",
            fields="nextPageToken,files(id,name,createdTime)",
            pageToken=page_token,
        ).execute()
        all_files.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    if not all_files:
        sys.exit("Keine Fotos im Google Drive Ordner gefunden.")

    print(f"{len(all_files)} Foto(s) gefunden – starte Download …")
    paths: list[tuple[str, str]] = []
    for idx, f in enumerate(all_files):
        ext       = Path(f["name"]).suffix.lower() or ".jpg"
        dest_path = os.path.join(dest, f"{idx:04d}{ext}")
        req       = svc.files().get_media(fileId=f["id"])
        buf       = io.BytesIO()
        dl        = MediaIoBaseDownload(buf, req)
        done      = False
        while not done:
            _, done = dl.next_chunk()
        Path(dest_path).write_bytes(buf.getvalue())
        caption = Path(f["name"]).stem
        paths.append((dest_path, caption))
        print(f"  [{idx + 1}/{len(all_files)}] {f['name']}")

    return paths


# ── ffmpeg Hilfsfunktionen ───────────────────────────────────────────────────
def esc(text: str) -> str:
    """Sonderzeichen für ffmpeg drawtext escapen."""
    text = text.replace("\\", "\\\\")
    text = text.replace("'",  "\\'")
    text = text.replace(":",  "\\:")
    text = text.replace("%",  "\\%")
    return text


def build_filter(captions: list[str]) -> str:
    """Erstellt den filter_complex-String für Slideshow mit Überblendungen."""
    n     = len(captions)
    parts: list[str] = []

    for i, caption in enumerate(captions):
        drawtext_title = (
            f"drawtext=text='{esc(TITLE)}':"
            f"fontfile={FONT_BOLD}:"
            f"fontsize=52:fontcolor=white:alpha=0.92:"
            f"x=(w-text_w)/2:y=40:"
            f"shadowcolor=black@0.6:shadowx=2:shadowy=2"
        )
        drawtext_caption = (
            f"drawtext=text='{esc(caption)}':"
            f"fontfile={FONT_NORMAL}:"
            f"fontsize=30:fontcolor=white:alpha=0.80:"
            f"x=(w-text_w)/2:y=h-64:"
            f"shadowcolor=black@0.5:shadowx=1:shadowy=1"
        )
        parts.append(
            f"[{i}:v]"
            f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=decrease,"
            f"pad={WIDTH}:{HEIGHT}:(ow-iw)/2:(oh-ih)/2:color=black,"
            f"setsar=1,"
            f"{drawtext_title},"
            f"{drawtext_caption}"
            f"[v{i}]"
        )

    if n == 1:
        parts.append("[v0]null[out]")
        return ";".join(parts)

    prev = "v0"
    for i in range(1, n):
        out_label = "out" if i == n - 1 else f"xf{i}"
        offset    = round(i * (DURATION - FADE), 3)
        parts.append(
            f"[{prev}][v{i}]xfade=transition=fade:duration={FADE}:offset={offset}[{out_label}]"
        )
        prev = out_label

    return ";".join(parts)


# ── Video erstellen ──────────────────────────────────────────────────────────
def create_video(photos: list[tuple[str, str]]) -> None:
    n              = len(photos)
    captions       = [c for _, c in photos]
    filter_complex = build_filter(captions)
    total_dur      = round(n * DURATION - (n - 1) * FADE, 3)
    has_music      = os.path.isfile(MUSIC)

    cmd: list[str] = ["ffmpeg", "-y"]

    # Jedes Foto als Eingabe (etwas länger als DURATION für Überblendung)
    for path, _ in photos:
        cmd += ["-loop", "1", "-t", str(DURATION + FADE), "-i", path]

    # Musik mit endlos-Schleife
    if has_music:
        cmd += ["-stream_loop", "-1", "-i", MUSIC]

    cmd += ["-filter_complex", filter_complex, "-map", "[out]"]

    if has_music:
        audio_idx = n
        fade_start = max(0.0, total_dur - 2.5)
        cmd += [
            "-map",   f"{audio_idx}:a",
            "-c:a",   "aac",
            "-b:a",   "128k",
            "-af",    f"afade=t=out:st={fade_start}:d=2.5",
            "-t",     str(total_dur),
        ]
    else:
        cmd += ["-an", "-t", str(total_dur)]

    cmd += [
        "-c:v",     "libx264",
        "-preset",  "fast",
        "-crf",     "23",
        "-pix_fmt", "yuv420p",
        "-r",       str(FPS),
        OUTPUT,
    ]

    print(f"\nErstelle Video ({n} Fotos, {total_dur:.1f}s) …")
    subprocess.run(cmd, check=True)
    size_mb = Path(OUTPUT).stat().st_size / 1_048_576
    print(f"\nFertig: {OUTPUT}  ({size_mb:.1f} MB)")


# ── Einstiegspunkt ───────────────────────────────────────────────────────────
def main() -> None:
    svc = drive_service()
    with tempfile.TemporaryDirectory() as tmpdir:
        photos = download_photos(svc, tmpdir)
        create_video(photos)


if __name__ == "__main__":
    main()
