#!/usr/bin/env python3
"""
generate.py — Genera las historias de Instagram a partir de un plan JSON.

Uso:
  python3 scripts/generate.py --plan plan.json [--proj-dir /ruta/proyecto]

El plan.json tiene esta estructura:
{
  "slides": [
    {
      "numero": 1,
      "tipo": "hook",            // hook | problema | revelacion | beneficios | prueba | cta
      "titulo": "Texto grande",
      "subtitulo": "Texto secundario",
      "texto_extra": "Texto pequeño opcional",
      "foto": "nombre_foto.jpg", // null para fondo sólido o AI
      "fondo_ia": {              // null si no se usa Kie AI
        "prompt": "descripción del fondo a generar"
      },
      "palabras_clave": ["palabra1", "palabra2"], // se resaltan en color primario
      "cta_palabra": "KEYWORD"  // solo en slide tipo cta
    }
  ]
}
"""

import json
import os
import sys
import time
import threading
import urllib.request
from datetime import datetime
from pathlib import Path

# Asegurar imports del proyecto
PROJ_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(PROJ_DIR / "scripts"))

from utils import (
    W, H, load_config, colors_from_config, font as _font,
    new_canvas, load_bg, gradient_overlay, draw_text,
    draw_pill, progress_bar, save,
)
from PIL import Image, ImageDraw


def font(proj_dir: Path, size: int, bold: bool = False):
    return _font(proj_dir, size, bold)


# ── Kie AI ─────────────────────────────────────────────────────────────────────

def kie_generate(prompt: str, api_key: str) -> str | None:
    """Genera imagen con Kie AI y retorna la URL del resultado."""
    payload = json.dumps({
        "model": "nano-banana-2",
        "input": {
            "prompt": prompt + ", professional quality, no text",
            "aspect_ratio": "9:16",
            "resolution": "1K",
            "output_format": "png",
        },
    }).encode()

    req = urllib.request.Request(
        "https://api.kie.ai/api/v1/jobs/createTask",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
        data = resp.get("data") or {}
        task_id = data.get("taskId")
        if not task_id:
            print(f"  ⚠️  Kie AI: {resp.get('msg', 'sin task_id')}")
            return None
    except Exception as e:
        print(f"  ⚠️  Kie AI error al crear tarea: {e}")
        return None

    # Polling
    for _ in range(60):
        time.sleep(3)
        try:
            poll = urllib.request.Request(
                f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={task_id}",
                headers={"Authorization": f"Bearer {api_key}"},
            )
            data = json.loads(urllib.request.urlopen(poll, timeout=15).read())
            inner = data.get("data") or {}
            state = inner.get("state")
            if state == "success":
                result_json = inner.get("resultJson", "{}")
                urls = json.loads(result_json).get("resultUrls", [])
                return urls[0] if urls else None
            if state in ("failed", "error"):
                print(f"  ⚠️  Kie AI tarea fallida: {inner.get('failMsg')}")
                return None
        except Exception as e:
            print(f"  ⚠️  Kie AI poll error: {e}")
    return None


def download_image(url: str, dest: Path) -> bool:
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0", "Referer": "https://kie.ai/"},
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            dest.write_bytes(r.read())
        return True
    except Exception as e:
        print(f"  ⚠️  Error descargando imagen: {e}")
        return False


# ── Renderizado de slides ──────────────────────────────────────────────────────

def render_slide(slide: dict, idx: int, total: int,
                 proj_dir: Path, cfg: dict, colors: dict,
                 kie_cache: dict, kie_key: str | None,
                 output_dir: Path) -> Path:

    tipo = slide.get("tipo", "hook")
    foto = slide.get("foto")
    fondo_ia = slide.get("fondo_ia")
    keywords = slide.get("palabras_clave", [])

    PRIMARY = colors["PRIMARY"]
    WHITE = colors["WHITE"]
    DIM = colors["DIM"]
    YELLOW = colors["YELLOW"]

    # ── Fondo ──────────────────────────────────────────────────────────────────
    if foto:
        foto_path = proj_dir / "fotos" / foto
        if foto_path.exists():
            img = load_bg(foto_path, darken=0.55)
            gradient_overlay(img, "bottom", 0.70)
        else:
            print(f"  ⚠️  Foto no encontrada: {foto}, usando fondo sólido")
            img = new_canvas(colors)
    elif fondo_ia and kie_key:
        cache_key = fondo_ia.get("prompt", "")
        if cache_key in kie_cache:
            img = load_bg(kie_cache[cache_key], darken=0.50)
        else:
            img = new_canvas(colors)
    else:
        img = new_canvas(colors)

    draw = ImageDraw.Draw(img)

    # ── Barra de progreso ──────────────────────────────────────────────────────
    progress_bar(draw, idx, total, PRIMARY)

    # ── Contenido según tipo ───────────────────────────────────────────────────
    titulo = slide.get("titulo", "")
    subtitulo = slide.get("subtitulo", "")
    texto_extra = slide.get("texto_extra", "")

    if tipo == "hook":
        # Etiqueta en la parte superior
        draw_pill(draw, cfg.get("etiqueta_hook", "NUEVA HISTORIA"), 120,
                  font(proj_dir, 34), PRIMARY)
        # Título grande centrado en la zona inferior (60% hacia abajo)
        y = 820
        y = draw_text(draw, titulo, y, font(proj_dir, 96, bold=True), WHITE,
                      max_w=960, stroke=1)
        if subtitulo:
            y += 20
            draw_text(draw, subtitulo, y, font(proj_dir, 80), PRIMARY,
                      max_w=960, stroke=2)

    elif tipo == "cta":
        cta_palabra = slide.get("cta_palabra", "PALABRA")
        nombre_marca = cfg.get("instagram_user") or cfg.get("nombre_marca", "@tumarca")
        y = 700
        draw_text(draw, titulo, y, font(proj_dir, 86, bold=True), WHITE, max_w=900)
        y += 160
        draw_text(draw, "Responde", y, font(proj_dir, 68), DIM)
        y += 100
        box_w, box_h = 520, 120
        bx = (W - box_w) // 2
        draw.rounded_rectangle([bx, y, bx + box_w, y + box_h], radius=24,
                               fill=(*YELLOW, 40), outline=YELLOW, width=3)
        kw_f = font(proj_dir, 62, bold=True)
        bb = draw.textbbox((0, 0), cta_palabra, font=kw_f)
        kx = (W - (bb[2] - bb[0])) // 2
        draw.text((kx + 2, y + 26 + 2), cta_palabra, font=kw_f, fill=(0, 0, 0, 120))
        draw.text((kx, y + 26), cta_palabra, font=kw_f, fill=YELLOW,
                  stroke_width=2, stroke_fill=YELLOW)
        y += box_h + 48
        draw_text(draw, subtitulo or "y te mando el tutorial completo.", y,
                  font(proj_dir, 62), DIM, max_w=880)
        if nombre_marca:
            draw_text(draw, nombre_marca, y + 100, font(proj_dir, 52), PRIMARY)

    else:
        # Slides genéricos: problema, revelacion, beneficios, prueba
        # Contenido centrado en la zona media-baja del slide
        y = 750
        if titulo:
            y = draw_text(draw, titulo, y, font(proj_dir, 96, bold=True), WHITE,
                          max_w=940, stroke=1)
            y += 28
        if subtitulo:
            y = draw_text(draw, subtitulo, y, font(proj_dir, 72), PRIMARY,
                          max_w=900, stroke=2)
            y += 28
        if texto_extra:
            draw_text(draw, texto_extra, y, font(proj_dir, 58), DIM, max_w=880)

    # ── Guardar ────────────────────────────────────────────────────────────────
    nombre = f"{idx:02d}-{tipo}.png"
    return save(img, output_dir, nombre)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True, help="Ruta al plan.json")
    parser.add_argument("--proj-dir", default=".", help="Directorio raíz del proyecto")
    args = parser.parse_args()

    proj_dir = Path(args.proj_dir).resolve()
    cfg = load_config(proj_dir)
    colors = colors_from_config(cfg)

    plan = json.loads(Path(args.plan).read_text())
    slides = plan["slides"]
    total = len(slides)

    ts = datetime.now().strftime("%Y-%m-%d_%H%M")
    output_dir = proj_dir / "output" / f"historias_{ts}"
    output_dir.mkdir(parents=True, exist_ok=True)

    kie_key = cfg.get("kie_ai_key") or os.environ.get("KIE_AI_API_KEY")
    kie_cache: dict[str, Path] = {}

    # Pre-generar fondos AI en paralelo
    if kie_key:
        ai_slides = [(i, s) for i, s in enumerate(slides)
                     if s.get("fondo_ia") and not s.get("foto")]
        if ai_slides:
            print(f"\n→ Generando {len(ai_slides)} fondo(s) con IA en paralelo...")
            results: dict[int, str | None] = {}

            def gen(idx, slide):
                try:
                    prompt = slide["fondo_ia"]["prompt"]
                    url = kie_generate(prompt, kie_key)
                    if url:
                        dest = output_dir / f"_bg_{idx:02d}.png"
                        if download_image(url, dest):
                            results[idx] = dest
                            print(f"  ✅ Fondo IA slide {idx+1} listo")
                except Exception as e:
                    print(f"  ⚠️  Thread slide {idx+1} error: {e}")

            threads = [threading.Thread(target=gen, args=(i, s)) for i, s in ai_slides]
            for t in threads:
                t.start()
            for t in threads:
                t.join()

            for idx, slide in ai_slides:
                if idx in results:
                    key = slide["fondo_ia"]["prompt"]
                    kie_cache[key] = results[idx]

    print(f"\n→ Renderizando {total} slides...")
    for i, slide in enumerate(slides, 1):
        render_slide(slide, i, total, proj_dir, cfg, colors,
                     kie_cache, kie_key, output_dir)

    # Guardar copia del plan
    (output_dir / "plan.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False))

    print(f"\n✅ Historias generadas en: {output_dir}")
    return str(output_dir)


if __name__ == "__main__":
    main()
