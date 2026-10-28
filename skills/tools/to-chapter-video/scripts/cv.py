"""Builds a narrated chapter video from a project folder: voice, compose, check, render, package.

Project layout (all paths relative to the project folder):
  video.json         title, voice, chapters and their beats (format: references/video-json.md)
  scenes/<id>.html   one scene fragment per chapter (format: references/scenes.md)
  assets/            images and other files the scenes reference as assets/<file>
  build/             generated: audio/, timing.json, hf/<id>/index.html, renders/, check/
  out/               generated: player.html and media/ to publish

Every stage is idempotent and can be rerun alone; chapter ids after a stage limit it to those chapters.

Usage: python3 cv.py <stage> <project> [chapter-id ...]
  stages: preflight, voice, compose, check, render, package, all (= voice compose check render package)
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
HF = ["npx", "--yes", "hyperframes@0.8.198"]
GSAP = "https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"
MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"
FONTS = ("https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600"
         "&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap")
TTS_URL = "https://openrouter.ai/api/v1/audio/speech"
MAX_FILE = 14.5e6
MAX_BATCH = 60e6


def log(msg):
    print(time.strftime("%H:%M:%S"), msg, flush=True)


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def duration(p):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
            capture_output=True, text=True)
    return float(r.stdout.strip())


class Project:
    def __init__(self, root, only):
        self.root = Path(root).resolve()
        self.cfg = json.loads((self.root / "video.json").read_text(encoding="utf-8"))
        self.build = self.root / "build"
        self.audio = self.build / "audio"
        self.only = set(only)
        ids = [c["id"] for c in self.cfg["chapters"]]
        unknown = self.only - set(ids)
        if unknown:
            raise SystemExit(f"unknown chapter ids: {sorted(unknown)}; known: {ids}")

    @property
    def chapters(self):
        return [c for c in self.cfg["chapters"] if not self.only or c["id"] in self.only]

    def voice_cfg(self):
        v = self.cfg.get("voice", {})
        return v.get("model", "fish-audio/drama-3"), v.get("voice")

    def beats(self, ch):
        """Each beat as {text, say}: text is shown in captions, say is spoken (defaults to text)."""
        return [{"text": b, "say": b} if isinstance(b, str) else {"text": b["text"], "say": b.get("say", b["text"])}
                for b in ch["beats"]]

    def clip(self, say):
        model, voice = self.voice_cfg()
        h = hashlib.sha256(json.dumps([model, voice, say]).encode()).hexdigest()[:16]
        return self.audio / f"{h}.mp3"

    def timing(self):
        """Per chapter: each beat's start, speech length and audio clip, back to back with a pause after each."""
        pause, end_pause = self.cfg.get("pause", 0.45), self.cfg.get("chapter_pause", 1.0)
        out = {}
        for ch in self.cfg["chapters"]:
            t, beats = 0.0, []
            bs = self.beats(ch)
            for i, b in enumerate(bs):
                clip = self.clip(b["say"])
                if not clip.exists():
                    raise SystemExit(f"no audio for {ch['id']} beat {i + 1}: run the voice stage first")
                d = duration(clip)
                beats.append({"start": round(t, 3), "dur": round(d, 3), "clip": clip.name, "text": b["text"]})
                t += d + (end_pause if i + 1 == len(bs) else pause)
            out[ch["id"]] = {"beats": beats, "total": round(t, 3)}
        return out


# ---------------------------------------------------------------------------------------------------- preflight
def preflight(p):
    ok = True
    if not os.environ.get("OPENROUTER_API_KEY"):
        print("MISSING  OPENROUTER_API_KEY is not set. Ask the user to export it in their shell profile "
              "(never paste it in chat or write it to a file).")
        ok = False
    else:
        print("ok       OPENROUTER_API_KEY is set")
    for tool in ("node", "npx", "ffmpeg", "ffprobe"):
        found = shutil.which(tool)
        print(f"{'ok' if found else 'MISSING':8} {tool}")
        ok &= bool(found)
    if shutil.which("node"):
        major = int(run(["node", "-v"], capture_output=True, text=True).stdout.strip().lstrip("v").split(".")[0])
        print(f"{'ok' if major >= 22 else 'MISSING':8} node >= 22 (found {major})")
        ok &= major >= 22
        subprocess.run(HF + ["telemetry", "disable"], capture_output=True)
        print("ok       HyperFrames telemetry disabled")
    if not ok:
        raise SystemExit(1)


# ---------------------------------------------------------------------------------------------------- voice
def openrouter(path, body=None):
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise SystemExit("OPENROUTER_API_KEY is not set; run the preflight stage")
    req = urllib.request.Request(f"https://openrouter.ai/api/v1{path}", method="POST" if body else "GET",
                                 data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def usage():
    try:
        return json.loads(openrouter("/key"))["data"]["usage"]
    except Exception:
        return None


def voice(p):
    p.audio.mkdir(parents=True, exist_ok=True)
    model, v = p.voice_cfg()
    todo = {}
    for ch in p.chapters:
        for b in p.beats(ch):
            clip = p.clip(b["say"])
            if not (clip.exists() and clip.stat().st_size > 1000):
                todo[clip] = b["say"]
    log(f"{len(todo)} clips to voice with {model} ({sum(map(len, todo.values()))} characters)")
    if not todo:
        return
    before = usage()

    def speak(item):
        clip, say = item
        body = {"model": model, "input": say, "response_format": "mp3"}
        if v:
            body["voice"] = v
        for attempt in range(4):
            try:
                data = openrouter("/audio/speech", body)
                if len(data) > 1000:
                    clip.write_bytes(data)
                    log(f"voiced {clip.name} ({len(data) // 1024} KB)")
                    return
                log(f"{clip.name}: short response ({len(data)} bytes), retrying")
            except Exception as e:
                log(f"{clip.name} attempt {attempt + 1} failed: {e}")
            time.sleep(3 * (attempt + 1))
        raise SystemExit(f"no audio for: {say[:60]}…")

    with ThreadPoolExecutor(3) as pool:
        list(pool.map(speak, todo.items()))
    after = usage()
    if before is not None and after is not None:
        log(f"voice cost: ${after - before:.4f} (OpenRouter key usage; it can lag a minute behind)")


# ---------------------------------------------------------------------------------------------------- compose
def compose(p):
    timing = p.timing()
    (p.build / "timing.json").write_text(json.dumps(timing, indent=1, ensure_ascii=False), encoding="utf-8")
    css = (SKILL / "templates" / "scene.css").read_text(encoding="utf-8")
    runtime = (SKILL / "templates" / "runtime.js").read_text(encoding="utf-8")
    theme = "".join(f"--{k}:{v};" for k, v in p.cfg.get("theme", {}).items())
    all_ids = [c["id"] for c in p.cfg["chapters"]]
    for ch in p.chapters:
        tm = timing[ch["id"]]
        src = (p.root / "scenes" / f"{ch['id']}.html").read_text(encoding="utf-8")
        scripts = "\n".join(re.findall(r"<script\b[^>]*>.*?</script>", src, flags=re.S))
        body = re.sub(r"<script\b[^>]*>.*?</script>", "", src, flags=re.S)
        n = all_ids.index(ch["id"]) + 1
        audio = "\n".join(
            f'<audio id="vo{i}" src="audio/{b["clip"]}" data-start="{b["start"]}" data-duration="{b["dur"]}"></audio>'
            for i, b in enumerate(tm["beats"], 1))
        footer = p.cfg.get("footer", p.cfg["title"])
        html = f"""<!doctype html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="{FONTS}">
<style>{css}
:root{{{theme}}}</style>
</head><body>
<div id="root" class="{ch.get('class', '')}" data-composition-id="root" data-width="1920" data-height="1080" data-start="0" data-duration="{tm['total']}">
<div class="frame">
{body}
</div>
<div class="footer"><span>{footer}</span><span>{ch['kicker']} · {n}/{len(all_ids)}</span></div>
<div class="prog" style="width:{n / len(all_ids) * 100:.1f}%"></div>
{audio}
</div>
<script src="{GSAP}"></script>
<script src="{MERMAID}"></script>
<script>window.__VIDEO = {json.dumps({"beats": [{"start": b["start"], "dur": b["dur"]} for b in tm["beats"]], "total": tm["total"]})};</script>
<script>{runtime}</script>
{scripts}
</body></html>
"""
        out = p.build / "hf" / ch["id"]
        if out.exists():
            shutil.rmtree(out)
        (out / "audio").mkdir(parents=True)
        (out / "index.html").write_text(html, encoding="utf-8")
        for b in tm["beats"]:
            shutil.copy2(p.audio / b["clip"], out / "audio" / b["clip"])
        if (p.root / "assets").exists():
            shutil.copytree(p.root / "assets", out / "assets")
        log(f"composed {ch['id']}: {len(tm['beats'])} beats, {tm['total']:.1f}s")


# ---------------------------------------------------------------------------------------------------- check
def beat_ends(p, cid):
    tm = json.loads((p.build / "timing.json").read_text(encoding="utf-8"))[cid]
    return [round(b["start"] + b["dur"], 2) for b in tm["beats"]]


def check(p):
    """Lint each composition and inspect its layout at the end of every beat, where the most is on screen."""
    failed = []
    for ch in p.chapters:
        d = p.build / "hf" / ch["id"]
        lint = subprocess.run(HF + ["lint", ".", "--json"], cwd=d, capture_output=True, text=True)
        ins = subprocess.run(HF + ["inspect", ".", "--json", "--at", ",".join(map(str, beat_ends(p, ch["id"])))],
                             cwd=d, capture_output=True, text=True)
        report = {"lint": parse_json(lint.stdout), "inspect": parse_json(ins.stdout)}
        (p.build / "check").mkdir(exist_ok=True)
        (p.build / "check" / f"{ch['id']}.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
        errors = [f for f in findings(report["lint"]) if f.get("severity") == "error"]
        issues = findings(report["inspect"])
        status = "ok" if not errors and not issues and lint.returncode == 0 and ins.returncode == 0 else "FAIL"
        log(f"check {ch['id']}: {status} ({len(errors)} lint errors, {len(issues)} layout issues)")
        for f in errors + issues:
            print("   ", json.dumps(f, ensure_ascii=False)[:400])
        if status == "FAIL":
            failed.append(ch["id"])
    if failed:
        raise SystemExit(f"check failed for {failed}; details in build/check/<id>.json")


def parse_json(text):
    start = min([i for i in (text.find("{"), text.find("[")) if i >= 0], default=-1)
    try:
        return json.loads(text[start:]) if start >= 0 else None
    except json.JSONDecodeError:
        return {"raw": text[-2000:]}


def findings(rep):
    if isinstance(rep, list):
        return rep
    if isinstance(rep, dict):
        for k in ("findings", "issues", "errors"):
            if isinstance(rep.get(k), list):
                return rep[k]
    return []


# ---------------------------------------------------------------------------------------------------- render
def render(p):
    out = p.build / "renders"
    out.mkdir(exist_ok=True)
    for ch in p.chapters:
        d, mp4 = p.build / "hf" / ch["id"], out / f"{ch['id']}.mp4"
        t = time.time()
        run(HF + ["render", ".", "-o", str(mp4), "--fps", "30", "--quality", "delivery"], cwd=d)
        log(f"rendered {ch['id']} in {time.time() - t:.0f}s")
        sheet(p, ch["id"], mp4)


def sheet(p, cid, mp4):
    """Contact sheet of the last frame of every beat, to eyeball overflow and crowding."""
    tmp = p.build / "check" / f"{cid}-frames"
    tmp.mkdir(parents=True, exist_ok=True)
    ends = beat_ends(p, cid)
    for i, t in enumerate(ends):
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, t - 0.1):.2f}", "-i", str(mp4), "-frames:v", "1",
             "-vf", "scale=640:-2", str(tmp / f"{i:02d}.png")])
    cols = min(3, len(ends))
    rows = -(-len(ends) // cols)
    run(["ffmpeg", "-v", "error", "-y", "-framerate", "1", "-i", str(tmp / "%02d.png"),
         "-vf", f"tile={cols}x{rows}:padding=8:color=white", "-frames:v", "1", str(p.build / "check" / f"{cid}.jpg")])
    shutil.rmtree(tmp)
    log(f"contact sheet: {p.build / 'check' / f'{cid}.jpg'}")


# ---------------------------------------------------------------------------------------------------- package
def captions(text, start, end):
    parts = [s.strip() for s in re.split(r"(?<=[.?!:])\s+", text) if s.strip()]
    total = sum(map(len, parts))
    t, out = start, []
    for s in parts:
        d = (end - start) * len(s) / total
        out.append({"start": round(t, 3), "end": round(t + d, 3), "text": s})
        t += d
    return out


def package(p):
    timing = json.loads((p.build / "timing.json").read_text(encoding="utf-8"))
    media = p.root / "out" / "media"
    media.mkdir(parents=True, exist_ok=True)
    chapters = []
    for n, ch in enumerate(p.cfg["chapters"], 1):
        cid, src = f"ch{n:02d}", p.build / "renders" / f"{ch['id']}.mp4"
        mp4, jpg = media / f"{cid}.mp4", media / f"{cid}.jpg"
        if not p.only or ch["id"] in p.only:
            crf = 23
            while True:
                run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-c:v", "libx264", "-preset", "slow", "-crf", str(crf),
                     "-g", "90", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k", "-ac", "1", "-movflags", "+faststart",
                     str(mp4)])
                if mp4.stat().st_size <= MAX_FILE or crf >= 35:
                    break
                crf += 3
            length = duration(mp4)
            run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, length - 0.8):.2f}", "-i", str(mp4), "-frames:v", "1",
                 "-vf", "scale=640:-2", "-q:v", "4", str(jpg)])
            log(f"{cid} ({ch['id']}): {length:.0f}s, {mp4.stat().st_size / 1e6:.1f} MB, crf {crf}")
        cues = [c for b in timing[ch["id"]]["beats"] for c in captions(b["text"], b["start"], b["start"] + b["dur"])]
        chapters.append({"n": n, "id": cid, "kicker": ch["kicker"], "title": ch["title"],
                         "seconds": round(duration(mp4), 1), "cues": cues})

    cfg = p.cfg
    groups = cfg.get("parts") or [["Chapters", list(range(1, len(chapters) + 1))]]
    total = sum(c["seconds"] for c in chapters)
    meta = cfg.get("meta") or f"{len(chapters)} chapters, {total / 60:.0f} minutes."
    model, _ = p.voice_cfg()
    html = (SKILL / "templates" / "player.html").read_text(encoding="utf-8")
    for k, v in {"__TITLE__": cfg["title"], "__EYEBROW__": cfg.get("eyebrow", "Video course"), "__META__": meta,
                 "__FOOT__": cfg.get("foot", f"Narration voiced with {model} via OpenRouter."),
                 "__STORE_KEY__": re.sub(r"[^a-z0-9]+", "-", cfg["title"].lower()).strip("-"),
                 "__CHAPTERS__": json.dumps(chapters, ensure_ascii=False), "__GROUPS__": json.dumps(groups)}.items():
        html = html.replace(k, v)
    (p.root / "out" / "player.html").write_text(html, encoding="utf-8")

    batches, cur, size = [], [], 0
    for c in chapters:
        files = [f"media/{c['id']}.mp4", f"media/{c['id']}.jpg"]
        s = sum((p.root / "out" / f).stat().st_size for f in files)
        if cur and size + s > MAX_BATCH:
            batches.append(cur)
            cur, size = [], 0
        cur += files
        size += s
    batches.append(cur)
    (p.root / "out" / "publish.json").write_text(json.dumps(batches, indent=1), encoding="utf-8")
    log(f"packaged {len(chapters)} chapters, {total / 60:.1f} min; publish in {len(batches)} batch(es): out/publish.json")


STAGES = {"preflight": preflight, "voice": voice, "compose": compose, "check": check, "render": render,
          "package": package}

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in [*STAGES, "all"]:
        raise SystemExit(__doc__)
    proj = Project(sys.argv[2], sys.argv[3:])
    for stage in (["voice", "compose", "check", "render", "package"] if sys.argv[1] == "all" else [sys.argv[1]]):
        log(f"== {stage}")
        STAGES[stage](proj)
