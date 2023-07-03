from tkinter import *
import networkx as nx
import matplotlib.pyplot as plt

class Grafo:
    def __init__(self):
        self.actividades = []
        self.grafo = nx.DiGraph()

    def agregar_actividad(self, nombre, duracion, predecesor=None):
        self.actividades.append((nombre, duracion, predecesor))
        self.grafo.add_node(nombre, duracion=duracion)
        if predecesor:
            self.grafo.add_edge(predecesor, nombre)

    def calcular_ruta_critica(self):
        ruta_critica = nx.algorithms.dag.dag_longest_path(self.grafo)
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

        self.etiqueta_predecesor = Label(self.actividades_frame, text="Predecesor (opcional):")
        self.etiqueta_predecesor.grid(row=2, column=0, padx=10, pady=10)
        self.predecesor = Entry(self.actividades_frame)
        self.predecesor.grid(row=2, column=1, padx=10, pady=10)

        self.boton_agregar = Button(self.actividades_frame, text="Agregar Actividad", command=self.agregar_actividad)
        self.boton_agregar.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.boton_ruta_critica = Button(self.actividades_frame, text="Calcular Ruta Crítica", command=self.calcular_ruta_critica)
        self.boton_ruta_critica.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.actividades_label = Label(self.ventana, text="Actividades:")
        self.actividades_label.pack(padx=10, pady=10)
        self.actividades_listbox = Listbox(self.ventana, width=50)
        self.actividades_listbox.pack(padx=10, pady=10)

        self.ventana.mainloop()

    def agregar_actividad(self):
        nombre = self.nombre.get()
        duracion = int(self.duracion.get())
        predecesor = self.predecesor.get()
        self.grafo.agregar_actividad(nombre, duracion, predecesor)

        actividad_text = f"{nombre} (Duración: {duracion})"
        if predecesor:
            actividad_text += f" - Predecesor: {predecesor}"
        self.actividades_listbox.insert(END, actividad_text)

        self.nombre.delete(0, 'end')
        self.duracion.delete(0, 'end')
        self.predecesor.delete(0, 'end')

    def calcular_ruta_critica(self):
        ruta_critica = self.grafo.calcular_ruta_critica()
        print("Ruta Crítica:", ruta_critica)

        # Visualizar el grafo con la ruta crítica
        G = self.grafo.grafo
        pos = nx.spring_layout(G)

        plt.figure(figsize=(10, 6))
        nx.draw(G, pos, with_labels=True, node_size=1000, node_color="lightblue", font_size=10, font_weight="bold")
        nx.draw_networkx_edges(G, pos, edgelist=[(ruta_critica[i], ruta_critica[i + 1]) for i in range(len(ruta_critica) - 1)],
                               edge_color='red', width=2)
        plt.title("Grafo con Ruta Crítica")
        plt.axis("off")
        plt.show()


InterfazGrafica()
