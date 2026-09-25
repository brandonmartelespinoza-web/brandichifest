# Guías de Morfofisiología (UNT) — reglas permanentes

Este repo guarda las guías de estudio semanales (`SEM NN/GUIA-SEMNN.html`) que se arman con el
**PROMPT-MAESTRO v2** (Drive: `SEMANAS DE MORFOFISIOLOGÍA/_herramientas-claude/PROMPT-MAESTRO.md`).
El prompt manda en todo lo demás; estas reglas se suman y **no se negocian**.

## 🖼️ Regla de imágenes (pedido explícito del usuario, 25/09/2026)

> *"te pediré que siempre revises que todo se vea bien, en especial con las imagenes, que tengan buena
> resolucion (si se puede), que esten bien encuadrados y que se logre ver todo el contenido q es necesario"*
> — y después: *"esto que quede como regla y sigue haciendolo con las semanas que vienen"*.

1. **La guía se entrega como UN SOLO archivo HTML con las imágenes incrustadas** (base64:
   `armarNN.py --embed`). La carpeta `img/` queda en el repo para reusar, pero el HTML no depende de ella.
   Motivo: el usuario abrió el HTML sin `img/` al lado y todas las figuras aparecieron rotas.
   Prueba obligatoria: copiar el HTML **solo** a otra carpeta, abrirlo por `file://` y confirmar 0 imágenes rotas.
2. **Resolución:** extraer cada imagen en su **resolución nativa** del PDF (xref) o renderizar la región a la
   escala que la iguala; nunca recortar sobre un JPEG ya comprimido si se puede volver al PDF.
   Ninguna imagen se muestra más de ~15 % por encima de su ancho natural (`style="max-width:Npx"`);
   si la fuente es chica o es captura de video, decirlo en el pie.
   Ojo: "ancho natural" = el de la foto **dentro del PDF** (xref), no el del recorte renderizado. Excepción
   aceptable: figuras con rótulos de texto vectorial nítido o micrografías con rótulos que hay que poder leer
   (se muestran un poco más grandes y el pie aclara que la foto original es chica).
3. **Encuadre y contenido completo:** nada de rótulos, ejes, epígrafes o recuadros cortados a medias; nada
   de basura ajena al contenido (barra "compartir pantalla" de Meet, bordes negros/grises de la diapositiva,
   las "pestañas" y líneas decorativas de la plantilla del teórico —`untab.py`—,
   marcas de agua, cursores, epígrafes del libro cortados). Si la barra de la videollamada tapa contenido,
   recortar por encima y **contar en el pie qué decía lo tapado**. Diapositivas anchas con mucho blanco:
   reacomodar las piezas (p. ej. en vertical) para que el texto se lea grande.
4. **Revisión visual real, figura por figura, antes de entregar:** capturar cada figura tal como se ve en la
   guía (`audit19.mjs`), armar hojas de contacto y **mirarlas**; para decidir un recorte, mirar la franja con
   reglas (`ruler.py`) en vez de estimar fracciones. Revisar también los SVG propios (rótulos que se pisan
   con líneas o contornos). Releer cada pie contra su imagen.
5. En el cierre de cada semana, informar qué figuras se corrigieron y cuáles quedan limitadas por la fuente.

## Herramientas (Linux, sesión en la nube)

SEM 20 en adelante: `_herramientas-claude-linux/sem20/` (ex20.py lee `spec1/2.txt`; untab.py; svgshot.mjs para
mirar cada SVG propio; cobertura20.py para el sílabo). Los recortes retocados a mano están anotados con `#` en los spec.


`_herramientas-claude-linux/` — ver `LEEME.md`. Flujo: `extract.py`/`fix19.py` (recortes desde el PDF) →
`sheet.py`/`ruler.py` (mirar) → fragmentos por pestaña → `chk19.py` → `armar19.py` (sin `--embed` para
controlar, con `--embed` para entregar) → `verify19.mjs` (clics reales) → `audit19.mjs` (capturas de
cada figura). Para una semana nueva, copiar los scripts como `*NN.*` y ajustar rutas/pestañas.

## Entrega

- Commit y push a la rama de trabajo; mandar el HTML al usuario con SendUserFile.
- El conector de Drive no sube archivos grandes: el usuario sube el HTML a su carpeta `SEM NN` de Drive.
