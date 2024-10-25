import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ExifTags

def seleccionar_imagen():
    # Abre un cuadro de diálogo para seleccionar la imagen
    filepath = filedialog.askopenfilename(
        filetypes=[("Imagenes JPG", "*.jpg"), ("Imagenes PNG", "*.png"), ("Todos los archivos", "*.*")]
    )
    if filepath:
        lbl_ruta.config(text=f"Imagen seleccionada: {filepath}")
        global imagen
        imagen = Image.open(filepath)
        
        # Corregir la orientación si es necesario
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = imagen._getexif()
            if exif and orientation in exif:
                if exif[orientation] == 3:
                    imagen = imagen.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    imagen = imagen.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    imagen = imagen.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # La imagen no tiene información EXIF o no se puede rotar
            pass

def exportar_imagen():
    if imagen is None:
        messagebox.showerror("Error", "Primero selecciona una imagen.")
        return
    
    # Pedir la calidad de exportación
    try:
        calidad = int(entrada_calidad.get())
        if not (0 <= calidad <= 100):
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Ingresa un valor de calidad entre 0 y 100.")
        return
    
    # Guardar la imagen con la calidad especificada
    save_path = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[("Imagen JPG", "*.jpg")]
    )
    if save_path:
        imagen.save(save_path, quality=calidad)
        messagebox.showinfo("Exportación completa", "Imagen exportada con éxito.")

# Configurar la ventana principal
ventana = tk.Tk()
ventana.title("Reductor de tamaño de imágenes")
ventana.geometry("400x200")

# Variables globales
imagen = None

# Etiqueta y botón para seleccionar la imagen
btn_seleccionar = tk.Button(ventana, text="Seleccionar imagen", command=seleccionar_imagen)
btn_seleccionar.pack(pady=10)

lbl_ruta = tk.Label(ventana, text="No se ha seleccionado ninguna imagen")
lbl_ruta.pack()

# Entrada y etiqueta para ajustar la calidad
lbl_calidad = tk.Label(ventana, text="Calidad de la imagen (0-100):")
lbl_calidad.pack()

entrada_calidad = tk.Entry(ventana)
entrada_calidad.insert(0, "50")  # Valor predeterminado de calidad
entrada_calidad.pack()

# Botón para exportar la imagen
btn_exportar = tk.Button(ventana, text="Exportar imagen", command=exportar_imagen)
btn_exportar.pack(pady=10)

ventana.mainloop()
