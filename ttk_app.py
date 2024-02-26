import tkinter as tk
from tkinter import ttk
import threading
from selenium_app import SeleniumApp

class TTKApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("400x200")
        self.master.resizable(False, False)
        style = ttk.Style()

        # Configurar el fondo con un color sólido
        self.master.configure(bg="#ECB107")  # Puedes cambiar "#ececec" al color que desees

        # Crear una barra superior con el nombre de la empresa
        style.configure("Top.TFrame", background="#00000")
        top_frame = ttk.Frame(master, style="Top.TFrame")
        top_frame.pack(side="top", fill="x")


        company_name_label = ttk.Label(top_frame, text="BIG PONS SA", foreground="#ECB107", background="#000000", font=("Arial", 14, "bold"))
        company_name_label.pack(pady=10)

        # Personalizar el estilo de los botones
        style.configure("TButton", foreground="#000000", background="#FFA600")  # Cambia el color según tus preferencias

        self.start_button = ttk.Button(master, text="Iniciar Proceso Selenium", command=self.on_start_button_click, style="TButton")
        self.start_button.pack(pady=20)


        self.progress_label = ttk.Label(master, text="Estado de ejecución: Esperando inicio", background="#FFA600", foreground="#000000", font=("Arial", 10, "bold"))
        self.progress_label.pack(pady=10)

        # Crear un pie de página con derechos de autor
        style.configure("Bottom.TFrame", background="#2c3e50")
        bottom_frame = ttk.Frame(master, style="Bottom.TFrame")
        bottom_frame.pack(side="bottom", fill="x")

        copyright_label = ttk.Label(bottom_frame, text="© 2024 Derechos de Autor", foreground="#ffffff", background="#2c3e50")
        copyright_label.pack(pady=5)

    def on_start_button_click(self):
        self.start_button.config(state=tk.DISABLED)
        self.progress_label.config(text="Estado de ejecución: Iniciando...")
        threading.Thread(target=self.run_selenium_process, daemon=True).start()

    def run_selenium_process(self):
        selenium_app = SeleniumApp(self.progress_label)
        selenium_app.run()