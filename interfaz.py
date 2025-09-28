import tkinter as tk
from tkinter import ttk, messagebox
import database
import modelo

class AppGastos:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Registro de Gastos Personales")
        self.ventana.geometry("700x500")

        # --- Frame para el Formulario de Entrada ---
        frame_formulario = tk.Frame(self.ventana, padx=10, pady=10)
        frame_formulario.pack(fill='x', padx=10, pady=5)

        tk.Label(frame_formulario, text="Monto:", font=("Helvetica", 12)).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.monto_entry = tk.Entry(frame_formulario, font=("Helvetica", 12))
        self.monto_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=2)

        tk.Label(frame_formulario, text="Categoría:", font=("Helvetica", 12)).grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.categoria_entry = tk.Entry(frame_formulario, font=("Helvetica", 12))
        self.categoria_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=2)

        tk.Label(frame_formulario, text="Descripción:", font=("Helvetica", 12)).grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.descripcion_entry = tk.Entry(frame_formulario, font=("Helvetica", 12))
        self.descripcion_entry.grid(row=2, column=1, sticky='ew', padx=5, pady=2)

        frame_formulario.columnconfigure(1, weight=1) # Permite que los Entry se expandan

        # --- Botones ---
        frame_botones = tk.Frame(self.ventana)
        frame_botones.pack(pady=10)
        
        tk.Button(frame_botones, text="Agregar Gasto", command=self.agregar_gasto, font=("Helvetica", 12)).pack(side='left', padx=10)
        tk.Button(frame_botones, text="Eliminar Gasto", command=self.eliminar_gasto, font=("Helvetica", 12)).pack(side='left', padx=10)

        # --- Frame para la Lista de Gastos (Treeview) ---
        frame_lista = tk.Frame(self.ventana)
        frame_lista.pack(fill='both', expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(frame_lista, columns=("ID", "Fecha", "Monto", "Categoría", "Descripción"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Monto", text="Monto")
        self.tree.heading("Categoría", text="Categoría")
        self.tree.heading("Descripción", text="Descripción")
        
        self.tree.column("ID", width=40, anchor='center')
        self.tree.column("Fecha", width=100, anchor='center')
        self.tree.column("Monto", width=80, anchor='e')
        self.tree.column("Categoría", width=120)
        self.tree.column("Descripción", width=300)

        self.tree.pack(fill='both', expand=True)
        
        self.actualizar_lista_gastos()

    def actualizar_lista_gastos(self):
        # Limpiar la lista actual
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Obtener y mostrar los gastos
        gastos_db = database.obtener_gastos()
        for gasto_tupla in gastos_db:
            gasto_obj = modelo.Gasto(*gasto_tupla)
            self.tree.insert("", "end", values=(gasto_obj.id, gasto_obj.fecha, f"${gasto_obj.monto:.2f}", gasto_obj.categoria, gasto_obj.descripcion))

    def agregar_gasto(self):
        try:
            monto = float(self.monto_entry.get())
            categoria = self.categoria_entry.get()
            descripcion = self.descripcion_entry.get()
            
            if not categoria:
                messagebox.showerror("Error", "La categoría es obligatoria.")
                return

            database.agregar_gasto(monto, categoria, descripcion)
            
            # Limpiar los campos
            self.monto_entry.delete(0, 'end')
            self.categoria_entry.delete(0, 'end')
            self.descripcion_entry.delete(0, 'end')
            
            self.actualizar_lista_gastos()
            
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número.")

    def eliminar_gasto(self):
        seleccionado = self.tree.focus()
        if not seleccionado:
            messagebox.showerror("Error", "Por favor, selecciona un gasto para eliminar.")
            return
        
        id_gasto = self.tree.item(seleccionado)['values'][0]
        
        confirmar = messagebox.askyesno("Confirmar", f"¿Estás seguro de que quieres eliminar el gasto con ID {id_gasto}?")
        if confirmar:
            database.eliminar_gasto(id_gasto)
            self.actualizar_lista_gastos()

# --- Bloque principal para iniciar la aplicación ---
if __name__ == "__main__":
    # Primero, nos aseguramos de que la base de datos y la tabla existan.
    database.conectar_db()
    
    # Luego, creamos y lanzamos la ventana de la aplicación.
    ventana_principal = tk.Tk()
    app = AppGastos(ventana_principal)
    ventana_principal.mainloop()