import random

def generar_poblacion_inicial(total_empleados, dias_laborales):
    # Calculamos el número de turnos en una semana (mañana y tarde)
    turnos_semana = 10 * dias_laborales
    
    # Calculamos el número de empleados por turno
    empleados_por_turno = total_empleados * dias_laborales // turnos_semana
    
    # Definimos el rango para el número de empleados por gen
    min_empleados_por_gen = empleados_por_turno // 2
    max_empleados_por_gen = empleados_por_turno * 2
    
    # Lista para almacenar la población inicial
    poblacion = []
    
    # Generamos cromosomas aleatorios para la población inicial
    for _ in range(10):  # Podríamos ajustar el tamaño de la población según sea necesario
        cromosoma = {i: [] for i in range(1, 11)}  # Diccionario para evitar duplicados de genes
        for turno in range(1, 11):  # Generar turnos del 1 al 10
            for _ in range(dias_laborales):  # Repetir para cada día laboral
                # Generamos un número aleatorio de empleados para este gen
                num_empleados = random.randint(min_empleados_por_gen, max_empleados_por_gen)
                # Creamos una tupla con el número de empleados y el área de trabajo
                empleado_area = (num_empleados, random.choice(['Cocina', 'Mesero', 'Limpieza']))
                # Añadimos el gen (turno y datos de empleados) a nuestro cromosoma
                cromosoma[turno].append(empleado_area)
        poblacion.append(cromosoma)
    
    return poblacion

# Ejemplo de uso
total_empleados = 30  # Total de empleados en la empresa
dias_laborales = 4    # Número de días laborales en la semana
poblacion_inicial = generar_poblacion_inicial(total_empleados, dias_laborales)
for cromosoma in poblacion_inicial:
    print(cromosoma)
    
def calcular_aptitud(cromosoma):
    # Diccionario para mapear los turnos a los días de la semana
    dias_por_turno = {
        1: 'Lunes',
        2: 'Martes',
        3: 'Miércoles',
        4: 'Jueves',
        5: 'Viernes',
        6: 'Lunes',
        7: 'Martes',
        8: 'Miércoles',
        9: 'Jueves',
        10: 'Viernes'
    }
    
    # Inicializamos contadores para las penalizaciones
    penalizacion_bs = 0  # Penalización por no cumplir los 4 días de trabajo
    penalizacion_bh = 0  # Penalización por no tener al menos 1 empleado por área
    penalizacion_jk = 0  # Penalización por tener un empleado en diferentes turnos para el mismo día
    
    # Listas para mantener registro del mejor y peor individuo por generación
    mejores_individuos = []
    peores_individuos = []
    
    # Calculamos la aptitud para cada cromosoma
    for turno, empleados_areas in cromosoma.items():
        # Diccionario para mantener un registro de los empleados por área y turno
        empleados_por_area = {'Cocina': 0, 'Mesero': 0, 'Limpieza': 0}
        
        # Listas para verificar los días trabajados y los turnos asignados en cada día
        dias_trabajados = []
        turnos_por_dia = {dia: [] for dia in dias_por_turno.values()}
        
        # Evaluamos cada gen en el cromosoma
        for num_empleados, area in empleados_areas:
            # Verificamos la penalización por tener un empleado en diferentes turnos para el mismo día
            dia = dias_por_turno[turno]
            if turno in turnos_por_dia[dia]:
                penalizacion_jk += 1
            
            # Actualizamos la lista de turnos para el día actual
            turnos_por_dia[dia].append(turno)
            
            # Verificamos si el día ya ha sido trabajado
            if dia not in dias_trabajados:
                dias_trabajados.append(dia)
            
            # Actualizamos el contador de empleados por área
            empleados_por_area[area] += num_empleados
        
        # Verificamos si se cumplen los 4 días de trabajo
        if len(dias_trabajados) < 4:
            penalizacion_bs += 1
        
        # Verificamos si hay al menos 1 empleado por área por turno
        if 0 in empleados_por_area.values():
            penalizacion_bh += 1
        
        # Guardamos el individuo actual para llevar registro del mejor y peor individuo
        mejores_individuos.append(penalizacion_bs + penalizacion_bh + penalizacion_jk)
        peores_individuos.append(penalizacion_bs + penalizacion_bh + penalizacion_jk)
    
    # Calculamos el promedio de aptitud por generación
    promedio_individuos = sum(mejores_individuos) / len(mejores_individuos)
    
    # Calculamos la aptitud total (penalización)
    aptitud = 1 / (1 + (0.3 * penalizacion_bs + 0.4 * penalizacion_bh + 0.8 * penalizacion_jk))
    
    return aptitud, max(mejores_individuos), min(peores_individuos), promedio_individuos, cromosoma

def calcular_aptitud_poblacion(poblacion):
    aptitudes = []
    for cromosoma in poblacion:
        aptitud, _, _, _, _ = calcular_aptitud(cromosoma)  # Asume que calcular_aptitud devuelve la aptitud y otros valores
        aptitudes.append((aptitud, cromosoma))
    
    # Ordenamos los cromosomas por su aptitud, donde una menor aptitud es mejor
    aptitudes.sort(key=lambda x: x[0])

    # El mejor individuo es el de menor aptitud y el peor el de mayor aptitud
    mejor_individuo = aptitudes[0]
    peor_individuo = aptitudes[-1]

    # Calculamos el promedio de aptitud por generación
    promedio_global = sum(aptitud for aptitud, _ in aptitudes) / len(aptitudes)

    return mejor_individuo, peor_individuo, promedio_global

def cruza_y_mutacion(poblacion, pc, pm):
    padres_para_cruza = [individuo for individuo in poblacion if random.random() < pc]
    random.shuffle(padres_para_cruza)  # Mezclamos para formar parejas al azar
    hijos = []

    for i in range(0, len(padres_para_cruza) - 1, 2):
        padre1, padre2 = padres_para_cruza[i], padres_para_cruza[i + 1]
        punto_de_cruza = random.randint(1, len(padre1) - 2)  # Punto al azar, evitando los extremos

        hijo1 = {}
        hijo2 = {}

        for turno in padre1:
            if turno < punto_de_cruza:
                hijo1[turno] = padre1[turno]
                hijo2[turno] = padre2[turno]
            else:
                hijo1[turno] = padre2[turno]
                hijo2[turno] = padre1[turno]

        hijos += [hijo1, hijo2]

    # Mutación
    for hijo in hijos:
        if random.random() < pm:
            puntos_de_mutacion = random.sample(list(hijo.keys()), 2)
            hijo[puntos_de_mutacion[0]], hijo[puntos_de_mutacion[1]] = hijo[puntos_de_mutacion[1]], hijo[puntos_de_mutacion[0]]

    poblacion.extend(hijos)
    return poblacion

def eliminar_duplicados(poblacion):
    poblacion_unicos = []
    for individuo in poblacion:
        if individuo not in poblacion_unicos:
            poblacion_unicos.append(individuo)
    return poblacion_unicos

def calcular_aptitud(cromosoma):
    # Diccionario para mapear los turnos a los días de la semana
    dias_por_turno = {
        1: 'Lunes',
        2: 'Martes',
        3: 'Miércoles',
        4: 'Jueves',
        5: 'Viernes',
        6: 'Lunes',
        7: 'Martes',
        8: 'Miércoles',
        9: 'Jueves',
        10: 'Viernes'
    }
    
    # Inicializamos contadores para las penalizaciones
    penalizacion_bs = 0  # Penalización por no cumplir los 4 días de trabajo
    penalizacion_bh = 0  # Penalización por no tener al menos 1 empleado por área
    penalizacion_jk = 0  # Penalización por tener un empleado en diferentes turnos para el mismo día
    
    # Listas para mantener registro del mejor y peor individuo por generación
    mejores_individuos = []
    peores_individuos = []
    
    # Calculamos la aptitud para cada cromosoma
    for turno, empleados_areas in cromosoma.items():
        # Diccionario para mantener un registro de los empleados por área y turno
        empleados_por_area = {'Cocina': 0, 'Mesero': 0, 'Limpieza': 0}
        
        # Listas para verificar los días trabajados y los turnos asignados en cada día
        dias_trabajados = []
        turnos_por_dia = {dia: [] for dia in dias_por_turno.values()}
        
        # Evaluamos cada gen en el cromosoma
        for num_empleados, area in empleados_areas:
            # Verificamos la penalización por tener un empleado en diferentes turnos para el mismo día
            dia = dias_por_turno[turno]
            if turno in turnos_por_dia[dia]:
                penalizacion_jk += 1
            
            # Actualizamos la lista de turnos para el día actual
            turnos_por_dia[dia].append(turno)
            
            # Verificamos si el día ya ha sido trabajado
            if dia not in dias_trabajados:
                dias_trabajados.append(dia)
            
            # Actualizamos el contador de empleados por área
            empleados_por_area[area] += num_empleados
        
        # Verificamos si se cumplen los 4 días de trabajo
        if len(dias_trabajados) < 4:
            penalizacion_bs += 1
        
        # Verificamos si hay al menos 1 empleado por área por turno
        if 0 in empleados_por_area.values():
            penalizacion_bh += 1
        
        # Guardamos el individuo actual para llevar registro del mejor y peor individuo
        mejores_individuos.append(penalizacion_bs + penalizacion_bh + penalizacion_jk)
        peores_individuos.append(penalizacion_bs + penalizacion_bh + penalizacion_jk)
    
    # Calculamos el promedio de aptitud por generación
    promedio_individuos = sum(mejores_individuos) / len(mejores_individuos)
    
    # Calculamos la aptitud total (penalización)
    aptitud = 1 / (1 + (0.3 * penalizacion_bs + 0.4 * penalizacion_bh + 0.8 * penalizacion_jk))
    
    return aptitud, max(mejores_individuos), min(peores_individuos), promedio_individuos, cromosoma

def calcular_aptitud_poblacion(poblacion):
    aptitudes = []
    for cromosoma in poblacion:
        aptitud, _, _, _, _ = calcular_aptitud(cromosoma)  # Asume que calcular_aptitud devuelve la aptitud y otros valores
        aptitudes.append((aptitud, cromosoma))
    
    # Ordenamos los cromosomas por su aptitud, donde una menor aptitud es mejor
    aptitudes.sort(key=lambda x: x[0])

    # El mejor individuo es el de menor aptitud y el peor el de mayor aptitud
    mejor_individuo = aptitudes[0]
    peor_individuo = aptitudes[-1]

    # Calculamos el promedio de aptitud por generación
    promedio_global = sum(aptitud for aptitud, _ in aptitudes) / len(aptitudes)

    return mejor_individuo, peor_individuo, promedio_global


def poda(poblacion):
    # Eliminar duplicados
    poblacion = eliminar_duplicados(poblacion)
    
    # Calcular aptitud para cada individuo y ordenar
    poblacion_con_aptitud = [(individuo, calcular_aptitud_poblacion(individuo)) for individuo in poblacion]
    poblacion_ordenada = sorted(poblacion_con_aptitud, key=lambda x: x[1])
    
    # Conservar solo los mejores 100 individuos
    poblacion_final = [individuo for individuo, aptitud in poblacion_ordenada[:100]]
    
    return poblacion_final

import random

# Asumimos que las funciones generar_poblacion_inicial, calcular_aptitud,
# cruza_y_mutacion, y eliminar_duplicados ya están definidas correctamente.

def seleccion_natural(poblacion, capacidad_poblacional):
    # Ordenamos la población por su aptitud (asumiendo que ya se calculó)
    poblacion.sort(key=lambda individuo: calcular_aptitud(individuo)[0])
    # Mantenemos solo los N mejores individuos según la capacidad poblacional
    return poblacion[:capacidad_poblacional]

def ejecutar_algoritmo_genetico(generaciones=100):
    # Inicializamos la población
    poblacion = generar_poblacion_inicial(total_empleados=30, dias_laborales=4)
    capacidad_poblacional = 10
    pc = 0.5  # Probabilidad de cruza
    pm = 0.1  # Probabilidad de mutación

    for _ in range(generaciones):
        # Aplicamos cruza y mutación
        poblacion = cruza_y_mutacion(poblacion, pc, pm)
        # Eliminamos duplicados para mantener diversidad
        poblacion = eliminar_duplicados(poblacion)
        # Aplicamos selección natural para limitar la población a la capacidad poblacional
        poblacion = seleccion_natural(poblacion, capacidad_poblacional)

    # Calculamos las métricas finales de la población final
    aptitudes = [calcular_aptitud_poblacion(poblacion)]
    print(aptitudes)

# Ejemplo de uso
ejecutar_algoritmo_genetico()
