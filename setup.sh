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

# 1. Dependencias Python
echo "→ Instalando dependencias Python..."
pip3 install -r "$PROJ_DIR/requirements.txt" -q
echo "  ✅ Dependencias listas"

# 2. Fuentes (Space Grotesk via Google Fonts)
FONTS_DIR="$PROJ_DIR/fonts"
if [ ! -f "$FONTS_DIR/SpaceGrotesk-Variable.ttf" ]; then
  echo "→ Descargando fuente Space Grotesk..."
  curl -sL "https://github.com/floriankarsten/space-grotesk/raw/master/fonts/ttf/SpaceGrotesk-Regular.ttf" \
    -o "$FONTS_DIR/SpaceGrotesk-Variable.ttf"
  curl -sL "https://github.com/floriankarsten/space-grotesk/raw/master/fonts/ttf/SpaceGrotesk-Bold.ttf" \
    -o "$FONTS_DIR/SpaceGrotesk-Bold.ttf"
  echo "  ✅ Fuentes descargadas"
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
