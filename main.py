import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import json
from Errores import Error
from analizadorlexico import AnalizadorLexico
from prettytable import PrettyTable
from analizadorsintactico import AnalizadorSintactico

class VentanaPrincipal:
    def __init__(self, master):
        self.master = master
        master.title("Analizador Léxico")

        # Create side menu
        self.menu = tk.Frame(master, bg="gray")
        self.menu.pack(side="left", fill="y", expand=True)

        # Buttons in the side menu
        self.btn1 = tk.Button(self.menu, text="Nuevo", font=('Roboto', 12), background='#4CAF50', foreground='white', width=10,
                              borderwidth=0, highlightthickness=0, padx=10, pady=5, relief=tk.FLAT)
        self.btn1.pack(pady=10)

        self.btn1.bind("<Enter>", self.on_enter)
        self.btn1.bind("<Leave>", self.on_leave)

        self.btn2 = tk.Button(self.menu, text="Abrir archivo", font=('Roboto', 12), background='#4CAF50', foreground='white', width=10,
                              borderwidth=0, highlightthickness=0, padx=10, pady=5, relief=tk.FLAT, command=self.abrir_archivo)
        self.btn2.pack(pady=10)

        self.btn2.bind("<Enter>", self.on_enter)
        self.btn2.bind("<Leave>", self.on_leave)

        self.btn3 = tk.Button(self.menu, text="Analizar", font=('Roboto', 12), background='#4CAF50', foreground='white', width=10,
                              borderwidth=0, highlightthickness=0, padx=10, pady=5, relief=tk.FLAT, command=self.analizar_archivo)
        self.btn3.pack(pady=10)

        self.btn3.bind("<Enter>", self.on_enter)
        self.btn3.bind("<Leave>", self.on_leave)

        self.btn4 = tk.Button(self.menu, text="Ver tokens", font=('Roboto', 12), background='#4CAF50', foreground='white', width=10,
                              borderwidth=0, highlightthickness=0, padx=10, pady=5, relief=tk.FLAT, command=self.ver_tokens)
        self.btn4.pack(pady=10)

        self.btn4.bind("<Enter>", self.on_enter)
        self.btn4.bind("<Leave>", self.on_leave)

        self.btn5 = tk.Button(self.menu, text="Ver errores", font=('Roboto', 12), background='#4CAF50', foreground='white', width=10,
                              borderwidth=0, highlightthickness=0, padx=10, pady=5, relief=tk.FLAT, command=self.ver_errores)
        self.btn5.pack(pady=10)

        self.btn5.bind("<Enter>", self.on_enter)
        self.btn5.bind("<Leave>", self.on_leave)

        self.btn6 = tk.Button(self.menu, text="Salir", font=('Roboto', 12), background='#4CAF50', foreground='white', width=10,
                              borderwidth=0, highlightthickness=0, padx=10, pady=5, relief=tk.FLAT, command=self.salir)
        self.btn6.pack(pady=10)

        self.btn6.bind("<Enter>", self.on_enter)
        self.btn6.bind("<Leave>", self.on_leave)

        # Text areas for input and output
        self.text1 = tk.Text(master, bg="white", fg="black", font=("Courier", 10), wrap="word")
        self.text1.pack(side="left", fill="both", expand=True, padx=10, pady=10, anchor="nw")

        self.text2 = tk.Text(master, bg="white", fg="black", font=("Courier", 10), height=10)
        self.text2.pack(side="left", fill="both", expand=True, padx=10, pady=10, anchor="nw")

    def on_enter(self, event):
            event.widget.config(background='#45a049', foreground='black')  # Color de fondo más oscuro al pasar el cursor
    def on_leave(self, enter):
            enter.widget.config(background='#4CAF50', foreground='white')  # Restaurar color de fondo original

    def abrir_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=(("Archivos TXT", "*.txt"), ("Todos los archivos", "*.*")))
        if archivo:
            with open(archivo, 'r') as f:
                contenido = f.read()
                self.text1.delete("1.0", "end")
                self.text1.insert("1.0", contenido)

    def analizar_archivo(self):
       pass



    def ver_tokens(self):
            contenido = self.text1.get("1.0", "end-1c")
            analizador = AnalizadorLexico()
            tokens, errores = analizador.analizar(contenido)
            if tokens:
                self.text2.delete("1.0", "end")
                table = PrettyTable(["Tipo", "Token", "Línea", "Columna"])
                for token in tokens:
                    table.add_row([token.tipo, token.contenido, token.linea, token.columna])
                self.text2.insert("end", table)
            else:
                messagebox.showinfo("Tokens", "No se encontraron tokens.")

    def ver_errores(self):
        contenido = self.text1.get("1.0", "end-1c")
        analizador_lexico = AnalizadorLexico()
        tokens, errores_lexicos = analizador_lexico.analizar(contenido)
        if errores_lexicos:
            self.text2.delete("1.0", "end")
            table = PrettyTable(["Tipo de Error", "Línea", "Columna", "Caracter", "Token Esperado", "Descripción"])
            for error in errores_lexicos:
                table.add_row([error["tipo"], error["linea"], error["columna"], error["caracter"], error.get("token_esperado", ""), error.get("descripcion", "")])
            self.text2.insert("end", str(table))
        else:
            analizador_sintactico = AnalizadorSintactico(tokens)
            errores_sintacticos = analizador_sintactico.analizar(tokens)
            if errores_sintacticos:
                self.text2.delete("1.0", "end")
                table = PrettyTable(["Tipo de Error", "Mensaje", "Token"])
                for error in errores_sintacticos:
                    table.add_row([error["tipo"], error["mensaje"], error["token"]["valor"]])
                self.text2.insert("end", str(table))
            else:
                messagebox.showinfo("Errores", "No se encontraron errores.")


    def salir(self):
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    ventana_principal = VentanaPrincipal(root)
    root.mainloop()