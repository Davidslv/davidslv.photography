"""Papaya film still: everything quiet except McLaren papaya and red.

Matches David's 'option C' recipe for the McLaren open day (notes.md, 10 Oct 2026): desaturate to about 60%
except papaya and red, which stay at camera colour (slightly boosted); light split tone; very light grain.
"""
import numpy as np
from PIL import Image, ImageFilter


def rgb_to_hsv(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(-1), a.min(-1)
    d = mx - mn + 1e-6
    h = np.where(mx == r, (g - b) / d % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    s = np.where(mx > 0, (mx - mn) / (mx + 1e-6), 0)
    return h, s, mx


def grade(im, keep=0.6, boost=1.06, grain=0.006, seed=7):
    a = np.asarray(im.convert("RGB"), np.float32) / 255
    h, s, v = rgb_to_hsv(a)
    # papaya/orange 12-45 deg, red 345-12 deg; soft edges in hue, needs some saturation and light
    def band(lo, hi, soft=8):
        return np.clip(np.minimum(h - (lo - soft), (hi + soft) - h) / soft, 0, 1)
    hue = np.maximum(band(12, 45), np.maximum(band(-30, 12), band(338, 390)))
    mask = hue * np.clip((s - 0.28) / 0.2, 0, 1) * np.clip((v - 0.12) / 0.15, 0, 1)
    m = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))
    mask = np.asarray(m, np.float32)[..., None] / 255
    lum = (a * np.array([0.2126, 0.7152, 0.0722], np.float32)).sum(-1, keepdims=True)
    quiet = lum + (a - lum) * keep
    loud = lum + (a - lum) * boost
    out = quiet * (1 - mask) + loud * mask
    # gentle curve: lifted blacks, soft shoulder
    out = 0.03 + 0.95 * np.clip(out, 0, 1) ** 0.94
    out = out - 0.06 * np.clip(out - 0.75, 0, None) ** 2 / 0.0625 * 0.25
    # split tone: teal shadows, amber highlights (small)
    l2 = (out * np.array([0.2126, 0.7152, 0.0722], np.float32)).sum(-1, keepdims=True)
    sh = np.clip(1 - l2 / 0.45, 0, 1) * (1 - mask)
    hi = np.clip((l2 - 0.6) / 0.4, 0, 1) * (1 - mask)
    out = out + sh * np.array([-0.012, 0.004, 0.014], np.float32) + hi * np.array([0.012, 0.005, -0.01], np.float32)
    if grain:
        rng = np.random.default_rng(seed)
        out = out + rng.normal(0, grain, out.shape[:2])[..., None].astype(np.float32)
    return Image.fromarray((np.clip(out, 0, 1) * 255 + .5).astype(np.uint8))
