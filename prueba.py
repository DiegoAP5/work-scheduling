import random
import pandas as pd

# Definir los parámetros del problema
total_empleados = 20  # Total de empleados disponibles
dias_laborales = 5    # Días laborales en la semana
num_turnos = 10       # Número total de turnos (mañana y tarde)
areas_trabajo = ['Cocina', 'Mesero', 'Limpieza']  # Áreas de trabajo

# Definir la clase Cromosoma
class Cromosoma:
    def __init__(self, genes):
        self.genes = genes  # Genes del cromosoma

    def __str__(self):
        return str(self.genes)

# Función para generar una población inicial de cromosomas aleatorios
def generar_poblacion_inicial(tam_poblacion):
    poblacion = []
    for _ in range(tam_poblacion):
        genes = []
        for _ in range(dias_laborales * num_turnos):
            # Generar un número aleatorio del 1 al 10 para representar el turno
            numero_turno = random.randint(1, num_turnos)
            # Seleccionar aleatoriamente un empleado y un área de trabajo
            empleado = random.randint(1, total_empleados)
            area_trabajo = random.choice(areas_trabajo)
            genes.append((numero_turno, empleado, area_trabajo))
        poblacion.append(Cromosoma(genes))
    return poblacion

# Función para realizar la cruza entre dos padres
def cruzar(padre1, padre2):
    punto_cruza = random.randint(1, len(padre1.genes) - 1)  # Seleccionar un punto de cruza aleatorio
    hijo1_genes = padre1.genes[:punto_cruza] + padre2.genes[punto_cruza:]
    hijo2_genes = padre2.genes[:punto_cruza] + padre1.genes[punto_cruza:]
    hijo1 = Cromosoma(hijo1_genes)
    hijo2 = Cromosoma(hijo2_genes)
    return hijo1, hijo2

# Función para realizar la mutación en un hijo
def mutar(hijo):
    if random.random() < probabilidad_mutacion:
        punto_mutacion1, punto_mutacion2 = random.sample(range(len(hijo.genes)), 2)  # Seleccionar dos puntos de mutación aleatorios
        hijo.genes[punto_mutacion1], hijo.genes[punto_mutacion2] = hijo.genes[punto_mutacion2], hijo.genes[punto_mutacion1]

# Función para calcular la aptitud de un cromosoma
def calcular_aptitud(cromosoma):
    penalizacion_bs = 0  # No cumplir los 5 días de trabajo
    penalizacion_bh = 0  # No tener al menos 1 empleado por área por turno
    penalizacion_jk = 0  # Tener un empleado en diferentes turnos para el mismo día
    empleados_por_dia = {day: {area: 0 for area in areas_trabajo} for day in range(dias_laborales)}

    for idx, turno in enumerate(cromosoma.genes):
        dia = idx // num_turnos
        num_turno, empleado, area_trabajo = turno
        empleados_por_dia[dia][area_trabajo] += 1
        if num_turno < 1 or num_turno > num_turnos:
            penalizacion_jk += 1

    for dia, empleados_por_area in empleados_por_dia.items():
        if sum(empleados_por_area.values()) != total_empleados:
            penalizacion_bs += 1

    for dia, empleados_por_area in empleados_por_dia.items():
        for area, num_empleados in empleados_por_area.items():
            if num_empleados == 0:
                penalizacion_bh += 1

    penalizacion_total = 1 / (1 + ((0.3 * penalizacion_bs) + (0.4 * penalizacion_bh) + (0.8 * penalizacion_jk)))
    
    return penalizacion_total, penalizacion_bs, penalizacion_bh, penalizacion_jk

# Función para eliminar individuos duplicados de la población
def podar_poblacion(poblacion):
    poblacion_unicos = []
    for cromosoma in poblacion:
        if cromosoma not in poblacion_unicos:
            poblacion_unicos.append(cromosoma)
    return poblacion_unicos

# Función para seleccionar los mejores individuos hasta alcanzar una población máxima
def seleccionar_mejores(poblacion, poblacion_maxima):
    poblacion_ordenada = sorted(poblacion, key=lambda x: calcular_aptitud(x)[0], reverse=True)
    return poblacion_ordenada[:poblacion_maxima]

# Parámetros del algoritmo genético
tam_poblacion = 100
generaciones = 100
probabilidad_cruza = 0.8
probabilidad_mutacion = 0.1

# Generar población inicial
poblacion = generar_poblacion_inicial(tam_poblacion)

# Ciclo de generaciones
for generacion in range(generaciones):
    # Selección y cruza de la población
    nueva_generacion = []
    for padre1 in poblacion:
        if random.random() < probabilidad_cruza:
            padre2 = random.choice(poblacion)
            hijo1, hijo2 = cruzar(padre1, padre2)
            mutar(hijo1)
            mutar(hijo2)
            nueva_generacion.append(hijo1)
            nueva_generacion.append(hijo2)
        else:
            nueva_generacion.append(padre1)
    
    poblacion = seleccionar_mejores(nueva_generacion, tam_poblacion)
    poblacion = podar_poblacion(poblacion)

import pandas as pd

import pandas as pd

# Función para obtener el nombre del día a partir de su índice
def obtener_nombre_dia(indice_dia):
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    return dias_semana[indice_dia]

# Crear un DataFrame para la población final
if poblacion:
    for dia in range(dias_laborales):
        print(f"Día: {obtener_nombre_dia(dia)}")
        cromosoma_dia = poblacion[dia]  # Obtener el cromosoma correspondiente al día
        for idx, gen in enumerate(cromosoma_dia.genes):
            empleado, puesto = gen
            print(f"Gen {idx + 1}: Empleado {empleado} ({puesto})")
        print()
else:
    print("La población está vacía.")
