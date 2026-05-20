# Historias IG Skill — Claude Code

Genera historias de Instagram profesionales para tu negocio con un solo comando en Claude Code.

El skill te hace preguntas la primera vez para entender tu marca, y después solo necesitas decirle el tema del día.

---

## ¿Qué genera?

6 slides listos para publicar (1080×1920 px), con:
- Tu foto de fondo o imagen generada con IA
- Tipografía de impacto con tus colores de marca
- Estructura narrativa probada: hook → problema → solución → beneficios → prueba → CTA
- Palabra clave de CTA lista para tu automatización de DMs

---

## Requisitos

- [Claude Code](https://claude.ai/code) instalado (con suscripción Pro o Max)
- Python 3.10+
- macOS o Linux *(Windows requiere WSL — ver nota abajo)*
- *(Opcional)* Cuenta de [Kie AI](https://kie.ai) para fondos generados con IA

> **Windows:** Usa PowerShell y corre `.\setup.ps1` (ver sección de instalación).

---

## Instalación

### Opción A — Instalación con Claude Code (recomendado)

Abre Claude Code, pega este mensaje y envíalo:

```
Clona https://github.com/santmun/historias-ig-skill.git en ~/historias-ig y corre el setup automáticamente según mi sistema operativo
```

Claude clonará el repositorio y ejecutará el instalador por ti.

Cuando termine, **cierra y vuelve a abrir Claude Code** para que detecte el nuevo skill.

---

### Opción B — Instalación manual

**1. Clona el repositorio**
```bash
git clone https://github.com/santmun/historias-ig-skill.git ~/historias-ig
cd ~/historias-ig
```

**2. Corre el instalador**

macOS / Linux:
```bash
chmod +x setup.sh && ./setup.sh
```

Windows (PowerShell):
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
.\setup.ps1
```

**3. Reinicia Claude Code** para que detecte el nuevo skill `/historias-ig`.

---

### *(Opcional)* Agrega Kie AI para fondos generados con IA

Si quieres que el skill genere fondos e ilustraciones automáticamente, abre `.env` y agrega tu key de [Kie AI](https://kie.ai):

```
KIE_AI_API_KEY=tu_key_aqui
```

Sin esto, el skill funciona perfectamente usando tus propias fotos como fondo.

---

## Primer uso

1. Pon al menos una foto tuya (o de tu negocio) en la carpeta `fotos/`
2. Abre Claude Code en la carpeta del proyecto:
   ```bash
   claude ~/historias-ig
   ```
3. Escribe:
   ```
   /historias-ig
   ```
4. El skill te hará preguntas sobre tu marca una sola vez y se configura automáticamente.

---

## Uso diario

```
/historias-ig
```

El skill te pregunta el tema del día, crea el guión, genera las imágenes y abre la carpeta con los resultados.

---

## Comandos disponibles

| Comando | Qué hace |
|---------|----------|
| `/historias-ig` | Genera historias del día |
| `/historias-ig reconfigurar` | Cambia los datos de tu marca |
| `/historias-ig fotos` | Re-escanea tus fotos disponibles |
| `/historias-ig ver` | Abre la última carpeta de output |

---

## Estructura del proyecto

```
historias-ig/
├── fotos/          ← Pon aquí tus fotos (JPG, PNG, WEBP)
├── output/         ← Las historias generadas aparecen aquí
├── scripts/
│   ├── generate.py     ← Motor de generación de imágenes
│   ├── scan_fotos.py   ← Escanea y cataloga tus fotos
│   └── utils.py        ← Funciones de renderizado
├── skill/
│   └── historias-ig.md ← El skill de Claude Code
├── fonts/          ← Fuentes (instaladas por setup.sh)
├── .env            ← Tus API keys (NO subir a git)
├── config.json     ← Tu configuración de marca (generado al primer uso)
└── setup.sh        ← Instalador automático
```

---

## Personalización

Después del primer uso, puedes editar `config.json` directamente para ajustar cualquier detalle de tu marca sin pasar por el onboarding otra vez.

---

## Créditos

Skill creado por [Horizontes IA](https://horizontesia.com) — Academia de educación y automatización con IA en español.

Comunidad: [horizontesia.com/comunidad](https://horizontesia.com/comunidad)
