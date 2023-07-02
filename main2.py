import tkinter as tk

class Actividad:
    def __init__(self, nombre, duracion, predecesoras=None):
        self.nombre = nombre
        self.duracion = duracion
        self.predecesoras = predecesoras if predecesoras else []
        self.dia_mas_temprano_inicio = 0
        self.dia_mas_temprano_terminacion = 0
        self.dia_mas_tardio_inicio = 0
        self.dia_mas_tardio_terminacion = 0
        self.holgura = 0

def crear_actividades_desde_entradas():
    actividades = []
    for i in range(len(actividades_entries)):
        nombre = actividades_entries[i].get()
        duracion = int(duracion_entries[i].get())
        predecesoras = predecesoras_entries[i].get().split(",") if predecesoras_entries[i].get() else []
        actividad = Actividad(nombre, duracion, predecesoras)
        actividades.append(actividad)
    return actividades

def calcular_dias_mas_tempranos(actividades):
    for actividad in actividades:
        if not actividad.predecesoras:
            actividad.dia_mas_temprano_inicio = 1
        else:
            dias_tempranos = [act.dia_mas_temprano_terminacion for act in actividades if act.nombre in actividad.predecesoras]
            actividad.dia_mas_temprano_inicio = max(dias_tempranos) + 1
        actividad.dia_mas_temprano_terminacion = actividad.dia_mas_temprano_inicio + actividad.duracion - 1

def calcular_dias_mas_tardios(actividades):
    actividades_ordenadas = sorted(actividades, key=lambda act: act.dia_mas_temprano_terminacion, reverse=True)
    for actividad in actividades_ordenadas:
        if not actividad.predecesoras:
            actividad.dia_mas_tardio_terminacion = actividad.dia_mas_temprano_terminacion
            actividad.dia_mas_tardio_inicio = actividad.dia_mas_temprano_inicio
        else:
            dias_tardios = [act.dia_mas_tardio_inicio for act in actividades if actividad.nombre in act.predecesoras]
            if dias_tardios:
                actividad.dia_mas_tardio_terminacion = min(dias_tardios) - 1
                actividad.dia_mas_tardio_inicio = actividad.dia_mas_tardio_terminacion - actividad.duracion + 1
            else:
                actividad.dia_mas_tardio_terminacion = actividad.dia_mas_temprano_terminacion
                actividad.dia_mas_tardio_inicio = actividad.dia_mas_temprano_inicio

def calcular_holgura(actividades):
    for actividad in actividades:
        actividad.holgura = actividad.dia_mas_tardio_inicio - actividad.dia_mas_temprano_inicio

def mostrar_resultados(actividades):
    resultados_text.delete("1.0", tk.END)

    for actividad in actividades:
        resultados_text.insert(tk.END, f"Actividad: {actividad.nombre}\n")
        resultados_text.insert(tk.END, f"Día más temprano de inicio: {actividad.dia_mas_temprano_inicio}\n")
        resultados_text.insert(tk.END, f"Día más temprano de terminación: {actividad.dia_mas_temprano_terminacion}\n")
        resultados_text.insert(tk.END, f"Día más tardío de inicio: {actividad.dia_mas_tardio_inicio}\n")
        resultados_text.insert(tk.END, f"Día más tardío de terminación: {actividad.dia_mas_tardio_terminacion}\n")
        resultados_text.insert(tk.END, f"Holgura: {actividad.holgura}\n\n")

def calcular_ruta_critica():
    actividades = crear_actividades_desde_entradas()
    calcular_dias_mas_tempranos(actividades)
    calcular_dias_mas_tardios(actividades)
    calcular_holgura(actividades)

    ruta_critica = []
    for actividad in actividades:
        if actividad.holgura == 0:
            ruta_actividad = obtener_ruta_actividad(actividad, actividades)
            ruta_critica.append(" --> ".join(ruta_actividad))

    mostrar_resultados(actividades)
    ruta_critica_text.delete("1.0", tk.END)
    ruta_critica_text.insert(tk.END, "\n".join(ruta_critica))

def obtener_ruta_actividad(actividad, actividades):
    ruta_actividad = [actividad.nombre]
    while actividad.predecesoras:
        predecesora = next(act for act in actividades if act.nombre == actividad.predecesoras[0])
        ruta_actividad.insert(0, predecesora.nombre)
        actividad = predecesora
    return ruta_actividad

# Crear la ventana principal
window = tk.Tk()
window.title("Cálculo de Ruta Crítica")

# Frame para las entradas de actividades
inputs_frame = tk.Frame(window)
inputs_frame.pack(pady=20)

# Etiquetas y campos de entrada para la cantidad de actividades
num_actividades_label = tk.Label(inputs_frame, text="Cantidad de actividades:")
num_actividades_label.grid(row=0, column=0, padx=10)

num_actividades_entry = tk.Entry(inputs_frame, width=10)
num_actividades_entry.grid(row=0, column=1, padx=10)

# Etiquetas y campos de entrada para las actividades
actividades_label = tk.Label(inputs_frame, text="Actividades:")
actividades_label.grid(row=1, column=0, padx=10)

duracion_label = tk.Label(inputs_frame, text="Duración:")
duracion_label.grid(row=1, column=1, padx=10)

predecesoras_label = tk.Label(inputs_frame, text="Predecesoras:")
predecesoras_label.grid(row=1, column=2, padx=10)

actividades_entries = []
duracion_entries = []
predecesoras_entries = []

def crear_campos_de_entrada():
    num_actividades = int(num_actividades_entry.get()) if num_actividades_entry.get() else 0

    # Eliminar los campos de entrada anteriores
    for entry in actividades_entries:
        entry.destroy()
    for entry in duracion_entries:
        entry.destroy()
    for entry in predecesoras_entries:
        entry.destroy()

    actividades_entries.clear()
    duracion_entries.clear()
    predecesoras_entries.clear()

    # Crear los nuevos campos de entrada
    for i in range(num_actividades):
        actividad_entry = tk.Entry(inputs_frame, width=10)
        actividad_entry.grid(row=i+2, column=0, padx=10, pady=5)
        actividades_entries.append(actividad_entry)

        duracion_entry = tk.Entry(inputs_frame, width=10)
        duracion_entry.grid(row=i+2, column=1, padx=10, pady=5)
        duracion_entries.append(duracion_entry)

        predecesoras_entry = tk.Entry(inputs_frame, width=15)
        predecesoras_entry.grid(row=i+2, column=2, padx=10, pady=5)
        predecesoras_entries.append(predecesoras_entry)

crear_campos_de_entrada()

# Botón para crear los campos de entrada
crear_campos_button = tk.Button(inputs_frame, text="Crear campos de entrada", command=crear_campos_de_entrada)
crear_campos_button.grid(row=0, column=2, padx=10)

# Botón para calcular la ruta crítica
calcular_button = tk.Button(window, text="Calcular ruta crítica", command=calcular_ruta_critica)
calcular_button.pack(pady=10)

# Frame para mostrar los resultados
resultados_frame = tk.Frame(window)
resultados_frame.pack(pady=20)

# Etiqueta para los resultados
resultados_label = tk.Label(resultados_frame, text="Resultados:")
resultados_label.pack()

# Texto para mostrar los resultados
resultados_text = tk.Text(resultados_frame, width=50, height=10)
resultados_text.pack()

# Frame para mostrar la ruta crítica
ruta_critica_frame = tk.Frame(window)
ruta_critica_frame.pack(pady=20)

# Etiqueta para la ruta crítica
ruta_critica_label = tk.Label(ruta_critica_frame, text="Ruta Crítica:")
ruta_critica_label.pack()

# Texto para mostrar la ruta crítica
ruta_critica_text = tk.Text(ruta_critica_frame, width=50, height=3)
ruta_critica_text.pack()

window.mainloop()
