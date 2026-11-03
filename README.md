# leer-paper

**Una skill para [Claude Code](https://claude.com/claude-code) que convierte un paper científico en una ruta de estudio lineal, por tópicos, y luego te acompaña como tutor.**

Leer un paper de principio a fin rara vez es la mejor forma de entenderlo. Las secciones no siguen el orden en que se construyen los conceptos, las ecuaciones aparecen sin derivación y las figuras —donde suele vivir el resultado— se leen a la pasada. `leer-paper` reorganiza el contenido en 4–8 tópicos donde cada uno depende solo de los anteriores, escribe una guía de estudio en Markdown y después te enseña tópico a tópico hasta que puedas explicarlo con tus palabras.

Funciona con papers de cualquier disciplina (física, biología, ciencias de la computación, economía…).

*English summary at the [end of this file](#english-summary).*

---

## Qué hace

| Fase | Qué ocurre | Escribe archivos |
|---|---|---|
| **1. Reconocimiento** | Lee abstract, introducción, figuras y conclusiones. Identifica la pregunta científica, la respuesta, la evidencia central y el tipo de paper. | No |
| **2. Mapa de tópicos** | Propone 4–8 tópicos ordenados por dependencia conceptual, con las páginas, figuras y ecuaciones que cubre cada uno. **Se detiene y espera tu visto bueno.** | No |
| **3. Guía de estudio** | Escribe la guía en `notes/<slug>/`, junto al PDF. | Sí |
| **4. Modo tutor** | Explica cada tópico en bloques cortos, te pide que lo expliques con tus palabras (técnica Feynman), te hace preguntas y marca tu progreso. | Sí (progreso) |

### Qué contiene cada tópico
Todos siguen la misma plantilla:

1. **Qué vas a aprender** y por qué importa dentro del paper.
2. **Prerrequisitos** puntuales.
3. **La idea**: primero en lenguaje llano, luego con rigor y con la página citada.
4. **Ecuaciones paso a paso**: de dónde salen, los pasos intermedios, el significado de cada término, los casos límite y un **chequeo de orden de magnitud** con los valores del propio paper.
5. **Cómo leer la figura**: ejes, qué mirar primero y qué conclusión saca el paper.
6. **Afirmación → evidencia**: qué dato o figura respalda cada afirmación y qué tan sólida es.
7. **Autoevaluación**: 3–5 preguntas (conceptual, cuantitativa y "¿qué pasaría si…?") con la respuesta oculta.

### Principios
- **No inventa.** Todo lo que atribuye al paper está en el paper, con la página citada: `(p. 4, §3.2, Ec. 5)`.
- **Separa voces.** Lo que agrega Claude (intuiciones, derivaciones intermedias, contexto externo) va marcado como `> 💡 Nota de apoyo:`, para que siempre sepas qué dice el paper y qué no.
- **Verifica.** Rehace los cálculos clave y lista en la síntesis los que no se reproducen.
- **Te pregunta antes de escribir.** Nada se escribe hasta que apruebes el mapa de tópicos.

---

## Instalación

Requiere [Claude Code](https://docs.claude.com/en/docs/claude-code) (CLI, app de escritorio o extensión de IDE).

**Para todos tus proyectos** (recomendado):

```bash
git clone https://github.com/ccanunez/leer-paper.git ~/.claude/skills/leer-paper
```

**Solo para un proyecto** (desde la raíz del proyecto):

```bash
git clone https://github.com/ccanunez/leer-paper.git .claude/skills/leer-paper
```

Si la skill no aparece, abre una sesión nueva de Claude Code para que se recargue la lista de skills.

**Para actualizarla:**

```bash
git -C ~/.claude/skills/leer-paper pull
```

### Opcional: PDFs largos
Claude Code lee papers cortos completos sin dependencias. Para leer por rangos de páginas (libros, tesis, papers de más de ~40 páginas) necesitas `poppler`:

```bash
brew install poppler
```

En Debian/Ubuntu se instala con `sudo apt-get install poppler-utils`.

---

## Uso

### 1. Crear la guía
```
/leer-paper papers/mi-paper.pdf
```
También se activa con lenguaje natural: *"ayúdame a entender este paper: papers/mi-paper.pdf"*.

Claude te mostrará algo como esto y esperará tu respuesta:

| # | Tópico | Objetivo | Cubre | Prerrequisitos |
|---|---|---|---|---|
| 1 | Contexto y motivación | … | p. 1–2, §1 | … |
| 2 | Método | … | p. 2–3, §2, Fig. 1 | 1 |
| … | … | … | … | … |

Puedes pedir ajustes ("une el 2 y el 3", "sáltate la parte instrumental") antes de aprobar.

### 2. Estudiar con el tutor
```
/leer-paper <slug> siguiente
```
Toma el primer tópico sin marcar, te lo explica, te pide que lo expliques de vuelta y te hace las preguntas. Si las respondes bien, lo marca `[x]` en el mapa; si no, repasa la parte débil y anota la duda en el archivo del tópico.

### 3. Otros comandos
| Comando | Qué hace |
|---|---|
| `/leer-paper <slug> tópico 3` | Estudia un tópico concreto |
| `/leer-paper <slug> quiz` | Repaso mezclado de los tópicos ya completados, priorizando los más antiguos y los que tienen dudas |

El `<slug>` es un nombre corto que la skill elige al crear la guía (p. ej. `cpd-pds70c-benisty2021`).

---

## Qué genera

```
papers/
├── mi-paper.pdf
└── notes/
    └── <slug>/
        ├── 00_mapa.md           # resumen en 3 líneas, prerrequisitos, glosario, ruta con casillas
        ├── 01_<tópico>.md
        ├── 02_<tópico>.md
        ├── …
        └── 99_sintesis.md       # supuestos, puntos a verificar, limitaciones, conexiones, lecturas
```

- **`00_mapa.md`** incluye una tabla de notación (símbolo, significado, unidades, dónde aparece) y la ruta de estudio con casillas `[ ]` que sirven de registro de progreso.
- **`99_sintesis.md`** es la lectura crítica: qué supuestos hace el paper y cuándo dejarían de valer, qué cálculos no se reproducen, qué limitaciones reconocen (y cuáles no) los autores, qué falta probar, cómo se conecta con tu trabajo y con otros PDFs de la misma carpeta, y qué referencias leer después.

Las ecuaciones se escriben en LaTeX (`$…$`, `$$…$$`) y las respuestas de autoevaluación en bloques `<details>`. Se ven bien en VS Code, Obsidian, GitHub y la mayoría de los visores de Markdown.

---

## Consejos
- **Pon tus PDFs en una carpeta del proyecto** (p. ej. `papers/` o `references/`). Así la síntesis puede relacionar el paper con los demás que tengas.
- **Si trabajas en un proyecto propio** (tesis, código, manuscrito), Claude lo usará para la sección "Conexión con tu trabajo". Si no encuentra contexto, te preguntará en vez de suponer.
- **No te saltes la técnica Feynman.** Explicar el tópico con tus palabras es lo que más rápido revela qué no entendiste.
- **Revisa los "puntos a verificar".** Suelen ser los mejores temas para discutir con tu supervisor o en un journal club.

## Limitaciones
- Los PDFs escaneados (sin capa de texto) se leen peor; Claude ve las páginas como imágenes.
- La calidad de las derivaciones depende de lo completo que sea el paper. Cuando falta información, la guía lo dice en lugar de rellenar.
- Es una ayuda de estudio, no un sustituto de leer el paper: verifica las citas de página en el original.

---

## Contribuir
Issues y pull requests son bienvenidos. Toda la skill vive en [`SKILL.md`](SKILL.md): son instrucciones en Markdown, no hay código que compilar. Si propones un cambio, cuenta con qué paper lo probaste.

## Licencia
[MIT](LICENSE)

---

## English summary

**`leer-paper` is a [Claude Code](https://claude.com/claude-code) skill that turns a scientific paper into a linear, topic-by-topic study path and then tutors you through it.**

1. **Skim:** extracts the research question, the answer and the key evidence.
2. **Topic map:** proposes 4–8 topics ordered by conceptual dependency, then waits for your approval.
3. **Study guide:** writes `notes/<slug>/` next to the PDF. It includes an overview with a glossary and progress checkboxes, one file per topic (plain-language idea, step-by-step equations with order-of-magnitude checks, how to read the key figure, claim → evidence table, self-quiz) and a critical synthesis.
4. **Tutor mode:** `/leer-paper <slug> siguiente` explains the next topic, asks you to explain it back (Feynman technique), quizzes you and tracks progress. `/leer-paper <slug> quiz` gives you a mixed review.

It never attributes to the paper anything that isn't in it, cites pages for every claim and flags its own additions with 💡. It writes in your language (Spanish by default).

**Install:**
```bash
git clone https://github.com/ccanunez/leer-paper.git ~/.claude/skills/leer-paper
```
**Use:** `/leer-paper path/to/paper.pdf`, or just ask Claude *"help me understand this paper"*.
