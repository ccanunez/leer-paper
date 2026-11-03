# Checklists de revisión según el tipo de paper

Usar la sección **Común** más la del tipo detectado en la Fase 1 (un paper puede tener dos
tipos, p. ej. observacional + modelado). Cada punto se evalúa en `99_sintesis.md` con lo que
hace el paper (citando página) y una evaluación: ✅ bien resuelto · ⚠️ parcial o discutible ·
❌ ausente o problemático · — no aplica.

## Común a todos
- ¿La conclusión principal se sigue de la evidencia, o el abstract dice más que los resultados?
- ¿Se reportan incertidumbres en los resultados clave? ¿Cómo se propagan?
- ¿Qué parámetros se fijaron en vez de ajustarse, y cuánto cambia el resultado si varían?
- ¿Se consideran explicaciones alternativas y se descartan con argumentos?
- ¿Están disponibles los datos, el código y los parámetros para reproducirlo?

## Observacional
- Selección de la muestra u objeto: ¿sesgos de selección o de detección?
- Calibración y reducción: ¿qué incertidumbre sistemática introducen?
- Significancia de las detecciones: S/N, número de pruebas, falsos positivos.
- Efectos instrumentales que imitan la señal (PSF/beam, artefactos, contaminación).
- Supuestos para pasar de lo observado a lo físico (distancia, opacidad, temperatura, modelo).

## Experimental (laboratorio, clínico, de campo)
- Diseño: grupo control, aleatorización, ciego, tamaño muestral justificado.
- Variables confusoras y cómo se controlan.
- Estadística: test adecuado a los datos, corrección por comparaciones múltiples, tamaño
  del efecto además del p-valor.
- Réplicas (técnicas y biológicas) y exclusión de datos: ¿criterios fijados de antemano?
- ¿El resultado se generaliza fuera de las condiciones del experimento?

## Simulación numérica
- Resolución: ¿se muestra convergencia? ¿Se resuelven las escalas relevantes?
- Condiciones iniciales y de borde: ¿influyen en el resultado?
- Física incluida y excluida (y qué cambiaría al incluir lo excluido).
- Tiempo de integración: ¿se alcanza un estado estacionario o se mira un transitorio?
- Código: ¿validado con problemas de prueba? ¿Público?

## Teórico-analítico
- Supuestos y aproximaciones: ¿en qué régimen son válidos? ¿Se respetan en la aplicación?
- Pasos de la derivación que se omiten o que no se pueden reconstruir.
- Casos límite: ¿el resultado recupera resultados conocidos?
- Predicciones falsables y cómo se comparan con datos.

## Computacional / aprendizaje automático
- Separación entrenamiento/validación/test y posibles fugas de datos.
- Baselines: ¿se compara con métodos simples y con el estado del arte en igualdad de condiciones?
- Varianza entre semillas o corridas; barras de error en las métricas.
- Ablaciones: ¿qué componente explica la mejora?
- Costo computacional y sensibilidad a hiperparámetros.

## Instrumental / métodos
- Validación con datos o casos donde la respuesta es conocida.
- Límites de aplicabilidad y modos de falla.
- Comparación con los métodos existentes (precisión, costo, supuestos).

## Revisión
- Criterio de selección de la literatura: ¿sistemático o a discreción?
- ¿Se presentan las posturas en conflicto de forma equilibrada?
- ¿Distingue resultados establecidos de especulación?
- Actualidad: ¿qué se publicó después que cambie el panorama?
