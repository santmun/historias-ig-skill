# setup.ps1 — Instalación automática de historias-ig-skill (Windows)
# Ejecutar desde PowerShell: .\setup.ps1

$ErrorActionPreference = "Stop"

$PROJ_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$SKILL_DEST = "$env:USERPROFILE\.claude\commands\historias-ig.md"

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-Host "  Instalador — Historias IG Skill"
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-Host ""

# 0. Verificar Python 3.10+
Write-Host "→ Verificando Python..."
$pythonCmd = $null
foreach ($cmd in @("python3", "python", "py")) {
    try {
        $ok = & $cmd -c "import sys; print(sys.version_info >= (3,10))" 2>$null
        if ($ok -eq "True") { $pythonCmd = $cmd; break }
    } catch {}
}
if (-not $pythonCmd) {
    Write-Host "  ❌ Python 3.10+ es requerido."
    Write-Host "     Descárgalo desde https://python.org"
    exit 1
}
Write-Host "  ✅ Python OK ($pythonCmd)"

# 1. Dependencias Python (Pillow)
Write-Host "→ Instalando dependencias Python..."
& $pythonCmd -m pip install -r "$PROJ_DIR\requirements.txt" -q 2>$null
if ($LASTEXITCODE -ne 0) {
    & $pythonCmd -m pip install -r "$PROJ_DIR\requirements.txt" -q --break-system-packages
}
Write-Host "  ✅ Dependencias listas"

# 2. Fuentes (Space Grotesk via Google Fonts)
$FONTS_DIR = "$PROJ_DIR\fonts"
New-Item -ItemType Directory -Force -Path $FONTS_DIR | Out-Null

function Test-FontFile($path) {
    if (-not (Test-Path $path)) { return $false }
    if ((Get-Item $path).Length -lt 50000) { return $false }
    $bytes = [System.IO.File]::ReadAllBytes($path)
    return $bytes[0] -ne 0x3C   # 0x3C = '<' (HTML)
}

$fontVariable = "$FONTS_DIR\SpaceGrotesk-Variable.ttf"
$fontBold     = "$FONTS_DIR\SpaceGrotesk-Bold.ttf"

if (-not (Test-FontFile $fontVariable)) {
    Write-Host "→ Descargando fuente Space Grotesk (Google Fonts)..."
    $client = New-Object System.Net.WebClient
    try {
        $client.DownloadFile(
            "https://fonts.gstatic.com/s/spacegrotesk/v22/V8mQoQDjQSkFtoMM3T6r8E7mF71Q-gOoraIAEj7oUUsj.ttf",
            $fontVariable
        )
        $client.DownloadFile(
            "https://fonts.gstatic.com/s/spacegrotesk/v22/V8mQoQDjQSkFtoMM3T6r8E7mF71Q-gOoraIAEj4PVksj.ttf",
            $fontBold
        )
    } finally { $client.Dispose() }

    if (Test-FontFile $fontVariable) {
        Write-Host "  ✅ Fuentes descargadas"
    } else {
        Write-Host "  ❌ Error al descargar fuentes (revisa tu conexión a internet)"
        Remove-Item $fontVariable -ErrorAction SilentlyContinue
        Remove-Item $fontBold -ErrorAction SilentlyContinue
        exit 1
    }
} else {
    Write-Host "  ✅ Fuentes ya instaladas"
}

# 3. Copiar skill a %USERPROFILE%\.claude\commands\
New-Item -ItemType Directory -Force -Path (Split-Path $SKILL_DEST) | Out-Null
# Usar forward slashes en el path para que Python los maneje igual en Windows
$projDirUnix = $PROJ_DIR.Replace("\", "/")
$skillContent = (Get-Content "$PROJ_DIR\skill\historias-ig.md" -Raw -Encoding UTF8)
$skillContent = $skillContent.Replace("{{PROJ_DIR}}", $projDirUnix)
Set-Content -Path $SKILL_DEST -Value $skillContent -Encoding UTF8 -NoNewline
Write-Host "  ✅ Skill instalado en $SKILL_DEST"

# 4. Crear .env si no existe
if (-not (Test-Path "$PROJ_DIR\.env")) {
    Copy-Item "$PROJ_DIR\.env.example" "$PROJ_DIR\.env"
    Write-Host "  ✅ Archivo .env creado — agrega tus API keys"
} else {
    Write-Host "  ✅ .env ya existe"
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-Host "  ✅ Instalación completa"
Write-Host ""
Write-Host "  Próximos pasos:"
Write-Host "  1. (Opcional) Agrega KIE_AI_API_KEY en .env para fondos con IA"
Write-Host "  2. Pon tus fotos en: $PROJ_DIR\fotos\"
Write-Host "  3. Abre Claude Code y escribe: /historias-ig"
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-Host ""
