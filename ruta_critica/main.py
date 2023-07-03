from tkinter import *
import networkx as nx
import matplotlib.pyplot as plt

class Grafo:
    def __init__(self):
        self.actividades = []
        self.grafo = nx.DiGraph()
        self.holguras = {}

    def agregar_actividad(self, nombre, duracion, predecesores=None):
        self.actividades.append((nombre, duracion, predecesores))
        self.grafo.add_node(nombre, duracion=duracion)
        if predecesores:
            predecesores_list = predecesores.split(',')
            for predecesor in predecesores_list:
                self.grafo.add_edge(predecesor.strip(), nombre)

    def calcular_ruta_critica(self):
        if not nx.is_directed_acyclic_graph(self.grafo):
            return None  # Retorna None si el grafo contiene ciclos

        ruta_critica = nx.algorithms.dag.dag_longest_path(self.grafo)

        # Calcula las holguras
        duraciones = nx.get_node_attributes(self.grafo, 'duracion')
        for actividad in self.actividades:
            nombre, duracion, _ = actividad
            holgura = sum(duraciones.values()) - duracion
            self.holguras[nombre] = holgura

        return ruta_critica


class InterfazGrafica:
    def __init__(self):
        self.grafo = Grafo()
        self.ventana = Tk()
        self.ventana.title("Cálculo de Ruta Crítica")

        self.actividades_frame = Frame(self.ventana)
        self.actividades_frame.pack(padx=10, pady=10)

        self.etiqueta_nombre = Label(self.actividades_frame, text="Nombre de la actividad:")
        self.etiqueta_nombre.grid(row=0, column=0, padx=10, pady=10)
        self.nombre = Entry(self.actividades_frame)
        self.nombre.grid(row=0, column=1, padx=10, pady=10)

        self.etiqueta_duracion = Label(self.actividades_frame, text="Duración de la actividad:")
        self.etiqueta_duracion.grid(row=1, column=0, padx=10, pady=10)
        self.duracion = Entry(self.actividades_frame)
        self.duracion.grid(row=1, column=1, padx=10, pady=10)

        self.etiqueta_predecesor = Label(self.actividades_frame, text="Predecesores (opcional, separados por comas):")
        self.etiqueta_predecesor.grid(row=2, column=0, padx=10, pady=10)
        self.predecesores = Entry(self.actividades_frame)
        self.predecesores.grid(row=2, column=1, padx=10, pady=10)

        self.boton_agregar = Button(self.actividades_frame, text="Agregar Actividad", command=self.agregar_actividad)
        self.boton_agregar.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.boton_ruta_critica = Button(self.actividades_frame, text="Calcular Ruta Crítica", command=self.calcular_ruta_critica)
        self.boton_ruta_critica.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.boton_reiniciar = Button(self.actividades_frame, text="Reiniciar", command=self.reiniciar)
        self.boton_reiniciar.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.actividades_label = Label(self.ventana, text="Actividades:")
        self.actividades_label.pack(padx=10, pady=10)
        self.actividades_listbox = Listbox(self.ventana, width=50)
        self.actividades_listbox.pack(padx=10, pady=10)

        self.ventana.mainloop()

    def agregar_actividad(self):
        nombre = self.nombre.get()
        duracion = int(self.duracion.get())
        predecesores = self.predecesores.get()
        self.grafo.agregar_actividad(nombre, duracion, predecesores)

        actividad_text = f"{nombre} (Duración: {duracion}, Holgura: {self.grafo.holguras.get(nombre, 0)})"
        if predecesores:
            actividad_text += f" - Predecesores: {predecesores}"
        self.actividades_listbox.insert(END, actividad_text)

        self.nombre.delete(0, 'end')
        self.duracion.delete(0, 'end')
        self.predecesores.delete(0, 'end')

    def calcular_ruta_critica(self):
        ruta_critica = self.grafo.calcular_ruta_critica()
        if ruta_critica is None:
            print("El grafo contiene ciclos. No se puede calcular la ruta crítica.")
            return

        print("Ruta Crítica:", ruta_critica)

        # Visualizar el grafo con la ruta crítica y las holguras
        G = self.grafo.grafo
        pos = nx.spring_layout(G)

        plt.figure(figsize=(10, 6))

        # Dibuja el grafo
        nx.draw(G, pos, with_labels=True, node_size=1000, node_color="lightblue", font_size=10, font_weight="bold")

        # Dibuja la ruta crítica
        nx.draw_networkx_edges(G, pos, edgelist=[(ruta_critica[i], ruta_critica[i + 1]) for i in range(len(ruta_critica) - 1)],
                               edge_color='red', width=2)

        # Dibuja las holguras junto a cada nodo
        holguras = self.grafo.holguras
        for node in G.nodes:
            holgura = holguras.get(node, 0)
            nx.draw_networkx_labels(G, pos, labels={node: f"{node}\nHolgura: {holgura}"}, font_size=8, font_color="black", verticalalignment="center")

        plt.title("Grafo con Ruta Crítica y Holguras")
        plt.axis("off")
        plt.show()

    def reiniciar(self):
        self.grafo = Grafo()
        self.actividades_listbox.delete(0, END)
        # Limpiar otros widgets si es necesario


InterfazGrafica()
