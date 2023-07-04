import networkx as nx
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
import numpy as np

class Grafo:
    def __init__(self):
        self.grafo = nx.DiGraph()
        self.holguras = {}
        self.dia_temprano_inicio = {}
        self.dia_temprano_finalizacion = {}
        self.dia_tardio_inicio = {}
        self.dia_tardio_finalizacion = {}
        self.matriz_adyacencia = []

    def agregar_actividad(self, nombre, duracion, predecesores):
        self.grafo.add_node(nombre, duracion=duracion)
        self.holguras[nombre] = 0

        if predecesores:
            predecesores = predecesores.split(',')
            for predecesor in predecesores:
                self.grafo.add_edge(predecesor, nombre)

    def calcular_ruta_critica(self):
        # Calcular los días más tempranos de inicio y finalización
        actividades_ordenadas = list(nx.topological_sort(self.grafo))
        for actividad in actividades_ordenadas:
            predecesores = list(self.grafo.predecessors(actividad))
            if not predecesores:
                self.dia_temprano_inicio[actividad] = 0
                self.dia_temprano_finalizacion[actividad] = self.grafo.nodes[actividad]['duracion']
            else:
                dia_temprano_inicio = max([self.dia_temprano_finalizacion[pred] for pred in predecesores])
                self.dia_temprano_inicio[actividad] = dia_temprano_inicio
                self.dia_temprano_finalizacion[actividad] = dia_temprano_inicio + self.grafo.nodes[actividad]['duracion']

        # Calcular los días más tardíos de inicio y finalización
        actividades_reverso = list(reversed(actividades_ordenadas))
        for actividad in actividades_reverso:
            sucesores = list(self.grafo.successors(actividad))
            if not sucesores:
                self.dia_tardio_finalizacion[actividad] = self.dia_temprano_finalizacion[actividad]
                self.dia_tardio_inicio[actividad] = self.dia_temprano_inicio[actividad]
            else:
                dia_tardio_finalizacion = min([self.dia_tardio_inicio[suc] for suc in sucesores])
                self.dia_tardio_finalizacion[actividad] = dia_tardio_finalizacion
                self.dia_tardio_inicio[actividad] = dia_tardio_finalizacion - self.grafo.nodes[actividad]['duracion']

        # Calcular la holgura de cada actividad
        for actividad in actividades_ordenadas:
            holgura = self.dia_tardio_inicio[actividad] - self.dia_temprano_inicio[actividad]
            self.holguras[actividad] = holgura

        # Obtener la ruta crítica
        ruta_critica = [actividad for actividad in actividades_ordenadas if self.holguras[actividad] == 0]
        return ruta_critica

    def calcular_matriz_adyacencia(self):
        actividades = list(self.grafo.nodes)
        num_actividades = len(actividades)
        self.matriz_adyacencia = np.zeros((num_actividades, num_actividades), dtype=int)

        for i, actividad in enumerate(actividades):
            sucesores = list(self.grafo.successors(actividad))
            for sucesor in sucesores:
                j = actividades.index(sucesor)
                self.matriz_adyacencia[i, j] = 1

        return self.matriz_adyacencia

class InterfazGrafica:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("Cálculo de Ruta Crítica")
        self.ventana.geometry("800x600")

        self.frame = Frame(self.ventana)
        self.frame.pack(pady=20)

        self.label_actividad = Label(self.frame, text="Actividad:")
        self.label_actividad.grid(row=0, column=0)

        self.label_duracion = Label(self.frame, text="Duración:")
        self.label_duracion.grid(row=0, column=1)

        self.label_predecesores = Label(self.frame, text="Predecesores:")
        self.label_predecesores.grid(row=0, column=2)

        self.actividad_entry = Entry(self.frame, width=10)
        self.actividad_entry.grid(row=1, column=0)

        self.duracion_entry = Entry(self.frame, width=10)
        self.duracion_entry.grid(row=1, column=1)

        self.predecesores_entry = Entry(self.frame, width=15)
        self.predecesores_entry.grid(row=1, column=2)

        self.agregar_button = Button(self.frame, text="Agregar Actividad", command=self.agregar_actividad)
        self.agregar_button.grid(row=2, column=0, columnspan=3, pady=10)

        self.calcular_button = Button(self.frame, text="Calcular Ruta Crítica", command=self.calcular_ruta_critica)
        self.calcular_button.grid(row=3, column=0, columnspan=3, pady=10)

        self.listbox_frame = Frame(self.ventana)
        self.listbox_frame.pack(pady=20)

        self.actividades_listbox = Listbox(self.listbox_frame, width=50)
        self.actividades_listbox.pack()

        self.diagrama_button = Button(self.ventana, text="Mostrar Diagrama", command=self.mostrar_diagrama)
        self.diagrama_button.pack(pady=10)

        self.reiniciar_button = Button(self.ventana, text="Reiniciar", command=self.reiniciar)
        self.reiniciar_button.pack()

        self.grafo = Grafo()

        self.ventana.mainloop()

    def agregar_actividad(self):
        nombre = self.actividad_entry.get()
        duracion = int(self.duracion_entry.get())
        predecesores = self.predecesores_entry.get()

        if nombre and duracion:
            self.grafo.agregar_actividad(nombre, duracion, predecesores)
            self.actividades_listbox.insert(END, f"{nombre} - Duración: {duracion}")

        self.actividad_entry.delete(0, END)
        self.duracion_entry.delete(0, END)
        self.predecesores_entry.delete(0, END)

    def calcular_ruta_critica(self):
        ruta_critica = self.grafo.calcular_ruta_critica()
        self.actividades_listbox.delete(0, END)
        for actividad in ruta_critica:
            duracion = self.grafo.grafo.nodes[actividad]['duracion']
            holgura = self.grafo.holguras[actividad]
            inicio_temprano = self.grafo.dia_temprano_inicio[actividad]
            inicio_tardio = self.grafo.dia_tardio_inicio[actividad]
            terminacion_temprana = self.grafo.dia_temprano_finalizacion[actividad]
            terminacion_tardia = self.grafo.dia_tardio_finalizacion[actividad]
            info_actividad = f"{actividad} ==> Holgura = {holgura}, Inicio más temprano = {inicio_temprano}, " \
                            f"Inicio más tardío = {inicio_tardio}, Terminación más temprano = {terminacion_temprana}, " \
                            f"Terminación más tardía = {terminacion_tardia}"
            self.actividades_listbox.insert(END, info_actividad)


    def mostrar_diagrama(self):
        ruta_critica = self.grafo.calcular_ruta_critica()
        grafo = self.grafo.grafo

        pos = nx.spring_layout(grafo)
        plt.figure(figsize=(10, 6))

        # Dibujar nodos
        nx.draw_networkx_nodes(grafo, pos, node_color='lightblue', node_size=500)

        # Dibujar arcos
        edge_colors = ['gray' if (u, v) not in ruta_critica else 'red' for u, v in grafo.edges]
        nx.draw_networkx_edges(grafo, pos, edge_color=edge_colors)

        # Dibujar etiquetas de nodos
        nx.draw_networkx_labels(grafo, pos, font_size=12, font_color='black')

        # Dibujar etiquetas de arcos
        edge_labels = {(u, v): grafo.nodes[v]['duracion'] for u, v in grafo.edges}
        nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels, font_size=8)

        # Mostrar grafo
        plt.axis('off')
        plt.title('Diagrama de Ruta Crítica')

        # Subrayar la ruta crítica en rojo
        red_edges = [edge for edge in grafo.edges if edge in ruta_critica]
        
        nx.draw_networkx_edges(grafo, pos, edgelist=red_edges, edge_color='red', width=2.0)

        plt.show()


    def reiniciar(self):
        self.actividades_listbox.delete(0, END)
        self.grafo = Grafo()

if __name__ == "__main__":
    InterfazGrafica()
