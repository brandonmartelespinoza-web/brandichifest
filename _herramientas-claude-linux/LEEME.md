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
