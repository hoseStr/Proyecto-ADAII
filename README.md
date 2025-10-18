# 🎓 Proyecto: Repartición Óptima de Cupos (ROC)

## 👤 Autor  
**Jose Miguel Fuertes Benavides**  
**Código:** 2224623  
**Curso:** Análisis de Algoritmos II  
**Universidad del Valle — Septiembre 2025**

---

## 📘 Descripción General

El proyecto **ROC (Repartición Óptima de Cupos)** busca resolver el problema de asignar cupos de materias a estudiantes de forma **justa y eficiente**, minimizando la **insatisfacción promedio** de todos los estudiantes.

Se implementan tres enfoques algorítmicos distintos:

- **Fuerza Bruta:** garantiza la solución óptima, pero con alta complejidad.  
- **Voraz:** rápido, aunque no siempre óptimo.  
- **Programación Dinámica:** balance entre tiempo y optimalidad.

Cada algoritmo calcula una solución al problema dado el conjunto de materias disponibles (`M`) y las solicitudes priorizadas de los estudiantes (`E`).

---

## 🧩 Formulación del Problema

Dado un conjunto de materias `M = {(Mi, mi)}` con sus cupos, y un conjunto de estudiantes `E = {(ej, msj)}` donde cada estudiante solicita materias con prioridades, el objetivo es **asignar materias sin sobrepasar los cupos**, minimizando la función de insatisfacción:

\[
F(M, E)(A) = \frac{1}{r}\sum_{j=1}^{r} f_j
\]

donde \(f_j\) mide la insatisfacción del estudiante *j* según las materias que no pudo obtener y sus prioridades.

---

## 🗂️ Estructura del Proyecto

### Directorio Principal
- **`main.py`** → Punto de entrada de la aplicación. Contiene la interfaz gráfica (Tkinter) y la lógica de ejecución de los algoritmos.

### Directorio `algorithms/`
- **`fuerza_bruta.py`** → Implementa el algoritmo de fuerza bruta (`rocFB`).  
- **`voraz.py`** → Implementa el algoritmo voraz (`rocV`).  
- **`programacion_dinamica.py`** → Implementa el algoritmo de programación dinámica (`rocPD_optimizado`).

### Directorio `models/`
- **`reparticion_cupos.py`** → Define las clases `Materia`, `Estudiante` y `ReparticionCupos`, junto con las funciones para calcular la insatisfacción total.

### Directorio `utils/`
- **`file_manager.py`** → Gestiona la lectura y escritura de archivos de entrada/salida.  
- **`ui_theme_utils.py`** → Contiene utilidades visuales para la interfaz gráfica.  
- **`test_generator.py`** → Permite generar casos de prueba de forma aleatoria.

### Directorio `BateriaPruebas/`
- Contiene varios archivos de entrada (`.txt`) con diferentes configuraciones de materias y estudiantes, usados para probar el rendimiento de los algoritmos.

---

## 📥 Formato de Entrada

El archivo de entrada tiene el siguiente formato:

```
k
M1,m1
M2,m2
...
Mk,mk
r
e1,s1
m11,p11
m12,p12
...
e2,s2
m21,p21
...
```

Donde:  
- `k` → número de materias  
- `Mi, mi` → código de la materia y su cupo  
- `r` → número de estudiantes  
- `ej, sj` → código del estudiante y número de materias que solicita  
- `mjl, pjl` → código y prioridad de cada materia solicitada

---

## 📤 Formato de Salida

El programa genera un archivo con el siguiente formato:

```
Costo
e1,a1
m11
m12
...
e2,a2
m21
...
```

Donde:  
- La primera línea contiene el **costo total de insatisfacción (F)**.  
- Cada bloque siguiente lista las materias asignadas a cada estudiante.

---

## ⚙️ Requisitos del Sistema

- **Python 3.8 o superior**
- **Bibliotecas:**  
  - `tkinter`  
  - `itertools`  
  - `heapq`  
  - `random`  
  - `math`  

*(Todas incluidas en la biblioteca estándar de Python.)*

---

## ▶️ Ejecución de la Aplicación

1. Abre una terminal en la carpeta raíz del proyecto.  
2. Ejecuta:
   ```bash
   python main.py
   ```
3. Se abrirá una **interfaz gráfica (Tkinter)** con las siguientes opciones:

   - **Seleccionar archivo:** carga una instancia del problema desde `BateriaPruebas/`.
   - **Elegir algoritmo:** selecciona *Fuerza Bruta*, *Voraz* o *Programación Dinámica*.
   - **Ejecutar:** muestra los resultados y el tiempo de ejecución.
   - **Guardar salida:** exporta la solución generada a un archivo `.txt`.

---

## ⚖️ Algoritmos Implementados

| Algoritmo | Descripción | Ventajas | Desventajas |
|------------|--------------|-----------|--------------|
| **Fuerza Bruta (`rocFB`)** | Genera todas las asignaciones posibles y elige la mejor. | Solución óptima garantizada. | Tiempo exponencial, impráctico para grandes casos. |
| **Voraz (`rocV`)** | Asigna cupos priorizando materias y estudiantes según heurísticas. | Rápido y simple. | Puede no encontrar la solución óptima. |
| **Programación Dinámica (`rocPD`)** | Divide el problema en subproblemas con soluciones parciales óptimas. | Balance entre eficiencia y calidad. | Requiere más memoria y diseño cuidadoso. |

---

## 💾 Guardar y Comparar Resultados

- Después de ejecutar un algoritmo, la interfaz permite **guardar la salida**.  
- Puedes **comparar los tres métodos** para observar diferencias en costo de insatisfacción y tiempos de ejecución.

---

## 📊 Complejidades Teóricas

| Algoritmo | Complejidad Temporal | Complejidad Espacial |
|------------|----------------------|----------------------|
| Fuerza Bruta | O(n!) | O(1) |
| Voraz | O(n log n) | O(n) |
| Programación Dinámica | O(k·r) | O(k·r) |

---

## 👨‍💻 Autor y Créditos
**Desarrollado por:**  
📌 *Jose Miguel Fuertes Benavides*  
📘 *Análisis de Algoritmos II — Universidad del Valle*  
📅 *Octubre de 2025*
