import random
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import os
import csv

class AG:
    def __init__(self, total_empleados, dias_laborales, areas, tamano_poblacion, poblacion_maxima, pc, pm, numero_generaciones):
        self.total_empleados = total_empleados
        self.dias_laborales = dias_laborales
        self.turnos = 14
        self.areas = areas
        self.tamano_poblacion = tamano_poblacion
        self.poblacion_maxima = poblacion_maxima
        self.pc = pc
        self.pm = pm
        self.numero_generaciones = numero_generaciones
        self.n_empleados_por_turno = self.calcular_empleados_por_turno()
        self.folder_path = 'images'            

    def calcular_empleados_por_turno(self):
        return (self.total_empleados * self.dias_laborales) // self.turnos

    def generar_cromosoma(self):
        cromosoma = {}
        for turno in range(1, self.turnos + 1):
            cromosoma[turno] = []
            for _ in range(self.n_empleados_por_turno):
                area = random.choice(self.areas)
                id_empleado = random.randint(1, self.total_empleados)
                cromosoma[turno].append((id_empleado, area))
        return cromosoma

    def generar_poblacion_inicial(self):
        return [self.generar_cromosoma() for _ in range(self.tamano_poblacion)]

    def fitness(self, cromosoma):
        empleado_dias = {emp_id: set() for emp_id in range(1, self.total_empleados + 1)}
        bs = 0
        bh = 0
        jk = 0

        for turno, asignaciones in cromosoma.items():
            empleados_turno = set()
            areas_turno = {area: 0 for area in self.areas}
            
            for empleado_id, area in asignaciones:
                empleados_turno.add(empleado_id)
                areas_turno[area] += 1
                dia = (turno - 1) % 7 + 1
                if empleado_id in empleado_dias[dia]:
                    jk += 1
                empleado_dias[dia].add(empleado_id)

            if any(cant == 0 for cant in areas_turno.values()):
                bh += 1

        for dias in empleado_dias.values():
            if len(dias) != 4:
                bs += 1

        fitness = 1 / (1 + (0.3 * bs + 0.4 * bh + 0.8 * jk))
        return fitness

    def evaluar_poblacion(self, poblacion):
        fitness_scores = [self.fitness(cromosoma) for cromosoma in poblacion]
        mejor_fitness = max(fitness_scores)
        peor_fitness = min(fitness_scores)
        promedio_fitness = sum(fitness_scores) / len(fitness_scores)
        return mejor_fitness, peor_fitness, promedio_fitness

    def seleccionar_para_cruza(self, poblacion):
        padres = []
        for individuo in poblacion:
            if random.random() < self.pc:
                padres.append(individuo)
        return padres

    def realizar_cruza(self, padres):
        random.shuffle(padres)
        hijos = []

        if len(padres) > 1 and random.random() < self.pc:
            for i in range(0, len(padres) - 1, 2):
                punto_cruza = random.randint(1, len(padres[i]) - 1)
                hijo1 = dict(list(padres[i].items())[:punto_cruza] + list(padres[i+1].items())[punto_cruza:])
                hijo2 = dict(list(padres[i+1].items())[:punto_cruza] + list(padres[i].items())[punto_cruza:])
                hijos.append(hijo1)
                hijos.append(hijo2)
        return hijos

    def mutacion(self, hijos):
        for hijo in hijos:
            if random.random() < self.pm:
                gene1, gene2 = random.sample(list(hijo.keys()), 2)
                hijo[gene1], hijo[gene2] = hijo[gene2], hijo[gene1]
        return hijos

    def poda(self, poblacion):
        poblacion.sort(key=lambda x: self.fitness(x), reverse=True)
        return poblacion[:self.poblacion_maxima]

    def algoritmo_genetico(self):
        poblacion = self.generar_poblacion_inicial()
        mejores_fitness = []
        peores_fitness = []
        promedios_fitness = []

        for generacion in range(self.numero_generaciones):
            mejor_fitness, peor_fitness, promedio_fitness = self.evaluar_poblacion(poblacion)
            mejores_fitness.append(mejor_fitness)
            peores_fitness.append(peor_fitness)
            promedios_fitness.append(promedio_fitness)
            
            padres = self.seleccionar_para_cruza(poblacion)
            hijos = self.realizar_cruza(padres)
            hijos_mutados = self.mutacion(hijos)
            
            poblacion.extend(hijos_mutados)
            poblacion = self.poda(poblacion)
            print(f"Generación {generacion + 1}: Mejor = {mejor_fitness}, Peor = {peor_fitness}, Promedio = {promedio_fitness}")

        self.mostrar_graficas(mejores_fitness,peores_fitness,promedios_fitness)
        self.mostrar_mejor_individuo(poblacion)
        self.guardar_poblacion(poblacion)
        
    def mostrar_graficas(self,mejores_fitness,peores_fitness,promedios_fitness):
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            
        plt.figure(figsize=(10, 5))
        plt.plot(mejores_fitness, label='Mejor Fitness')
        plt.plot(peores_fitness, label='Peor Fitness')
        plt.plot(promedios_fitness, label='Promedio Fitness')
        plt.title('Evolución del Fitness por Generación')
        plt.xlabel('Generación')
        plt.ylabel('Fitness')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(self.folder_path, 'evolucion.png'))
        plt.show()
        
    def mostrar_mejor_individuo(self, poblacion):
        mejor_individuo = max(poblacion, key=self.fitness)
        window = tk.Tk()
        window.title("Mejor Individuo")

        headers = ["Turno", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        for i, header in enumerate(headers):
            ttk.Label(window, text=header, relief="groove", borderwidth=2).grid(row=0, column=i, sticky='ewns')

        turnos = ["Mañana", "Tarde"]
        for i, turno in enumerate(turnos, 1):
            ttk.Label(window, text=turno, relief="groove", borderwidth=2).grid(row=i, column=0, sticky='ewns')
            for j in range(1, 8):
                turno_index = (i - 1) * 5 + j
                asignaciones = mejor_individuo.get(turno_index, [])
                asignaciones_str = '\n'.join(f"ID:{emp_id} Área:{area}" for emp_id, area in asignaciones)
                ttk.Label(window, text=asignaciones_str, relief="groove", borderwidth=2).grid(row=i, column=j, sticky='ewns')

        for i in range(8):
            window.grid_columnconfigure(i, weight=1)
            window.grid_rowconfigure(0, weight=1)
        for i in range(1, len(turnos) + 1):
            window.grid_rowconfigure(i, weight=1)
        window.mainloop()
        
    def guardar_poblacion(seff,poblacion, archivo='ultima_poblacion.csv'):
        with open(archivo, mode='w', newline='') as file:
            writer = csv.writer(file)
            headers = ['Cromosoma', 'Turno', 'Empleado ID', 'Area']
            writer.writerow(headers)
            
            for idx, cromosoma in enumerate(poblacion):
                for turno, asignaciones in cromosoma.items():
                    for empleado_id, area in asignaciones:
                        writer.writerow([idx + 1, turno, empleado_id, area])