from tkinter import Canvas, Tk, Frame
from math import cos, sin, radians
import time

ventana = Tk()
ventana.title('ProgressBar Circular')
ventana.geometry('620x650-10+10')
ventana.config(bg='black')
ventana.overrideredirect(1)

frame = Frame(ventana, height=600, width=600, bg='black', relief='sunken')
frame.grid(columnspan=2, row=0)

canvas = Canvas(frame, bg='black', width=585, height=585, relief='raised', bd=1)
canvas.grid(padx=5, pady=5)

nivel = 0
inicio_tiempo = 0
duracion = 5

def calculate_coordinates(nivel):
    # Calcula las coordenadas de inicio y fin de la barra de progreso
    centro_x = (100 + 500) / 2
    centro_y = (100 + 500) / 2
    inicio_x = centro_x + 120 * sin(radians(nivel))  # Ajuste de la posición inicial
    inicio_y = centro_y - 120 * cos(radians(nivel))
    final_x = centro_x + 120 * sin(radians(nivel + 8))
    final_y = centro_y - 120 * cos(radians(nivel + 8))
    return inicio_x, inicio_y, final_x, final_y

def draw_progress_bar(inicio_x, inicio_y, final_x, final_y):
    # Dibuja la barra de progreso en el lienzo
    canvas.create_line(inicio_x, inicio_y, final_x, final_y,
                       fill='deep sky blue', width=60)  # Modificar el ancho de la línea

def draw_circles_and_text(centro_x, centro_y):
    # Dibuja los círculos y el texto en el lienzo
    canvas.create_oval(150, 150, 450, 450, fill='', outline='dark violet', width=5)
    canvas.create_oval(180, 180, 420, 420, fill='gray22', outline='dark violet', width=5)

    texto = int((nivel / 3.6))
    texto = str(texto) + '%'
    canvas.create_text(centro_x, centro_y, text=texto, font=('Arial', 42, 'bold'), fill='deep sky blue')
    canvas.create_text(centro_x, centro_y + 50, text='NO QUITE', font=('Cambria Math', 22, 'bold'), fill='white')
    canvas.create_text(centro_x, centro_y + 80, text='LA MANO', font=('Cambria Math', 25, 'bold'), fill='orange')

def update_progress_bar():
    global nivel, inicio_tiempo

    tiempo_actual = time.time()
    tiempo_transcurrido = tiempo_actual - inicio_tiempo

    if tiempo_transcurrido < duracion:
        nivel = int((tiempo_transcurrido / duracion) * 360)
        nivel %= 360

        canvas.create_oval(100, 100, 500, 500, fill="", outline='', width=5)

        inicio_x, inicio_y, final_x, final_y = calculate_coordinates(nivel)
        draw_progress_bar(inicio_x, inicio_y, final_x, final_y)

        centro_x = (100 + 500) / 2
        centro_y = (100 + 500) / 2

        draw_circles_and_text(centro_x, centro_y)

        ventana.after(10, update_progress_bar)
    else:
        nivel = 359
        canvas.create_oval(100, 100, 500, 500, fill="", outline='', width=5)

        inicio_x, inicio_y, final_x, final_y = calculate_coordinates(nivel)
        draw_progress_bar(inicio_x, inicio_y, final_x, final_y)

        centro_x = (100 + 500) / 2
        centro_y = (100 + 500) / 2

        draw_circles_and_text(centro_x, centro_y)

        ventana.after(500, ventana.destroy)

inicio_tiempo = time.time()
update_progress_bar()
ventana.mainloop()
