import tkinter as tk
from tkinter import ttk, filedialog, StringVar, IntVar
from ttkthemes import ThemedStyle
from rembg import remove
from PIL import Image, ImageTk

def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.ico")])
    if file_path:
        process_image(file_path)

def process_image(file_path):
    input_image = Image.open(file_path)
    root.after(10, process_image_async, input_image)

def process_image_async(input_image):
    output_image = remove(input_image)

    output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if output_path:
        output_image.save(output_path, format=output_format.get(), quality=output_quality.get())

    show_images(input_image, output_image)

def show_images(input_image, output_image):
    input_image.thumbnail((200, 200))
    output_image.thumbnail((200, 200))

    input_photo = ImageTk.PhotoImage(input_image)
    output_photo = ImageTk.PhotoImage(output_image)

    input_label.config(image=input_photo)
    output_label.config(image=output_photo)

    input_label.image = input_photo
    output_label.image = output_photo

def open_options_window():
    options_window = tk.Toplevel(root)
    options_window.title("Configuración")

    quality_label = ttk.Label(options_window, text="Calidad de Salida:")
    quality_label.grid(row=0, column=0, padx=10, pady=10)

    quality_scale = ttk.Scale(options_window, from_=1, to=100, orient=tk.HORIZONTAL, variable=output_quality)
    quality_scale.set(90)
    quality_scale.grid(row=0, column=1, padx=10, pady=10)

    format_label = ttk.Label(options_window, text="Formato de Archivo:")
    format_label.grid(row=1, column=0, padx=10, pady=10)

    format_combobox = ttk.Combobox(options_window, values=["PNG", "JPEG"], textvariable=output_format)
    format_combobox.set("PNG")
    format_combobox.grid(row=1, column=1, padx=10, pady=10)

root = tk.Tk()
root.title("Remover Fondo de Imagen")
root.configure(bg='white')

style = ThemedStyle(root)
style.set_theme("plastik")

main_frame = ttk.Frame(root, padding=(20, 20, 20, 20), style='My.TFrame')
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

open_button = ttk.Button(main_frame, text="Seleccionar Imagen", command=open_file_dialog, style='TButton')
style.configure('TButton', font=('Arial', 12))

open_button.grid(row=0, column=0, pady=10)

input_label = ttk.Label(main_frame, text="Imagen Original", font=('Arial', 12, 'bold'))
output_label = ttk.Label(main_frame, text="Imagen Sin Fondo", font=('Arial', 12, 'bold'))

input_label.grid(row=2, column=0, pady=5)
output_label.grid(row=2, column=1, pady=5)

options_menu = tk.Menu(root)
options_menu.add_command(label="Configuración", command=open_options_window)
root.config(menu=options_menu)

output_quality = IntVar()
output_format = StringVar()

root.mainloop()
