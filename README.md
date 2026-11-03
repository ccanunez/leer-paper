# leer-paper

**Una skill para [Claude Code](https://claude.com/claude-code) que convierte un paper científico en una ruta de estudio lineal, por tópicos, lo verifica con código y luego te enseña como tutor.**

Leer un paper de principio a fin rara vez es la mejor forma de entenderlo. Las secciones no siguen el orden en que se construyen los conceptos, las ecuaciones aparecen sin derivación, los números rara vez se comprueban y las figuras —donde suele vivir el resultado— se leen a la pasada. `leer-paper` reorganiza el contenido en 4–8 tópicos donde cada uno depende solo de los anteriores. Escribe una guía de estudio, rehace los cálculos con sus incertidumbres, busca qué pasó después con el resultado y te enseña tópico a tópico. Solo te evalúa cuando tú digas que estás listo.

Funciona con papers de cualquier disciplina (física, biología, ciencias de la computación, economía…).

*English summary at the [end of this file](#english-summary).*

---

## Qué hace

| Fase | Qué ocurre | Escribe archivos |
|---|---|---|
| **1. Reconocimiento** | Lee abstract, introducción, figuras, conclusiones y disponibilidad de datos/código. Identifica la pregunta, la respuesta, la evidencia central y el tipo de paper. | No |
| **2. Diagnóstico y mapa** | Te hace 2–3 preguntas para ajustar el nivel. Propone 4–8 tópicos ordenados por dependencia conceptual y **espera tu visto bueno**. | No |
| **3. Guía de estudio** | Escribe la guía en `notes/<slug>/`, con la ficha de parámetros, el script de verificación, el estado actual del resultado y la lectura crítica. | Sí |
| **4. Tutor** | Te enseña cada tópico en bloques cortos con práctica, pistas, ejemplos numéricos y la técnica Feynman. Te evalúa al final, si quieres, y agenda cada pregunta para repaso espaciado. | Sí (progreso) |

### Qué contiene la guía
- **Un archivo por tópico**, todos con la misma plantilla:
  - Qué vas a aprender y por qué importa.
  - Prerrequisitos.
  - La idea, primero en lenguaje llano y luego con rigor.
  - Ecuaciones paso a paso, con ejemplo numérico e incertidumbre.
  - Cómo leer la figura.
  - Tabla afirmación → evidencia.
  - Autoevaluación con pistas y respuestas ocultas.
- **`params.toml`:** todos los valores de entrada del paper, con unidades, incertidumbre y página. Lo puedes importar en tu propio código.
- **`verify.py`:** rehace los cálculos clave y dice cuáles se reproducen. Propaga las incertidumbres con Monte Carlo e indica qué entrada domina cada resultado. Si tienes sympy, también comprueba pasos algebraicos.
- **Estado actual del resultado:** busca en [OpenAlex](https://openalex.org) los papers que lo citan, lee sus abstracts y clasifica cada uno como confirma, refina, en tensión, refuta o usa.
- **Código y datos del paper:** si hay un repositorio público, lo revisa (con tu permiso) y compara lo que dice el texto con lo que hace el código.
- **Lectura crítica:**
  - el argumento como diagrama;
  - un checklist según el tipo de paper (observacional, experimental, simulación, teórico, ML, instrumental o revisión; ver [`checklists.md`](checklists.md));
  - supuestos, limitaciones y puntos a verificar;
  - preguntas abiertas conectadas con tu trabajo.
- **Biblioteca compartida:**
  - un glosario común con los conflictos de notación entre papers;
  - un `referencias.bib`;
  - un índice con tu progreso y lo que toca repasar.

### Principios
- **No inventa.** Todo lo que atribuye al paper está en el paper, con la página citada: `(p. 4, §3.2, Ec. 5)`.
- **Separa voces.** Lo que agrega Claude (intuiciones, derivaciones, literatura posterior) va marcado como `> 💡 Nota de apoyo:`.
- **Verifica con código.** Nunca ajusta una entrada para que un cálculo cuadre: lo que no se reproduce va a la síntesis con su causa probable.
- **Enseña antes de evaluar.** El tutor explica, practica contigo y te pide explicarlo con tus palabras. La evaluación llega solo cuando dices que estás listo.
- **Te pregunta antes de escribir** (el mapa de tópicos) y **antes de descargar** (el código del paper).

---

## Instalación

Requiere [Claude Code](https://docs.claude.com/en/docs/claude-code) (CLI, app de escritorio o extensión de IDE), `python3` 3.11 o superior y `curl`.

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

### Opcionales
- **`poppler`:** para leer por rangos de páginas en libros, tesis y papers de más de ~40 páginas. Se instala con `brew install poppler` en macOS o con `sudo apt-get install poppler-utils` en Debian/Ubuntu.
- **`sympy`:** para comprobar derivaciones (`pip install sympy`).
- **`matplotlib`:** para reproducir figuras (`pip install matplotlib`).

---

## Uso

### 1. Crear la guía
```
/leer-paper papers/mi-paper.pdf
```
También se activa con lenguaje natural: *"ayúdame a entender este paper: papers/mi-paper.pdf"*. Si solo quieres decidir si vale la pena leerlo, usa `/leer-paper papers/mi-paper.pdf rápido`, que hace un resumen de una página.

Claude te hará un par de preguntas de diagnóstico, te mostrará algo como esto y esperará tu respuesta:

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
Una sesión recorre el tópico completo, un bloque por mensaje:

1. Dónde estás en el mapa.
2. Un repaso rápido de los prerrequisitos.
3. Bloques de contenido, cada uno con una pregunta de práctica sin nota y pistas graduadas si te trabas:
   - la intuición;
   - lo que dice el paper;
   - la ecuación, que derivas tú;
   - un ejemplo numérico en el que primero predices el resultado;
   - un "¿qué pasaría si…?" con las incertidumbres;
   - la figura;
   - la crítica y el estado actual;
   - la conexión con tu trabajo.
4. Explicar el tópico con tus palabras (técnica Feynman).
5. Escribir tu resumen.

Al final te pregunta si quieres evaluarte ahora o en otro momento (`evaluar N`). Si apruebas, el tópico queda marcado `[x]` y se pinta en el mapa conceptual.

### 3. Repasar
| Comando | Qué hace |
|---|---|
| `/leer-paper <slug> quiz` | Las preguntas de esta guía que tocan hoy, reformuladas para que no las respondas de memoria |
| `/leer-paper hoy` | Las que tocan hoy en **todas** tus guías, intercaladas |
| `/leer-paper <slug> anki` | Exporta preguntas y glosario a `anki.txt`, listo para importar en Anki |

Cada pregunta queda en un registro. Si la respondes bien, el intervalo crece (1 → 3 → 7 → 14 → 30 → 60 días); si fallas, vuelve a 1.

### 4. Ir más allá
| Comando | Qué hace |
|---|---|
| `/leer-paper <slug> tópico N` | Estudia un tópico concreto |
| `/leer-paper <slug> figura N` | Reproduce la figura N con código, a partir de las tablas y ecuaciones del paper. Puede superponer tus datos |
| `/leer-paper <slug> actualizar` | Rehace la búsqueda de qué pasó después con el resultado |
| `/leer-paper <slug> journal-club` | Guion por minuto, preguntas probables del público y preguntas para la discusión |
| `/leer-paper <slug> referee` | Informe de referee como ejercicio de lectura crítica |
| `/leer-paper comparar <slug1> <slug2> …` | Compara papers con guía: supuestos, parámetros comunes, dónde discrepan y por qué |

El `<slug>` es un nombre corto que la skill elige al crear la guía (p. ej. `cpd-pds70c-benisty2021`).

---

## Qué genera

```
papers/
├── mi-paper.pdf
└── notes/
    ├── README.md                # índice: progreso y repasos pendientes de cada guía
    ├── glosario.md              # glosario compartido + conflictos de notación
    ├── referencias.bib          # BibTeX de todas las guías
    ├── comparaciones/<tema>.md  # /leer-paper comparar
    └── <slug>/
        ├── 00_mapa.md           # resumen, mapa conceptual (Mermaid), glosario, ruta, registro de repaso
        ├── 01_<tópico>.md … NN_<tópico>.md
        ├── params.toml          # valores de entrada con unidades, incertidumbre y página
        ├── verify.py            # python3 verify.py
        ├── 99_sintesis.md       # argumento, checklist, puntos a verificar, estado actual, ideas
        ├── figuras/             # /leer-paper <slug> figura N
        ├── codigo/              # código del paper, si lo descargaste
        └── anki.txt, journal_club.md, referee.md, resumen.md   # según los comandos que uses
```

Ejemplo de salida de `verify.py`:
```
OK  M_dust CPD, granos de 1 mm [M⊕]: calculado 0.00683, paper 0.007 (p. 6)
    ↳ M_dust, 1 mm [M⊕]: 0.00563 (+0.0024 / −0.0013), percentiles 16–50–84
      T_cpd      cambia el resultado hasta 45%
      F_pico     cambia el resultado hasta 10%
NO  R_Bondi [au]: calculado 18.5, paper 11 (p. 6) con μ = 2.34 (gas molecular)
OK  R_Bondi [au]: calculado 11, paper 11 (p. 6) con μ = 1.4 se reproduce
```

Las ecuaciones se escriben en LaTeX (`$…$`, `$$…$$`) y los diagramas en Mermaid. Se ven bien en GitHub, Obsidian y VS Code (con una extensión de Mermaid).

---

## Consejos
- **Pon tus PDFs en una carpeta del proyecto** (p. ej. `papers/` o `references/`). Así la síntesis puede relacionar el paper con los demás y el glosario crece en un solo lugar.
- **Si trabajas en un proyecto propio** (tesis, código, manuscrito), Claude lo usará para la conexión con tu trabajo y las preguntas abiertas. Si no encuentra contexto, te preguntará en vez de suponer.
- **Responde las preguntas de práctica antes de pedir la respuesta.** Equivocarte en una predicción y ver por qué es la parte del tutor que más enseña.
- **Evalúate al día siguiente**, no justo después de estudiar: mide mejor lo que retienes.
- **Haz `/leer-paper hoy` unos minutos al día.** El repaso espaciado funciona por constancia, no por sesiones largas.
- **Edita `params.toml`** para probar otros supuestos, y vuelve a correr `verify.py`.

## Limitaciones
- Los PDFs escaneados (sin capa de texto) se leen peor; Claude ve las páginas como imágenes.
- La calidad de las derivaciones depende de lo completo que sea el paper. Cuando falta información, la guía lo dice en lugar de rellenar.
- El estado actual se basa en abstracts de OpenAlex. Es un buen punto de partida, no una revisión bibliográfica: lee los papers que importan.
- Cuando el paper no da una incertidumbre, `params.toml` puede usar un supuesto marcado con 💡. Revísalo antes de citar un resultado.
- Es una ayuda de estudio, no un sustituto de leer el paper: verifica las citas de página en el original.

---

## Contribuir
Issues y pull requests son bienvenidos. Son instrucciones en Markdown más un script de Python; no hay nada que compilar.

| Archivo | Qué contiene |
|---|---|
| [`SKILL.md`](SKILL.md) | Flujo principal y comandos |
| [`plantillas.md`](plantillas.md) | Plantillas de todos los archivos |
| [`verificacion.md`](verificacion.md) | `params.toml`, `verify.py`, figuras |
| [`investigacion.md`](investigacion.md) | Estado actual, código del paper, BibTeX |
| [`tutor.md`](tutor.md) | Tutor, evaluación, repaso espaciado |
| [`checklists.md`](checklists.md) | Revisión crítica por tipo de paper |
| [`scripts/citas.py`](scripts/citas.py) | Búsqueda de citas en OpenAlex |

Si propones un cambio, cuenta con qué paper lo probaste. Los checklists de disciplinas lejanas a la física son los que más se benefician de revisión experta.

## Licencia
[MIT](LICENSE)

---

## English summary

**`leer-paper` is a [Claude Code](https://claude.com/claude-code) skill that turns a scientific paper into a linear, topic-by-topic study path, checks it with code and then tutors you through it.**

1. **Skim:** extracts the research question, the answer, the key evidence and whether data or code are public.
2. **Diagnose and map:** asks a few questions to set your level, then proposes 4–8 topics ordered by conceptual dependency and waits for your approval.
3. **Study guide:** writes `notes/<slug>/` next to the PDF. It contains:
   - a file per topic: plain-language idea, step-by-step equations, how to read the key figure, claim → evidence table and a self-quiz with hints;
   - `params.toml`, with every input value, its unit, uncertainty and page;
   - `verify.py`, which recomputes the key numbers, propagates uncertainties with Monte Carlo and ranks which input dominates each result;
   - a "current status" section built from the papers that cite it (via OpenAlex);
   - a critical synthesis with the argument as a Mermaid diagram, a checklist for the paper type and open research questions.

   A shared glossary, a BibTeX file and a library index tie the guides together.
4. **Tutor:** `/leer-paper <slug> siguiente` teaches one topic in short blocks, with practice questions, graded hints, predict-then-check numerical examples and the Feynman technique. It only evaluates you when you say you are ready. Every question is scheduled for spaced repetition: `quiz` covers one guide, `hoy` covers your whole library, and `anki` exports flashcards.
5. **More:**
   - `figura N` reproduces a figure;
   - `comparar` contrasts papers;
   - `journal-club` and `referee` prepare a talk or a review;
   - `actualizar` refreshes the literature search.

It never attributes to the paper anything that isn't in it, cites pages for every claim and flags its own additions with 💡. It writes in your language (Spanish by default).

**Install:**
```bash
git clone https://github.com/ccanunez/leer-paper.git ~/.claude/skills/leer-paper
```
**Use:** `/leer-paper path/to/paper.pdf`, or just ask Claude *"help me understand this paper"*.
