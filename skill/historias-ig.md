# /historias-ig — Generador de Historias de Instagram

Genera una secuencia completa de 6 historias de Instagram para tu negocio.
El skill se auto-configura en el primer uso y recuerda tus preferencias.

**Directorio del proyecto:** `{{PROJ_DIR}}`

---

## FLUJO PRINCIPAL

### Al invocar `/historias-ig`

**Paso 1 — Verificar configuración**

Lee `{{PROJ_DIR}}/config.json`. Si no existe, ejecuta el **ONBOARDING** (ver sección abajo).

**Paso 2 — Pedir el tema del día**

Pregunta al usuario:
> "¿Cuál es el tema de hoy? (ej: 'cómo automaticé mis reportes con IA', 'por qué dejé Excel', 'el error que casi me costó un cliente')"

**Paso 3 — Escanear fotos disponibles**

Corre:
```bash
python3 {{PROJ_DIR}}/scripts/scan_fotos.py --proj-dir {{PROJ_DIR}}
```
Esto genera/actualiza `{{PROJ_DIR}}/catalogo.json` con las fotos disponibles.

**Paso 4 — Crear el plan de 6 slides**

Usando la información del `config.json` y el tema del día, crea un plan con esta estructura narrativa:

| Slide | Tipo | Función |
|-------|------|---------|
| 1 | `hook` | Pregunta o declaración que detenga el scroll |
| 2 | `problema` | El dolor/contexto que tu audiencia siente |
| 3 | `revelacion` | La solución o el giro inesperado |
| 4 | `beneficios` | Qué gana quien lo aplica (3 puntos concretos) |
| 5 | `prueba` | Resultado real, número, o captura de pantalla |
| 6 | `cta` | Llamada a acción con palabra clave |

**Reglas para el plan:**
- `titulo`: texto grande y de impacto (máx 8 palabras)
- `subtitulo`: texto secundario con el dato o elaboración
- `palabras_clave`: 1-3 palabras del título que se resaltarán en el color primario de la marca
- `foto`: nombre de archivo de `catalogo.json` que mejor encaje con el tema del slide (puede ser `null`)
- `fondo_ia`: objeto `{"prompt": "..."}` si el usuario tiene Kie AI Y no hay foto. Prompt en inglés, estilo visual que encaje con la marca.
- `cta_palabra`: una sola palabra en MAYÚSCULAS (3-8 letras, sin acentos) temáticamente relacionada al contenido

**Formato del plan JSON:**
```json
{
  "slides": [
    {
      "numero": 1,
      "tipo": "hook",
      "titulo": "¿Cuánto tiempo pierdes cada semana?",
      "subtitulo": null,
      "texto_extra": null,
      "foto": "oficina_escritorio.jpg",
      "fondo_ia": null,
      "palabras_clave": ["tiempo", "semana"],
      "cta_palabra": null
    },
    {
      "numero": 6,
      "tipo": "cta",
      "titulo": "¿Quieres aprender a hacerlo?",
      "subtitulo": "y te mando el tutorial completo.",
      "texto_extra": null,
      "foto": "foto_tuya_mirando_camara.jpg",
      "fondo_ia": null,
      "palabras_clave": [],
      "cta_palabra": "AUTOMATIZA"
    }
  ]
}
```

Muestra el plan al usuario en formato legible (no el JSON crudo) y pide confirmación antes de continuar.

**Paso 5 — Guardar el plan y generar**

Guarda el plan en `{{PROJ_DIR}}/plan.json` y corre:
```bash
python3 {{PROJ_DIR}}/scripts/generate.py \
  --plan {{PROJ_DIR}}/plan.json \
  --proj-dir {{PROJ_DIR}}
```

**Paso 6 — Mostrar resultados**

Lee y muestra al menos el slide 1 (hook) y el slide 6 (CTA) para que el usuario vea el resultado.
Luego abre la carpeta de output:
```bash
open {{PROJ_DIR}}/output/
```

---

## ONBOARDING (primer uso)

Si no existe `config.json`, haz estas preguntas **una por una** (no todas juntas):

1. **¿Cómo se llama tu marca o negocio?**
   → Guarda como `nombre_marca`

2. **¿A qué se dedica tu negocio? Descríbelo en 1-2 oraciones.**
   → Guarda como `descripcion_negocio`

3. **¿Cuál es tu nombre? (para personalizar los textos)**
   → Guarda como `nombre_usuario`

4. **¿Cuál es tu usuario de Instagram?**
   → Guarda como `instagram_user` (agregar @ si no lo pone)

5. **¿Cuáles son tus colores de marca?**
   Opciones:
   - a) Tengo los códigos hex → pedirle fondo y color primario/acento
   - b) Usar paleta por defecto (oscuro con cyan, estilo tech)
   - c) Elegir entre paletas predefinidas: [oscuro-cyan] [oscuro-naranja] [oscuro-verde] [claro-profesional]

   Paletas predefinidas:
   - `oscuro-cyan`: fondo `#08080F`, primario `#00E5FF`
   - `oscuro-naranja`: fondo `#0D0A08`, primario `#FF6B35`
   - `oscuro-verde`: fondo `#080F09`, primario `#00E676`
   - `claro-profesional`: fondo `#F8F9FA`, primario `#1A1A2E`

   → Guarda como `colores: { fondo, primario }`

6. **¿Tienes cuenta en Kie AI? (kie.ai)**
   Si sí: pedir que abra `{{PROJ_DIR}}/.env` y agregue su `KIE_AI_API_KEY`
   Si no: mencionar que el skill funcionará perfectamente con sus fotos, sin generación de imágenes IA

7. **¿Cuál es tu CTA habitual?**
   - a) Responde [PALABRA] y te mando [algo]
   - b) Comenta [PALABRA] y te llega [algo]
   - c) DM directo
   → Guarda como `cta_formato`

8. **¿Qué etiqueta quieres en el primer slide?** (ej: "NUEVA HISTORIA", "HOY COMPARTO", "ESTO ME PASÓ")
   → Guarda como `etiqueta_hook`

Una vez respondidas, **crea `{{PROJ_DIR}}/config.json`**:
```json
{
  "nombre_marca": "...",
  "descripcion_negocio": "...",
  "nombre_usuario": "...",
  "instagram_user": "@...",
  "etiqueta_hook": "...",
  "colores": {
    "fondo": "#08080F",
    "primario": "#00E5FF"
  },
  "kie_ai_key": null,
  "cta_formato": "Responde [PALABRA] y te mando [algo]"
}
```

Luego escanea las fotos:
```bash
python3 {{PROJ_DIR}}/scripts/scan_fotos.py --proj-dir {{PROJ_DIR}}
```

Muestra el resumen de cuántas fotos encontró y sus nombres.

Si no hay fotos aún, indica:
> "Perfecto, la configuración está lista. Cuando quieras generar tus primeras historias, pon tus fotos en `{{PROJ_DIR}}/fotos/` y corre `/historias-ig` de nuevo."

Si hay fotos, continúa directo al Paso 2 del flujo principal.

---

## COMANDOS DE UTILIDAD

**`/historias-ig reconfigurar`** → Borra `config.json` y corre el onboarding de nuevo.

**`/historias-ig fotos`** → Re-escanea la carpeta de fotos y actualiza `catalogo.json`.

**`/historias-ig ver`** → Abre la última carpeta de output generada.

---

## NOTAS TÉCNICAS

- **Fuentes**: Space Grotesk Variable (instalada por `setup.sh` en `{{PROJ_DIR}}/fonts/`)
- **Canvas**: 1080×1920 RGBA, guardado como PNG RGB optimizado
- **Kie AI**: modelo `nano_banana_2`, aspect ratio `9:16`, polling cada 3 seg
- **Fallback sin fotos**: fondo sólido con el color de marca + gradiente
- **Palabras clave**: se resaltan automáticamente en el color primario de la marca

---

## CONTEXTO PARA GENERAR BUENOS PLANES

Al crear el plan de slides, considera:

- El **hook** debe generar una respuesta emocional inmediata: curiosidad, identificación con un problema, o sorpresa. Evita abrir con "Hoy les cuento..." — mejor una pregunta directa o una afirmación que choca.
- El **problema** debe resonar con la audiencia específica del negocio. Usa el `descripcion_negocio` del config para contextualizarlo.
- La **revelación** debe sentirse como un alivio o un "wow, no lo había pensado así".
- Los **beneficios** son concretos y cuantificables cuando sea posible (tiempo, dinero, pasos).
- La **prueba** es más poderosa con números reales o capturas de pantalla.
- El **CTA** tiene una sola palabra clave, en mayúsculas, sin acentos, 3-8 letras.
