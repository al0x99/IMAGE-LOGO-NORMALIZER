from PIL import Image, ImageOps
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import os
import io
import tkinter as tk
from tkinter import filedialog

# imposta le dimensioni del rettangolo
rectangle_width = 500
rectangle_height = 300

# apri la finestra di dialogo per selezionare la cartella dei loghi
root = tk.Tk()
root.withdraw()
logos_path = filedialog.askdirectory()

# apri la finestra di dialogo per selezionare la cartella di salvataggio
root = tk.Tk()
root.withdraw()
save_path = filedialog.askdirectory()

# ciclo attraverso ogni file nella cartella dei loghi
for filename in os.listdir(logos_path):
    # verifica che il file sia un'immagine PNG, JPG, JPEG o SVG
    if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.svg'):
        # apre il file immagine del logo
        logo_path = os.path.join(logos_path, filename)

        if filename.endswith('.svg'):
            # converte il file SVG in immagine PIL
            drawing = svg2rlg(logo_path)
            logo = Image.open(io.BytesIO(renderPM.drawToString(drawing)))
        else:
            logo = Image.open(logo_path)

        # ottiene le dimensioni del logo
        logo_width, logo_height = logo.size

        # calcola la scala di ridimensionamento
        scale = min(rectangle_width / logo_width, rectangle_height / logo_height)

        # ridimensiona il logo
        new_width = int(logo_width * scale)
        new_height = int(logo_height * scale)
        logo = logo.resize((new_width, new_height))

        # crea un'immagine bianca del rettangolo
        rectangle = Image.new("RGB", (rectangle_width, rectangle_height), color="white")

        # calcola la posizione del logo nel rettangolo
        x_offset = int((rectangle_width - new_width) / 2)
        y_offset = int((rectangle_height - new_height) / 2)

        # posiziona il logo nel rettangolo
        rectangle.paste(logo, (x_offset, y_offset))

        # converti l'immagine in RGBA se ha una tavolozza di colori
        if rectangle.mode == 'P':
            rectangle = rectangle.convert('RGBA')

        # verifica se l'immagine ha un canale alfa e lo imposta a 255 (completamente opaco)
        if 'A' in rectangle.getbands():
            rectangle.putalpha(255)

        # rende l'immagine bianco e nero
        rectangle = ImageOps.grayscale(rectangle)

        # salva l'immagine in formato PNG nella cartella di salvataggio selezionata
        new_filename = os.path.splitext(filename)[0] + '_logoblackandwhite.png'
        new_path = os.path.join(save_path, new_filename)
        rectangle.save(new_path, format='PNG', compress_level=9)
