"""
utils.py — Funciones de renderizado compartidas para historias de Instagram.
Canvas: 1080x1920 RGBA
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H = 1080, 1920


def load_config(proj_dir: Path) -> dict:
    import json
    cfg_path = proj_dir / "config.json"
    if not cfg_path.exists():
        raise FileNotFoundError("config.json no encontrado. Corre /historias-ig para configurar.")
    return json.loads(cfg_path.read_text())


def colors_from_config(cfg: dict) -> dict:
    c = cfg.get("colores", {})
    def hex2rgb(h: str) -> tuple:
        h = h.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    return {
        "BG":       hex2rgb(c.get("fondo",    "#08080F")),
        "PRIMARY":  hex2rgb(c.get("primario",  "#00E5FF")),
        "WHITE":    (255, 255, 255),
        "DIM":      (180, 185, 195),
        "YELLOW":   (255, 230, 50),
    }


def font(proj_dir: Path, size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    fname = "SpaceGrotesk-Bold.ttf" if bold else "SpaceGrotesk-Variable.ttf"
    path = proj_dir / "fonts" / fname
    try:
        return ImageFont.truetype(str(path), size)
    except Exception:
        return ImageFont.load_default()


def new_canvas(colors: dict) -> Image.Image:
    return Image.new("RGBA", (W, H), (*colors["BG"], 255))


def load_bg(path: str | Path, darken: float = 0.55, blur: int = 0) -> Image.Image:
    bg = Image.open(path).convert("RGBA")
    r = max(W / bg.width, H / bg.height)
    nw, nh = int(bg.width * r), int(bg.height * r)
    bg = bg.resize((nw, nh), Image.LANCZOS)
    l, t = (nw - W) // 2, (nh - H) // 2
    bg = bg.crop((l, t, l + W, t + H))
    if blur:
        bg = bg.filter(ImageFilter.GaussianBlur(blur))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, int(255 * darken)))
    bg.alpha_composite(overlay)
    return bg


def gradient_overlay(img: Image.Image, direction: str = "bottom", strength: float = 0.80):
    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(grad)
    for i in range(H):
        if direction == "top":
            t = 1 - i / H
        elif direction == "bottom":
            t = i / H
        else:
            t = abs(i / H - 0.5) * 2
        alpha = int(255 * strength * (t ** 1.5))
        d.line([(0, i), (W, i)], fill=(0, 0, 0, alpha))
    img.alpha_composite(grad)


def draw_text(draw, text: str, y: int, fnt, color=(255, 255, 255),
              max_w: int = 940, line_gap: int = 14, shadow: bool = True,
              stroke: int = 0) -> int:
    """Texto centrado con word-wrap. Retorna el y final."""
    words = text.split()
    lines, cur = [], []
    for word in words:
        test = " ".join(cur + [word])
        bb = draw.textbbox((0, 0), test, font=fnt)
        if bb[2] - bb[0] > max_w and cur:
            lines.append(" ".join(cur))
            cur = [word]
        else:
            cur.append(word)
    if cur:
        lines.append(" ".join(cur))

    lh = fnt.size + line_gap
    for line in lines:
        bb = draw.textbbox((0, 0), line, font=fnt)
        x = (W - (bb[2] - bb[0])) // 2
        if shadow:
            draw.text((x + 3, y + 3), line, font=fnt, fill=(0, 0, 0, 160))
        draw.text((x, y), line, font=fnt, fill=color,
                  stroke_width=stroke, stroke_fill=color if stroke else None)
        y += lh
    return y


def draw_pill(draw, text: str, y: int, fnt, bg_color, text_color=(8, 8, 16)):
    """Píldora centrada con texto."""
    bb = draw.textbbox((0, 0), text, font=fnt)
    pw, ph = bb[2] - bb[0] + 52, bb[3] - bb[1] + 26
    px = (W - pw) // 2
    draw.rounded_rectangle([px, y, px + pw, y + ph], radius=ph // 2, fill=(*bg_color, 230))
    draw.text((px + 26, y + 13), text, font=fnt, fill=text_color)
    return y + ph


def rounded_insert(canvas: Image.Image, img_path: Path, x: int, y: int,
                   w: int, h: int, radius: int = 28):
    """Inserta imagen con esquinas redondeadas."""
    img = Image.open(img_path).convert("RGBA")
    r = max(w / img.width, h / img.height)
    nw, nh = int(img.width * r), int(img.height * r)
    img = img.resize((nw, nh), Image.LANCZOS)
    l, t = (nw - w) // 2, (nh - h) // 2
    img = img.crop((l, t, l + w, t + h))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w, h], radius=radius, fill=255)
    img.putalpha(mask)
    canvas.alpha_composite(img, (x, y))


def progress_bar(draw, current: int, total: int, primary_color):
    """Barra de progreso en la parte superior."""
    seg_w = (W - 24 * (total + 1)) // total
    for i in range(total):
        x = 24 + i * (seg_w + 24)
        color = (*primary_color, 255) if i < current else (255, 255, 255, 80)
        draw.rounded_rectangle([x, 28, x + seg_w, 32], radius=2, fill=color)


def save(img: Image.Image, output_dir: Path, name: str) -> Path:
    flat = Image.new("RGB", (W, H))
    flat.paste(img.convert("RGB"), mask=img.split()[3] if img.mode == "RGBA" else None)
    path = output_dir / name
    flat.save(path, "PNG", optimize=True)
    print(f"  ✅ {name}")
    return path
