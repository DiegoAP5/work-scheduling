import random
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

def calcular_empleados_por_turno():
    return (TOTAL_EMPLEADOS * DIAS_LABORALES) // TURNOS

def generar_cromosoma():
    cromosoma = {}
    for turno in range(1, TURNOS + 1):
        cromosoma[turno] = []
        for _ in range(N_EMPLEADOS_POR_TURNO):
            area = random.choice(AREAS)
            id_empleado = random.randint(1, TOTAL_EMPLEADOS)
            cromosoma[turno].append((id_empleado, area))
    return cromosoma

def generar_poblacion_inicial(tamano_poblacion):
    return [generar_cromosoma() for _ in range(tamano_poblacion)]


def calcular_fitness(cromosoma):
    empleado_dias = {emp_id: set() for emp_id in range(1, TOTAL_EMPLEADOS + 1)}
    penalizacion_bs = 0
    penalizacion_bh = 0
    penalizacion_jk = 0

    for turno, asignaciones in cromosoma.items():
        empleados_turno = set()
        areas_turno = {area: 0 for area in AREAS}
        
        for empleado_id, area in asignaciones:
            empleados_turno.add(empleado_id)
            areas_turno[area] += 1
            dia = (turno - 1) % 5 + 1
            if empleado_id in empleado_dias[dia]:
                penalizacion_jk += 1
            empleado_dias[dia].add(empleado_id)

        if any(cant == 0 for cant in areas_turno.values()):
            penalizacion_bh += 1

    for dias in empleado_dias.values():
        if len(dias) != 4:
            penalizacion_bs += 1

    fitness = 1 / (1 + (0.3 * penalizacion_bs + 0.4 * penalizacion_bh + 0.8 * penalizacion_jk))
    return fitness

def evaluar_poblacion(poblacion):
    fitness_scores = [calcular_fitness(cromosoma) for cromosoma in poblacion]
    mejor_fitness = max(fitness_scores)
    peor_fitness = min(fitness_scores)
    promedio_fitness = sum(fitness_scores) / len(fitness_scores)
    return mejor_fitness, peor_fitness, promedio_fitness

def seleccionar_para_cruza(poblacion, pc):
    padres = []
    for individuo in poblacion:
        if random.random() < pc:
            padres.append(individuo)
    return padres

def realizar_cruza(padres, pc):
    random.shuffle(padres)
    hijos = []

    if random.random() < pc:
        for i in range(0, len(padres) - 1, 2):
            punto_cruza = random.randint(1, len(padres[i]) - 1)
            hijo1 = dict(list(padres[i].items())[:punto_cruza] + list(padres[i+1].items())[punto_cruza:])
            hijo2 = dict(list(padres[i+1].items())[:punto_cruza] + list(padres[i].items())[punto_cruza:])
            hijos.append(hijo1)
            hijos.append(hijo2)
    return hijos

def mutacion(hijos, pm):
    for hijo in hijos:
        if random.random() < pm:
            gene1, gene2 = random.sample(list(hijo.keys()), 2)
            hijo[gene1], hijo[gene2] = hijo[gene2], hijo[gene1]
    return hijos

def poda_poblacion(poblacion, max_poblacion=100):
    if len(poblacion) > max_poblacion:
        poblacion.sort(key=lambda x: calcular_fitness(x), reverse=True)
        poblacion = poblacion[:max_poblacion]
    return poblacion

def algoritmo_genetico(tamano_poblacion, pc, pm, numero_generaciones):
    poblacion = generar_poblacion_inicial(tamano_poblacion)
    mejores_fitness = []
    peores_fitness = []
    promedios_fitness = []
    
    for generacion in range(numero_generaciones):
        mejor_fitness, peor_fitness, promedio_fitness = evaluar_poblacion(poblacion)
        mejores_fitness.append(mejor_fitness)
        peores_fitness.append(peor_fitness)
        promedios_fitness.append(promedio_fitness)
        
        padres = seleccionar_para_cruza(poblacion, pc)
        hijos = realizar_cruza(padres, pc)
        hijos_mutados = mutacion(hijos, pm)
        
        poblacion.extend(hijos_mutados)
        poblacion = poda_poblacion(poblacion)
        print(f"Generación {generacion + 1}: Mejor = {mejor_fitness}, Peor = {peor_fitness}, Promedio = {promedio_fitness}")
    
    plt.figure(figsize=(10, 5))
    plt.plot(mejores_fitness, label='Mejor Fitness')
    plt.plot(peores_fitness, label='Peor Fitness')
    plt.plot(promedios_fitness, label='Promedio Fitness')
    plt.title('Evolución del Fitness por Generación')
    plt.xlabel('Generación')
    plt.ylabel('Fitness')
    plt.legend()
    plt.grid(True)
    plt.show()

    mostrar_mejor_individuo(poblacion)

def mostrar_mejor_individuo(poblacion):
    mejor_individuo = max(poblacion, key=calcular_fitness)
    window = tk.Tk()
    window.title("Mejor Individuo")

    headers = ["Turno", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    for i, header in enumerate(headers):
        ttk.Label(window, text=header).grid(row=0, column=i, sticky='ew')

    turnos = ["Mañana", "Tarde"]
    for i, turno in enumerate(turnos, 1):
        ttk.Label(window, text=turno).grid(row=i, column=0, sticky='ew')
        for j in range(1, 8):
            turno_index = (i - 1) * 5 + j
            asignaciones = mejor_individuo[turno_index]
            asignaciones_str = '\n'.join(f"ID:{emp_id} Área:{area}" for emp_id, area in asignaciones)
            ttk.Label(window, text=asignaciones_str).grid(row=i, column=j, sticky='ew')

    for i in range(6):
        window.grid_columnconfigure(i, weight=1)
    window.grid_rowconfigure(0, weight=1)
    for i in range(1, len(turnos) + 1):
        window.grid_rowconfigure(i, weight=1)

    window.mainloop()
    

TOTAL_EMPLEADOS = 20
DIAS_LABORALES = 4
TURNOS = 14
AREAS = ['Cocina', 'Mesero', 'Limpieza']
pm = 0.9
pc = 0.8
numero_generaciones = 100
tamano_poblacion = 100
N_EMPLEADOS_POR_TURNO = calcular_empleados_por_turno()
algoritmo_genetico(tamano_poblacion, pc, pm, numero_generaciones)
