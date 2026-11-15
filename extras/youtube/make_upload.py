"""Make an upload copy of a finished clip that fits the 10 MB browser-upload limit.

Usage:  python make_upload.py <clip.mp4> [--target-mb 9.5]
Writes  Desktop/youtube/upload/<name>_upload.mp4 and prints its path.
Two-pass H.264 sized from the clip's duration; YouTube re-encodes Shorts anyway,
so ~3-4 Mbps for a 20-40s vertical clip is visually lossless after upload.
"""
import argparse, os, re, subprocess, sys, tempfile

import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
OUT_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "youtube", "upload")
AUDIO_KBPS = 160


def duration(path):
    err = subprocess.run([FF, "-hide_banner", "-i", path], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip")
    ap.add_argument("--target-mb", type=float, default=9.5)
    args = ap.parse_args()

    src = os.path.abspath(args.clip)
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, os.path.splitext(os.path.basename(src))[0] + "_upload.mp4")

    if os.path.getsize(src) <= args.target_mb * 1e6:
        subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", src, "-c", "copy",
                        "-movflags", "+faststart", out], check=True)
    else:
        d = duration(src)
        vkbps = int(args.target_mb * 8e3 / d * 0.96 - AUDIO_KBPS)  # 4% container headroom
        common = ["-c:v", "libx264", "-preset", "slow", "-b:v", f"{vkbps}k",
                  "-maxrate", f"{int(vkbps * 1.15)}k", "-bufsize", f"{vkbps * 2}k"]
        with tempfile.TemporaryDirectory() as tmp:
            log = os.path.join(tmp, "pass")
            subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", src, *common,
                            "-pass", "1", "-passlogfile", log, "-an", "-f", "null", os.devnull], check=True)
            subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", src, *common,
                            "-pass", "2", "-passlogfile", log, "-c:a", "aac", "-b:a", f"{AUDIO_KBPS}k",
                            "-movflags", "+faststart", out], check=True)

    mb = os.path.getsize(out) / 1e6
    if mb >= 10:
        sys.exit(f"still {mb:.2f} MB — rerun with --target-mb {args.target_mb - 1}")
    print(f"{out}  ({mb:.2f} MB)")


if __name__ == "__main__":
    main()
