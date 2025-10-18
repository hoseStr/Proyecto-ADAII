from models.reparticion_cupos import Materia, Estudiante, ReparticionCupos

def leer_instancia(ruta):
    with open(ruta, 'r') as f:
        lineas = [l.strip() for l in f.readlines() if l.strip()]
    
    k = int(lineas[0])
    materias = []
    pos = 1
    for _ in range(k):
        cod, cupo = lineas[pos].split(',')
        materias.append(Materia(cod, int(cupo)))
        pos += 1

    r = int(lineas[pos])
    pos += 1
    estudiantes = []
    for _ in range(r):
        cod_est, num_solic = lineas[pos].split(',')
        num_solic = int(num_solic)
        pos += 1
        solicitudes = []
        for _ in range(num_solic):
            cod_mat, prio = lineas[pos].split(',')
            solicitudes.append((cod_mat, int(prio)))
            pos += 1
        estudiantes.append(Estudiante(cod_est, solicitudes))

    return ReparticionCupos(materias, estudiantes)


def guardar_salida(ruta_salida, costo, asignaciones):
    """
    Guarda la salida en la ruta indicada.

    Args:
        ruta_salida: ruta completa del archivo de salida a escribir.
        costo: valor numérico de la insatisfacción.
        asignaciones: dict {estudiante: [materia_cod, ...]}
    """
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(f"{costo:.4f}\n")
        for est, mats in asignaciones.items():
            f.write(f"{est},{len(mats)}\n")
            for m in mats:
                f.write(f"{m}\n")


def guardar_salida_desde_entrada(ruta_entrada, costo, asignaciones, suffix="_salida"):
    """
    Guarda la salida en un archivo cuyo nombre deriva del archivo de entrada.

    Ejemplo: 'BateriaPruebas/Prueba1.txt' -> 'BateriaPruebas/Prueba1_salida.txt'

    Args:
        ruta_entrada: ruta al archivo de entrada usado para generar la instancia.
        costo: valor numérico de la insatisfacción.
        asignaciones: dict {estudiante: [materia_cod, ...]}
        suffix: sufijo a añadir al nombre base del archivo (antes de la extensión).
    Returns:
        ruta_salida usada.
    """
    import os
    base = os.path.basename(ruta_entrada)
    name, ext = os.path.splitext(base)
    if not ext:
        ext = '.txt'
    nombre_salida = f"{name}{suffix}{ext}"
    ruta_dir = os.path.dirname(ruta_entrada) or '.'
    ruta_salida = os.path.join(ruta_dir, nombre_salida)
    guardar_salida(ruta_salida, costo, asignaciones)
    return ruta_salida