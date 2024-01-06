import tkinter as tk
from tkinter import ttk, filedialog, StringVar, IntVar
from ttkthemes import ThemedStyle
from rembg import remove
from PIL import Image, ImageTk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Remover Fondo de Imagen")
        self.root.configure(bg='white')

        self.style = ThemedStyle(self.root)
        self.style.set_theme("plastik")

        self.main_frame = ttk.Frame(self.root, padding=(20, 20, 20, 20), style='My.TFrame')
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.open_button = ttk.Button(self.main_frame, text="Seleccionar Imagen", command=self.open_file_dialog, style='TButton')
        self.style.configure('TButton', font=('Arial', 12))
        self.open_button.grid(row=0, column=0, pady=10)

        self.input_label = ttk.Label(self.main_frame, text="Imagen Original", font=('Arial', 12, 'bold'))
        self.output_label = ttk.Label(self.main_frame, text="Imagen Sin Fondo", font=('Arial', 12, 'bold'))

        self.input_label.grid(row=2, column=0, pady=5)
        self.output_label.grid(row=2, column=1, pady=5)

        self.options_menu = tk.Menu(self.root)
        self.options_menu.add_command(label="Configuración", command=self.open_options_window)
        self.root.config(menu=self.options_menu)

        self.output_quality = IntVar()
        self.output_format = StringVar()
        self.output_format.set("PNG")  # Formato predeterminado

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.ico;*.tiff;*.webp")])
        if file_path:
            self.process_image(file_path)

    def process_image(self, file_path):
        input_image = Image.open(file_path)
        output_image = remove(input_image)

        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"),
                                                                                       ("JPEG files", "*.jpg;*.jpeg"),
                                                                                       ("TIFF files", "*.tiff"),
                                                                                       ("GIF files", "*.gif"),
                                                                                       ("BMP files", "*.bmp"),
                                                                                       ("ICO files", "*.ico"),
                                                                                       ("WebP files", "*.webp")])
        if output_path:
            output_image.save(output_path, format=self.output_format.get(), quality=self.output_quality.get())
            self.show_images(input_image, output_image)

    def show_images(self, input_image, output_image):
        input_image.thumbnail((200, 200))
        output_image.thumbnail((200, 200))

        input_photo = ImageTk.PhotoImage(input_image)
        output_photo = ImageTk.PhotoImage(output_image)

        self.input_label.config(image=input_photo)
        self.output_label.config(image=output_photo)

        self.input_label.image = input_photo
        self.output_label.image = output_photo

    def open_options_window(self):
        options_window = tk.Toplevel(self.root)
        options_window.title("Configuración")

        quality_label = ttk.Label(options_window, text="Calidad de Salida:")
        quality_label.grid(row=0, column=0, padx=10, pady=10)

        quality_scale = ttk.Scale(options_window, from_=1, to=100, orient=tk.HORIZONTAL, variable=self.output_quality)
        quality_scale.set(90)
        quality_scale.grid(row=0, column=1, padx=10, pady=10)

        format_label = ttk.Label(options_window, text="Formato de Archivo:")
        format_label.grid(row=1, column=0, padx=10, pady=10)

        format_combobox = ttk.Combobox(options_window, values=["PNG", "JPEG", "TIFF", "GIF", "BMP", "ICO", "WebP"], textvariable=self.output_format)
        format_combobox.set(self.output_format.get())  # Seleccionar el formato actual
        format_combobox.grid(row=1, column=1, padx=10, pady=10)

# Crear la aplicación
root = tk.Tk()
app = App(root)
root.mainloop()
