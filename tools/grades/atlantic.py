"""Atlantic: a quiet editorial look for the Ericeira skimboard set (2012, Sony A350 JPEGs).

Everything sits at about 80% saturation except the green boards, which keep their colour. Exposure is
normalised per frame (backlit sea frames come down, flat ones go up), highlights roll off softly so the
white water keeps detail, blacks are lifted a touch, a small warm/cool split, light grain and sharpening.
"""
import numpy as np
from PIL import Image, ImageFilter

W = np.array([0.2126, 0.7152, 0.0722], np.float32)


def _hue(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(-1), a.min(-1)
    d = mx - mn + 1e-6
    h = np.where(mx == r, (g - b) / d % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    return h, (mx - mn) / (mx + 1e-6), mx


def grade(im, keep=0.8, ev=0.0, shadows=0.0, grain=0.007, seed=11):
    a = np.asarray(im.convert("RGB"), np.float32) / 255
    lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    # exposure: median luminance toward 0.18 linear, at most +-0.7 EV, plus a manual nudge
    med = float(np.median((lin * W).sum(-1)))
    auto = np.clip(np.log2(0.16 / max(med, 1e-4)), -0.7, 0.7) * 0.6
    lin = lin * 2 ** (auto + ev)
    # soft shoulder in linear light
    lin = np.where(lin < 0.75, lin, 0.75 + 0.25 * np.tanh((lin - 0.75) / 0.25))
    a = np.where(lin <= 0.0031308, lin * 12.92, 1.055 * np.clip(lin, 0, 1) ** (1 / 2.4) - 0.055)
    h, s, v = _hue(a)
    green = np.clip(np.minimum(h - 70, 160 - h) / 12, 0, 1) * np.clip((s - 0.3) / 0.2, 0, 1) * np.clip((v - 0.15) / 0.15, 0, 1)
    m = np.asarray(Image.fromarray((green * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2)), np.float32)[..., None] / 255
    lum = (a * W).sum(-1, keepdims=True)
    a = (lum + (a - lum) * keep) * (1 - m) + (lum + (a - lum) * 1.05) * m
    a = np.clip(a, 0, 1)
    if shadows:  # lift dark tones (backlit figures) without touching the highlights
        l0 = (a * W).sum(-1, keepdims=True)
        a = a + shadows * 0.35 * (1 - l0) ** 3 * np.clip(l0 * 6, 0, 1) + shadows * 0.06 * (1 - l0) ** 4
    # gentle S, lifted blacks
    a = np.clip(a, 0, 1)
    a = a + 0.22 * (a - 0.5) * (1 - np.abs(2 * a - 1))
    a = 0.018 + 0.98 * a
    l2 = (a * W).sum(-1, keepdims=True)
    sh = np.clip(1 - l2 / 0.4, 0, 1) * (1 - m)
    hi = np.clip((l2 - 0.55) / 0.45, 0, 1) * (1 - m)
    a = a + sh * np.array([-0.01, 0.002, 0.012], np.float32) + hi * np.array([0.014, 0.006, -0.008], np.float32)
    if grain:
        a = a + np.random.default_rng(seed).normal(0, grain, a.shape[:2])[..., None].astype(np.float32)
    out = Image.fromarray((np.clip(a, 0, 1) * 255 + .5).astype(np.uint8))
    return out.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
