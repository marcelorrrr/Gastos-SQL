class Gasto:
    
    def __init__(self, id, fecha, monto, categoria, descripcion):
        # Asignamos los datos a los atributos del objeto.
        self.id = id
        self.fecha = fecha
        self.monto = monto
        self.categoria = categoria
        self.descripcion = descripcion

    def __str__(self):
        """
        Define cómo se verá el objeto Gasto cuando lo imprimamos.
        Esto es muy útil para depuración y para mostrarlo en la interfaz.
        """
        return f"[{self.fecha}] - {self.categoria}: ${self.monto:.2f} ({self.descripcion})"
    