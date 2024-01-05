# Importar el módulo tkinter y el submódulo ttk para crear la interfaz gráfica
import tkinter as tk
from tkinter import ttk
import winsound

# Función para desvanecer gradualmente la ventana
def fade_out():
    # Obtener el valor actual de la propiedad de opacidad (alpha) de la ventana
    alpha = window.attributes("-alpha")

    # Verificar si la opacidad es mayor que 0
    if alpha > 0:
        # Reducir la opacidad en 0.05
        window.attributes("-alpha", alpha - 0.05)

        # Programar una llamada recursiva después de 50 milisegundos
        window.after(50, fade_out)
    else:
        # Cuando la opacidad llega a 0, destruir la ventana
        window.destroy()

# Crear la ventana principal
window = tk.Tk()
# Reproducir un sonido después de cierto tiempo
window.after(1500, lambda: winsound.PlaySound("notification_sound.wav", winsound.SND_FILENAME))
"""""
sound = winsound.PlaySound("notification_sound.wav", winsound.SND_FILENAME)
window.after(1500, lambda: sound)
"""""
# Configurar el título de la ventana
window.title("ERROR AL COLOCAR LA MANO")

# Configurar el ícono de la ventana
icon_image = tk.PhotoImage(file="logo_museo.png")
window.iconphoto(False, icon_image)

"""""
# Cambiar dinámicamente el color de fondo
def change_background_color():
    current_color = window.cget("bg")
    new_color = "yellow" if current_color == "red" else "red"
    window.configure(bg=new_color)
    window.after(1000, change_background_color)

# Llamar a la función para cambiar el color después de un tiempo
window.after(2000, change_background_color)
"""""

# Crear una etiqueta en la ventana con un mensaje y configuraciones de fuente y color
label = tk.Label(window, text="Coloque nuevamente la mano", font=("Arial", 16), fg="red")

# Empaquetar la etiqueta en la ventana con márgenes
label.pack(padx=32, pady=32)

# Configurar el margen en centímetros y calcular el equivalente en píxeles
margen_centimetros = 5
margen_pixeles = int(margen_centimetros * 37.8)

# Configurar la geometría de la ventana con un desplazamiento horizontal
window.geometry(f"+{margen_pixeles}+0")

# Configurar el grosor del borde y el color de fondo de la ventana
border_width = 5
window.configure(bg="#f0f0f0", bd=border_width, relief=tk.RAISED)

# Iniciar el temporizador para el cierre automático después de 2 segundos
window.after(2000, fade_out)

# Iniciar el bucle principal de Tkinter para mantener la interfaz gráfica en ejecución
window.mainloop()
