import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import os
import re

# Datos de ejemplo de habitaciones reservadas (simulación)
habitaciones_reservadas = {
    '101': False,
    '102': True,  # Esta habitación está ocupada
    '103': False,
}

def verificar_disponibilidad():
    habitacion = entry_habitacion.get()
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

    # Validaciones de entrada
    if not nombre or not email or not codigo or not dias:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):  # Validar formato de email
        messagebox.showerror("Error", "Por favor, ingresa un correo electrónico válido.")
        return

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
    
    try:
        # Crear un documento PDF con formato
        doc = SimpleDocTemplate(archivo, pagesize=letter)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(name="Title", fontSize=18, alignment=1, fontName="Helvetica-Bold", textColor=colors.darkblue)
        text_style = ParagraphStyle(name="Text", fontSize=12, fontName="Helvetica", textColor=colors.black)
        
        # Encabezado
        title = Paragraph("Comprobante de Reserva", title_style)
        elements.append(title)
        elements.append(Spacer(1, 20))  # Espaciado entre el título y el contenido

        # Información de la reserva
        elements.append(Paragraph(f"<b>Nombre:</b> {nombre}", text_style))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"<b>Habitación:</b> {habitacion}", text_style))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"<b>Días:</b> {dias}", text_style))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"<b>Total a pagar:</b> ${total_pagar}", text_style))
        elements.append(Spacer(1, 30))  # Espaciado final

        # Detalles adicionales o pie de página
        footer_style = ParagraphStyle(name="Footer", fontSize=10, alignment=1, fontName="Helvetica-Oblique", textColor=colors.grey)
        footer = Paragraph("Gracias por elegirnos. ¡Esperamos verte pronto!", footer_style)
        elements.append(footer)

        # Crear el documento PDF
        doc.build(elements)

        # Abrir el PDF automáticamente
        os.system(f"start {archivo}")
    
    except Exception as e:
        print(f"No se pudo generar el comprobante. Error: {e}")

# Configuración de la interfaz
tk_root = tk.Tk()
tk_root.title("Sistema Hotelero")
tk_root.geometry("450x500")
tk_root.configure(bg='#f0f0f0')  # Fondo de pantalla suave

# Título de la aplicación
title_label = tk.Label(tk_root, text="Reserva de Habitaciones", font=("Arial", 16, "bold"), fg="#333", bg="#f0f0f0")
title_label.pack(pady=10)

# Etiquetas y campos de entrada con mejoras visuales
tk.Label(tk_root, text="Nombre del Cliente:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
entry_nombre = tk.Entry(tk_root, font=("Arial", 12), bd=2, relief="solid", width=30)
entry_nombre.pack(pady=5)

tk.Label(tk_root, text="Correo Electrónico:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
entry_email = tk.Entry(tk_root, font=("Arial", 12), bd=2, relief="solid", width=30)
entry_email.pack(pady=5)

tk.Label(tk_root, text="Número de Habitación:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
entry_habitacion = tk.Entry(tk_root, font=("Arial", 12), bd=2, relief="solid", width=30)
entry_habitacion.pack(pady=5)

tk.Button(tk_root, text="Verificar Disponibilidad", font=("Arial", 12), bg="#4CAF50", fg="white", command=verificar_disponibilidad, width=20).pack(pady=10)

tk.Label(tk_root, text="Número de Días:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
entry_dias = tk.Entry(tk_root, font=("Arial", 12), bd=2, relief="solid", width=30)
entry_dias.pack(pady=5)

tk.Button(tk_root, text="Reservar Habitación", font=("Arial", 12), bg="#2196F3", fg="white", command=realizar_reserva, width=20).pack(pady=15)

# Espaciado final para que la ventana no quede pegada a la parte inferior
tk_root.mainloop()

