import random
import numpy as np

# Definición de parámetros
NUM_EMPLEADOS = 20  # Número total de empleados
DIAS_TRABAJO = 4  # Número de días de trabajo por empleado
MAX_INDIVIDUOS = 100  # Tamaño máximo de la población
PROB_CRUZA = 0.8  # Probabilidad de cruza
PROB_MUTACION = 0.1  # Probabilidad de mutación
MAX_GENERACIONES = 100  # Número máximo de generaciones

# Definición de la población inicial
def generar_poblacion_inicial(num_individuos):
    poblacion = []
    for _ in range(num_individuos):
        individuo = np.random.randint(2, size=(10, NUM_EMPLEADOS))  # Matriz de 10x20
        poblacion.append(individuo)
    return poblacion

def calcular_fitness(individuo):
    # Restricción 1: El empleado no trabaja en más de un turno en el mismo día
    bs = np.sum(np.sum(individuo, axis=1) > 1)

    # Restricción 2: Hay al menos 1 cocinero
    bh = 0 if np.sum(individuo[:, :5]) > 0 else 1

    # Restricción 3: El empleado trabaja los 4 días especificados
    jk = sum(np.sum(individuo, axis=0) < DIAS_TRABAJO)

    return 1 / (1 + (0.3 * bs + 0.2 * bh + 0.8 * jk))

# Selección de padres por torneo
def seleccionar_padres(poblacion, fitness_poblacion):
    padres = []
    for _ in range(2):
        seleccionados = random.sample(list(zip(poblacion, fitness_poblacion)), k=5)
        seleccionados.sort(key=lambda x: x[1], reverse=True)
        padres.append(seleccionados[0][0])
    return padres

# Cruza de dos padres
def cruzar(padre1, padre2):
    punto_cruza = random.randint(1, 9)
    hijo1 = np.concatenate((padre1[:punto_cruza], padre2[punto_cruza:]), axis=0)
    hijo2 = np.concatenate((padre2[:punto_cruza], padre1[punto_cruza:]), axis=0)
    return hijo1, hijo2

# Mutación
def mutar(individuo):
    prob_mutacion = PROB_MUTACION
    for i in range(10):
        for j in range(NUM_EMPLEADOS):
            if random.random() < prob_mutacion:
                individuo[i, j] = 1 - individuo[i, j]  # Cambiar de 0 a 1 o viceversa
    return individuo

# Algoritmo genético principal
def algoritmo_genetico():
    poblacion = generar_poblacion_inicial(MAX_INDIVIDUOS)
    for generacion in range(MAX_GENERACIONES):
        fitness_poblacion = [calcular_fitness(individuo) for individuo in poblacion]

        # Selección de los mejores individuos
        poblacion_fitness = list(zip(poblacion, fitness_poblacion))
        poblacion_fitness.sort(key=lambda x: x[1], reverse=True)
        poblacion = [individuo for individuo, _ in poblacion_fitness[:MAX_INDIVIDUOS]]

        # Generación de nueva población mediante cruza y mutación
        nueva_poblacion = []
        while len(nueva_poblacion) < MAX_INDIVIDUOS:
            padre1, padre2 = seleccionar_padres(poblacion, fitness_poblacion)
            if random.random() < PROB_CRUZA:
                hijo1, hijo2 = cruzar(padre1, padre2)
                hijo1 = mutar(hijo1)
                hijo2 = mutar(hijo2)
                nueva_poblacion.append(hijo1)
                nueva_poblacion.append(hijo2)
        poblacion = nueva_poblacion

    # Seleccionar el mejor individuo de la última generación
    mejor_individuo = max(poblacion, key=calcular_fitness)
    return mejor_individuo

def mostrar_horario(individuo):
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    turnos = ['Mañana', 'Tarde']
    print('Horario:')
    for i in range(10):
        print(f'Turno {i+1}:')
        print('Día\tMañana\tTarde')
        for j, dia in enumerate(dias):
            print(f'{dia}\t', end='')
            for k, turno in enumerate(turnos):
                empleados = []
                for num_empleado, trabaja in enumerate(individuo[i]):
                    if trabaja and (k == 0 and j < 5 or k == 1 and j >= 5):
                        empleados.append(f'{num_empleado}({turno})')
                print(f'{", ".join(empleados) if empleados else "-"}', end='\t')
            print()

# Ejecución del algoritmo genético
mejor_horario = algoritmo_genetico()
print("Mejor horario generado:")
mostrar_horario(mejor_horario)
