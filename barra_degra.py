from tkinter import Canvas, Tk, Frame
from math import cos, sin, radians
import time

ventana = Tk()
ventana.geometry('560x500-10+5')
ventana.config(bg='black')
ventana.overrideredirect(1)

frame = Frame(ventana, height=600, width=600, bg='black', relief='sunken')
frame.grid(columnspan=2, row=0)

canvas = Canvas(frame, bg='black', width=545, height=485, bd=1)
canvas.grid(padx=5, pady=5)

inicio_tiempo = time.perf_counter()
duracion = 5

def calculate_coordinates(nivel):
    centro_x = (100 + 500) / 2 - 30
    centro_y = (100 + 500) / 2 - 30
    inicio_x = centro_x + 120 * sin(radians(nivel))
    inicio_y = centro_y - 120 * cos(radians(nivel))
    final_x = centro_x + 120 * sin(radians(nivel + 8))
    final_y = centro_y - 120 * cos(radians(nivel + 8))
    return inicio_x, inicio_y, final_x, final_y

def draw_progress_bar(inicio_x, inicio_y, final_x, final_y, gradiente):
    color = f'#{gradiente[0]:02X}{gradiente[1]:02X}{gradiente[2]:02X}'  # RGB color
    canvas.create_line(inicio_x, inicio_y, final_x, final_y, fill=color, width=60)
    

def draw_circles_and_text(centro_x, centro_y):
    centro_x -= 30  # Ajusta según sea necesario
    centro_y -= 30  # Ajusta según sea necesario
    canvas.create_oval(150 - 30, 150 - 30, 450 - 30, 450 - 30, fill='', outline='dark violet', width=5)
    canvas.create_oval(180 - 30, 180 - 30, 420 - 30, 420 - 30, fill='gray22', outline='dark violet', width=5)

    centro_x += 35  # Puedes ajustar este valor según sea necesario

    texto = int((nivel / 3.6))
    texto = str(texto) + '%'
    canvas.create_text(centro_x, centro_y, text=texto, font=('Arial', 42, 'bold'), fill='deep sky blue')
    canvas.create_text(centro_x, centro_y + 50, text='NO QUITE', font=('Cambria Math', 22, 'bold'), fill='white')
    canvas.create_text(centro_x, centro_y + 80, text='LA MANO', font=('Cambria Math', 25, 'bold'), fill='orange')

def update_progress_bar():
    global nivel, inicio_tiempo

    tiempo_actual = time.perf_counter()
    tiempo_transcurrido = tiempo_actual - inicio_tiempo

    print(f"Tiempo transcurrido: {tiempo_transcurrido:.4f} segundos")

    if tiempo_transcurrido < duracion:
        nivel = int((tiempo_transcurrido / duracion) * 360)
        nivel %= 360

        canvas.create_oval(100, 100, 500, 500, fill="", outline='', width=5)
        inicio_x, inicio_y, final_x, final_y = calculate_coordinates(nivel)

        r = int((nivel / 360) * 255)
        g = 255 - r
        b = 0
        gradiente = (r, g, b)
        draw_progress_bar(inicio_x, inicio_y, final_x, final_y, gradiente)

        centro_x = (100 + 500) / 2 - 30
        centro_y = (100 + 500) / 2 - 30
        draw_circles_and_text(centro_x, centro_y)

        ventana.after(60, update_progress_bar)  # Aumenta el intervalo a 50 ms
    else:
        nivel = 360
        canvas.create_oval(100, 100, 500, 500, fill="", outline='', width=5)
        inicio_x, inicio_y, final_x, final_y = calculate_coordinates(nivel)

        gradiente = (255, 0, 0)
        draw_progress_bar(inicio_x, inicio_y, final_x, final_y, gradiente)

        centro_x = (100 + 500) / 2 - 30
        centro_y = (100 + 500) / 2 - 30
        draw_circles_and_text(centro_x, centro_y)

        ventana.after(500, ventana.destroy)

update_progress_bar()
ventana.mainloop()
