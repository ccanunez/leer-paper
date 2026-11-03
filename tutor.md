# Modo tutor

Principio: **primero enseñar a fondo, después evaluar**. Una sesión de estudio
(`siguiente` / `tópico N`) recorre el tópico completo con explicaciones, ejemplos y
preguntas de práctica sin nota. La evaluación llega al final y sólo si el usuario dice que
está listo; si no, se pospone (`evaluar N`).

Antes de empezar, leer `00_mapa.md` (nivel, objetivo, ruta, registro), el archivo del tópico,
`params.toml` y la salida de `python3 verify.py`. Si el tópico tiene `## Dudas pendientes`,
empezar por ellas.

## Cómo enseñar
- **Un bloque por mensaje**, corto (≤ ~15 líneas), y **esperar la respuesta** del usuario
  antes de seguir. Nunca volcar el tópico entero.
- Cada bloque termina con **una** pregunta de práctica (sin nota) que obligue a usar lo recién
  explicado: predecir, calcular, completar un paso, interpretar.
- **Pistas graduadas** cuando el usuario se equivoca o se traba: pista 1 (hacia dónde mirar) →
  pista 2 (el paso clave) → solución explicada. Ante un error, nombrar el malentendido
  concreto ("estás sumando flujos en Jy y Jy/beam"), no sólo dar la respuesta correcta.
- **Predecir y luego comprobar:** antes de mostrar un número de `verify.py` o una
  sensibilidad, pedir al usuario que prediga (orden de magnitud, sentido del cambio).
- Ajustar al **nivel** de `00_mapa.md` y a lo que el usuario pida en el momento
  ("más despacio", "más profundo", "sáltate esto", "dame un ejemplo").
- Citar página en todo lo que es del paper y marcar con 💡 lo que no.

## Sesión de estudio
1. **Orientación.** Mostrar el mapa conceptual (Mermaid de `00_mapa.md`) señalando dónde
   estamos y qué tópicos previos se usan. Objetivo del tópico en una frase.
2. **Activar prerrequisitos.** 1–2 preguntas rápidas. Si hay un hueco: mini-explicación, o
   enlace a otra guía o a `notes/glosario.md` si el concepto ya está explicado allí.
3. **Enseñar en bloques**, en este orden (saltar los que el tópico no tenga):
   1. *Intuición* — la idea en lenguaje llano, con una analogía si ayuda.
   2. *Lo que dice el paper* — con rigor y páginas.
   3. *Ecuación paso a paso* — derivar con el usuario: pedirle que complete un paso o
      identifique un término. Casos límite.
   4. *Ejemplo trabajado* — evaluar la ecuación con `params.toml`; el usuario predice,
      luego se muestra el bloque de `verify.py`. Si no se reproduce, discutir por qué.
   5. *¿Qué pasaría si…?* — usar la salida de `incertidumbre()`: qué entrada domina y
      cuánto. Si el usuario propone otro valor, calcularlo (editar una copia de los valores
      en un `python3 -c`, sin tocar `params.toml`).
   6. *La figura* — lectura guiada: ejes, qué mirar primero, una pregunta sobre lo que se
      ve. Ofrecer `figura N` si reproducirla ayuda (ver `verificacion.md`).
   7. *Evidencia y crítica* — tabla afirmación → evidencia; el punto del checklist que
      toca este tópico; qué dice el estado actual (¿se confirmó?) y, si se revisó, cómo
      lo implementa el código.
   8. *Conexión* — con el trabajo del usuario, con otras guías, con el glosario compartido.
4. **Técnica Feynman.** Pedir al usuario que explique el tópico completo con sus palabras,
   como a un compañero. Señalar con precisión lo que falta o está mal, sin dar la respuesta
   completa de inmediato; repetir hasta que la explicación cubra lo esencial.
5. **Resumen del usuario.** Pedirle 3–5 líneas con lo que se lleva. Corregir lo que esté mal
   y guardarlo en el archivo del tópico bajo `## Mi resumen (<fecha>)`.
6. **Puerta de evaluación.** Preguntar: "¿Quieres evaluarte ahora o prefieres repasar algo
   antes?". Si repasa, volver al bloque que pida. Si pospone, anotar en el tópico
   `## Estado: estudiado <fecha>, evaluación pendiente` y sugerir `evaluar N` para otro día
   (evaluarse al día siguiente mide mejor la retención).

## Evaluación (`evaluar N`, o al final de la sesión de estudio)
- Las preguntas de autoevaluación del tópico, una a una, **sin pistas en el primer intento**.
  Si falla, una pista y un segundo intento (cuenta como incorrecta en el registro).
- Al menos una pregunta cuantitativa se resuelve con números, no sólo con el método.
- Registrar cada pregunta en "Registro de repaso" (ver abajo).
- **Aprobado** si responde bien todas o todas menos una: marcar `[x]` con fecha en la ruta
  (`- [x] 01 — … (aprobado 2026-11-03)`) y añadir `class TN hecho` al Mermaid.
- Si no: repasar la parte débil en el momento, anotar la duda en `## Dudas pendientes` y
  dejar el tópico sin marcar.
- Regenerar `notes/README.md`.

## Al terminar todos los tópicos
Sesión de síntesis con `99_sintesis.md`: recorrer el diagrama del argumento pidiendo al
usuario que conecte cada evidencia con su afirmación; discutir los puntos a verificar y el
estado actual; elegir con el usuario una de las preguntas abiertas. Ofrecer
`journal-club`, `referee` o `anki`.

## Repaso espaciado
Cada pregunta se identifica como `<tópico>.<n>` (p. ej. `03.2`) y tiene una fila en
"Registro de repaso" de `00_mapa.md`. Intervalos: 1 → 3 → 7 → 14 → 30 → 60 días.
- Correcta: pasar al siguiente intervalo. Incorrecta o incompleta: volver a 1.
- Próximo repaso = último repaso + intervalo.

`quiz` (una guía): 3–5 preguntas cuyo próximo repaso sea hoy o antes (las más atrasadas
primero); si faltan, completar con preguntas de tópicos `[x]` que no estén en el registro o
que tengan dudas pendientes. Formular la pregunta con otras palabras o valores que en el
archivo cuando sea posible, para que no se responda de memoria. Corregir, explicar y
actualizar el registro. Si no toca nada, decirlo y dar la fecha del próximo repaso.

`hoy` (toda la biblioteca): buscar todas las guías (`find . -path "*notes/*/00_mapa.md"`),
reunir las preguntas que tocan hoy o antes y hacer 5–10 **intercalando papers** (mezclar
temas mejora la retención). Actualizar cada registro y regenerar `notes/README.md`.

## `anki` — exportar flashcards
Escribir `notes/<slug>/anki.txt` (importar en Anki con Archivo → Importar):
```
#separator:tab
#html:true
#tags column:3
<pregunta>	<respuesta (p. N)>	<slug> <slug>::NN
```
- Una tarjeta por pregunta de autoevaluación y una por término del glosario
  (anverso: término; reverso: significado y unidades), con la etiqueta `<slug>::glosario`.
- Convertir `$…$` en `\(…\)` y `$$…$$` en `\[…\]` (MathJax de Anki); quitar `<details>`;
  reemplazar saltos de línea y tabuladores dentro de un campo por `<br>`.
- Si el archivo ya existe, sobrescribirlo (Anki actualiza las tarjetas con el mismo anverso).
