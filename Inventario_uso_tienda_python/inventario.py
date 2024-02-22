"""Librerias"""
from tkinter import *
from tkinter import ttk
import sqlite3


# Creamos clase de Articulo

class Articulos:
    """clase que representa mi app de inventario"""

    base_de_datos = "inventario_uso_tienda.db"

    def __init__(self, window):
        self.wind = window
        self.wind.title("Inventario de uso tienda")

        # container LabelFrame
        frame = LabelFrame(self.wind, text="Registra un nuevo articulo")
        frame.grid(row=0, column=0, columnspan=6, pady=20)

        # entrada numero de material
        Label(frame, text="Material: ").grid(row=1, column=0)
        self.material = Entry(frame)
        self.material.focus()
        self.material.grid(row=1, column=1)

        # entrada referencia articulo

        Label(frame, text="Referencia: ").grid(row=2, column=0)
        self.referencia = Entry(frame)
        self.referencia.grid(row=2, column=1)

        # entrada descripcion de articulo

        Label(frame, text="Descripcion: ").grid(row=3, column=0)
        self.descripcion = Entry(frame)
        self.descripcion.grid(row=3, column=1)

        # entrada cantidad bultos de articulo

        Label(frame, text="Bultos: ").grid(row=4, column=0)
        self.bultos = Entry(frame)
        self.bultos.grid(row=4, column=1)

        # entrada cantidad piezas de articulo

        Label(frame, text="Piezas: ").grid(row=5, column=0)
        self.piezas = Entry(frame)
        self.piezas.grid(row=5, column=1)

        # boton para agregar articulo

        ttk.Button(frame, text="Guardar Articulo", command=self.agregar_articulos).grid(
            row=6, columnspan=2, sticky=W + E)

        # mensaje despues del boton

        self.message = Label(frame, text="", fg="red")
        self.message.grid(row=7, column=0, columnspan=2, sticky=W + E)

        # creamos tabla de visualizacion de base de datos

        self.tree = ttk.Treeview(columns=('#1', '#2', '#3', '#4'))
        self.tree.grid(row=6, column=0, columnspan=2)
        self.tree.heading("#0", text="Material", anchor=CENTER)
        self.tree.heading("#1", text="Referencia", anchor=CENTER)
        self.tree.heading("#2", text="Descripcion", anchor=CENTER)
        self.tree.heading("#3", text="Bultos", anchor=CENTER)
        self.tree.heading("#4", text="Piezas", anchor=CENTER)

        # creamos botones para eliminar y actualiza la tabla
        ttk.Button(text="Eliminar Articulo", command=self.eliminar_articulo).grid(
            row=7, column=0, sticky=W + E,)
        ttk.Button(text="Editar Articulo", command=self.actualizar_articulo).grid(
            row=7, column=1, sticky=W + E)

        # colocamos la funcion mostrar articulos en esta area para que funcione
        self.mostrar_articulos()

    # definimos funcion para conectarnos con base de datos

    def consulta_de_datos(self, query, parametros=()):
        """funcion para consutar a la base de datos"""
        with sqlite3.connect(self.base_de_datos) as conn:
            cursor = conn.cursor()
            resultado = cursor.execute(query, parametros)
            conn.commit()
        return resultado

    # funcion para tomar datos de la base de datos

    def mostrar_articulos(self):
        """funcion para ejecutar la consulta"""
        # limpiamos la tabla creada
        registros = self.tree.get_children()
        for elemento in registros:
            self.tree.delete(elemento)
        # consultamos articulos registrados
        query = "SELECT * FROM Inventario_uso_tienda ORDER BY Material DESC"
        resultados = self.consulta_de_datos(query)
        # rellenando con registros las tablas
        for row in resultados:
            self.tree.insert("", 0, text=row[0], values=(
                row[1], row[2], row[3], row[4], ...))

    # funcion para validar si la longitud de la entrada en diferente de 0
    def validacion(self):
        """validacion"""
        return len(self.material.get()) != 0 and len(self.referencia.get()) != 0 and len(self.descripcion.get()) != 0 and len(self.bultos.get()) != 0 and len(self.piezas.get()) != 0

    # funcion para agregar articulos
    def agregar_articulos(self):
        """funcion para agregar articulo nuevo"""
        if self.validacion() is True:
            query = "INSERT INTO Inventario_uso_tienda VALUES (?, ?, ?, ?, ?)"
            parametros = (self.material.get(), self.referencia.get(),
                          self.descripcion.get(), self.bultos.get(), self.piezas.get())
            self.consulta_de_datos(query, parametros)
            self.message["text"] = f"""El articulo {
                self.descripcion.get()} ha sido guardado satisfactoriamente"""
            self.material.delete(0, END)
            self.referencia.delete(0, END)
            self.descripcion.delete(0, END)
            self.bultos.delete(0, END)
            self.piezas.delete(0, END)
        else:
            self.message["text"] = "Se necesita rellenar todos los campos"

        self.mostrar_articulos()

    # funcion para eliminar articulo

    def eliminar_articulo(self):
        """funcion que elimina articulo seleccionado"""
        self.message["text"] = ""
        try:
            self.tree.item(self.tree.selection())["text"]
        except IndexError as e:
            self.message["text"] = "Por favor selecciona un registro"
            return
        self.message["text"] = ""
        seleccion = self.tree.item(self.tree.selection())["text"]
        query = "DELETE FROM Inventario_uso_tienda WHERE Material = ?"
        self.consulta_de_datos(query, (seleccion, ))
        self.message["text"] = f"""¡El articulo {
            seleccion} ha sido eliminado!"""
        self.mostrar_articulos()

    # funcion para actualizar algun articulo

    def actualizar_articulo(self):
        """funcion para actualizar losa articulos"""
        self.message["text"] = ""
        try:
            self.tree.item(self.tree.selection())["text"]
        except IndexError as e:
            self.message["text"] = "Por favor selecciona un registro"
            return
        material = self.tree.item(self.tree.selection())["text"]  # material
        referencia = self.tree.item(self.tree.selection())[
            "values"][0]  # referencia
        descripcion = self.tree.item(self.tree.selection())[
            "values"][1]  # descripcion
        bultos = self.tree.item(self.tree.selection())[
            "values"][2]  # bultos
        piezas = self.tree.item(self.tree.selection())[
            "values"][3]  # bultos
        self.ventana_editar = Toplevel()
        self.ventana_editar.title = "Editar articulo seleccionado"

        # datos material viejos row 0
        Label(self.ventana_editar, text="Material a editar: ").grid(
            row=0, column=1)
        Entry(self.ventana_editar, textvariable=StringVar(
            self.ventana_editar, value=material), state="readonly").grid(row=0, column=2)
        # datos material nuevos row 1
        Label(self.ventana_editar, text="Material nuevo: ").grid(row=1, column=1)
        nuevo_material = Entry(self.ventana_editar)
        nuevo_material.grid(row=1, column=2)

        # datos referencia vieja row 2
        Label(self.ventana_editar, text="Referencia a editar: ").grid(
            row=2, column=1)
        Entry(self.ventana_editar, textvariable=StringVar(
            self.ventana_editar, value=referencia), state="readonly").grid(row=2, column=2)
        # datos referencia nueva row 3
        Label(self.ventana_editar, text="Referencia nueva: ").grid(
            row=3, column=1)
        nueva_referencia = Entry(self.ventana_editar)
        nueva_referencia.grid(row=3, column=2)

        # datos referencia vieja row 4
        Label(self.ventana_editar, text="Descripcion a editar: ").grid(
            row=4, column=1)
        Entry(self.ventana_editar, textvariable=StringVar(
            self.ventana_editar, value=descripcion), state="readonly").grid(row=4, column=2)
        # datos descripcion nuevos row 5
        Label(self.ventana_editar, text="Descripcion nueva: ").grid(
            row=5, column=1)
        nueva_descripcion = Entry(self.ventana_editar)
        nueva_descripcion.grid(row=5, column=2)

        # datos bultos viejos row 6
        Label(self.ventana_editar, text="Cantidad de bultos a editar: ").grid(
            row=6, column=1)
        Entry(self.ventana_editar, textvariable=StringVar(
            self.ventana_editar, value=bultos), state="readonly").grid(row=6, column=2)
        # datos descripcion nuevos row 7
        Label(self.ventana_editar, text="Cantidad de bultos nueva: ").grid(
            row=7, column=1)
        nueva_cantidad_bultos = Entry(self.ventana_editar)
        nueva_cantidad_bultos.grid(row=7, column=2)

        # datos bultos viejos row 8
        Label(self.ventana_editar, text="Cantidad de piezas a editar: ").grid(
            row=8, column=1)
        Entry(self.ventana_editar, textvariable=StringVar(
            self.ventana_editar, value=piezas), state="readonly").grid(row=8, column=2)
        # datos descripcion nuevos row 9
        Label(self.ventana_editar, text="Cantidad de piezas nueva: ").grid(
            row=9, column=1)
        nueva_cantidad_piezas = Entry(self.ventana_editar)
        nueva_cantidad_piezas.grid(row=9, column=2)

        # boton para actualizar

        Button(self.ventana_editar, text="Actualizar", command=lambda: self.actualizar_datos(material, nuevo_material.get(), descripcion, nueva_descripcion.get(
        ), referencia, nueva_referencia.get(), bultos, nueva_cantidad_bultos.get(), piezas, nueva_cantidad_piezas.get())).grid(row=10, column=2, sticky=W)

    def actualizar_datos(self, material, nuevo_material, descripcion, nueva_descripcion, referencia, nueva_referencia, bultos, nueva_cantidad_bultos, piezas, nueva_cantidad_piezas):
        """funcion para actualizar datos"""
        query = "UPDATE Inventario SET Material = ?, descripcion = ?, Referencia = ?, Cantidad = ? WHERE Material = ? AND descripcion = ? AND Referencia = ? AND Cantidad = ?"
        parametros = (nuevo_material, nueva_descripcion, nueva_referencia,
                      nueva_cantidad_bultos, nueva_cantidad_piezas, material, descripcion, referencia, bultos, piezas)
        self.consulta_de_datos(query, parametros)
        self.ventana_editar.destroy()
        self.message["text"] = f"El articulo {descripcion} ha sido actualizado"
        self.mostrar_articulos()


if __name__ == "__main__":
    window = Tk()
    app = Articulos(window)
    window.mainloop()
