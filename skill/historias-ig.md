# /historias-ig — Generador de Historias de Instagram

Genera una secuencia de historias de Instagram eligiendo la estructura narrativa viral más adecuada al tema y objetivo del día.

**Directorio del proyecto:** `{{PROJ_DIR}}`

---

## FLUJO PRINCIPAL

### Al invocar `/historias-ig`

**Paso 1 — Verificar configuración**

Lee `{{PROJ_DIR}}/config.json`. Si no existe, ejecuta el **ONBOARDING** (ver sección abajo).

**Paso 2 — Pedir tema y objetivo**

Pregunta al usuario (juntas, en un solo mensaje):
> "¿Cuál es el tema de hoy? ¿Y qué objetivo buscas con estas historias?"
>
> Objetivo — elige uno:
> - **Lead magnet** — entregas valor gratuito y capturas leads
> - **Urgencia** — empujas a comprar/inscribirse ahora
> - **Humanización** — conexión emocional, sin venta directa
> - **Educativa** — posicionarte como experto
> - **Prueba social** — mostrar transformación de cliente o resultado propio
> - **Libre** — tú decides / Claude elige

Si el usuario no especifica objetivo, Claude lo infiere del tema.

**Paso 3 — Seleccionar estructura narrativa**

Con el tema + objetivo, Claude **elige la estructura más adecuada** de las 35 disponibles (ver sección ESTRUCTURAS abajo). Presenta al usuario:

> "Voy a usar la estructura **[NOMBRE]**: [flujo en una línea]. ¿Continuamos?"

Si el usuario quiere otra, muestra las 3 mejores alternativas y deja elegir.

**Paso 4 — Escanear fotos disponibles**

```bash
python3 {{PROJ_DIR}}/scripts/scan_fotos.py --proj-dir {{PROJ_DIR}}
```

**Paso 5 — Crear el plan de slides**

Genera el plan siguiendo el flujo de la estructura elegida. El número de slides varía según la estructura (5-7 típicamente).

**Reglas para cada slide:**
- `tipo`: usa `hook` para el primer slide, `cta` para el último, y el nombre descriptivo del paso intermedio para los demás (ej: `problema`, `revelacion`, `error`, `aprendizaje`, etc.)
- `titulo`: texto de impacto, máx 8 palabras
- `subtitulo`: elaboración o dato secundario
- `palabras_clave`: 1-3 palabras del título que se resaltan en el color primario
- `foto`: nombre de archivo de `catalogo.json` que encaje con el slide (o `null`)
- `fondo_ia`: `{"prompt": "..."}` si hay Kie AI y no hay foto. Prompt en inglés, estilo visual coherente con la marca
- `cta_palabra`: solo en el último slide — una palabra en MAYÚSCULAS, 3-8 letras, sin acentos, relacionada al tema

**Formato del plan JSON:**
```json
{
  "estructura": "NOMBRE DE LA ESTRUCTURA",
  "objetivo": "lead_magnet | urgencia | humanizacion | educativa | prueba_social | libre",
  "slides": [
    {
      "numero": 1,
      "tipo": "hook",
      "titulo": "Texto grande de impacto",
      "subtitulo": null,
      "texto_extra": null,
      "foto": "foto.jpg",
      "fondo_ia": null,
      "palabras_clave": ["palabra1"],
      "cta_palabra": null
    },
    {
      "numero": 5,
      "tipo": "cta",
      "titulo": "¿Quieres el recurso completo?",
      "subtitulo": "y te lo mando ahora.",
      "texto_extra": null,
      "foto": null,
      "fondo_ia": {"prompt": "..."},
      "palabras_clave": [],
      "cta_palabra": "RECURSO"
    }
  ]
}
```

Muestra el plan al usuario en formato legible (no JSON crudo) y pide confirmación.

**Paso 6 — Guardar el plan y generar**

```bash
python3 {{PROJ_DIR}}/scripts/generate.py \
  --plan {{PROJ_DIR}}/plan.json \
  --proj-dir {{PROJ_DIR}}
```

**Paso 7 — Mostrar resultados**

Muestra el slide 1 (hook) y el último (CTA). Luego:
```bash
open {{PROJ_DIR}}/output/
```

---

## 35 ESTRUCTURAS NARRATIVAS

### TIER 1 — Las más poderosas (prioridad)

#### #1 STORYTELLING CHISME ⭐
**Cuándo**: Máximo engagement, reactivar cuenta
**Flujo**: Chisme → Participación → Revelación → Valor → CTA
**Slides**: 5
**Hook tipo**: "No saben lo que me pasó ayer…" / "No van a creer esto"
**Ideal para**: Objetivo libre, humanización

#### #10 SOLTAMOS LA BOMBA ⭐
**Cuándo**: Lanzamientos, anuncios grandes, cambios drásticos
**Flujo**: Tensión → Problema del avatar → Revelación → Beneficio → CTA
**Slides**: 5
**Hook tipo**: "Hoy soltamos la bomba 💣" / "Esto cambia todo"
**Ideal para**: Urgencia, lead magnet

#### #21 STORYTELLING DE ERROR PROPIO ⭐
**Cuándo**: Humanización fuerte, generar empatía
**Flujo**: Confesión → Contexto → Error → Aprendizaje → Aplicación → CTA
**Slides**: 6
**Hook tipo**: "Hoy cometí un error [adjetivo]…" / "Fallé en esto y aprendí algo clave"
**Ideal para**: Humanización, educativa

#### #9 ALGO ME HA SORPRENDIDO ⭐
**Cuándo**: Datos contraintuitivos, insights inesperados
**Flujo**: Impacto → Datos → Explicación → Conclusión → CTA
**Slides**: 5
**Hook tipo**: "Algo me sorprendió analizando [tema] hoy…"
**Ideal para**: Educativa, prueba social

### TIER 2 — Cambio y transformación

#### #5 CÓMO PASAR DE X A Y
**Flujo**: Estado inicial → Estado final → Proceso → Cambio clave → CTA
**Slides**: 5-6
**Ideal para**: Prueba social, lead magnet

#### #17 EVOLUCIÓN VISIBLE
**Flujo**: Antes → Durante → Después → Insight → CTA
**Slides**: 5
**Ideal para**: Prueba social, humanización

#### #4 SOLO TUVE QUE HACER UN CAMBIO
**Flujo**: Problema → Error → Cambio único → Resultado → CTA
**Slides**: 5
**Ideal para**: Educativa, lead magnet

#### #32 EL CAMBIO DE PERSONAJE
**Flujo**: Antes emocional → Punto de quiebre → Nueva versión → Prueba → CTA
**Slides**: 5
**Ideal para**: Humanización, prueba social

#### #33 TRANSFORMACIÓN DEL CLIENTE
**Flujo**: Antes → Duda → Punto clave → Después → Invitación
**Slides**: 5
**Ideal para**: Prueba social, urgencia

### TIER 3 — Educativas

#### #22 MICROENTRENAMIENTO
**Flujo**: Tema → Paso 1 → Paso 2 → Paso 3 → CTA
**Slides**: 5
**Hook tipo**: "Mini entrenamiento: [tema] en 3 pasos"
**Ideal para**: Lead magnet, educativa

#### #8 EXPLICACIÓN DE CONCEPTO
**Flujo**: ¿Qué es? → ¿Por qué importa? → Micro-explicación → Ejemplo → CTA
**Slides**: 5
**Ideal para**: Educativa, lead magnet

#### #19 LO QUE NADIE TE CUENTA
**Flujo**: Verdad oculta → Por qué pasa → Consecuencia → Qué hacer → CTA
**Slides**: 5
**Hook tipo**: "Lo que NADIE te cuenta sobre [tema]…"
**Ideal para**: Educativa, lead magnet

#### #6 ESTO ES LO QUE SUCEDE CUANDO
**Flujo**: Resultado llamativo → Explicación → Proceso → Demostración → CTA
**Slides**: 5
**Ideal para**: Prueba social, educativa

#### #34 DESMENTIDA ESTRATÉGICA
**Flujo**: Mito → Por qué es falso → Prueba → Qué sí funciona → CTA
**Slides**: 5
**Ideal para**: Educativa, lead magnet

### TIER 4 — Errores y creencias

#### #7 EL ERROR FATAL
**Flujo**: Error → Consecuencia → Corrección → Beneficio → CTA
**Slides**: 5
**Ideal para**: Educativa, humanización

#### #20 DETECCIÓN DE CREENCIA
**Flujo**: Creencia → Por qué es falsa → Evidencia → Nueva creencia → CTA
**Slides**: 5
**Ideal para**: Educativa, lead magnet

#### #27 DESMONTANDO UNA OBJECIÓN
**Flujo**: Objeción → Por qué aparece → Contraprueba → Reemplazo → CTA
**Slides**: 5
**Ideal para**: Urgencia, lead magnet

#### #12 ESTO TE PUEDE ESTAR FRENANDO
**Flujo**: Detección → Ejemplo → Efecto → Corrección → CTA
**Slides**: 5
**Ideal para**: Educativa, humanización

#### #31 ROMPIENDO EL CICLO
**Flujo**: Ciclo negativo → Identificación → Ruptura → Nuevo camino → CTA
**Slides**: 5
**Ideal para**: Humanización, lead magnet

### TIER 5 — Narrativas personales

#### #18 DIARIO PERSONAL
**Flujo**: Momento → Emoción → Reflexión → Aprendizaje → CTA
**Slides**: 5
**Hook tipo**: "Hoy [haciendo algo cotidiano] pensaba en algo…"
**Ideal para**: Humanización, libre

#### #15 LECCIÓN INESPERADA
**Flujo**: Escena → Detalle → Insight → Aplicación → CTA
**Slides**: 5
**Hook tipo**: "Hoy en [lugar] pasó algo que no esperaba…"
**Ideal para**: Humanización, libre

#### #28 NARRATIVA DE RUTINA
**Flujo**: Momento cotidiano → Acción → Micro-explicación → Enseñanza → CTA
**Slides**: 5
**Ideal para**: Humanización, libre

#### #25 STORYTELLING DE MOMENTO INCÓMODO
**Flujo**: Escena incómoda → Emoción → Revelación → Enseñanza → CTA
**Slides**: 5
**Ideal para**: Humanización

#### #29 INICIO → CAOS → ORDEN
**Flujo**: Inicio tranquilo → Aparición del caos → Explicación → Orden → CTA
**Slides**: 5
**Ideal para**: Humanización, educativa

### TIER 6 — Visuales e impacto

#### #16 APERTURA CINEMATOGRÁFICA
**Flujo**: Escena visual impactante → Corte → Explicación → Lección → CTA
**Slides**: 5
**Hook tipo**: Imagen inesperada + frase de 3 palabras
**Ideal para**: Libre, humanización

#### #13 DEMOSTRACIÓN → CTA DIRECTA
**Flujo**: Prueba funcionando → Explicación → Beneficio → CTA
**Slides**: 4-5
**Ideal para**: Prueba social, urgencia

#### #23 PREDICCIÓN / ALERTA
**Flujo**: Advertencia → Prueba → Explicación → Acción → CTA
**Slides**: 5
**Hook tipo**: "ALERTA: si sigues haciendo X, va a pasar Y"
**Ideal para**: Urgencia, educativa

#### #24 ROMPE PATRÓN VISUAL
**Flujo**: Impacto visual → Pregunta → Explicación → Reposicionamiento → CTA
**Slides**: 5
**Ideal para**: Libre, reactivar cuenta

### TIER 7 — Otros

#### #3 HICE ESTA COSA NUEVA
**Flujo**: Innovación → Confesión → Validación → Demo → Acceso → CTA
**Slides**: 6
**Ideal para**: Lead magnet, urgencia (lanzamientos)

#### #11 SI HACES X, MIRA ESTA HISTORIA
**Flujo**: Segmentación → Problema → Mini enseñanza → Aplicación → CTA
**Slides**: 5
**Hook tipo**: "Si haces [actividad], para y lee esto"
**Ideal para**: Lead magnet, educativa

#### #14 MINI DOCUMENTAL DE CASO
**Flujo**: Personaje → Problema → Proceso → Resultado → CTA
**Slides**: 5
**Ideal para**: Prueba social, urgencia

#### #26 PREGUNTA RETÓRICA
**Flujo**: Pregunta → Micro reflexión → Explicación → Enseñanza → CTA
**Slides**: 5
**Hook tipo**: "¿Y si el problema no es X sino Y?"
**Ideal para**: Educativa, libre

#### #2 ACTUALIZACIÓN SOBRE PROBLEMA
**Flujo**: Estado → Problema → Hallazgo → Demostración → CTA
**Slides**: 5
**Ideal para**: Lead magnet, prueba social

#### #35 ATMÓSFERA / ESCENA SENSITIVA
**Flujo**: Escena sensorial → Emoción → Reflexión → Conexión → CTA
**Slides**: 5
**Ideal para**: Humanización, libre

---

## TABLA DE SELECCIÓN RÁPIDA

| Objetivo | Estructuras recomendadas (en orden) |
|----------|-------------------------------------|
| Lead magnet | #22 Microentrenamiento, #19 Nadie te cuenta, #11 Si haces X |
| Urgencia | #10 Bomba, #23 Alerta, #13 Demo directa |
| Humanización | #21 Error propio, #18 Diario, #15 Lección inesperada |
| Educativa | #8 Concepto, #22 Microentrenamiento, #34 Desmentida |
| Prueba social | #33 Cliente, #17 Evolución, #14 Mini documental |
| Libre / máximo engagement | #1 Chisme, #9 Sorpresa, #21 Error propio |
| Reactivar cuenta dormida | #1 Chisme, #21 Error, #15 Lección inesperada |

---

## REGLAS DE CTA

**Formato obligatorio del último slide:**
```
Responde [PALABRA] y te [mando/paso/envío] [algo concreto]
```

**Reglas de la palabra clave:**
- Una sola palabra, MAYÚSCULAS, 3-8 caracteres, sin acentos ni símbolos
- Temáticamente relacionada al contenido (no genérica como "INFO" o "HOLA")
- Ejemplos: AGENTE, STACK, SKILL, GUIA, CASO, ERROR, RUTA, AUTO, VENTAS

**Nunca escribir:** "link en bio", "mándame DM", "Call to Action"

---

## REGLAS DE FONDOS

Para cada slide, en orden de prioridad:
1. **Foto real** del catálogo si encaja con el tema/emoción del slide
2. **Fondo IA** (Kie AI) con prompt descriptivo en inglés — estilo visual coherente con la marca
3. **Fondo sólido** — solo como último recurso, máx 1 slide por secuencia

El **hook** siempre debe tener el fondo más impactante de la secuencia.
El **CTA** puede tener fondo sólido si el texto debe dominar sin distracciones.

---

## ONBOARDING (primer uso)

Si no existe `config.json`, haz estas preguntas **una por una**:

1. **¿Cómo se llama tu marca o negocio?** → `nombre_marca`

2. **¿A qué se dedica tu negocio? (1-2 oraciones)** → `descripcion_negocio`

3. **¿Cuál es tu nombre?** → `nombre_usuario`

4. **¿Cuál es tu usuario de Instagram?** → `instagram_user` (agregar @ si no lo pone)

5. **¿Cuáles son tus colores de marca?**
   - a) Tengo los códigos hex → pedir fondo y primario/acento
   - b) Paleta por defecto (oscuro con cyan)
   - c) Elegir paleta: `oscuro-cyan` (#08080F / #00E5FF) | `oscuro-naranja` (#0D0A08 / #FF6B35) | `oscuro-verde` (#080F09 / #00E676) | `claro-profesional` (#F8F9FA / #1A1A2E)
   → `colores: { fondo, primario }`

6. **¿Tienes cuenta en Kie AI?** (kie.ai)
   Si sí: pedir que abra `{{PROJ_DIR}}/.env` y agregue `KIE_AI_API_KEY`
   Si no: el skill funciona con fotos propias

7. **¿Cuál es tu CTA habitual?**
   - a) Responde [PALABRA] y te mando [algo]
   - b) Comenta [PALABRA] y te llega [algo]
   → `cta_formato`

8. **¿Qué etiqueta quieres en el primer slide?** (ej: "NUEVA HISTORIA", "HOY COMPARTO", "ESTO ME PASÓ")
   → `etiqueta_hook`

Crear `{{PROJ_DIR}}/config.json`:
```json
{
  "nombre_marca": "...",
  "descripcion_negocio": "...",
  "nombre_usuario": "...",
  "instagram_user": "@...",
  "etiqueta_hook": "...",
  "colores": { "fondo": "#08080F", "primario": "#00E5FF" },
  "kie_ai_key": null,
  "cta_formato": "Responde [PALABRA] y te mando [algo]"
}
```

Escanear fotos:
```bash
python3 {{PROJ_DIR}}/scripts/scan_fotos.py --proj-dir {{PROJ_DIR}}
```

Si no hay fotos: indicar que las agreguen en `{{PROJ_DIR}}/fotos/` antes de generar.
Si hay fotos: continuar al Paso 2 del flujo principal.

---

## COMANDOS DE UTILIDAD

**`/historias-ig reconfigurar`** → Borra `config.json` y corre el onboarding de nuevo.

**`/historias-ig fotos`** → Re-escanea la carpeta de fotos.

**`/historias-ig ver`** → Abre la última carpeta de output.

---

## NOTAS TÉCNICAS

- **Fuentes**: Space Grotesk (instalada por `setup.sh` en `{{PROJ_DIR}}/fonts/`)
- **Canvas**: 1080×1920 RGBA, guardado como PNG RGB optimizado
- **Kie AI**: modelo `nano-banana-2`, aspect ratio `9:16`, URLs en `resultJson`
- **Fallback sin fotos**: fondo sólido con el color de marca
- **Palabras clave**: resaltadas en el color primario de la marca
