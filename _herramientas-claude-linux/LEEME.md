# Herramientas usadas para la guía de la Semana 19 (sesión en la nube, Linux)

Equivalentes en Python/Node de las herramientas de Windows (`pdf2png.mjs`, `crop.ps1`, `check.js`, etc.).
Las rutas internas apuntan a `/home/user/work/`; ajustalas si las reusás en otra máquina.

| Script | Qué hace |
|---|---|
| `dec.py` | Decodifica un archivo bajado de Drive (JSON base64) a disco |
| `render.py <pdf> <prefijo> <escala> [páginas]` | Páginas de PDF → PNG (PyMuPDF) |
| `sheet.py <salida> <cols> <ancho> img...` | Hoja de contacto con el nombre de cada imagen, para revisar recortes |
| `extract.py <spec>` | Extrae imágenes embebidas (por xref) o recorta regiones de página a alta escala |
| `armar19.py` | Ensambla la guía: chasis de SEM 17 + fragmentos de `frag-sem19/`, renumera figuras, reescribe `initDrag` |
| `chk19.py <html>` | Controles estáticos: etiquetas, `.lee`, imágenes faltantes/duplicadas/sin usar, alts, tablas, `data-correct` ↔ feedback, `data-pos` |
| `verify19.mjs` | Verificación en Chromium con clicks reales: pestañas, mini-tests, semáforos + reload, drag-drops, test 40/40, scroll a 1280 y 375 px, consola |

Requisitos: `pip install pymupdf pillow`; Playwright de Node.

## Revisión visual de imágenes (agregado)

- `python3 armar19.py --embed` → incrusta todas las imágenes dentro del HTML (base64). La guía queda en **un solo archivo** que se ve bien aunque se mueva o se suba a Drive sin la carpeta `img/`. Sin `--embed`, el HTML depende de `img/` al lado.
- `node audit19.mjs <carpeta>` → saca una captura de cada figura tal como se ve en la guía e indica si alguna se muestra ampliada por encima de su resolución original.
- `python3 fix19.py [nombres]` → rehace los recortes corregidos desde el PDF original (resolución nativa): saca barras de videollamada, bordes negros, epígrafes cortados.
- `python3 ruler.py salida.png 0.3 img...` → franja inferior de cada imagen con reglas cada 10 px, para decidir dónde recortar.

## Semana 20 (carpeta `sem20/`)

- `ex20.py spec.txt [nombres]` → extrae figuras (x = imagen nativa, c = render de región) a `raw/`; admite una 5.ª columna `w x0 y0 x1 y1` para tapar restos.
- `untab.py` → borra las pestañas marrones de la plantilla del teórico que quedan en los recortes.
- `svgshot.mjs frag.html prefijo` → captura cada esquema SVG propio para revisar que ningún rótulo se corte o se pise.
- `cobertura20.py` → busca cada ítem del sílabo en el texto de la guía (83/83).
- `overflow.mjs` → encuentra qué elemento genera scroll horizontal a 375 px.
- `rehacer_par20.py` → reemplaza en la guía ya ensamblada (con imágenes incrustadas) la pestaña Pared abdominal, el aviso y el test final por los fragmentos de `frag-sem20/`, y renumera figuras/initDrag. Sirve para rehacer una pestaña sin el chasis de SEM 17 que necesita `armar20.py`.
- El PDF del apunte *Pared abdominal* (10 MB) no baja por el conector de Drive (`download_file_content` corta la sesión); `read_file_content` sí da el texto. Las 6 láminas (`img/par-*.jpg`) las pasó el usuario como capturas ya recortadas; solo se les sacó el encabezado de la plantilla del atlas o la marca de agua de arriba, a su tamaño original. `rehacer_par20.py` también las incrusta en base64.
