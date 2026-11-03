---
name: leer-paper
description: Ayuda a leer, entender y estudiar un paper científico separándolo en tópicos ordenados linealmente (cada uno depende sólo de los anteriores), escribe una guía de estudio en Markdown con verificación numérica y lectura crítica, actúa como tutor con repaso espaciado y compara varios papers entre sí. Úsala cuando el usuario diga "lee/estudia/explícame este paper", "ayúdame a entender este artículo", "compara estos papers", "help me read/study/understand this paper", comparta un PDF de un paper, o invoque `/leer-paper <ruta.pdf | slug> [siguiente | tópico N | quiz | anki]` o `/leer-paper comparar <slug> <slug>…`.
---

# Leer un paper por tópicos

Objetivo: que el usuario entienda el paper en profundidad, de forma lineal, sin saltos
conceptuales. Sirve para papers de cualquier disciplina. Escribir en el idioma del usuario
(por defecto español), conservando los términos técnicos que suelen usarse en inglés.

## Argumentos

- `/leer-paper <ruta.pdf>` → Fases 1–3 (crear la guía).
- `/leer-paper <slug> siguiente` → Fase 4 con el primer tópico sin marcar.
- `/leer-paper <slug> tópico N` → Fase 4 con el tópico N.
- `/leer-paper <slug> quiz` → repaso espaciado de las preguntas que tocan hoy.
- `/leer-paper <slug> anki` → exportar flashcards para Anki.
- `/leer-paper comparar <slug1> <slug2> […]` → comparar papers que ya tienen guía.

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
- Fecha de hoy (para el registro de repaso): `date +%F`.

## Fase 1 — Lectura de reconocimiento (no escribir archivos)

Leer título, abstract, introducción (último párrafo), figuras y sus captions, conclusiones.
Determinar:
- Pregunta científica que responde el paper.
- Afirmación principal (la respuesta) y la evidencia central.
- Tipo: observacional / experimental / simulación / teórico-analítico / computacional-ML /
  instrumental / revisión (puede ser más de uno). Define qué checklist se aplica en la síntesis.
- Datos, métodos o códigos clave.

## Fase 2 — Mapa de tópicos (esperar OK del usuario)

Dividir el contenido en **4–8 tópicos** agrupados por concepto, no necesariamente por sección.
Orden: cada tópico depende sólo de los anteriores (el primero suele ser el contexto/motivación,
el último los resultados y su interpretación). Mostrar al usuario una tabla:

| # | Tópico | Objetivo (1 frase) | Cubre (págs/§/figs/ecs) | Prerrequisitos |

Luego **detenerse y esperar confirmación o ajustes** antes de escribir archivos.

## Fase 3 — Escribir la guía

Carpeta: `notes/<slug>/` en el mismo directorio del PDF (crearla si no existe). Archivos, en
este orden: `00_mapa.md`, un `NN_<nombre>.md` por tópico, `verify.py`, `99_sintesis.md`, y
actualizar `notes/glosario.md`.

**Biblioteca compartida.** Antes de escribir, mirar si `notes/` ya tiene otras guías y un
`notes/glosario.md`. Si un prerrequisito ya está explicado en otra guía, enlazarlo
(`../<otro-slug>/03_<nombre>.md`) en vez de repetirlo entero.

### `00_mapa.md`
```markdown
# <Título del paper>
<Autores> (<año>), <revista>. DOI/arXiv: …  · PDF: <ruta relativa>

## En tres líneas
- **Pregunta:** …
- **Respuesta:** …
- **Evidencia clave:** …

## Prerrequisitos generales
- <concepto> — por qué hace falta; dónde repasarlo (libro, paper de la carpeta u otra guía)

## Glosario y notación
| Símbolo / término | Significado | Unidades | Dónde aparece |

## Ruta de estudio
- [ ] 01 — <tópico> → [01_<nombre>.md](01_<nombre>.md)
- [ ] 02 — …
- [ ] Síntesis → [99_sintesis.md](99_sintesis.md)

## Registro de repaso
| Pregunta | Último repaso | Resultado | Intervalo (días) | Próximo repaso |
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
cada término, casos límite y un chequeo de orden de magnitud con valores del paper (el mismo
cálculo va en `verify.py`).
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

### `verify.py` — verificación numérica reproducible
Rehace con código los cálculos clave del paper (los que sostienen la conclusión y los que
aparecen en los chequeos de orden de magnitud). Plantilla:

```python
"""Verificación numérica: <título corto> (<autores, año>).
Ejecutar: python3 verify.py"""
import math

# Constantes (cgs)
G, k_B, m_H = 6.674e-8, 1.381e-16, 1.673e-24
c, h = 2.998e10, 6.626e-27
au, pc = 1.496e13, 3.086e18
M_sun, M_jup, M_earth = 1.989e33, 1.898e30, 5.972e27

resultados = []

def check(nombre, calculado, paper, pagina, rtol=0.1, nota=""):
    """Compara con el valor del paper; rtol refleja el redondeo con que lo reporta."""
    ok = math.isclose(calculado, paper, rel_tol=rtol)
    resultados.append(ok)
    print(f"{'OK' if ok else 'NO'}  {nombre}: calculado {calculado:.3g}, paper {paper:.3g} ({pagina}) {nota}")

# --- Un bloque por cálculo: la ecuación y la página en un comentario, entradas del paper ---
# <Nombre> (p. N, Ec. M): <ecuación>

print(f"\n{sum(resultados)}/{len(resultados)} cálculos se reproducen")
```

Reglas:
- Entradas tal como las da el paper, con su página en un comentario. **Nunca ajustar una
  entrada para forzar un OK**: si no se reproduce, buscar la causa probable (otra constante,
  otro supuesto, un error de tipeo) y dejarla en `nota`.
- Biblioteca estándar; usar numpy/scipy sólo si hacen falta (integrales, ajustes) y están
  instaladas.
- Ejecutarlo con `python3 verify.py`. Cada `NO` pasa a "Puntos a verificar" de la síntesis.
- Omitirlo sólo si el paper no tiene cálculos reproducibles (p. ej. una revisión cualitativa).

### `99_sintesis.md`
```markdown
# Síntesis y lectura crítica
## Supuestos y simplificaciones (y cuándo dejarían de valer)
## Revisión según el tipo de paper
| Punto | Qué hace el paper (pág.) | Evaluación |
## Puntos a verificar (resultado de `verify.py`: lo que no se reproduce y por qué)
## Limitaciones que reconocen los autores / que no reconocen
## Qué quedaría por probar
## Conexión con el trabajo del usuario y otros papers de la carpeta
## Referencias del paper que vale la pena leer después (y por qué)
```
Para "Revisión según el tipo de paper", leer `checklists.md` (en el directorio de esta
skill) y aplicar la sección **Común** más la del tipo detectado en la Fase 1.

Para la conexión con el trabajo del usuario, mirar el proyecto actual (README, notas,
manuscrito) y los PDFs vecinos; si no hay contexto, preguntar en vez de suponer.

### `notes/glosario.md` — glosario compartido entre papers
```markdown
# Glosario compartido
| Término / símbolo | Significado | Unidades | Guías (slug, pág.) |

## Conflictos de notación
| Símbolo | Significado en cada guía |
```
Agregar los términos nuevos del paper y añadir el slug a los que ya existen. Si un símbolo
significa otra cosa que en otra guía (p. ej. `κ` por gramo de gas frente a por gramo de
polvo), registrarlo en "Conflictos de notación" y advertirlo en el glosario de `00_mapa.md`.

Al terminar, informar la ruta de la carpeta, el resumen de `verify.py` y sugerir
`/leer-paper <slug> siguiente`.

## Fase 4 — Modo tutor

1. Leer `00_mapa.md` y el archivo del tópico (primer `[ ]` para `siguiente`, o el N pedido).
2. Explicarlo en conversación en bloques cortos, terminando cada bloque con una pregunta breve.
3. **Técnica Feynman:** pedir al usuario que explique la idea central con sus palabras;
   señalar con precisión lo que falta o está mal, sin dar la respuesta completa de inmediato.
4. Hacer las preguntas de autoevaluación del archivo una a una y registrar cada una en
   "Registro de repaso" (ver abajo).
5. Si el usuario las responde bien, marcar `[x]` en `00_mapa.md` con la fecha
   (`- [x] 01 — … (aprobado 2026-11-03)`). Si no, repasar la parte débil y anotar la duda
   en el archivo del tópico bajo `## Dudas pendientes`.

### Repaso espaciado
Cada pregunta se identifica como `<tópico>.<n>` (p. ej. `03.2`) y tiene una fila en
"Registro de repaso". Intervalos: 1 → 3 → 7 → 14 → 30 → 60 días.
- Respuesta correcta: pasar al siguiente intervalo. Incorrecta o incompleta: volver a 1.
- Próximo repaso = último repaso + intervalo.

`quiz`: elegir 3–5 preguntas cuyo próximo repaso sea hoy o antes (las más atrasadas primero);
si faltan, completar con preguntas de tópicos `[x]` que aún no estén en el registro o que
tengan dudas pendientes. Corregir y actualizar el registro. Si no toca nada hoy, decirlo y
ofrecer un repaso igual o la fecha del próximo.

### `anki` — exportar flashcards
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

## Comparar papers — `/leer-paper comparar <slug1> <slug2> […]`

Requiere que cada slug tenga guía; si falta alguna, ofrecer crearla antes. Leer `00_mapa.md`,
`99_sintesis.md` y `verify.py` de cada guía, y el PDF sólo cuando falte un valor. Escribir
`notes/comparaciones/<tema>.md` (tema corto en minúsculas con guiones, acordado con el usuario):

```markdown
# Comparación: <tema>
Guías: [<slug1>](../<slug1>/00_mapa.md) — <autores, año> · [<slug2>](…) — …

## Pregunta y enfoque
| | <slug1> | <slug2> |
| Pregunta | | |
| Tipo, datos y método | | |
| Supuestos clave | | |
| Resultado principal (± incertidumbre) | | |

## Parámetros en común
| Parámetro (unidades) | <slug1> (pág.) | <slug2> (pág.) | ¿Compatibles? |

## Dónde coinciden
## Dónde discrepan y por qué
Para cada discrepancia: causa probable (supuesto, dato, método, época, constante) y qué
observación o cálculo la resolvería.
## Qué paper usar para qué
```
Reglas: comparar en las mismas unidades; "compatibles" significa dentro de las incertidumbres
reportadas (decir cuáles); citar como `(<slug>, p. N)`; si la comparación revela un cálculo a
rehacer, añadirlo al `verify.py` correspondiente.
