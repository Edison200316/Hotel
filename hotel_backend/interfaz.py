import tkinter as tk
from tkinter import messagebox
from reportlab.pdfgen import canvas
import os

# Datos de ejemplo de habitaciones reservadas (simulación)
habitaciones_reservadas = {
    '101': False,
    '102': True,  # Esta habitación está ocupada
    '103': False,
}

def verificar_disponibilidad():
    habitacion = entry_habitacion.get()  # Usamos el nombre correcto
    if habitacion in habitaciones_reservadas:
        if habitaciones_reservadas[habitacion]:
            messagebox.showwarning("Ocupada", f"La habitación {habitacion} ya está reservada.")
        else:
            messagebox.showinfo("Disponible", f"La habitación {habitacion} está disponible.")
    else:
        messagebox.showerror("Error", "Número de habitación no válido")

def realizar_reserva():
    nombre = entry_nombre.get()
    email = entry_email.get()
    codigo = entry_habitacion.get()
    dias = entry_dias.get()

    if not dias.isdigit():
        messagebox.showerror("Error", "Por favor, ingresa un número válido de días.")
        return

    dias = int(dias)
    precio_por_noche = 50  # Precio base por noche

    if habitaciones_reservadas.get(codigo, True):
        messagebox.showwarning("Ocupada", f"La habitación {codigo} ya está reservada.")
        return

    total_pagar = dias * precio_por_noche
    habitaciones_reservadas[codigo] = True  # Marcar habitación como reservada

    generar_comprobante(nombre, codigo, dias, total_pagar)
    messagebox.showinfo("Reserva Exitosa", f"Reserva completada para {nombre}\nTotal a pagar: ${total_pagar}")

def generar_comprobante(nombre, habitacion, dias, total_pagar):
    archivo = f"comprobante_{nombre}.pdf"
    c = canvas.Canvas(archivo)
    c.drawString(100, 750, "Comprobante de Reserva")
    c.drawString(100, 730, f"Nombre: {nombre}")
    c.drawString(100, 710, f"Habitación: {habitacion}")
    c.drawString(100, 690, f"Días: {dias}")
    c.drawString(100, 670, f"Total a pagar: ${total_pagar}")
    c.save()
    os.system(f"start {archivo}")  # Abre el PDF automáticamente

# Configuración de la interfaz
tk_root = tk.Tk()
tk_root.title("Sistema Hotelero")
tk_root.geometry("400x400")

tk.Label(tk_root, text="Nombre del Cliente:").pack()
entry_nombre = tk.Entry(tk_root)
entry_nombre.pack()

tk.Label(tk_root, text="Correo Electrónico:").pack()
entry_email = tk.Entry(tk_root)
entry_email.pack()

tk.Label(tk_root, text="Número de Habitación:").pack()
entry_habitacion = tk.Entry(tk_root)  # Cambié a entry_habitacion
entry_habitacion.pack()

tk.Button(tk_root, text="Verificar Disponibilidad", command=verificar_disponibilidad).pack()

tk.Label(tk_root, text="Número de Días:").pack()
entry_dias = tk.Entry(tk_root)
entry_dias.pack()

tk.Button(tk_root, text="Reservar Habitación", command=realizar_reserva).pack()

tk_root.mainloop()