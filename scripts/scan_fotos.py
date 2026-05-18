#!/usr/bin/env python3
"""
scan_fotos.py — Escanea la carpeta /fotos/ y genera catalogo.json
con metadata básica de cada foto para que el generador las use.

Uso: python3 scripts/scan_fotos.py [--proj-dir /ruta/al/proyecto]
"""

import json
import sys
from pathlib import Path


EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def scan(proj_dir: Path) -> list[dict]:
    fotos_dir = proj_dir / "fotos"
    fotos = []

    for f in sorted(fotos_dir.iterdir()):
        if f.suffix.lower() not in EXTENSIONS:
            continue

        from PIL import Image
        try:
            img = Image.open(f)
            w, h = img.size
            orientation = "portrait" if h > w else "landscape"
        except Exception:
            w, h, orientation = 0, 0, "unknown"

        fotos.append({
            "archivo": f.name,
            "path": str(f),
            "orientacion": orientation,
            "ancho": w,
            "alto": h,
            "descripcion": "",  # El usuario puede llenar esto manualmente
            "tags": [],         # El skill puede sugerir tags según el nombre
            "usado_en": [],
        })

    return fotos


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--proj-dir", default=".", help="Directorio raíz del proyecto")
    args = parser.parse_args()

    proj_dir = Path(args.proj_dir).resolve()
    fotos = scan(proj_dir)

    catalogo_path = proj_dir / "catalogo.json"
    catalogo_path.write_text(json.dumps(fotos, indent=2, ensure_ascii=False))

    print(f"✅ {len(fotos)} foto(s) catalogada(s) → catalogo.json")
    for f in fotos:
        print(f"   • {f['archivo']} ({f['orientacion']}, {f['ancho']}×{f['alto']})")

    return fotos


if __name__ == "__main__":
    main()
