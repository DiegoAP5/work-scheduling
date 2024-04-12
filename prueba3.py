import random

# Parámetros
total_empleados = 20  # Ejemplo: 20 empleados en total
dias_laborales = 4
turnos = 10  # 5 turnos de mañana y 5 turnos de tarde
areas_de_trabajo = ['Cocina', 'Mesero', 'Limpieza']

# Calcula el número de empleados por turno
n = (total_empleados * dias_laborales) // turnos

def generar_cromosoma():
    cromosoma = {}
    for turno in range(1, turnos + 1):
        # Asignar aleatoriamente el área de trabajo y generar un ID único para cada empleado en el turno
        cromosoma[turno] = [(random.randint(1, total_empleados), random.choice(areas_de_trabajo)) for _ in range(n)]
    return cromosoma

def generar_poblacion_inicial(tamaño_poblacion):
    return [generar_cromosoma() for _ in range(tamaño_poblacion)]

def calcular_aptitud(cromosoma):
    # Inicializar conteos de penalización
    penalizaciones_bs = 0
    penalizaciones_bh = 0
    penalizaciones_jk = 0
    
    # Diccionario para rastrear los turnos trabajados por cada empleado
    turnos_por_empleado = {}
    
    # Verificar cumplimiento de al menos 1 empleado por área en cada turno
    empleados_por_turno_y_area = {turno: {'Cocina': 0, 'Mesero': 0, 'Limpieza': 0} for turno in range(1, 11)}
    
    for turno, empleados in cromosoma.items():
        dias_trabajados = set() # Para BH
        for empleado_id, area in empleados:
            # Añadir turno trabajado
            if empleado_id not in turnos_por_empleado:
                turnos_por_empleado[empleado_id] = []
            turnos_por_empleado[empleado_id].append(turno)
            
            # Contar empleados por área en cada turno
            empleados_por_turno_y_area[turno][area] += 1

    # Verificar BH: Al menos 1 empleado en cada área por turno
    for turno, areas in empleados_por_turno_y_area.items():
        for area, count in areas.items():
            if count == 0:
                penalizaciones_bh += 1
    
    # Verificar BS y JK
    for empleado, turnos in turnos_por_empleado.items():
        dias_trabajados = set((t - 1) // 5 for t in turnos)  # Mapear turnos a días
        if len(dias_trabajados) < 4:
            penalizaciones_bs += 1
        if len(turnos) > len(set(turnos)):
            penalizaciones_jk += 1
    
    # Calcular puntaje de aptitud basado en las penalizaciones
    fitness_score = 1 / (1 + ((0.8 * penalizaciones_bs) + (0.8 * penalizaciones_bh) + (0.8 * penalizaciones_jk)))
    return fitness_score

def cruza(cromosoma1, cromosoma2):
    punto_cruza = random.randint(1, len(cromosoma1)-1)  # Elegir un punto al azar para cruzar
    hijo1 = dict(list(cromosoma1.items())[:punto_cruza] + list(cromosoma2.items())[punto_cruza:])
    hijo2 = dict(list(cromosoma2.items())[:punto_cruza] + list(cromosoma1.items())[punto_cruza:])
    return hijo1, hijo2

def seleccion_para_cruza(poblacion, pc):
    padres = []
    hijos = []
    for cromosoma in poblacion:
        if random.random() < pc:
            padres.append(cromosoma)
    random.shuffle(padres)
    for i in range(0, len(padres) - 1, 2):
        hijos.extend(cruza(padres[i], padres[i+1]))
    return hijos

def mutacion(hijo, pm, total_empleados):
    if random.random() < pm:
        turno_a_mutar = random.choice(list(hijo.keys()))
        idx_empleado_a_mutar = random.randint(0, len(hijo[turno_a_mutar]) - 1)

        # Generar un nuevo empleado evitando duplicados y manteniendo el rango
        empleado_valido = False
        intentos = 0
        while not empleado_valido and intentos < 50:
            nuevo_id = random.randint(1, total_empleados)
            empleado_valido = all(nuevo_id != emp[0] for emp in hijo[turno_a_mutar])
            intentos += 1

        if empleado_valido:
            # Selecciona un área al azar para simplificar, se podría manejar de otra manera más específica
            areas = ['Cocina', 'Mesero', 'Limpieza']
            nuevo_area = random.choice(areas)
            hijo[turno_a_mutar][idx_empleado_a_mutar] = (nuevo_id, nuevo_area)
        else:
            print("No se encontró un ID de empleado válido después de varios intentos.")

    return hijo

def poda(poblacion, max_poblacion=100):
    # Eliminar duplicados y ordenar por fitness
    poblacion_unicos = {tuple(sorted([(k, tuple(v)) for k, v in cromo.items()])): cromo for cromo in poblacion}
    poblacion = list(poblacion_unicos.values())
    poblacion.sort(key=lambda x: calcular_aptitud(x), reverse=True)
    return poblacion[:max_poblacion]

def ejecutar_generaciones(poblacion_inicial, pc, pm, generaciones, total_empleados):
    historial_mejor_aptitud = []
    historial_promedio_aptitud = []
    historial_peor_aptitud = []

    poblacion = poblacion_inicial

    for _ in range(generaciones):
        # Selección y cruce
        hijos = seleccion_para_cruza(poblacion, pc)
        # Mutación
        poblacion = poblacion + [mutacion(hijo, pm, total_empleados) for hijo in hijos]
        # Poda para eliminar duplicados y mantener los mejores
        poblacion = poda(poblacion, 100)  # Asumiendo una función 'poda' que maneja el tamaño de la población

        # Evaluar aptitudes para estadísticas
        aptitudes = [calcular_aptitud(individuo) for individuo in poblacion]
        mejor_aptitud = min(aptitudes)
        peor_aptitud = max(aptitudes)
        promedio_aptitud = sum(aptitudes) / len(aptitudes)

        historial_mejor_aptitud.append(mejor_aptitud)
        historial_promedio_aptitud.append(promedio_aptitud)
        historial_peor_aptitud.append(peor_aptitud)

    # Encontrar el mejor individuo al final de todas las generaciones
    mejor_individuo = poblacion[aptitudes.index(min(aptitudes))]

    return mejor_individuo, historial_mejor_aptitud, historial_promedio_aptitud, historial_peor_aptitud

# Configuración inicial
total_empleados = 20
poblacion_inicial = generar_poblacion_inicial(total_empleados)  # Asumiendo una función que genera la población inicial
pc = 0.7  # Probabilidad de cruce
pm = 0.1  # Probabilidad de mutación
generaciones = 1000  

# Ejecutar las generaciones
mejor_individuo, historial_mejor, historial_promedio, historial_peor = ejecutar_generaciones(poblacion_inicial, pc, pm, generaciones, total_empleados)

# Mostrar el mejor individuo y los historiales

print("Historial de la mejor aptitud:", historial_mejor)
print("Historial de la aptitud promedio:", historial_promedio)
print("Historial de la peor aptitud:", historial_peor)
print("Mejor individuo:", mejor_individuo)