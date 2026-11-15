"""YT Grab: paste a YouTube link, pick a quality, download into the clipping folder.

Built on yt-dlp + ffmpeg (bundled via imageio-ffmpeg). Only download content you
have the rights to use, e.g. sources a clipping campaign provides.
"""
import os
import re
import shutil
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import imageio_ffmpeg
import yt_dlp

DEFAULT_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "youtube", "clipping")

QUALITIES = {
    "Best available (up to 4K)": "bv*+ba/b",
    "1080p (recommended for clipping)": "bv*[height<=1080]+ba/b[height<=1080]",
    "720p (smaller file)": "bv*[height<=720]+ba/b[height<=720]",
    "Audio only (m4a)": "ba[ext=m4a]/ba",
}

LIME, INK, PANEL, TEXT, MUTED = "#C6FF3D", "#0B0B0D", "#17171B", "#F2F2F2", "#8A8A93"


def build_options(fmt_key, folder, section):
    argv = ["--no-playlist", "--no-mtime", "-o", os.path.join(folder, "%(title).120B.%(ext)s"),
            "-f", QUALITIES[fmt_key], "--ffmpeg-location", imageio_ffmpeg.get_ffmpeg_exe()]
    if not fmt_key.startswith("Audio"):
        # highest allowed resolution first, then prefer H.264 so editors open it without fuss
        argv += ["-S", "res,vcodec:h264,acodec:m4a", "--merge-output-format", "mp4"]
    if shutil.which("node"):
        argv += ["--js-runtimes", "node"]  # needed to unlock YouTube's HD formats
    if section:
        argv += ["--download-sections", f"*{section}", "--force-keyframes-at-cuts"]
    return yt_dlp.parse_options(argv).ydl_opts


def parse_section(text):
    """Accept '16:28-17:20', '1:02:03-1:03:00' or blank. Returns normalised text or None."""
    text = text.strip().replace(" ", "")
    if not text:
        return None
    if not re.fullmatch(r"(\d+:)?\d{1,2}:\d{2}-(\d+:)?\d{1,2}:\d{2}", text):
        raise ValueError("Time range must look like 16:28-17:20")
    return text


class App:
    def __init__(self, root):
        self.root = root
        root.title("YT Grab")
        root.configure(bg=INK)
        root.minsize(480, 0)  # height follows the content, so display scaling can't cut off the progress bar

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground=PANEL, background=PANEL, foreground=TEXT,
                        arrowcolor=LIME, bordercolor=PANEL)
        style.map("TCombobox", fieldbackground=[("readonly", PANEL)], foreground=[("readonly", TEXT)])
        style.configure("lime.Horizontal.TProgressbar", troughcolor=PANEL, background=LIME,
                        bordercolor=PANEL, lightcolor=LIME, darkcolor=LIME)

        pad = {"padx": 18}
        tk.Label(root, text="YT Grab", bg=INK, fg=LIME, font=("Segoe UI Black", 20)).pack(anchor="w", pady=(14, 0), **pad)
        tk.Label(root, text="Paste a link → pick quality → Download", bg=INK, fg=MUTED,
                 font=("Segoe UI", 10)).pack(anchor="w", **pad)

        self.url = self._field("YouTube link", "")
        row = tk.Frame(root, bg=INK); row.pack(fill="x", **pad)
        tk.Button(row, text="Paste", command=self.paste, **self._btn()).pack(side="left", pady=(4, 0))

        tk.Label(root, text="Quality", bg=INK, fg=TEXT, font=("Segoe UI Semibold", 10)).pack(anchor="w", pady=(10, 2), **pad)
        self.quality = ttk.Combobox(root, values=list(QUALITIES), state="readonly", font=("Segoe UI", 10))
        self.quality.current(1)
        self.quality.pack(fill="x", **pad)

        self.section = self._field("Only this part (optional, e.g. 16:28-17:20)", "")

        tk.Label(root, text="Save to", bg=INK, fg=TEXT, font=("Segoe UI Semibold", 10)).pack(anchor="w", pady=(10, 2), **pad)
        frow = tk.Frame(root, bg=INK); frow.pack(fill="x", **pad)
        self.folder = tk.StringVar(value=DEFAULT_DIR)
        tk.Entry(frow, textvariable=self.folder, bg=PANEL, fg=TEXT, insertbackground=TEXT, relief="flat",
                 font=("Segoe UI", 10)).pack(side="left", fill="x", expand=True, ipady=5)
        tk.Button(frow, text="Browse", command=self.browse, **self._btn()).pack(side="left", padx=(6, 0))

        self.go = tk.Button(root, text="Download", command=self.start, bg=LIME, fg=INK, activebackground="#D9FF6E",
                            relief="flat", font=("Segoe UI Black", 12), cursor="hand2")
        self.go.pack(fill="x", pady=(16, 8), ipady=6, **pad)
        self.bar = ttk.Progressbar(root, style="lime.Horizontal.TProgressbar", maximum=100)
        self.bar.pack(fill="x", **pad)
        self.status = tk.Label(root, text="Ready.", bg=INK, fg=MUTED, font=("Segoe UI", 10), anchor="w", justify="left",
                               wraplength=520)
        self.status.pack(fill="x", pady=(6, 16), **pad)
        root.update_idletasks()
        root.geometry(f"{max(560, root.winfo_reqwidth())}x{root.winfo_reqheight()}")
        self.last_file = None

    def _btn(self):
        return dict(bg=PANEL, fg=TEXT, activebackground="#24242A", activeforeground=TEXT, relief="flat",
                    font=("Segoe UI", 10), cursor="hand2", padx=10)

    def _field(self, label, default):
        tk.Label(self.root, text=label, bg=INK, fg=TEXT, font=("Segoe UI Semibold", 10)).pack(anchor="w", padx=18, pady=(10, 2))
        var = tk.StringVar(value=default)
        tk.Entry(self.root, textvariable=var, bg=PANEL, fg=TEXT, insertbackground=TEXT, relief="flat",
                 font=("Segoe UI", 10)).pack(fill="x", padx=18, ipady=5)
        return var

    def paste(self):
        try:
            self.url.set(self.root.clipboard_get().strip())
        except tk.TclError:
            pass

    def browse(self):
        d = filedialog.askdirectory(initialdir=self.folder.get() or DEFAULT_DIR)
        if d:
            self.folder.set(d)

    def say(self, text, pct=None):
        def upd():
            self.status.config(text=text)
            if pct is not None:
                self.bar["value"] = pct
        self.root.after(0, upd)

    def start(self):
        url = self.url.get().strip()
        if not re.match(r"https?://(www\.|m\.)?(youtube\.com|youtu\.be)/", url):
            messagebox.showwarning("YT Grab", "Paste a YouTube link first.")
            return
        try:
            section = parse_section(self.section.get())
        except ValueError as e:
            messagebox.showwarning("YT Grab", str(e))
            return
        folder = self.folder.get().strip() or DEFAULT_DIR
        os.makedirs(folder, exist_ok=True)
        self.go.config(state="disabled", text="Downloading…")
        self.bar["value"] = 0
        threading.Thread(target=self.run, args=(url, self.quality.get(), folder, section), daemon=True).start()

    def hook(self, d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            if d.get("fragment_count"):
                pct = 100 * (d.get("fragment_index") or 0) / d["fragment_count"]
            elif total:
                pct = 100 * d.get("downloaded_bytes", 0) / total
            else:
                pct = None
            speed = d.get("_speed_str", "").strip()
            self.say(f"Downloading {d.get('info_dict', {}).get('format_note', '')}  {speed}".strip(), pct)
        elif d["status"] == "finished":
            self.say("Merging video + audio…", 100)

    def pp_hook(self, d):
        if d["status"] == "finished" and d.get("info_dict", {}).get("filepath"):
            self.last_file = d["info_dict"]["filepath"]

    def run(self, url, fmt_key, folder, section):
        try:
            opts = build_options(fmt_key, folder, section)
            opts.update(progress_hooks=[self.hook], postprocessor_hooks=[self.pp_hook], quiet=True, no_warnings=True)
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                path = self.last_file or ydl.prepare_filename(info)
            h = info.get("height")
            self.say(f"Done ✓  {os.path.basename(path)}" + (f"  ({h}p)" if h else ""), 100)
            self.root.after(0, lambda: self.done(path))
        except Exception as e:  # show yt-dlp's message instead of crashing the window
            msg = re.sub(r"\x1b\[[0-9;]*m", "", str(e))
            self.say(f"Failed: {msg}", 0)
            self.root.after(0, lambda: self.go.config(state="normal", text="Download"))

    def done(self, path):
        self.go.config(state="normal", text="Download")
        if os.path.exists(path):
            subprocess.run(["explorer", "/select,", os.path.normpath(path)])


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
