import tkinter as tk
from tkinter import ttk, messagebox
import database
import modelo

# --- NUEVA CLASE PARA LA VENTANA DE EDICIÓN ---
class VentanaEdicion:
    def __init__(self, parent, gasto_id, callback_actualizar):
        self.ventana_edicion = tk.Toplevel(parent)
        self.ventana_edicion.title("Editar Gasto")
        self.gasto_id = gasto_id
        self.callback_actualizar = callback_actualizar # Función para refrescar la lista principal

        # Obtener datos actuales del gasto para pre-llenar el formulario
        gasto_actual_tupla = database.obtener_gasto_por_id(self.gasto_id)
        gasto_actual = modelo.Gasto(*gasto_actual_tupla)

        # Crear formulario
        tk.Label(self.ventana_edicion, text="Monto:").grid(row=0, column=0, padx=5, pady=5)
        self.monto_entry = tk.Entry(self.ventana_edicion)
        self.monto_entry.grid(row=0, column=1, padx=5, pady=5)
        self.monto_entry.insert(0, gasto_actual.monto)

        tk.Label(self.ventana_edicion, text="Categoría:").grid(row=1, column=0, padx=5, pady=5)
        self.categoria_entry = tk.Entry(self.ventana_edicion)
        self.categoria_entry.grid(row=1, column=1, padx=5, pady=5)
        self.categoria_entry.insert(0, gasto_actual.categoria)

        tk.Label(self.ventana_edicion, text="Descripción:").grid(row=2, column=0, padx=5, pady=5)
        self.descripcion_entry = tk.Entry(self.ventana_edicion)
        self.descripcion_entry.grid(row=2, column=1, padx=5, pady=5)
        self.descripcion_entry.insert(0, gasto_actual.descripcion)

        tk.Button(self.ventana_edicion, text="Guardar Cambios", command=self.guardar_cambios).grid(row=3, column=0, columnspan=2, pady=10)

    def guardar_cambios(self):
        try:
            nuevo_monto = float(self.monto_entry.get())
            nueva_categoria = self.categoria_entry.get()
            nueva_descripcion = self.descripcion_entry.get()

            if not nueva_categoria:
                messagebox.showerror("Error", "La categoría es obligatoria.")
                return

            database.editar_gasto(self.gasto_id, nuevo_monto, nueva_categoria, nueva_descripcion)
            self.callback_actualizar() # Llama a la función para refrescar la lista
            self.ventana_edicion.destroy() # Cierra la ventana de edición

        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número.")

class AppGastos:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Registro de Gastos Personales")
        self.ventana.geometry("700x500")

        # --- Frame para el Formulario de Entrada ---
        frame_formulario = tk.Frame(self.ventana, padx=10, pady=10)
        frame_formulario.pack(fill='x', padx=10, pady=5)
        # (El resto del formulario no cambia)
        tk.Label(frame_formulario, text="Monto:", font=("Helvetica", 12)).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.monto_entry = tk.Entry(frame_formulario, font=("Helvetica", 12))
        self.monto_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=2)
        tk.Label(frame_formulario, text="Categoría:", font=("Helvetica", 12)).grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.categoria_entry = tk.Entry(frame_formulario, font=("Helvetica", 12))
        self.categoria_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=2)
        tk.Label(frame_formulario, text="Descripción:", font=("Helvetica", 12)).grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.descripcion_entry = tk.Entry(frame_formulario, font=("Helvetica", 12))
        self.descripcion_entry.grid(row=2, column=1, sticky='ew', padx=5, pady=2)
        frame_formulario.columnconfigure(1, weight=1)

        # --- Botones ---
        frame_botones = tk.Frame(self.ventana)
        frame_botones.pack(pady=10)
        tk.Button(frame_botones, text="Agregar Gasto", command=self.agregar_gasto, font=("Helvetica", 12)).pack(side='left', padx=10)
        tk.Button(frame_botones, text="Editar Gasto", command=self.abrir_ventana_edicion, font=("Helvetica", 12)).pack(side='left', padx=10) # --- NUEVO BOTÓN ---
        tk.Button(frame_botones, text="Eliminar Gasto", command=self.eliminar_gasto, font=("Helvetica", 12)).pack(side='left', padx=10)

        # --- Frame para la Lista de Gastos (Treeview) ---
        frame_lista = tk.Frame(self.ventana)
        frame_lista.pack(fill='both', expand=True, padx=10, pady=10)
        self.tree = ttk.Treeview(frame_lista, columns=("ID", "Fecha", "Monto", "Categoría", "Descripción"), show='headings')
        # (El resto del Treeview no cambia)
        self.tree.heading("ID", text="ID"); self.tree.heading("Fecha", text="Fecha"); self.tree.heading("Monto", text="Monto")
        self.tree.heading("Categoría", text="Categoría"); self.tree.heading("Descripción", text="Descripción")
        self.tree.column("ID", width=40, anchor='center'); self.tree.column("Fecha", width=100, anchor='center'); self.tree.column("Monto", width=80, anchor='e')
        self.tree.column("Categoría", width=120); self.tree.column("Descripción", width=300)
        self.tree.pack(fill='both', expand=True)
        self.actualizar_lista_gastos()

    # --- NUEVO MÉTODO PARA ABRIR LA VENTANA DE EDICIÓN ---
    def abrir_ventana_edicion(self):
        seleccionado = self.tree.focus()
        if not seleccionado:
            messagebox.showerror("Error", "Por favor, selecciona un gasto para editar.")
            return
        
        id_gasto = self.tree.item(seleccionado)['values'][0]
        VentanaEdicion(self.ventana, id_gasto, self.actualizar_lista_gastos)

    def actualizar_lista_gastos(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        gastos_db = database.obtener_gastos()
        for gasto_tupla in gastos_db:
            gasto_obj = modelo.Gasto(*gasto_tupla)
            self.tree.insert("", "end", values=(gasto_obj.id, gasto_obj.fecha, f"${gasto_obj.monto:.2f}", gasto_obj.categoria, gasto_obj.descripcion))

    def agregar_gasto(self):
        try:
            monto = float(self.monto_entry.get()); categoria = self.categoria_entry.get(); descripcion = self.descripcion_entry.get()
            if not categoria: messagebox.showerror("Error", "La categoría es obligatoria."); return
            database.agregar_gasto(monto, categoria, descripcion)
            self.monto_entry.delete(0, 'end'); self.categoria_entry.delete(0, 'end'); self.descripcion_entry.delete(0, 'end')
            self.actualizar_lista_gastos()
        except ValueError: messagebox.showerror("Error", "El monto debe ser un número.")

    def eliminar_gasto(self):
        seleccionado = self.tree.focus()
        if not seleccionado: messagebox.showerror("Error", "Por favor, selecciona un gasto para eliminar."); return
        id_gasto = self.tree.item(seleccionado)['values'][0]
        if messagebox.askyesno("Confirmar", f"¿Estás seguro de que quieres eliminar el gasto con ID {id_gasto}?"):
            database.eliminar_gasto(id_gasto)
            self.actualizar_lista_gastos()

# --- Bloque principal para iniciar la aplicación ---
if __name__ == "__main__":
    database.conectar_db()
    ventana_principal = tk.Tk()
    app = AppGastos(ventana_principal)
    ventana_principal.mainloop()