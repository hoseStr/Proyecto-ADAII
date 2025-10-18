"""
Módulo: voraz.py
Algoritmo Voraz para el problema de repartición óptima de cupos.

Estrategia: Asignar materias priorizando estudiantes y sus prioridades de forma greedy.
"""

"""
def rocV(instancia):
    Algoritmo Voraz para asignación de materias.
    
    Estrategia Greedy:
    1. Procesar estudiantes en orden (puede variarse según heurística)
    2. Para cada estudiante, intentar asignar TODAS sus materias solicitadas
    3. Asignar en orden de prioridad decreciente (prioridad 5 primero)
    4. Asignar solo si hay cupo disponible
    
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
    Temporal: O(r * s * log(s)) donde r=estudiantes, s=materias solicitadas promedio
              El log(s) viene del ordenamiento de solicitudes
    Espacial: O(r * s)
    
    Nota sobre optimalidad:
    -----------------------
    Este algoritmo NO garantiza encontrar la solución óptima en todos los casos.
    Es una heurística greedy que puede dar soluciones subóptimas cuando hay
    conflictos en la asignación de cupos limitados.
    # Inicializar estructuras
    asignaciones = {e.codigo: [] for e in instancia.estudiantes}
    cupos = {m.codigo: m.cupo for m in instancia.materias}
    
    # Procesar cada estudiante
    for estudiante in instancia.estudiantes:
        # Ordenar solicitudes por prioridad (mayor prioridad primero)
        # P = {1, 2, 3, 4, 5} donde 5 es la mayor prioridad
        solicitudes_ordenadas = sorted(
            estudiante.solicitudes, 
            key=lambda x: x[1],  # Ordenar por prioridad
            reverse=True  # Mayor prioridad primero
        )
        
        # Intentar asignar cada materia solicitada
        for materia_codigo, prioridad in solicitudes_ordenadas:
            # Verificar si hay cupo disponible
            if cupos.get(materia_codigo, 0) > 0:
                # Asignar la materia
                asignaciones[estudiante.codigo].append(materia_codigo)
                cupos[materia_codigo] -= 1
    
    # Calcular costo de la solución
    costo = instancia.calcular_insatisfaccion(asignaciones)
    
    return asignaciones, costo
"""

def rocV(instancia):
    """
    Algoritmo voraz avanzado con estrategia de peso.
    
    Estrategia: Asignar materias priorizando por un "peso" que combina:
    - Prioridad del estudiante para esa materia
    - Escasez de cupos (cupos restantes / demanda)
    
    Esta estrategia intenta balancear mejor las asignaciones considerando
    la disponibilidad global de cada materia.
    
    Complejidad:
    ------------
    Temporal: O(r * s + r * s * log(r*s))
    """
    # Calcular demanda por materia
    demanda = {}
    for estudiante in instancia.estudiantes:
        for materia_codigo, _ in estudiante.solicitudes:
            demanda[materia_codigo] = demanda.get(materia_codigo, 0) + 1
    
    # Crear lista de todas las solicitudes con peso
    solicitudes_globales = []
    for estudiante in instancia.estudiantes:
        for materia_codigo, prioridad in estudiante.solicitudes:
            # Calcular escasez: menor valor = materia más escasa
            cupo_total = next((m.cupo for m in instancia.materias if m.codigo == materia_codigo), 0)
            escasez = cupo_total / demanda.get(materia_codigo, 1)
            
            # Peso: prioridad / escasez (mayor peso = más importante asignar)
            peso = prioridad / escasez if escasez > 0 else prioridad * 1000
            
            solicitudes_globales.append({
                'estudiante': estudiante.codigo,
                'materia': materia_codigo,
                'prioridad': prioridad,
                'peso': peso
            })
    
    # Ordenar por peso (mayor peso primero)
    solicitudes_globales.sort(key=lambda x: x['peso'], reverse=True)
    
    # Asignar en orden de peso
    asignaciones = {e.codigo: [] for e in instancia.estudiantes}
    cupos = {m.codigo: m.cupo for m in instancia.materias}
    
    for solicitud in solicitudes_globales:
        est_codigo = solicitud['estudiante']
        mat_codigo = solicitud['materia']
        
        # Verificar que el estudiante no tenga ya esa materia asignada
        if mat_codigo not in asignaciones[est_codigo]:
            # Verificar cupo disponible
            if cupos.get(mat_codigo, 0) > 0:
                asignaciones[est_codigo].append(mat_codigo)
                cupos[mat_codigo] -= 1
    
    costo = instancia.calcular_insatisfaccion(asignaciones)
    return asignaciones, costo