#importacion de librerias 
from tkinter import Canvas, Tk, Frame
from math import cos, sin, radians
import time

# Crear la ventana principal de la aplicación
ventana = Tk()
# Configurar la geometría y el fondo de la ventana
ventana.geometry('560x500-10+5')
ventana.config(bg='black')
# ocultar la barra de titulo
#ventana.overrideredirect(1) 

# Crear un marco en la ventana para contener otros elementos
frame = Frame(ventana, height=600, width=600, bg='black', relief='sunken')
frame.grid(columnspan=2, row=0)

# Crear un lienzo (canvas) dentro del marco para dibujar elementos gráficos
canvas = Canvas(frame, bg='black', width=685, height=485, bd=0)
canvas.grid(padx=5, pady=5)

# Establecer el tiempo de inicio del programa
inicio_tiempo = time.time()
# Establecer la duración de la barra de progreso en segundos
duracion = 5

# Función que calcula las coordenadas de inicio y fin de la barra de progreso
def calculate_coordinates(nivel):
    centro_x = (100 + 500) / 2
    centro_y = (100 + 500) / 2
    inicio_x = centro_x + 120 * sin(radians(nivel))
    inicio_y = centro_y - 120 * cos(radians(nivel))
    final_x = centro_x + 120 * sin(radians(nivel + 8))
    final_y = centro_y - 120 * cos(radians(nivel + 8))
    return inicio_x, inicio_y, final_x, final_y

# Función que dibuja la barra de progreso en el lienzo
def draw_progress_bar(inicio_x, inicio_y, final_x, final_y):
    canvas.create_line(inicio_x, inicio_y, final_x, final_y,
                       fill='deep sky blue', width=60)
    
# Función que dibuja círculos y texto en el lienzo
def draw_circles_and_text(centro_x, centro_y):
    canvas.create_oval(150, 150, 450, 450, fill='', outline='dark violet', width=5)
    canvas.create_oval(180, 180, 420, 420, fill='gray22', outline='dark violet', width=5)

    texto = int((nivel / 3.6))
    texto = str(texto) + '%'
    canvas.create_text(centro_x, centro_y, text=texto, font=('Arial', 42, 'bold'), fill='deep sky blue')
    canvas.create_text(centro_x, centro_y + 50, text='NO QUITE', font=('Cambria Math', 22, 'bold'), fill='white')
    canvas.create_text(centro_x, centro_y + 80, text='LA MANO', font=('Cambria Math', 25, 'bold'), fill='orange')

# Función que actualiza dinámicamente la barra de progreso
def update_progress_bar():
    global nivel

    # Obtener el tiempo actual
    tiempo_actual = time.time()
    # Calcular el tiempo transcurrido desde el inicio del programa
    tiempo_transcurrido = tiempo_actual - inicio_tiempo

    # Verificar si el tiempo transcurrido es menor que la duración especificada
    if tiempo_transcurrido < duracion:
        # Calcular el nivel de la barra de progreso en función del tiempo
        nivel = int((tiempo_transcurrido / duracion) * 360)
        nivel %= 360

       # Limpiar el lienzo
        canvas.create_oval(100, 100, 500, 500, fill="", outline='', width=5)
         # Calcular las coordenadas de inicio y fin de la barra de progreso
        inicio_x, inicio_y, final_x, final_y = calculate_coordinates(nivel)

        # Dibujar la barra de progreso en el lienzo
        draw_progress_bar(inicio_x, inicio_y, final_x, final_y)

       # Calcular las coordenadas del centro
        centro_x = (100 + 500) / 2
        centro_y = (100 + 500) / 2

        # Dibujar círculos y texto en el lienzo
        draw_circles_and_text(centro_x, centro_y)
        # Programar una nueva actualización después de 10 milisegundos
        ventana.after(10, update_progress_bar)
    else:
        # Cuando la duración ha pasado, establecer el nivel en su valor máximo
        nivel = 359

        # Limpiar el lienzo
        canvas.create_oval(100, 100, 500, 500, fill="", outline='', width=5)

        # Calcular las coordenadas de inicio y fin de la barra de progreso
        inicio_x, inicio_y, final_x, final_y = calculate_coordinates(nivel)

        # Dibujar la barra de progreso en el lienzo
        draw_progress_bar(inicio_x, inicio_y, final_x, final_y)

        # Calcular las coordenadas del centro
        centro_x = (100 + 500) / 2
        centro_y = (100 + 500) / 2

        # Dibujar círculos y texto en el lienzo
        draw_circles_and_text(centro_x, centro_y)

        # Programar la destrucción de la ventana después de 500 milisegundos
        ventana.after(500, ventana.destroy)
# Iniciar el proceso de actualización de la barra de progreso
update_progress_bar()
# Iniciar el bucle principal de Tkinter para mantener la interfaz gráfica en ejecución
ventana.mainloop()
