import tkinter as tk
import random
import matplotlib.pyplot as plt
from Empleado import empleados

class AG:
    def __init__(self, dias_trabajo, areas, empleados_turno, generaciones, poblacion_max, poblacion_ini, pm, pc):
        self.dias_trabajo = dias_trabajo
        self.areas = areas
        self.empleados_turno = empleados_turno
        self.generaciones = generaciones
        self.poblacion_max = poblacion_max
        self.poblacion_ini = poblacion_ini
        self.pm = pm
        self.pc = pc

    def crear_individuo(self):
        if len(empleados) < self.empleados_turno * len(self.areas):
            raise ValueError("No hay suficientes empleados para cubrir las áreas en un turno.")
        
        semana = []
        for dia in range(1, 8):
            dia_schedule = {'dia': dia, 'turnos': {}}
            empleados_disponibles = empleados.copy()
            for turno in [1, 2]:
                turno_schedule = {}
                random.shuffle(empleados_disponibles)
                empleados_asignados = empleados_disponibles[:self.empleados_turno]
                empleados_disponibles = empleados_disponibles[self.empleados_turno:]
                
                empleados_por_area = self.empleados_turno // len(self.areas)
                inicio = 0
                for area in self.areas:
                    turno_schedule[area] = empleados_asignados[inicio:inicio + empleados_por_area]
                    inicio += empleados_por_area
                
                dia_schedule['turnos'][turno] = turno_schedule
            semana.append(dia_schedule)
        return semana

    def crear_poblacion_inicial(self):
        return [self.crear_individuo() for _ in range(self.poblacion_ini)]

    def calcular_fitness(self, individuo):
        empleados_dias_trabajados = {emp['id']: 0 for emp in empleados}
        bh = 0
        jk = 0

        for dia in individuo:
            empleados_vistos = set()
            for turno in dia['turnos'].values():
                for area, empleados_en_area in turno.items():
                    if len(empleados_en_area) == 0:
                        bh += 1
                    for emp in empleados_en_area:
                        emp_id = emp['id']
                        if emp_id in empleados_vistos:
                            jk += 1
                        empleados_vistos.add(emp_id)
                        empleados_dias_trabajados[emp_id] += 1

        bs = sum(1 for emp_dias in empleados_dias_trabajados.values() if emp_dias != self.dias_trabajo)

        total = 0.3 * bs + 0.4 * bh + 0.8 * jk
        fitness = 1 / (1 + total)
        return fitness

    def evaluar_poblacion(self, poblacion):
        fitness_scores = [self.calcular_fitness(individuo) for individuo in poblacion]
        mejor_fitness = max(fitness_scores)
        peor_fitness = min(fitness_scores)
        promedio_fitness = sum(fitness_scores) / len(fitness_scores)
        return mejor_fitness, peor_fitness, promedio_fitness

    def realizar_cruza(self, padre1, padre2):
        if random.random() < self.pc:
            punto_cruza = random.randint(1, len(padre1) - 1)
            hijo1 = padre1[:punto_cruza] + padre2[punto_cruza:]
            hijo2 = padre2[:punto_cruza] + padre1[punto_cruza:]
            return hijo1, hijo2
        return padre1, padre2

    def seleccionar_para_cruza(self, poblacion):
        seleccionados = [individuo for individuo in poblacion if random.random() < self.pc]
        random.shuffle(seleccionados)
        hijos = []
        for i in range(0, len(seleccionados) - 1, 2):
            nuevos_hijos = self.realizar_cruza(seleccionados[i], seleccionados[i + 1])
            hijos.extend(nuevos_hijos)
        return hijos

    def mutar(self, individuo):
        if random.random() < self.pm:
            dia_mutar = random.choice(individuo)
            turno_mutar = random.choice(list(dia_mutar['turnos'].keys()))
            area_mutar = random.choice(list(dia_mutar['turnos'][turno_mutar].keys()))

            if len(dia_mutar['turnos'][turno_mutar][area_mutar]) > 1:
                emp1, emp2 = random.sample(range(len(dia_mutar['turnos'][turno_mutar][area_mutar])), 2)
                dia_mutar['turnos'][turno_mutar][area_mutar][emp1], dia_mutar['turnos'][turno_mutar][area_mutar][emp2] = \
                    dia_mutar['turnos'][turno_mutar][area_mutar][emp2], dia_mutar['turnos'][turno_mutar][area_mutar][emp1]

    def aplicar_mutacion(self, poblacion):
        for individuo in poblacion:
            self.mutar(individuo)

    def poda(self, poblacion):
        unique_poblacion = {str(ind): ind for ind in poblacion}.values()
        sorted_poblacion = sorted(unique_poblacion, key=lambda x: self.calcular_fitness(x), reverse=True)
        return sorted_poblacion[:self.poblacion_max]

    def ejecutar_algoritmo(self):
        poblacion = self.crear_poblacion_inicial()
        estadisticas = {'mejor': [], 'peor': [], 'promedio': []}

        for _ in range(self.generaciones):
            poblacion = self.poda(poblacion)
            hijos = self.seleccionar_para_cruza(poblacion)
            self.aplicar_mutacion(hijos)
            
            poblacion.extend(hijos)
            
            mejor, peor, promedio = self.evaluar_poblacion(poblacion)
            estadisticas['mejor'].append(mejor)
            estadisticas['peor'].append(peor)
            estadisticas['promedio'].append(promedio)

        plt.figure(figsize=(10, 5))
        plt.plot(estadisticas['mejor'], label='Mejor Fitness')
        plt.plot(estadisticas['peor'], label='Peor Fitness')
        plt.plot(estadisticas['promedio'], label='Promedio Fitness')
        plt.xlabel('Generación')
        plt.ylabel('Fitness')
        plt.title('Evolución del Algoritmo Genético')
        plt.legend()
        plt.show()       
        return poblacion[0]

    def mostrar_mejor_individuo(self, mejor_individuo):
        root = tk.Tk()
        root.title("Mejor Horario")
        for dia in mejor_individuo:
            frame_dia = tk.Frame(root, borderwidth=2, relief="solid")
            frame_dia.pack(side="left", expand=True, fill="both")
            tk.Label(frame_dia, text=f"Día {dia['dia']}").pack()

            for turno_id, turno in dia['turnos'].items():
                turno_nombre = "Mañana" if turno_id == 1 else "Tarde"
                frame_turno = tk.Frame(frame_dia, borderwidth=2, relief="solid")
                frame_turno.pack(expand=True, fill="both")
                tk.Label(frame_turno, text=turno_nombre).pack()

                for area, empleados in turno.items():
                    frame_area = tk.Frame(frame_turno, borderwidth=1, relief="solid")
                    frame_area.pack(expand=True, fill="both")
                    tk.Label(frame_area, text=f"Área {area}").pack()

                    for emp in empleados:
                        tk.Label(frame_area, text=f"ID {emp['id']}x").pack()

        root.mainloop()
