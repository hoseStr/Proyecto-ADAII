"""
Utilidades combinadas para tema e interfaz de usuario de la aplicación ModCI
"""
import tkinter as tk
from tkinter import ttk, font
import time
import math

from algorithms.fuerza_bruta import rocFB
from algorithms.voraz import rocV
from algorithms.programacion_dinamica import rocPD
from utils.file_manager import leer_instancia, guardar_salida_desde_entrada

class UIManager:
    """Clase para gestionar la interfaz de usuario y los temas de la aplicación"""


    def __init__(self, root):
        import os
        from tkinter import filedialog
        self.root = root
        self.current_theme = "light"

        # Definir tema único (claro)
        self.theme = {
            "bg": "#f5f5f5",
            "fg": "#333333",
            "text_bg": "white",
            "border": "#dddddd"
        }

        # Configurar el tema
        self.apply_theme()

        # --- Interfaz personalizada ---
        self.frame = ttk.Frame(self.root)
        self.frame.pack(padx=30, pady=30)

        # Apartado para seleccionar archivo de prueba
        self.ruta_entrada = ""
        self.file_frame = ttk.Frame(self.frame)
        self.file_frame.pack(fill='x', pady=(0, 10))
        self.file_btn = ttk.Button(self.file_frame, text="Seleccionar archivo de prueba", command=self.seleccionar_archivo)
        self.file_btn.pack(side='left')
        # Área para mostrar la entrada (debajo del botón de archivo)
        from tkinter import scrolledtext
        self.file_label = ttk.Label(self.file_frame, text=os.path.basename(self.ruta_entrada), width=30, foreground='#1565c0')
        self.file_label.pack(side='left', padx=(10,0))
        self.input_label = ttk.Label(self.frame, text="Entrada seleccionada:")
        self.input_label.pack(pady=(5, 0))
        self.input_text = scrolledtext.ScrolledText(self.frame, height=8, width=60, wrap=tk.WORD, state='disabled')
        self.input_text.pack(pady=(0, 10))

        # Apartado para seleccionar algoritmo (debajo del área de entrada)
        self.label = ttk.Label(self.frame, text="Seleccione el algoritmo a ejecutar:")
        self.label.pack(pady=(0, 10))

        self.btn_fb = ttk.Button(self.frame, text="Fuerza Bruta", command=self.run_fb)
        self.btn_fb.pack(fill='x', pady=2)

        self.btn_vz = ttk.Button(self.frame, text="Voraz", command=self.run_vz)
        self.btn_vz.pack(fill='x', pady=2)

        self.btn_pd = ttk.Button(self.frame, text="Programación Dinámica", command=self.run_pd)
        self.btn_pd.pack(fill='x', pady=2)

        # Área para mostrar la salida (resultado)
        self.output_label = ttk.Label(self.frame, text="Salida:")
        self.output_label.pack(pady=(5, 0))
        self.output_text = scrolledtext.ScrolledText(self.frame, height=8, width=60, wrap=tk.WORD, state='disabled')
        self.output_text.pack(pady=(0, 10))

        # Botón para guardar la salida en archivo derivado del archivo de entrada
        self.save_btn = ttk.Button(self.frame, text="Guardar salida (nombre de entrada)", command=self._save_output, state='disabled')
        self.save_btn.pack(fill='x', pady=(0, 10))

        # Etiqueta para mostrar estado/resultado breve (ej: "Calculando..." o resumen)
        self.result_label = ttk.Label(self.frame, text="", foreground='#00695c')
        self.result_label.pack(pady=(5, 0))

        # Spinner state defaults (spinner drawing is optional)
        self._spinner_running = False
        self._spinner_angle = 0
        # canvas reserved for spinner if needed later
        self.spinner_canvas = tk.Canvas(self.frame, width=40, height=40, bg=self.theme["bg"], highlightthickness=0)
        # no pack by default; only used if spinner is enabled

        # Texto por defecto para widgets de tipo texto
        self.text_config = {
            "bg": self.theme["text_bg"],
            "fg": self.theme["fg"],
            "font": ("Consolas", 10),
            "selectbackground": "#a6a6a6",
            "selectforeground": "white",
            "borderwidth": 1,
            "relief": "solid",
            "insertbackground": self.theme["fg"]
        }

    def seleccionar_archivo(self):
        from tkinter import filedialog
        import os
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de prueba",
            initialdir="BateriaPruebas",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        if ruta:
            self.ruta_entrada = ruta
            self.file_label.config(text=os.path.basename(ruta), foreground='#1565c0')
            # Mostrar contenido del archivo en el área de entrada
            try:
                with open(ruta, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                self.input_text.config(state='normal')
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(tk.END, contenido)
                self.input_text.config(state='disabled')
            except Exception as e:
                self.input_text.config(state='normal')
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(tk.END, f"Error al leer archivo: {e}")
                self.input_text.config(state='disabled')


    def apply_theme(self):
        theme = self.theme
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=10)
        heading_font = font.Font(family="Segoe UI", size=12, weight="bold")
        style = ttk.Style()
        style.configure(".", background=theme["bg"], foreground=theme["fg"])
        style.configure("TFrame", background=theme["bg"])
        style.configure("TLabelframe", background=theme["bg"])
        style.configure("TLabelframe.Label", background=theme["bg"], foreground=theme["fg"], font=heading_font)
        style.configure("TLabel", background=theme["bg"], foreground=theme["fg"])
        style.configure("TButton", padding=(5, 2))
        style.configure("Primario.TButton", padding=(5, 2))
        style.configure("Secundario.TButton", padding=(5, 2))
        style.configure("Acento.TButton", padding=(5, 2))
        self.root.configure(background=theme["bg"])

    def run_algorithm(self, algofunc):
        # Deshabilitar botones y mostrar spinner avanzado
        self.btn_fb.config(state='disabled')
        self.btn_vz.config(state='disabled')
        self.btn_pd.config(state='disabled')
        self.result_label.config(text="Calculando, por favor espere...")

    # Eliminado spinner, solo texto de carga
        self.root.update_idletasks()

        # Ejecutar algoritmo en segundo plano para no congelar la interfaz
        import threading
        threading.Thread(target=lambda: self._run_algorithm_bg(algofunc), daemon=True).start()

    def _run_algorithm_bg(self, algofunc):
        instancia = leer_instancia(self.ruta_entrada)
        start = time.time()
        asign, costo = algofunc(instancia)
        elapsed = time.time() - start
        # Guardar último resultado para permitir guardado a disco
        self._last_result = {
            'costo': costo,
            'asignaciones': asign,
            'elapsed': elapsed
        }
        # Preparar salida en texto
        salida_lines = [f"Insatisfacción: {costo:.4f}", f"Tiempo: {elapsed:.6f} s", "Asignaciones:"]
        for est, mats in asign.items():
            salida_lines.append(f"{est}: {', '.join(mats)}")
        salida_text = '\n'.join(salida_lines)
        # Actualizar la interfaz en el hilo principal
        self.root.after(0, lambda: self._show_result(costo, elapsed, salida_text))

    def _show_result(self, costo, elapsed, salida_text):
        # Mostrar resultado en el área de salida
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, salida_text)
        self.output_text.config(state='disabled')
        self.result_label.config(text=f"Insatisfacción: {costo:.4f}\nTiempo: {elapsed:.6f} s")
        self.btn_fb.config(state='normal')
        self.btn_vz.config(state='normal')
        self.btn_pd.config(state='normal')
        # Habilitar botón de guardar si existe ruta de entrada y resultado
        if getattr(self, 'ruta_entrada', '') and hasattr(self, '_last_result'):
            self.save_btn.config(state='normal')
        else:
            self.save_btn.config(state='disabled')

    def _animate_spinner(self):
        if not self._spinner_running:
            self.spinner_canvas.delete("all")
            return
        self.spinner_canvas.delete("all")
        x, y, r = 20, 20, 16
        width = 4
        extent = 90
        # Dibuja un arco que rota
        self.spinner_canvas.create_arc(
            x - r, y - r, x + r, y + r,
            start=self._spinner_angle, extent=extent,
            style=tk.ARC, outline="#0078D7", width=width
        )
        self._spinner_angle = (self._spinner_angle + 10) % 360
        self.root.after(16, self._animate_spinner)

    def run_fb(self):
        self.run_algorithm(rocFB)

    def run_vz(self):
        self.run_algorithm(rocV)

    def run_pd(self):
        self.run_algorithm(rocPD)
        # Si se requiere configuración para widgets de texto, usar self.theme
        self.text_config = {
            "bg": self.theme["text_bg"],
            "fg": self.theme["fg"],
            "font": ("Consolas", 10),
            "selectbackground": "#a6a6a6",
            "selectforeground": "white",
            "borderwidth": 1,
            "relief": "solid",
            "insertbackground": self.theme["fg"]  # Color del cursor
        }
        return self.text_config

    def _save_output(self):
        """Guarda la última salida en un archivo cuyo nombre deriva del archivo de entrada."""
        if not getattr(self, 'ruta_entrada', None):
            # No hay archivo de entrada seleccionado
            self.result_label.config(text="No hay archivo de entrada seleccionado para derivar el nombre.")
            return
        if not hasattr(self, '_last_result'):
            self.result_label.config(text="No hay resultado para guardar.")
            return
        ruta = guardar_salida_desde_entrada(self.ruta_entrada, self._last_result['costo'], self._last_result['asignaciones'])
        self.result_label.config(text=f"Salida guardada en: {ruta}")
    
    # Método toggle_theme eliminado ya que no será necesario
    
    def get_text_config(self):
        """Devuelve la configuración para widgets de texto"""
        return self.text_config
    
    def get_current_theme(self):
        """Devuelve el nombre del tema actual"""
        return self.current_theme

def create_tooltip(widget, text):
    """Crea un tooltip para un widget"""
    tooltip = tk.Label(widget.master, text=text, background="#ffffe0", relief="solid", borderwidth=1)
    tooltip.config(font=("Segoe UI", 8))
    
    def enter(event):
        x = widget.winfo_rootx() + widget.winfo_width() // 2
        y = widget.winfo_rooty() + widget.winfo_height() + 5
        tooltip.lift()
        tooltip.place(x=x, y=y, anchor="n")
    
    def leave(event):
        tooltip.place_forget()
    
    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)
    
    return tooltip

def create_button(parent, text, command, style="TButton", tooltip_text=None):
    """
    Crea un botón con estilo y opcionalmente un tooltip
    
    Args:
        parent: Widget padre
        text: Texto del botón
        command: Función a ejecutar
        style: Estilo del botón (TButton, Primario.TButton, etc.)
        tooltip_text: Texto del tooltip (opcional)
    
    Returns:
        El botón creado
    """
    btn = ttk.Button(parent, text=text, command=command, style=style)
    
    if tooltip_text:
        create_tooltip(btn, tooltip_text)
        