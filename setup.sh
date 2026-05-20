#!/bin/bash
# setup.sh — Instalación automática de historias-ig-skill
set -e

PROJ_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DEST="$HOME/.claude/commands/historias-ig.md"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Instalador — Historias IG Skill"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 0. Verificar Python 3.10+
echo "→ Verificando Python..."
python3 -c "import sys; exit(0) if sys.version_info >= (3, 10) else exit(1)" 2>/dev/null || {
  echo "  ❌ Python 3.10+ es requerido."
  echo "     Instálalo desde https://python.org o con 'brew install python'"
  exit 1
}
echo "  ✅ Python OK"

# 1. Dependencias Python
echo "→ Instalando dependencias Python..."
pip3 install -r "$PROJ_DIR/requirements.txt" -q
echo "  ✅ Dependencias listas"

# 2. Fuentes (Space Grotesk via Google Fonts)
FONTS_DIR="$PROJ_DIR/fonts"
mkdir -p "$FONTS_DIR"

_check_font() {
  local f="$1"
  # Los archivos TTF válidos empiezan con bytes 00 01 00 00 o 00 00 01 00
  # Si se descarga HTML en vez de la fuente, el archivo empieza con "<"
  local first
  first=$(head -c 5 "$f" 2>/dev/null)
  if echo "$first" | grep -q "^<"; then
    return 1  # Es HTML, no una fuente
  fi
  # Verificar tamaño mínimo (fuentes reales > 50KB)
  local size
  size=$(wc -c < "$f" 2>/dev/null || echo 0)
  [ "$size" -gt 50000 ]
}

if [ ! -f "$FONTS_DIR/SpaceGrotesk-Variable.ttf" ] || ! _check_font "$FONTS_DIR/SpaceGrotesk-Variable.ttf"; then
  echo "→ Descargando fuente Space Grotesk (Google Fonts)..."
  curl -sL "https://fonts.gstatic.com/s/spacegrotesk/v22/V8mQoQDjQSkFtoMM3T6r8E7mF71Q-gOoraIAEj7oUUsj.ttf" \
    -o "$FONTS_DIR/SpaceGrotesk-Variable.ttf"
  curl -sL "https://fonts.gstatic.com/s/spacegrotesk/v22/V8mQoQDjQSkFtoMM3T6r8E7mF71Q-gOoraIAEj4PVksj.ttf" \
    -o "$FONTS_DIR/SpaceGrotesk-Bold.ttf"
  if _check_font "$FONTS_DIR/SpaceGrotesk-Variable.ttf"; then
    echo "  ✅ Fuentes descargadas"
  else
    echo "  ❌ Error al descargar fuentes (revisa tu conexión a internet)"
    rm -f "$FONTS_DIR/SpaceGrotesk-Variable.ttf" "$FONTS_DIR/SpaceGrotesk-Bold.ttf"
    exit 1
  fi
else
  echo "  ✅ Fuentes ya instaladas"
fi

# 3. Copiar skill a ~/.claude/commands/
mkdir -p "$HOME/.claude/commands"
# Inyectar el path del proyecto en el skill
sed "s|{{PROJ_DIR}}|$PROJ_DIR|g" "$PROJ_DIR/skill/historias-ig.md" > "$SKILL_DEST"
echo "  ✅ Skill instalado en $SKILL_DEST"

# 4. Crear .env si no existe
if [ ! -f "$PROJ_DIR/.env" ]; then
  cp "$PROJ_DIR/.env.example" "$PROJ_DIR/.env"
  echo "  ✅ Archivo .env creado — agrega tus API keys"
else
  echo "  ✅ .env ya existe"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ Instalación completa"
echo ""
echo "  Próximos pasos:"
echo "  1. (Opcional) Agrega KIE_AI_API_KEY en .env para fondos con IA"
echo "  2. Pon tus fotos en: $PROJ_DIR/fotos/"
echo "  3. Abre Claude Code y escribe: /historias-ig"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
