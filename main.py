import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from algorithm import AG

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scheduler Genetic Algorithm")
        self.root.geometry("500x400")

        self.setup_widgets()

    def setup_widgets(self):
        inputs = [
            ("Empleados por turno", 1, 0),
            ("Días Laborales", 1, 1),
            ("Áreas (separadas por comas)", 1, 2),
            ("Población máxima", 1, 3),
            ("Población inicial", 1, 4),
            ("Probabilidad de Cruce (0.1 a 1.0)", 1, 5),
            ("Probabilidad de Mutación (0.1 a 1.0)", 1, 6),
            ("Número de Generaciones", 1, 7),
        ]

        self.entries = {}
        for label_text, column, row in inputs:
            label = ttk.Label(self.root, text=label_text)
            label.grid(row=row, column=column - 1, padx=10, pady=10, sticky=tk.E)
            entry = ttk.Entry(self.root)
            entry.grid(row=row, column=column, padx=10, pady=10, sticky=tk.W)
            self.entries[label_text] = entry
        
        run_button = ttk.Button(self.root, text="Ejecutar Algoritmo", command=self.run_ga)
        run_button.grid(row=len(inputs) + 1, column=1, pady=20)

    def run_ga(self):
        try:
            total_empleados = int(self.entries["Empleados por turno"].get())
            dias_laborales = int(self.entries["Días Laborales"].get())
            areas = self.entries["Áreas (separadas por comas)"].get().split(",")
            tamano_poblacion = int(self.entries["Población inicial"].get())
            poblacion_maxima = int(self.entries["Población máxima"].get())
            pc = float(self.entries["Probabilidad de Cruce (0.1 a 1.0)"].get())
            pm = float(self.entries["Probabilidad de Mutación (0.1 a 1.0)"].get())
            numero_generaciones = int(self.entries["Número de Generaciones"].get())

            scheduler_ga = AG(
                dias_laborales, areas, total_empleados, numero_generaciones, poblacion_maxima, tamano_poblacion, pm, pc
            )
            mejor_individuo = scheduler_ga.ejecutar_algoritmo()
            scheduler_ga.mostrar_mejor_individuo(mejor_individuo)
        except ValueError as e:
            messagebox.showerror("Error", "Por favor, ingresa valores válidos.\n" + str(e))
        except Exception as e:
            messagebox.showerror("Error de Ejecución", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()
