import sqlite3
from datetime import date

def conectar_db():
    """Crea una conexión a la base de datos y la tabla si no existen."""
    conn = sqlite3.connect('gastos.db')
    cursor = conn.cursor()
    
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY,
            fecha TEXT NOT NULL,
            monto REAL NOT NULL,
            categoria TEXT NOT NULL,
            descripcion TEXT
        )
    """)
    conn.commit()
    return conn


def agregar_gasto(monto, categoria, descripcion):
    """Inserta un nuevo registro de gasto en la base de datos."""
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Obtenemos la fecha de hoy en formato de texto (YYYY-MM-DD)
    fecha_hoy = date.today().isoformat()
    
    cursor.execute("INSERT INTO gastos (fecha, monto, categoria, descripcion) VALUES (?, ?, ?, ?)",
                   (fecha_hoy, monto, categoria, descripcion))
    
    conn.commit()
    conn.close()
    print("Gasto agregado exitosamente.")

def obtener_gastos():
    """Obtiene y devuelve todos los gastos de la base de datos."""
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM gastos ORDER BY fecha DESC")
    gastos = cursor.fetchall()
    
    conn.close()
    return gastos

"""# --- Función de prueba ---
def probar_db():
    #Función para verificar que todo funciona correctamente.
    print("Iniciando prueba de la base de datos...")
    
    # Agregamos dos gastos de ejemplo
    agregar_gasto(50.25, "Comida", "Almuerzo en el trabajo")
    agregar_gasto(120.00, "Transporte", "Carga de combustible")
    
    # Obtenemos y mostramos los gastos
    print("\nGastos guardados:")
    todos_los_gastos = obtener_gastos()
    for gasto in todos_los_gastos:
        print(gasto)

# Si ejecutamos este archivo directamente, se ejecutará la prueba.
if __name__ == "__main__":
    probar_db()
"""

# En database.py

def eliminar_gasto(id_gasto):
    """Elimina un registro de gasto de la base de datos por su ID."""
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM gastos WHERE id = ?", (id_gasto,))
    
    conn.commit()
    conn.close()
    print(f"Gasto con ID {id_gasto} eliminado.")

def editar_gasto(id_gasto, nuevo_monto, nueva_categoria, nueva_descripcion):
    """Actualiza un registro de gasto existente en la base de datos."""
    conn = conectar_db()
    cursor = conn.cursor()
    
    # El comando UPDATE modifica las columnas de la fila que cumpla la condición WHERE.
    cursor.execute("""
        UPDATE gastos 
        SET monto = ?, categoria = ?, descripcion = ?
        WHERE id = ?
    """, (nuevo_monto, nueva_categoria, nueva_descripcion, id_gasto))
    
    conn.commit()
    conn.close()
    print(f"Gasto con ID {id_gasto} actualizado.")

def obtener_gasto_por_id(id_gasto):
    """Obtiene y devuelve un único gasto por su ID."""
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM gastos WHERE id = ?", (id_gasto,))
    gasto = cursor.fetchone() # fetchone() devuelve solo un registro
    
    conn.close()
    return gasto