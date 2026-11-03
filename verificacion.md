# Verificación numérica, incertidumbres y figuras

## `params.toml` — ficha de parámetros
Todos los valores numéricos que usa el paper como entrada (constantes del sistema, valores
adoptados, resultados de otros trabajos que usa), con unidades, incertidumbre y página.
`verify.py`, `comparar`, `figura N` y el tutor los leen de aquí; el usuario puede importarlo
en su propio código (`tomllib` está en la biblioteca estándar desde Python 3.11).

```toml
# <Autores (año)>, "<título>".
# valor + unidad; error = 1σ (o [−, +]) o rango = [mín, máx] (uniforme). Sin error → fijo.
# fuente: página del paper, o "💡 supuesto" si el paper no da la incertidumbre.

[d]
valor = 112.4
unidad = "pc"
error = 0.2
pagina = "p. 1"

[T_cpd]
valor = 26
unidad = "K"
rango = [20, 40]
pagina = "p. 6"
fuente = "💡 supuesto: el paper no da incertidumbre para T; rango ilustrativo"
```
Reglas:
- Claves cortas, válidas como identificador (`M_p`, `kappa_1mm`, `F_pico`).
- Unidades de la tabla `UNIDADES` de `verify.py`; si falta una, añadirla allí.
- **Incertidumbres:** usar la del paper. Si el paper no la da pero el resultado depende
  fuertemente del valor, se puede poner un `rango` o `error` razonable marcado como
  `fuente = "💡 supuesto: …"` explicando de dónde sale. Si no hay base para suponerla,
  dejarlo fijo.
- Los resultados del paper (lo que se quiere reproducir) no van aquí: van en `check()`.

## `verify.py` — verificación reproducible
Rehace los cálculos clave (los que sostienen la conclusión y los ejemplos numéricos de los
tópicos), propaga incertidumbres con Monte Carlo e indica qué entrada domina cada resultado.

Plantilla (copiar tal cual el bloque de utilidades; escribir los cálculos abajo):

```python
"""Verificación numérica: <título corto> (<autores, año>).
Ejecutar: python3 verify.py   (entradas en params.toml)"""
import math
import random
import tomllib
from pathlib import Path

# Constantes (cgs)
G, k_B, m_H, sigma_SB = 6.674e-8, 1.381e-16, 1.673e-24, 5.670e-5
c, h = 2.998e10, 6.626e-27
au, pc, yr = 1.496e13, 3.086e18, 3.156e7
M_sun, M_jup, M_earth = 1.989e33, 1.898e30, 5.972e27
R_sun, R_jup = 6.957e10, 7.149e9

UNIDADES = {"": 1, "K": 1, "cm2/g": 1, "au": au, "pc": pc, "M_sun": M_sun, "M_jup": M_jup,
            "M_earth": M_earth, "R_sun": R_sun, "R_jup": R_jup, "Jy": 1e-23, "mJy": 1e-26,
            "uJy": 1e-29, "um": 1e-4, "mm": 0.1, "cm": 1, "deg": math.pi / 180, "yr": yr}

P = tomllib.loads((Path(__file__).parent / "params.toml").read_text())
X0 = {k: q["valor"] * UNIDADES[q.get("unidad", "")] for k, q in P.items()}  # valores centrales, cgs
resultados = []
random.seed(1)


def check(nombre, calculado, paper, pagina, rtol=0.1, nota=""):
    """Compara con el valor del paper; rtol refleja el redondeo con que lo reporta."""
    ok = math.isclose(calculado, paper, rel_tol=rtol)
    resultados.append(ok)
    print(f"{'OK' if ok else 'NO'}  {nombre}: calculado {calculado:.3g}, paper {paper:.3g} ({pagina}) {nota}")


def extremos(k):
    """(bajo, alto) en cgs: ±1σ si hay error, los bordes si hay rango; None si es fijo."""
    q, f = P[k], UNIDADES[P[k].get("unidad", "")]
    if "rango" in q:
        return q["rango"][0] * f, q["rango"][1] * f
    if "error" in q:
        lo, hi = q["error"] if isinstance(q["error"], list) else (q["error"],) * 2
        return (q["valor"] - lo) * f, (q["valor"] + hi) * f
    return None


def sorteo(k):
    """Un valor al azar: uniforme en el rango, o normal (dividida si el error es [−, +])."""
    q, f = P[k], UNIDADES[P[k].get("unidad", "")]
    if "rango" in q:
        return random.uniform(*q["rango"]) * f
    lo, hi = q["error"] if isinstance(q.get("error"), list) else (q.get("error", 0),) * 2
    z = abs(random.gauss(0, 1))
    x = q["valor"] - z * lo if random.random() < lo / ((lo + hi) or 1) else q["valor"] + z * hi
    return x * f


def incertidumbre(nombre, fn, unidad=1, n=20000):
    """Monte Carlo sobre todas las entradas con error o rango, y sensibilidad a cada una."""
    con_error = [k for k in P if extremos(k)]
    muestras = sorted(fn({**X0, **{k: sorteo(k) for k in con_error}}) / unidad for _ in range(n))
    q16, q50, q84 = (muestras[int(n * p)] for p in (0.16, 0.5, 0.84))
    print(f"    ↳ {nombre}: {q50:.3g} (+{q84 - q50:.2g} / −{q50 - q16:.2g}), percentiles 16–50–84")
    central = fn(X0)
    sens = []
    for k in con_error:
        vals = [fn({**X0, k: v}) for v in extremos(k)]
        if max(vals) != min(vals):
            sens.append((max(abs(v / central - 1) for v in vals), k))
    for s, k in sorted(sens, reverse=True):
        print(f"      {k:<10} cambia el resultado hasta {s:.0%}")


# --- <Nombre> (p. N, Ec. M): <ecuación> ---
# def <calculo>(x):              # x: dict de entradas en cgs (X0 o un sorteo)
#     return ...
# check("<nombre> [unidad]", <calculo>(X0) / <unidad>, <valor del paper>, "p. N")
# incertidumbre("<nombre> [unidad]", <calculo>, <unidad>)

# --- Derivaciones simbólicas (opcional, requiere sympy) ---
try:
    import sympy as sp
    # ok = sp.simplify(<lado izquierdo> - <lado derecho>) == 0
    # print(f"{'OK' if ok else 'NO'}  [sympy] <qué paso de la derivación se comprueba>")
    # resultados.append(ok)
except ImportError:
    print("--  [sympy] no instalado: se omiten las derivaciones simbólicas (pip install sympy)")

print(f"\n{sum(resultados)}/{len(resultados)} cálculos se reproducen")
```

Reglas:
- Cada cálculo es una función de `x` (un dict de entradas en cgs) para poder evaluarla en
  los valores centrales y en los sorteos del Monte Carlo. Comentario con la ecuación y la
  página encima.
- **Nunca ajustar una entrada para forzar un OK.** Si no se reproduce, probar la causa
  probable (otra constante, otro supuesto, un factor geométrico) en un `check` adicional con
  `nota` que la explique, como hipótesis, no como corrección.
- `incertidumbre()` sólo para los resultados que sostienen la conclusión. La mediana puede
  diferir del valor central si el rango de alguna entrada es asimétrico: comentarlo.
- **Derivaciones simbólicas:** para pasos algebraicos no triviales de la sección 4 de un
  tópico (despejes, límites, expansiones), comprobarlos con `sp.simplify(a - b) == 0` o
  `sp.limit`. Si sympy no está instalado, el script sigue y lo avisa.
- Biblioteca estándar más sympy opcional; numpy/scipy sólo si hacen falta (integrales,
  ajustes) y están instaladas.
- Ejecutar con `python3 verify.py`. Cada `NO` va a "Puntos a verificar" de la síntesis; la
  entrada dominante de cada resultado también.
- Omitirlo sólo si el paper no tiene cálculos reproducibles (p. ej. una revisión cualitativa).

## `figura N` — reproducir una figura
Escribir `notes/<slug>/figuras/figN.py` (matplotlib), ejecutarlo y guardar `figN.png`.
- **Datos legítimos, en este orden:** tablas del paper; ecuaciones del paper evaluadas con
  `params.toml` (curvas de modelo); datos públicos del paper (ver `investigacion.md`).
  **Nunca inventar puntos ni "leerlos a ojo" de la figura.** Si la figura sólo se puede
  rehacer digitalizándola, decirlo y ofrecer que el usuario la digitalice (p. ej. con
  WebPlotDigitizer) y entregue un CSV.
- Mismos ejes, unidades y escalas que el original; en el título, `Reproducción de Fig. N (p. M)`
  y la fuente de cada serie en la leyenda.
- Si el usuario pasa sus propios datos (ruta a un CSV, FITS, etc.), superponerlos con otro
  color y una leyenda clara: es la forma más directa de conectar el paper con su trabajo.
- Importar las funciones de `verify.py` en vez de reescribir las ecuaciones:
  `sys.path.insert(0, str(Path(__file__).parents[1])); import verify` (el import ejecuta
  los checks; es aceptable).
- Añadir la imagen a la sección 5 del tópico correspondiente.
- Si matplotlib no está instalado, sugerir `pip install matplotlib`.
