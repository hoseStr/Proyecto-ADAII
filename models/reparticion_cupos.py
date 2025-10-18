class Materia:
    def __init__(self, codigo, cupo):
        self.codigo = codigo
        self.cupo = cupo
    
    def __repr__(self):
        return f"Materia({self.codigo}, cupo={self.cupo})"


class Estudiante:
    def __init__(self, codigo, solicitudes):
        """
        Parámetros:
        -----------
        codigo : str
            Código del estudiante
        solicitudes : list of tuples
            Lista de tuplas (codigo_materia, prioridad)
        """
        self.codigo = codigo
        self.solicitudes = solicitudes
    
    def __repr__(self):
        return f"Estudiante({self.codigo}, {len(self.solicitudes)} materias)"


class ReparticionCupos:
    def __init__(self, materias, estudiantes):
        """
        Parámetros:
        -----------
        materias : list of Materia
            Lista de objetos Materia
        estudiantes : list of Estudiante
            Lista de objetos Estudiante
        """
        self.materias = materias
        self.estudiantes = estudiantes
        
        # Validar instancia al crearla
        self._validar_instancia()
    
    def _validar_instancia(self):
        """
        Valida que la instancia cumpla todas las restricciones del problema.
        Lanza ValueError si hay violaciones.
        """
        codigos_materias = {m.codigo for m in self.materias}
        
        for estudiante in self.estudiantes:
            # Verificar que no haya materias repetidas
            codigos_solicitados = [codigo for codigo, _ in estudiante.solicitudes]
            if len(codigos_solicitados) != len(set(codigos_solicitados)):
                raise ValueError(
                    f"ERROR: Estudiante {estudiante.codigo} tiene materias repetidas"
                )
            
            # Verificar que las prioridades estén en {1, 2, 3, 4, 5}
            for codigo_mat, prioridad in estudiante.solicitudes:
                if prioridad not in {1, 2, 3, 4, 5}:
                    raise ValueError(
                        f"ERROR: Estudiante {estudiante.codigo} tiene prioridad {prioridad} "
                        f"inválida (debe estar en {{1, 2, 3, 4, 5}})"
                    )
                
                # Verificar que la materia exista
                if codigo_mat not in codigos_materias:
                    raise ValueError(
                        f"ERROR: Estudiante {estudiante.codigo} solicita materia {codigo_mat} "
                        f"que no existe"
                    )
            
            # Verificar restricción de suma de prioridades
            if len(estudiante.solicitudes) > 0:
                num_materias = len(estudiante.solicitudes)
                gamma = 3 * num_materias - 1
                suma_prioridades = sum(p for _, p in estudiante.solicitudes)
                
                if suma_prioridades > gamma:
                    raise ValueError(
                        f"ERROR: Estudiante {estudiante.codigo} viola restricción: "
                        f"suma_prioridades={suma_prioridades} > γ({num_materias})={gamma}"
                    )
    
    def calcular_insatisfaccion(self, asignaciones):
        """
        Calcula la función de insatisfacción general F_<M,E>(A).
        
        Fórmula:
        f_j = (1 - |ma_j|/|ms_j|) × (Σ prioridades_no_asignadas / γ(|ms_j|))
        F_<M,E>(A) = (Σ f_j) / r
        
        Parámetros:
        -----------
        asignaciones : dict
            Diccionario {codigo_estudiante: [lista_codigos_materias_asignadas]}
        
        Retorna:
        --------
        float: Valor de insatisfacción en [0, 1]
        
        Garantías:
        ----------
        - Retorna un valor en el rango [0, 1]
        - Valida que las asignaciones sean correctas
        """
        if not self.estudiantes:
            return 0.0
        
        suma_insatisfacciones = 0.0
        r = len(self.estudiantes)
        
        for estudiante in self.estudiantes:
            # ms_j: solicitudes del estudiante (lista de tuplas)
            ms_j = estudiante.solicitudes
            
            # ma_j: materias asignadas (lista de códigos)
            ma_j = asignaciones.get(estudiante.codigo, [])
            
            # Caso especial: estudiante sin solicitudes
            if len(ms_j) == 0:
                # No contribuye a la insatisfacción
                continue
            
            # Convertir asignaciones a conjunto para búsqueda eficiente
            materias_asignadas_set = set(ma_j)
            
            # VALIDACIÓN: Las materias asignadas deben estar en las solicitadas
            codigos_solicitados = {codigo for codigo, _ in ms_j}
            materias_invalidas = materias_asignadas_set - codigos_solicitados
            if materias_invalidas:
                raise ValueError(
                    f"ERROR: Estudiante {estudiante.codigo} tiene asignadas materias "
                    f"{materias_invalidas} que NO solicitó"
                )
            
            # |ms_j|: número de materias solicitadas
            num_solicitadas = len(ms_j)
            
            # |ma_j|: número de materias asignadas
            num_asignadas = len(ma_j)
            
            # γ(|ms_j|) = 3 * |ms_j| - 1
            gamma = 3 * num_solicitadas - 1
            
            # Suma de prioridades de materias NO asignadas
            suma_prioridades_no_asignadas = sum(
                prioridad
                for codigo_materia, prioridad in ms_j
                if codigo_materia not in materias_asignadas_set
            )
            
            # Calcular f_j
            proporcion_no_asignadas = 1.0 - (num_asignadas / num_solicitadas)
            proporcion_prioridades = suma_prioridades_no_asignadas / gamma
            
            f_j = proporcion_no_asignadas * proporcion_prioridades
            
            # VALIDACIÓN INTERNA: f_j debe estar en [0, 1]
            if f_j < 0 or f_j > 1.0001:  # Tolerancia por punto flotante
                raise RuntimeError(
                    f"ERROR INTERNO: f_j={f_j:.6f} fuera de rango [0,1] "
                    f"para estudiante {estudiante.codigo}\n"
                    f"  num_solicitadas={num_solicitadas}\n"
                    f"  num_asignadas={num_asignadas}\n"
                    f"  suma_prioridades_no_asignadas={suma_prioridades_no_asignadas}\n"
                    f"  gamma={gamma}"
                )
            
            suma_insatisfacciones += f_j
        
        # Calcular promedio
        F = suma_insatisfacciones / r
        
        # VALIDACIÓN FINAL: F debe estar en [0, 1]
        if F > 1.0001:  # Tolerancia por punto flotante
            raise RuntimeError(
                f"ERROR GRAVE: F={F:.6f} > 1.0\n"
                f"Hay un error en el cálculo o en las entradas"
            )
        
        # Asegurar que esté exactamente en [0, 1]
        return max(0.0, min(F, 1.0))
    
    def validar_asignacion(self, asignaciones):
        """
        Valida que una asignación sea factible (no exceda cupos).
        
        Parámetros:
        -----------
        asignaciones : dict
            {codigo_estudiante: [lista_materias_asignadas]}
        
        Retorna:
        --------
        tuple: (es_valida, mensaje_error)
        """
        # Contar cuántos estudiantes reciben cada materia
        cupos_usados = {}
        
        for estudiante in self.estudiantes:
            materias_asignadas = asignaciones.get(estudiante.codigo, [])
            
            for materia_codigo in materias_asignadas:
                cupos_usados[materia_codigo] = cupos_usados.get(materia_codigo, 0) + 1
        
        # Verificar que no se exceden cupos
        for materia in self.materias:
            usado = cupos_usados.get(materia.codigo, 0)
            if usado > materia.cupo:
                return False, (
                    f"Materia {materia.codigo} excede cupo: "
                    f"{usado} asignados > {materia.cupo} disponibles"
                )
        
        return True, "Asignación válida"
    
    def __repr__(self):
        return (
            f"ReparticionCupos("
            f"{len(self.materias)} materias, "
            f"{len(self.estudiantes)} estudiantes)"
        )