---
name: leer-paper
description: Ayuda a leer, entender y estudiar un paper científico separándolo en tópicos ordenados linealmente (cada uno depende sólo de los anteriores), escribe una guía de estudio en Markdown y luego actúa como tutor tópico a tópico. Úsala cuando el usuario diga "lee/estudia/explícame este paper", "ayúdame a entender este artículo", "help me read/study/understand this paper", comparta un PDF de un paper, o invoque `/leer-paper <ruta.pdf | slug> [siguiente | tópico N | quiz]`.
---

# Leer un paper por tópicos

Objetivo: que el usuario entienda el paper en profundidad, de forma lineal, sin saltos
conceptuales. Sirve para papers de cualquier disciplina. Escribir en el idioma del usuario
(por defecto español), conservando los términos técnicos que suelen usarse en inglés.

## Argumentos

- `/leer-paper <ruta.pdf>` → Fases 1–3 (crear la guía).
- `/leer-paper <slug> siguiente` → Fase 4 con el primer tópico sin marcar.
- `/leer-paper <slug> tópico N` → Fase 4 con el tópico N.
- `/leer-paper <slug> quiz` → repaso de tópicos ya marcados.

`<slug>`: nombre corto en minúsculas con guiones (p. ej. `cpd-pds70c-benisty2021`).
Para encontrar una guía existente: `find . -path "*notes/<slug>/00_mapa.md"`.

## Reglas generales

- **No inventar.** Todo lo que se atribuye al paper debe estar en el paper. Citar página
  (y sección/ecuación/figura) en cada afirmación: `(p. 4, §3.2, Ec. 5)`.
- **Separar voces.** Lo que añade Claude (intuición, derivaciones intermedias, contexto que
  el paper no da) va marcado con `> 💡 Nota de apoyo:`. Así el usuario sabe qué es del paper.
- Leer el PDF con la herramienta Read, primero sin `pages` (funciona para papers cortos). El
  parámetro `pages` (máx. 20 por llamada) requiere `poppler`; si falla, sugerir `brew install
  poppler`. Si el PDF tiene más de ~40 páginas o es un libro, preguntar qué capítulo/rango
  estudiar antes de seguir.
- Ecuaciones en LaTeX con `$…$` y `$$…$$`.

## Fase 1 — Lectura de reconocimiento (no escribir archivos)

Leer título, abstract, introducción (último párrafo), figuras y sus captions, conclusiones.
Determinar:
- Pregunta científica que responde el paper.
- Afirmación principal (la respuesta) y la evidencia central.
- Tipo: observacional / teórico-analítico / simulación / instrumental / revisión.
- Datos, métodos o códigos clave.

## Fase 2 — Mapa de tópicos (esperar OK del usuario)

Dividir el contenido en **4–8 tópicos** agrupados por concepto, no necesariamente por sección.
Orden: cada tópico depende sólo de los anteriores (el primero suele ser el contexto/motivación,
el último los resultados y su interpretación). Mostrar al usuario una tabla:

| # | Tópico | Objetivo (1 frase) | Cubre (págs/§/figs/ecs) | Prerrequisitos |

Luego **detenerse y esperar confirmación o ajustes** antes de escribir archivos.

## Fase 3 — Escribir la guía

Carpeta: `notes/<slug>/` en el mismo directorio del PDF (crearla si no existe).

### `00_mapa.md`
```markdown
# <Título del paper>
<Autores> (<año>), <revista>. DOI/arXiv: …  · PDF: <ruta relativa>

## En tres líneas
- **Pregunta:** …
- **Respuesta:** …
- **Evidencia clave:** …

## Prerrequisitos generales
- <concepto> — por qué hace falta; dónde repasarlo (libro/paper de la misma carpeta si existe)

## Glosario y notación
| Símbolo / término | Significado | Unidades | Dónde aparece |

## Ruta de estudio
- [ ] 01 — <tópico> → [01_<nombre>.md](01_<nombre>.md)
- [ ] 02 — …
- [ ] Síntesis → [99_sintesis.md](99_sintesis.md)
```

### `NN_<nombre>.md` (uno por tópico, misma plantilla)
```markdown
# NN — <Tópico>
Cubre: págs …, §…, Figs …, Ecs …

## 1. Qué vas a aprender y por qué importa
## 2. Antes de empezar (prerrequisitos puntuales)
## 3. La idea
Primero en lenguaje llano (2–4 frases), luego con rigor, citando página.
## 4. Ecuaciones clave paso a paso
Para cada ecuación: de dónde sale, derivación con los pasos intermedios, significado físico de
cada término, casos límite y un chequeo de orden de magnitud con valores del paper.
## 5. Cómo leer la figura
Ejes y unidades, qué representa cada curva/color, qué mirar primero, qué conclusión saca el paper.
## 6. Afirmación → evidencia
| Afirmación del paper | Evidencia (dato/fig/ec, pág.) | ¿Qué tan sólida? |
## 7. Autoevaluación
1. <pregunta conceptual>
   <details><summary>Respuesta</summary>…</details>
(3–5 preguntas: al menos una conceptual, una cuantitativa y una de "¿qué pasaría si…?")
```
Omitir las secciones 4 o 5 sólo si el tópico no tiene ecuaciones o figuras.

### `99_sintesis.md`
```markdown
# Síntesis y lectura crítica
## Supuestos y simplificaciones (y cuándo dejarían de valer)
## Puntos a verificar (cálculos del paper que no se reproducen al rehacerlos)
## Limitaciones que reconocen los autores / que no reconocen
## Qué quedaría por probar
## Conexión con el trabajo del usuario y otros papers de la carpeta
## Referencias del paper que vale la pena leer después (y por qué)
```
Para la conexión con el trabajo del usuario, mirar el proyecto actual (README, notas,
manuscrito) y los PDFs vecinos; si no hay contexto, preguntar en vez de suponer.

Al terminar, informar la ruta de la carpeta y sugerir `/leer-paper <slug> siguiente`.

## Fase 4 — Modo tutor

1. Leer `00_mapa.md` y el archivo del tópico (primer `[ ]` para `siguiente`, o el N pedido).
2. Explicarlo en conversación en bloques cortos, terminando cada bloque con una pregunta breve.
3. **Técnica Feynman:** pedir al usuario que explique la idea central con sus palabras;
   señalar con precisión lo que falta o está mal, sin dar la respuesta completa de inmediato.
4. Hacer las preguntas de autoevaluación del archivo una a una.
5. Si el usuario las responde bien, marcar `[x]` en `00_mapa.md`. Si no, repasar la parte
   débil y anotar la duda en el archivo del tópico bajo `## Dudas pendientes`.

`quiz`: elegir 3–5 preguntas mezcladas de tópicos ya marcados `[x]` (priorizando los más
antiguos y los que tienen dudas pendientes) y corregir.
