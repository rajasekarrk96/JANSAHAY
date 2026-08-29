"""Render the JANSAHAY 2-minute demo video from the captured live-app stills."""
import os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import imageio_ffmpeg

SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SP)
from timeline import (W, H, FPS, TOTAL, FADE_IN, FADE_OUT, XFADE,
                      SCENES, SHOTS, DENIAL_CALLOUT, build_cues)

SHOTS_DIR = os.path.join(SP, "shots")
OUT = os.path.join(SP, "jansahay_demo_2min_silent.mp4")

FONT = "C:/Windows/Fonts/segoeui.ttf"
FONT_B = "C:/Windows/Fonts/segoeuib.ttf"
FONT_SB = "C:/Windows/Fonts/seguisb.ttf"
MONO = "C:/Windows/Fonts/consola.ttf"
MONO_B = "C:/Windows/Fonts/consolab.ttf"
if not os.path.exists(FONT_SB):
    FONT_SB = FONT_B

AMBER = (245, 158, 11)
ROSE = (244, 63, 94)
INK = (11, 18, 32)
WHITE = (255, 255, 255)

f_caption = ImageFont.truetype(FONT_SB, 38)
f_chip = ImageFont.truetype(FONT_B, 24)
f_chipnum = ImageFont.truetype(FONT_B, 20)
f_call_h = ImageFont.truetype(FONT_B, 26)
f_call_b = ImageFont.truetype(FONT, 24)
f_mono = ImageFont.truetype(MONO, 22)
f_mono_b = ImageFont.truetype(MONO_B, 24)

CUES = build_cues()
FULL = (0.0, 0.0, float(W), float(H))


# ------------------------------------------------------------------ helpers
def ease(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


def to_169(rect, pad=0.12):
    """Expand a focus rect to 16:9, with padding, clamped to the frame."""
    x0, y0, x1, y1 = rect
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    w, h = (x1 - x0) * (1 + pad), (y1 - y0) * (1 + pad)
    if w / h < W / H:
        w = h * W / H
    else:
        h = w * H / W
    if w > W or h > H:
        k = min(W / w, H / h)
        w, h = w * k, h * k
    x0 = min(max(cx - w / 2, 0), W - w)
    y0 = min(max(cy - h / 2, 0), H - h)
    return (x0, y0, x0 + w, y0 + h)


def lerp_rect(a, b, u):
    return tuple(a[i] + (b[i] - a[i]) * u for i in range(4))


_cache = {}
def load_shot(name):
    if name not in _cache:
        im = Image.open(os.path.join(SHOTS_DIR, name + ".png")).convert("RGB")
        if im.size != (W, H):
            im = im.resize((W, H), Image.LANCZOS)
        _cache[name] = np.asarray(im, dtype=np.uint8)
    return _cache[name]


def shot_frame(seg, t):
    """One shot at time t: an eased push-in toward its focus rect."""
    name, s, e, focus = seg
    u = ease((t - s) / max(0.001, e - s))
    if focus is None:
        target = to_169((W * 0.06, H * 0.05, W * 0.94, H * 0.95), pad=0.0)
    else:
        target = to_169(focus)
    start = lerp_rect(FULL, target, 0.55)      # settle in, don't leap
    x0, y0, x1, y1 = lerp_rect(start, target, u)
    src = load_shot(name)
    crop = src[int(round(y0)):int(round(y1)), int(round(x0)):int(round(x1))]
    interp = cv2.INTER_AREA if crop.shape[1] > W else cv2.INTER_CUBIC
    return cv2.resize(crop, (W, H), interpolation=interp)


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def bake(layer):
    """PIL RGBA layer -> (bbox, rgb float array, alpha float array) for fast compositing."""
    bbox = layer.getbbox()
    if bbox is None:
        return None
    sub = layer.crop(bbox)
    arr = np.asarray(sub, dtype=np.float32)
    return bbox, arr[..., :3], (arr[..., 3:4] / 255.0)


def paste(frame, baked, alpha=1.0):
    if baked is None or alpha <= 0:
        return
    (x0, y0, x1, y1), rgb, a = baked
    a = a * alpha
    region = frame[y0:y1, x0:x1].astype(np.float32)
    frame[y0:y1, x0:x1] = (region * (1 - a) + rgb * a).astype(np.uint8)


# ------------------------------------------------------------ overlay layers
def make_caption(num, label, text):
    """Lower band: scene pill + scene label + the narration line."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    lines = wrap(d, text, f_caption, W - 520)
    lh = 52
    band_h = 30 + 26 + 14 + lh * len(lines) + 24
    x0, x1 = 170, W - 170
    top = H - 44 - band_h
    d.rounded_rectangle((x0, top, x1, top + band_h), radius=22, fill=(8, 13, 24, 236))
    d.rounded_rectangle((x0, top, x0 + 8, top + band_h), radius=4, fill=AMBER + (255,))

    num_txt = f"{num:02d}"
    nw = d.textlength(num_txt, font=f_chipnum)
    px = x0 + 34
    d.rounded_rectangle((px, top + 26, px + nw + 20, top + 26 + 30), radius=7,
                        fill=AMBER + (255,))
    d.text((px + 10, top + 28), num_txt, font=f_chipnum, fill=INK + (255,))
    d.text((px + nw + 36, top + 29), label.upper(), font=f_chip,
           fill=(148, 163, 184, 255))

    y = top + 30 + 26 + 14
    for ln in lines:
        tw = d.textlength(ln, font=f_caption)
        d.text(((W - tw) / 2, y), ln, font=f_caption, fill=(240, 245, 252, 255))
        y += lh
    return layer


def make_denial():
    """The server's real 403 response to an out-of-role action."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    bw, bh = 900, 250
    x, y = W - bw - 90, 140
    d.rounded_rectangle((x, y, x + bw, y + bh), radius=20, fill=(10, 15, 26, 244),
                        outline=ROSE + (255,), width=3)
    d.text((x + 30, y + 26), "SERVER RESPONSE", font=f_call_h, fill=(148, 163, 184, 255))
    st = DENIAL_CALLOUT["status"]
    sw = d.textlength(st, font=f_mono_b)
    d.rounded_rectangle((x + bw - sw - 60, y + 24, x + bw - 26, y + 60), radius=9,
                        fill=ROSE + (255,))
    d.text((x + bw - sw - 43, y + 28), st, font=f_mono_b, fill=WHITE + (255,))
    d.text((x + 30, y + 76), DENIAL_CALLOUT["request"], font=f_mono, fill=(203, 213, 225, 255))
    yy = y + 120
    for ln in wrap(d, DENIAL_CALLOUT["detail"], f_call_b, bw - 60):
        d.text((x + 30, yy), ln, font=f_call_b, fill=(254, 226, 226, 255))
        yy += 34
    return layer


SCENE_LABEL = {n: lbl for n, lbl, _, _ in SCENES}
CAPTION_LAYERS = {}
for _cs, _ce, _txt in CUES:
    _n = next(n for n, _l, s_, e_ in SCENES if s_ <= _cs < e_)
    CAPTION_LAYERS[_txt] = bake(make_caption(_n, SCENE_LABEL[_n], _txt))
DENIAL_LAYER = bake(make_denial())


# ------------------------------------------------------------------ assembly
def scene_at(t):
    for n, lbl, s, e in SCENES:
        if s <= t < e:
            return n, s, e
    n, lbl, s, e = SCENES[-1]
    return n, s, e


def cue_at(t):
    for s, e, txt in CUES:
        if s <= t < e:
            return s, e, txt
    return None


def base_at(t):
    idx = len(SHOTS) - 1
    for i, seg in enumerate(SHOTS):
        if seg[1] <= t < seg[2]:
            idx = i
            break
    seg = SHOTS[idx]
    img = shot_frame(seg, t)
    if idx > 0 and t - seg[1] < XFADE:
        prev = SHOTS[idx - 1]
        a = ease((t - seg[1]) / XFADE)
        prev_img = shot_frame(prev, prev[2])
        img = cv2.addWeighted(prev_img, 1 - a, img, a, 0)
    return img


def alpha_ramp(t, s, e, ramp=0.30):
    if t < s or t >= e:
        return 0.0
    return min(1.0, min((t - s) / ramp, (e - t) / ramp, 1.0))


def render_frame(t):
    frame = base_at(t).copy()

    cue = cue_at(t)
    if cue:
        cs, ce, txt = cue
        paste(frame, CAPTION_LAYERS[txt], alpha_ramp(t, cs, ce, 0.25))

    paste(frame, DENIAL_LAYER,
          alpha_ramp(t, DENIAL_CALLOUT["start"], DENIAL_CALLOUT["end"], 0.35))

    # progress bar
    u = min(1.0, t / TOTAL)
    frame[H - 7:H, :, :] = (frame[H - 7:H, :, :] * 0.55).astype(np.uint8)
    frame[H - 7:H, :int(W * u), :] = AMBER

    k = 1.0
    if t < FADE_IN:
        k = ease(t / FADE_IN)
    elif t > TOTAL - FADE_OUT:
        k = ease((TOTAL - t) / FADE_OUT)
    if k < 1.0:
        frame = (frame.astype(np.float32) * k).astype(np.uint8)
    return frame


def main():
    n_frames = int(round(TOTAL * FPS))
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [ff, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0",
           "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", OUT]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    for i in range(n_frames):
        proc.stdin.write(render_frame(i / FPS).tobytes())
        if i % 300 == 0:
            print(f"  frame {i}/{n_frames}  t={i/FPS:6.2f}s", flush=True)
    proc.stdin.close()
    err = proc.stderr.read().decode("utf-8", "ignore")
    if proc.wait() != 0:
        print(err[-2500:])
        raise SystemExit("ffmpeg failed")
    print("wrote", OUT, os.path.getsize(OUT) // 1024, "KB")


if __name__ == "__main__":
    main()
