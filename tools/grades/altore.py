"""Altore: a dry August look for the Sicily set (Nikon Z 6II NEFs, Aug 2025, Monte Altore and the town).

Warm early light, white soil kept off the clip, greens pulled to dry olive, the grapes left blue-black and rich.
Blacks lifted a touch, a soft shoulder, fine grain. The night variant keeps the same curve and takes the sodium
orange down to amber and the violet festival lights down, so the town sits with the vineyard.

Three strengths: gentle, mid, film.

    from altore import develop, grade
    im = grade(develop(nef_path), "mid", night=False)

Source is the camera's full-size JPEG inside the NEF (see develop).
"""
import numpy as np
from PIL import Image

W = np.array([0.2126, 0.7152, 0.0722], np.float32)

STRENGTH = {
    #          sat   green  olive  lift   shoulder warm  grain  vignette contrast
    "gentle": (0.95, 0.85, 6.0, 0.015, 0.30, 0.015, 0.004, 0.00, 0.20),
    "mid":    (0.88, 0.70, 12.0, 0.035, 0.50, 0.030, 0.008, 0.08, 0.40),
    "film":   (0.80, 0.55, 18.0, 0.060, 0.70, 0.045, 0.014, 0.16, 0.60),
}


def develop(path, long_edge=3000):
    """NEF to float sRGB 0-1 from the camera's own full-size render (JpgFromRaw), upright.

    A plain rawpy develop turned the Z 6II skies cyan; Nikon's render keeps the colour David saw.
    """
    import io
    import subprocess
    from PIL import ImageOps
    jpg = subprocess.run(["exiftool", "-b", "-JpgFromRaw", str(path)], capture_output=True, check=True).stdout
    o = subprocess.run(["exiftool", "-n", "-s3", "-Orientation", str(path)], capture_output=True, text=True).stdout.strip()
    im = Image.open(io.BytesIO(jpg)).convert("RGB")
    im = im.rotate({"3": 180, "6": 270, "8": 90}.get(o, 0), expand=True)
    im.thumbnail((long_edge, long_edge), Image.LANCZOS)
    return np.asarray(im, np.float32) / 255


def _rgb2hsv(a):
    """RGB 0-1 to H in degrees, S and V 0-1 (same convention as OpenCV's float HSV)."""
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(-1), a.min(-1)
    d = mx - mn
    dd = np.where(d == 0, 1, d)
    h = np.where(mx == r, (g - b) / dd % 6, np.where(mx == g, (b - r) / dd + 2, (r - g) / dd + 4)) * 60
    h = np.where(d == 0, 0, h)
    s = np.where(mx > 0, d / np.where(mx == 0, 1, mx), 0)
    return h.astype(np.float32), s.astype(np.float32), mx.astype(np.float32)


def _hsv2rgb(h, s, v):
    h = (h % 360) / 60
    i = np.floor(h).astype(np.int32) % 6
    f = h - np.floor(h)
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    r = np.choose(i, [v, q, p, p, t, v]); g = np.choose(i, [t, v, v, q, p, p]); b = np.choose(i, [p, p, t, v, v, q])
    return np.stack([r, g, b], -1).astype(np.float32)


def _exposure(a, night):
    """Normalise each frame: day frames to a mid median, night frames kept dark."""
    lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    med = float(np.median(a @ W))
    target = 0.20 if night else 0.33
    ev = np.clip(np.log2(target / max(med, 1e-4)) * 0.6, -0.6, 0.6 if night else 0.0)  # never brighten a day frame
    lin = lin * 2 ** ev
    return np.where(lin <= 0.0031308, lin * 12.92, 1.055 * np.clip(lin, 0, None) ** (1 / 2.4) - 0.055)


def _ev(a, ev):
    """Per-photo exposure in stops, in linear light."""
    lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4) * 2 ** ev
    return np.where(lin <= 0.0031308, lin * 12.92, 1.055 * np.clip(lin, 0, None) ** (1 / 2.4) - 0.055)


def _night_balance(a, amount=0.12):
    """Take part of the sodium cast out, so walls read warm cream rather than orange."""
    m = a.reshape(-1, 3).mean(0)
    gain = (m.mean() / np.maximum(m, 1e-4)) ** amount
    return a * gain


def _tone(a, lift, shoulder, contrast=0.35):
    """Mids held, a gentle S, highlights eased down so white soil keeps detail, blacks lifted. On luma, so colour holds."""
    y = a @ W
    sm = y * y * (3 - 2 * y)
    yt = y + contrast * (sm - y)                                        # gentle S around the middle
    yt = yt * (1 - shoulder * 0.10 * np.clip((yt - 0.65) / 0.35, 0, 1) ** 2)   # ease the top
    yt = lift + (1 - lift) * np.clip(yt, 0, 1)                      # lifted toe
    k = yt / np.maximum(y, 1e-5)
    mx = np.maximum(a.max(-1), 1e-5)
    safe = np.minimum(k, 0.995 / mx)                   # scale only as far as the brightest channel allows
    out = a * safe[..., None]
    short = np.clip(yt - out @ W, 0, None) / np.maximum(1 - out @ W, 1e-5)
    return out + (1 - out) * short[..., None]          # make up the rest towards white, so no channel clips and hue holds


def _colour(a, sat, green, olive, night):
    h, s, v = _rgb2hsv(np.clip(a, 0, 1).astype(np.float32))

    def band(lo, hi, soft=15):
        return np.clip(np.minimum(h - lo + soft, hi - h + soft) / soft, 0, 1)

    g = band(65, 160)                                   # greens: drier, towards olive
    s *= 1 - g * (1 - green)
    h -= g * olive * np.clip((h - 60) / 40, 0, 1)
    grape = band(200, 285)                              # blue-black grapes: keep rich, a little deeper
    sky = band(185, 240, 10) * np.clip((v - 0.55) / 0.25, 0, 1)   # bright blue is sky, not grape
    grape = np.maximum(grape - sky, 0) + sky
    s *= 1 + (grape - sky) * 0.10 - sky * 0.06
    v *= 1 - (grape - sky) * 0.06
    if night:
        orange = band(12, 45)                           # sodium to amber
        s *= 1 + orange * 0.05                          # keep the sodium warmth
        h += orange * 3
        violet = band(260, 335)
        s *= 1 - violet * 0.55
    s *= sat if not night else (1 + sat) / 2
    return _hsv2rgb(h, np.clip(s, 0, 1), v)


def _split(a, warm):
    y = (a @ W)[..., None]
    hi = np.clip((y - 0.45) / 0.5, 0, 1)
    lo = np.clip((0.4 - y) / 0.4, 0, 1)
    blue = np.clip((a[..., 2:3] - a[..., 0:1]) / 0.12, 0, 1)                # keep skies blue, not mint
    hi = hi * (1 - blue)
    a = a + hi * np.array([warm, warm * 0.35, -warm], np.float32)          # warm paper highlights
    a = a + lo * np.array([warm * 0.3, warm * 0.25, -warm * 0.4], np.float32)  # olive-brown shadows
    return a


def _finish(a, grain, vignette, seed=7):
    h, w = a.shape[:2]
    if vignette:
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        d = ((xx / w - 0.5) ** 2 + (yy / h - 0.5) ** 2) / 0.5
        a = a * (1 - vignette * d ** 1.5)[..., None]
    if grain:
        rng = np.random.default_rng(seed)
        n = rng.standard_normal((h, w)).astype(np.float32)
        k = np.array([0.18, 0.64, 0.18], np.float32)          # about a 0.7 px gaussian, so the grain clumps a little
        n = k[0] * np.roll(n, 1, 0) + k[1] * n + k[2] * np.roll(n, -1, 0)
        n = (k[0] * np.roll(n, 1, 1) + k[1] * n + k[2] * np.roll(n, -1, 1)) / 0.69
        y = a @ W
        a = a + (n * grain * 4 * np.sqrt(np.clip(y * (1 - y), 0, 0.25)))[..., None]
    return a


def grade(a, strength="mid", night=False, contrast=None, ev=0.0):
    """a: float sRGB 0-1 (from develop) or a PIL image. Returns a PIL image."""
    if isinstance(a, Image.Image):
        a = np.asarray(a.convert("RGB"), np.float32) / 255
    sat, green, olive, lift, shoulder, warm, grain, vig, c = STRENGTH[strength]
    contrast = c if contrast is None else contrast
    if night:
        lift *= 0.6
    a = _exposure(a, night)
    if ev:
        a = _ev(a, ev)
    if night:
        a = _night_balance(a)
    a = _tone(a, lift, shoulder, contrast)
    a = _colour(a, sat, green, olive, night)
    a = _split(a, 0 if night else warm)
    a = _finish(a, grain, vig)
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))


def cube(path, strength="mid", n=33):
    """Write the pointwise part of Altore (tone, colour, split) as a .cube 3D LUT for Lightroom, Photoshop or Resolve.

    Left out because a LUT cannot hold them: per-frame exposure, grain and vignette.
    """
    sat, green, olive, lift, shoulder, warm, grain, vig, contrast = STRENGTH[strength]
    g = np.linspace(0, 1, n, dtype=np.float32)
    b, gg, r = np.meshgrid(g, g, g, indexing="ij")          # .cube order: red changes fastest
    a = np.stack([r, gg, b], -1).reshape(1, -1, 3)
    a = _tone(a, lift, shoulder, contrast)
    a = _colour(a, sat, green, olive, False)
    a = _split(a, warm)
    a = np.clip(a, 0, 1).reshape(-1, 3)
    with open(path, "w") as f:
        f.write(f'TITLE "Altore {strength.title()}"\n# davidslv.photography, Sicily 2025. sRGB in, sRGB out.\nLUT_3D_SIZE {n}\n')
        f.writelines(f"{x:.6f} {y:.6f} {z:.6f}\n" for x, y, z in a)


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    for s in STRENGTH:
        cube(f"{out}/Altore {s.title()}.cube", s)
