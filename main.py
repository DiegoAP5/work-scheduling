import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from algorithm import SchedulerGA

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scheduler Genetic Algorithm")
        self.root.geometry("500x400")

        # Create and pack widgets
        self.setup_widgets()

    def setup_widgets(self):
        # Labels and entries for input
        inputs = [
            ("Total de Empleados", 1, 0),
            ("Días Laborales", 1, 1),
            ("Áreas", 1, 3),
            ("Tamaño de Población", 1, 4),
            ("Probabilidad de Cruce", 1, 5),
            ("Probabilidad de Mutación", 1, 6),
            ("Número de Generaciones", 1, 7),
        ]

        self.entries = {}
        for label_text, column, row in inputs:
            label = ttk.Label(self.root, text=label_text)
            label.grid(row=row, column=column - 1, padx=10, pady=10, sticky=tk.E)
            entry = ttk.Entry(self.root)
            entry.grid(row=row, column=column, padx=10, pady=10, sticky=tk.W)
            self.entries[label_text] = entry
        
        # Button to run the GA
        run_button = ttk.Button(self.root, text="Ejecutar Algoritmo", command=self.run_ga)
        run_button.grid(row=len(inputs) + 1, column=1, pady=20)

    def run_ga(self):
        try:
            total_empleados = int(self.entries["Total de Empleados"].get())
            dias_laborales = int(self.entries["Días Laborales"].get())
            areas = self.entries["Áreas"].get().split(",")
            tamano_poblacion = int(self.entries["Tamaño de Población"].get())
            pc = float(self.entries["Probabilidad de Cruce"].get())
            pm = float(self.entries["Probabilidad de Mutación"].get())
            numero_generaciones = int(self.entries["Número de Generaciones"].get())

            scheduler_ga = SchedulerGA(
                total_empleados, dias_laborales, areas, tamano_poblacion, pc, pm, numero_generaciones
            )
            scheduler_ga.algoritmo_genetico()
        except ValueError as e:
            messagebox.showerror("Error", "Por favor, ingresa valores válidos.\n" + str(e))
        except Exception as e:
            messagebox.showerror("Error de Ejecución", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()
