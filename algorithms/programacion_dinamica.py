from itertools import combinations
from collections import defaultdict
import heapq
import time

def rocPD(reparticion, beam_width=5000, max_states=100000):

    """
    Programacion dinámica para asignación de materias a estudiantes:
     - codificación de estado como entero (mixed-radix),
     - precomputación de deltas enteros por elección,
     - ordenamiento de estudiantes por menor branching,
     - beam search adaptativo + poda por dominancia.

    Parámetros:
      reparticion: objeto con atributos:
         - materias: lista de objetos con .codigo y .cupo
         - estudiantes: lista de objetos con .codigo y .solicitudes (lista de tuplas (codigo_materia, prioridad))
      beam_width: ancho del beam (int). Si es None o 0 -> no beam (cuidado con memoria).
      max_states: límite absoluto para prevenir explosion.

    Retorna:
      (asig_dict, F_promedio)
    """
    start_time = time.time()

    materias = reparticion.materias
    estudiantes = reparticion.estudiantes
    r = len(estudiantes)
    k = len(materias)
    if r == 0:
        return {}, 0.0

    # ----------------------------------------------------------
    # Preparativos: mapeos, bases y multiplicadores para mixed-radix
    # ----------------------------------------------------------
    materia_a_idx = {m.codigo: i for i, m in enumerate(materias)}
    idx_a_materia = {i: m.codigo for i, m in enumerate(materias)}
    cupos_init = [m.cupo for m in materias]
    bases = [c + 1 for c in cupos_init]  # cada dígito en 0..cupo
    mult = [1] * k
    for i in range(1, k):
        mult[i] = mult[i-1] * bases[i-1]  # multiplicador para la posición i

    # Funciones para manipular estado entero
    def encode(cupos_tuple):
        s = 0
        for i, val in enumerate(cupos_tuple):
            s += val * mult[i]
        return s

    def extract_digit(state_int, idx):
        return (state_int // mult[idx]) % bases[idx]

    # estado entero inicial
    init_state_int = encode(tuple(cupos_init))

    # ----------------------------------------------------------
    # Precompute: para cada estudiante, todas las elecciones (maj),
    # su vector need (list), delta_int (sum need[i]*mult[i]) y f_j
    # ----------------------------------------------------------
    choices_per_student = []
    print("Precomputando opciones por estudiante...")
    for est in estudiantes:
        reqs = est.solicitudes  # lista de (codigo_materia, prioridad)
        s = len(reqs)
        gamma = 3 * s - 1 if s > 0 else 1
        # generar subconjuntos (si s muy grande, se puede limitar)
        max_subsets = 1 << s
        # Si s grande (>12) limitar conjuntos -> aquí dejamos sin limitar pero podrías truncar
        local_choices = []
        for mask in range(0, max_subsets):
            maj = []
            need = [0] * k
            for bit in range(s):
                if (mask >> bit) & 1:
                    codigo, prio = reqs[bit]
                    idx = materia_a_idx.get(codigo, None)
                    if idx is None:
                        idx = None
                        break
                    need[idx] += 1
                    maj.append((codigo, prio))
            # si alguna materia no existe, saltar
            if any(val is None for val in maj):
                continue
            assigned_count = len(maj)
            sum_unassigned_priorities = sum(p for (c, p) in reqs if (c, p) not in maj)
            f_j = (1 - assigned_count / s) * (sum_unassigned_priorities / gamma) if s > 0 else 0.0
            # delta int
            delta = 0
            need_tuple = tuple(need)
            for i_idx, n in enumerate(need_tuple):
                if n:
                    delta += n * mult[i_idx]
            # store choice as (maj_course_codes_list, need_tuple, delta_int, f_j)
            maj_codes = [c for c, _ in maj]
            local_choices.append((maj_codes, need_tuple, delta, f_j))
        # If no choices (shouldn't happen) add empty
        if not local_choices:
            local_choices.append(([], tuple([0]*k), 0, 0.0))
        choices_per_student.append(local_choices)

    # ----------------------------------------------------------
    # Strategy: reorder students to process those with fewer opciones first
    # keep mapping to restore backpointers to original indices
    # ----------------------------------------------------------
    order = list(range(r))
    order.sort(key=lambda i: len(choices_per_student[i]))  # students with fewer choices first
    ordered_choices = [choices_per_student[i] for i in order]
    ordered_students = [estudiantes[i] for i in order]

    # ----------------------------------------------------------
    # DP by niveles (capa por estudiante) usando estados enteros
    # dp: dict state_int -> cost
    # backpointers: lista de dicts por nivel: new_state_int -> (prev_state_int, choice_idx)
    # ----------------------------------------------------------
    dp = {init_state_int: 0.0}
    back = []

    for level, (est, choices) in enumerate(zip(ordered_students, ordered_choices)):
        t0 = time.time()
        new_dp = {}
        backptr = {}
        # iterate existing states
        for state_int, cost_so_far in dp.items():
            # try every choice
            for choice_idx, (maj_codes, need_tuple, delta_int, f_j) in enumerate(choices):
                # feasibility check: for each idx with need > 0, check digit >= need
                feasible = True
                for idx_i, need_val in enumerate(need_tuple):
                    if need_val:
                        digit = extract_digit(state_int, idx_i)
                        if digit < need_val:
                            feasible = False
                            break
                if not feasible:
                    continue
                # new state integer = state_int - delta_int  (safe because feasible)
                new_state_int = state_int - delta_int
                new_cost = cost_so_far + f_j
                # dominance: keep best cost per state
                prev = new_dp.get(new_state_int)
                if prev is None or new_cost < prev:
                    new_dp[new_state_int] = new_cost
                    backptr[new_state_int] = (state_int, choice_idx)
        if not new_dp:
            # no feasible assignment at this level
            print(f"No factible al procesar estudiante {level} (original idx {order[level]}). Termino.")
            return {e.codigo: [] for e in estudiantes}, 1.0

        # Apply beam / poda si es necesario
        if beam_width and len(new_dp) > beam_width:
            # keep beam_width states with smallest cost
            # Using heap to be efficient
            heap = [(-cost, st) for st, cost in new_dp.items()]  # negative for max-heap
            heapq.heapify(heap)
            # reduce heap to beam_width
            while len(heap) > beam_width:
                heapq.heappop(heap)
            # build new limited dict
            limited_states = {st: -negcost for (negcost, st) in [(c, s) for c,s in [(item[0], item[1]) for item in heap]]}
            # But above reconstruction is messy; simpler:
            best = heapq.nsmallest(beam_width, new_dp.items(), key=lambda x: x[1])
            new_dp = dict(best)
            backptr = {st: backptr[st] for st, _ in best}

        # safety hard limit
        if len(new_dp) > max_states:
            # keep top max_states
            best = sorted(new_dp.items(), key=lambda x: x[1])[:max_states]
            new_dp = dict(best)
            backptr = {st: backptr[st] for st, _ in best}

        dp = new_dp
        back.append(backptr)
        t1 = time.time()
        # progreso
        print(f"Nivel {level+1}/{r} (estudiante {est.codigo}): estados={len(dp)} time={t1-t0:.3f}s")

    # ----------------------------------------------------------
    # Encontrar mejor estado final y reconstruir solución
    # ----------------------------------------------------------
    best_final_state, best_cost = min(dp.items(), key=lambda kv: kv[1])
    total_insat = best_cost
    F_prom = total_insat / r

    # backtracking: reconstruct assignments in 'ordered' space
    assignments_ordered = [None] * r
    cur_state = best_final_state
    for level in range(r-1, -1, -1):
        prev_state, choice_idx = back[level][cur_state]
        maj_codes, need_tuple, delta_int, f_j = ordered_choices[level][choice_idx]
        assignments_ordered[level] = maj_codes[:]  # list of assigned course codes
        cur_state = prev_state

    # restore to original student order
    assignments = {}
    for pos, student_idx in enumerate(order):
        assignments[estudiantes[student_idx].codigo] = assignments_ordered[pos]

    elapsed = time.time() - start_time
    print(f"\nCompletado en {elapsed:.3f}s. Insatisfacción total={total_insat:.6f} F_prom={F_prom:.6f}")
    return assignments, F_prom