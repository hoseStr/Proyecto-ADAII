"""
Módulo: fuerza_bruta.py
Algoritmo de Fuerza Bruta para el problema de repartición óptima de cupos.
"""

from itertools import product


def rocFB(instancia):
    """
    Algoritmo de Fuerza Bruta que explora todas las posibles asignaciones
    de materias a estudiantes y retorna la óptima.
    
    Parámetros:
    -----------
    instancia : Instancia
        Objeto con materias, estudiantes y método calcular_insatisfaccion()
    
    Retorna:
    --------
    tuple: (asignacion, costo)
        - asignacion: dict {codigo_estudiante: [lista_materias_asignadas]}
        - costo: float con F_<M,E>(A)
    
    Complejidad:
    ------------
    Temporal: O(2^(suma de materias solicitadas))
    Espacial: O(r * k) donde r=estudiantes, k=materias promedio
    """
    materias = instancia.materias
    estudiantes = instancia.estudiantes
    cupos = {m.codigo: m.cupo for m in materias}
    
    # Generar todos los subconjuntos de materias por estudiante
    opciones_por_estudiante = []
    for est in estudiantes:
        materias_solicitadas = [mat_codigo for mat_codigo, _ in est.solicitudes]
        subconjuntos = generar_subconjuntos(materias_solicitadas)
        opciones_por_estudiante.append((est.codigo, subconjuntos))
    
    mejor_asignacion = None
    mejor_costo = float("inf")
    
    # Explorar todas las combinaciones posibles
    listas_opciones = [opciones for _, opciones in opciones_por_estudiante]
    
    for combinacion in product(*listas_opciones):
        asignacion_actual = {}
        cupos_usados = {}
        factible = True
        
        # Construir asignación y verificar cupos
        for idx, subconjunto_materias in enumerate(combinacion):
            estudiante_codigo = opciones_por_estudiante[idx][0]
            asignacion_actual[estudiante_codigo] = list(subconjunto_materias)
            
            for materia in subconjunto_materias:
                cupos_usados[materia] = cupos_usados.get(materia, 0) + 1
                if cupos_usados[materia] > cupos.get(materia, 0):
                    factible = False
                    break
            if not factible:
                break
        
        if factible:
            costo = instancia.calcular_insatisfaccion(asignacion_actual)
            if costo < mejor_costo:
                mejor_costo = costo
                mejor_asignacion = dict(asignacion_actual)
    
    if mejor_asignacion is None:
        return {}, float("inf")
    
    return mejor_asignacion, mejor_costo


def generar_subconjuntos(lista):
    """
    Genera todos los subconjuntos de una lista usando máscaras binarias.
    
    Para n elementos genera 2^n subconjuntos.
    """
    n = len(lista)
    subconjuntos = []
    
    for mascara in range(2**n):
        subconjunto = []
        for j in range(n):
            if mascara & (1 << j):
                subconjunto.append(lista[j])
        subconjuntos.append(tuple(subconjunto))
    
    return subconjuntos