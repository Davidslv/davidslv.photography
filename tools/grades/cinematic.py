"""Cinematic film still, after David's option A for the McLaren corridor (notes.md, 10 Oct 2026).

Start from a KERBSIDE D01 Meet Signature render, crop to 2.39:1, lift the blacks, soften the highlights,
teal in the shadows and amber in the highlights, saturation down about 8%, a subtle vignette, fine grain.
"""
import numpy as np
from PIL import Image


def cinematic(im, centre_y=0.55, grain=0.007, seed=11):
    w, h = im.size
    ch = round(w / 2.39)
    if ch < h:
        top = int(min(max(centre_y * h - ch / 2, 0), h - ch))
        im = im.crop((0, top, w, top + ch))
    a = np.asarray(im.convert("RGB"), np.float32) / 255
    lum = (a * np.array([0.2126, 0.7152, 0.0722], np.float32)).sum(-1, keepdims=True)
    a = lum + (a - lum) * 0.92
    a = 0.045 + 0.93 * a
    a = a - 0.08 * np.clip(a - 0.72, 0, None) ** 2 / 0.0784 * 0.3
    l2 = (a * np.array([0.2126, 0.7152, 0.0722], np.float32)).sum(-1, keepdims=True)
    sh = np.clip(1 - l2 / 0.5, 0, 1)
    hi = np.clip((l2 - 0.55) / 0.45, 0, 1)
    a = a + sh * np.array([-0.02, 0.008, 0.024], np.float32) + hi * np.array([0.024, 0.01, -0.018], np.float32)
    hh, ww = a.shape[:2]
    y, x = np.ogrid[:hh, :ww]
    r = np.sqrt(((x - ww / 2) / (ww / 2)) ** 2 + ((y - hh / 2) / (hh / 2)) ** 2)
    a = a * (1 - 0.18 * np.clip(r - 0.55, 0, None) ** 1.6)[..., None]
    if grain:
        a = a + np.random.default_rng(seed).normal(0, grain, (hh, ww))[..., None].astype(np.float32)
    return Image.fromarray((np.clip(a, 0, 1) * 255 + .5).astype(np.uint8))
