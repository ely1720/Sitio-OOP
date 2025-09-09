import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
from fpdf import FPDF
from datetime import datetime
from datetime import date
import re


DB_FILE = "usuarios.db"

# ------------------- Base de datos -------------------
def crear_tabla():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            segundo_nombre TEXT,
            apellido_paterno TEXT NOT NULL,
            apellido_materno TEXT NOT NULL,
            correo TEXT NOT NULL,
            carrera TEXT,
            telefono TEXT,
            edad TEXT,
            sexo TEXT,
            anio_ingreso TEXT,
            estado TEXT,
            municipio TEXT,
            estado_civil TEXT,
            matricula TEXT
        )
    """)
    conn.commit()
    conn.close()

def insertar_usuario(datos):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuarios (
            nombre, segundo_nombre, apellido_paterno, apellido_materno,
            correo, carrera, telefono, edad, sexo, anio_ingreso,
            estado, municipio, estado_civil, matricula
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, datos)
    conn.commit()
    conn.close()

def contar_usuarios():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    total = cursor.fetchone()[0]
    conn.close()
    return total

# ------------------- Formulario 1 -------------------
class Formulario1:
    def __init__(self, root, siguiente):
        self.root = root
        self.siguiente = siguiente

        self.nombre_var = tk.StringVar()
        self.segnombre_var = tk.StringVar()
        self.apellido_paterno_var = tk.StringVar()
        self.apellido_materno_var = tk.StringVar()
        self.fnac_var = tk.StringVar()
        self.correo_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.estado_civil_var = tk.StringVar()
        self.sexo_var = tk.StringVar()

        # Regex para nombres
        self.re_nombre = re.compile(r"^[A-Za-zÀ-ÿ\s'-]+$")

        self.cargar_formulario()

    def _solo_digitos(self, texto):
        return texto.isdigit() or texto == ""

    # Capitalización automática
    def capitalizar(self, var):
        var.set(var.get().title())

    def cargar_formulario(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#E6FFDE")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        estilo_label = {'bg': "#E6FFDE", 'fg': 'black', 'font': ('Arial', 10, 'bold')}
        entry_width = 25

        tk.Label(frame, text="Datos Personales", font=('Arial',14,'bold'), bg="#E6FFDE").grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(frame, text="Nombre", **estilo_label).grid(row=1, column=0, sticky="w")
        e_nombre = tk.Entry(frame, textvariable=self.nombre_var, width=entry_width)
        e_nombre.grid(row=1,column=1)
        self.nombre_var.trace_add("write", lambda *args: self.capitalizar(self.nombre_var))

        tk.Label(frame, text="Segundo nombre", **estilo_label).grid(row=1, column=2, sticky="w")
        e_segnom = tk.Entry(frame, textvariable=self.segnombre_var, width=entry_width)
        e_segnom.grid(row=1,column=3)
        self.segnombre_var.trace_add("write", lambda *args: self.capitalizar(self.segnombre_var))

        tk.Label(frame, text="Apellido Paterno", **estilo_label).grid(row=2,column=0, sticky="w")
        e_paterno = tk.Entry(frame, textvariable=self.apellido_paterno_var, width=entry_width)
        e_paterno.grid(row=2,column=1)
        self.apellido_paterno_var.trace_add("write", lambda *args: self.capitalizar(self.apellido_paterno_var))

        tk.Label(frame, text="Apellido Materno", **estilo_label).grid(row=2,column=2, sticky="w")
        e_materno = tk.Entry(frame, textvariable=self.apellido_materno_var, width=entry_width)
        e_materno.grid(row=2,column=3)
        self.apellido_materno_var.trace_add("write", lambda *args: self.capitalizar(self.apellido_materno_var))

        tk.Label(frame, text="Fecha nacimiento", **estilo_label).grid(row=3,column=0, sticky="w")
        self.fnac_widget = DateEntry(frame, textvariable=self.fnac_var, date_pattern="dd-mm-yyyy", width=entry_width-3, state="readonly")#CAMBIARA
        self.fnac_widget.grid(row=3,column=1)

        tk.Label(frame, text="Sexo", **estilo_label).grid(row=3,column=2, sticky="w")
        ttk.Combobox(frame, textvariable=self.sexo_var, values=["Femenino","Masculino","Otro"], state="readonly", width=entry_width-2).grid(row=3,column=3)

        tk.Label(frame, text="Estado civil", **estilo_label).grid(row=4,column=0, sticky="w")
        ttk.Combobox(frame, textvariable=self.estado_civil_var, values=["Soltero(a)","Casado(a)","Divorciado(a)"], state="readonly", width=entry_width-2).grid(row=4,column=1)

        vcmd_num = (self.root.register(self._solo_digitos), "%P")
        tk.Label(frame, text="Teléfono", **estilo_label).grid(row=4,column=2, sticky="w")
        tk.Entry(frame, textvariable=self.telefono_var, width=entry_width, validate="key", validatecommand=vcmd_num).grid(row=4,column=3)

        tk.Label(frame, text="Correo electrónico (@gmail/@outlook)", **estilo_label).grid(row=5,column=0, sticky="w")
        tk.Entry(frame, textvariable=self.correo_var, width=entry_width*2+6).grid(row=5,column=1,columnspan=3)

        tk.Button(frame, text="Siguiente", bg="#3e9055", fg="black", width=20, command=self.siguiente_form).grid(row=6,column=0,columnspan=4,pady=20)

    def validar_personales(self):
        nombre = self.nombre_var.get().strip()
        paterno = self.apellido_paterno_var.get().strip()
        materno = self.apellido_materno_var.get().strip()
        segnombre = self.segnombre_var.get().strip()

        if not nombre or not self.re_nombre.match(nombre):
            messagebox.showerror("Error", "Nombre inválido")
            return False
        if segnombre and not self.re_nombre.match(segnombre):
            messagebox.showerror("Error", "Segundo nombre inválido")
            return False
        if not paterno or not self.re_nombre.match(paterno):
            messagebox.showerror("Error", "Apellido paterno inválido")
            return False
        if not materno or not self.re_nombre.match(materno):
            messagebox.showerror("Error", "Apellido materno inválido")
            return False

        # Fecha nacimiento
        try:
            fnac = self.fnac_widget.get_date()
        except:
            messagebox.showerror("Error", "Fecha de nacimiento inválida")
            return False
        hoy = date.today()
        edad = hoy.year - fnac.year - ((hoy.month, hoy.day) < (fnac.month, fnac.day))
        if fnac > hoy or edad < 17 or edad > 100:
            messagebox.showerror("Error", "Edad fuera de rango (17-100)")
            return False

        # Teléfono
        tel = self.telefono_var.get()
        if not (tel.isdigit() and len(tel)==10 and len(set(tel))>1):
            messagebox.showerror("Error", "Teléfono inválido, 10 dígitos")
            return False

        # Correo
        correo = self.correo_var.get().strip()
        if not correo or not re.match(r"^[\w\.-]+@(?:gmail|outlook)\.com$", correo, flags=re.IGNORECASE):
            messagebox.showerror("Error", "Correo inválido. Debe terminar en @gmail.com o @outlook.com")
            return False

        # Sexo y estado civil
        if not self.sexo_var.get():
            messagebox.showerror("Error", "Seleccione sexo")
            return False
        if not self.estado_civil_var.get():
            messagebox.showerror("Error", "Seleccione estado civil")
            return False

        return True

    def siguiente_form(self):
        if self.validar_personales():
            self.root.withdraw()
            self.siguiente.deiconify()



# ------------------- Formulario 2 -------------------
class Formulario2:
    def __init__(self, root, anterior, siguiente):
        self.root = root
        self.anterior = anterior
        self.siguiente = siguiente

        self.nacionalidad_var = tk.StringVar()
        self.codigopostal_var = tk.StringVar()
        self.estado_var = tk.StringVar()
        self.municipio_var = tk.StringVar()
        self.localidad_var = tk.StringVar()

        self.municipios_por_estado = {
            "Guerrero": ["Huamuxtitlan", "Xochilhuehuetlan", "Tlapa de Comonfort", "Alpoyeca", "Olinala"],
            "Puebla": ["Tulcingo del valle", "Puebla de Zaragoza"],
            "Oaxaca": ["San juan Ozolotepec", "Salina Cruz", "San Andres Lagunas"]
        }

        self.cargar_formulario()

    # ------------------- Funciones auxiliares -------------------
    def capitalizar(self, var):
        var.set(var.get().title())

    def _solo_digitos(self, texto):
        return texto.isdigit() or texto == ""

    # ------------------- Formulario -------------------
    def cargar_formulario(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#E6FFDE")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        estilo_label = {'bg': "#E6FFDE", 'fg':'black', 'font':('Segoe UI',10,'bold')}
        entry_width = 25

        tk.Label(frame, text="Datos de ubicación", font=('Segoe UI',16,'bold'), bg="#E6FFDE").grid(row=0,column=0,columnspan=4,pady=20)
        tk.Label(frame, text="Nacionalidad", **estilo_label).grid(row=1,column=1,sticky="w")
        e_nac = tk.Entry(frame, textvariable=self.nacionalidad_var, width=entry_width)
        e_nac.grid(row=1,column=2)
        self.nacionalidad_var.trace_add("write", lambda *args: self.capitalizar(self.nacionalidad_var))

        tk.Label(frame, text="Código Postal", **estilo_label).grid(row=2,column=1,sticky="w")
        e_cp = tk.Entry(frame, textvariable=self.codigopostal_var, width=entry_width)
        e_cp.grid(row=2,column=2)
        vcmd_cp = (self.root.register(self._solo_digitos), "%P")
        e_cp.config(validate="key", validatecommand=vcmd_cp)

        tk.Label(frame, text="Estado", **estilo_label).grid(row=3,column=1,sticky="w")
        self.estado_combo = ttk.Combobox(frame, textvariable=self.estado_var, values=list(self.municipios_por_estado.keys()), state="readonly", width=entry_width-2)
        self.estado_combo.grid(row=3,column=2)
        self.estado_combo.bind("<<ComboboxSelected>>", self.actualizar_municipios)

        tk.Label(frame, text="Municipio", **estilo_label).grid(row=4,column=1,sticky="w")
        self.municipio_combo = ttk.Combobox(frame, textvariable=self.municipio_var, state="readonly", width=entry_width-2)
        self.municipio_combo.grid(row=4,column=2)

        tk.Label(frame, text="Localidad", **estilo_label).grid(row=5,column=1,sticky="w")
        e_loc = tk.Entry(frame, textvariable=self.localidad_var, width=entry_width)
        e_loc.grid(row=5,column=2)
        self.localidad_var.trace_add("write", lambda *args: self.capitalizar(self.localidad_var))

        tk.Button(frame, text="Atrás", width=15, bg="#3e9055", fg="black", command=self.volver).grid(row=6,column=0,columnspan=2,pady=10)
        tk.Button(frame, text="Siguiente", width=15, bg="#3e9055", fg="black", command=self.siguiente_form).grid(row=6,column=2,columnspan=2,pady=10)

    # ------------------- Métodos funcionales -------------------
    def actualizar_municipios(self, event):
        estado = self.estado_var.get()
        self.municipio_combo['values'] = self.municipios_por_estado.get(estado, [])
        self.municipio_combo.set("")

    def validar_ubicacion(self):
        cp = self.codigopostal_var.get().strip()
        if cp and (not cp.isdigit() or len(cp) != 5):
            messagebox.showerror("Error","Código Postal inválido (si se proporciona debe tener 5 dígitos)")
            return False

        nac = self.nacionalidad_var.get().strip()
        if not nac:
            messagebox.showerror("Error","Nacionalidad obligatoria")
            return False

        if nac.lower() == "mexicana":
            if not self.estado_var.get():
                messagebox.showerror("Error","Seleccione estado")
                return False
            if not self.municipio_var.get():
                messagebox.showerror("Error","Seleccione municipio")
                return False
            if not self.localidad_var.get().strip():
                messagebox.showerror("Error","Localidad obligatoria")
                return False
        else:
            if not self.localidad_var.get().strip():
                messagebox.showerror("Error","Localidad obligatoria")
                return False

        return True

    def siguiente_form(self):
        if self.validar_ubicacion():
            self.root.withdraw()
            self.siguiente.deiconify()

    def volver(self):
        self.root.withdraw()
        self.anterior.deiconify()


# ------------------- Formulario 3 -------------------
class Formulario3:
    def __init__(self, root, anterior):
        self.root = root
        self.anterior = anterior
        self.escuela_var = tk.StringVar()
        self.carrera_var = tk.StringVar()
        self.anio_var = tk.StringVar()
        self.cargar_formulario()

    def cargar_formulario(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#E6FFDE")
        frame.pack(padx=30,pady=30)

        tk.Label(frame, text="Universidad Tecnológica de Izúcar de Matamoros", bg="#E6FFDE", fg='black', font=('Times New Roman',15,'bold')).grid(row=0,column=0,columnspan=4,pady=15)
        tk.Label(frame, text="Campus", bg="#E6FFDE", fg='black').grid(row=1,column=1, sticky="w", padx=5, pady=5)
        ttk.Combobox(frame, textvariable=self.escuela_var, values=["Tulcingo de Valle","Izúcar de Matamoros"]).grid(row=1,column=2)
        tk.Label(frame, text="Carrera", bg="#E6FFDE", fg='black').grid(row=2,column=1, sticky="w", padx=5, pady=5)
        ttk.Combobox(frame, textvariable=self.carrera_var, values=["TI","CONTA","EDUCACION"]).grid(row=2,column=2)
        tk.Label(frame, text="Año de ingreso", bg="#E6FFDE", fg='black').grid(row=3,column=1, sticky="w", padx=5, pady=5)
        tk.Entry(frame, textvariable=self.anio_var).grid(row=3,column=2)

        tk.Button(frame, text="Volver", width=15, bg="#3e9055", fg="black", command=self.volver).grid(row=4,column=1,pady=10)
        tk.Button(frame, text="Finalizar", width=15, bg="#3e9055", fg="black", command=self.mostrar_resumen).grid(row=4,column=2,pady=10)

    def volver(self):
        self.root.withdraw()
        self.anterior.deiconify()

    def mostrar_resumen(self):
        # Validar primero
        anio = self.anio_var.get().strip()
        if not anio.isdigit() or int(anio) < 2000 or int(anio) > datetime.now().year:
            messagebox.showerror("Error","Año de ingreso inválido")
            return

        if not self.carrera_var.get().strip():
            messagebox.showerror("Error","Seleccione carrera")
            return

        # Solo si pasa la validación se oculta la ventana y se abre el resumen
        self.root.withdraw()
        Resumen(tk.Toplevel(), f1, f2, self)




    def generar_matricula(self):
        anio = self.anio_var.get().strip()[-2:]
        if not anio.isdigit():
            anio = datetime.now().strftime("%y")
        fijo = "34"
        carrera_map = {"TI": "TI", "CONTA": "CO", "EDUCACION": "ED"}
        carrera_abrev = carrera_map.get(self.carrera_var.get().upper(), "XX")
        consecutivo = contar_usuarios() + 1
        consecutivo_str = str(consecutivo).zfill(3)
        return f"{anio}{fijo}{carrera_abrev}{consecutivo_str}"


# ------------------- Ventana de Búsqueda y Resumen -------------------
class VentanaBuscar:
    def __init__(self, root):
        self.root = root
        self.root.title("Buscar alumno")
        self.root.geometry("700x400")
        self.root.minsize(650,350)

        # responsiva
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        frame = tk.Frame(self.root, bg="#E6FFDE")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(frame, text="Buscar alumno", font=("Arial",14,"bold"), bg="#E6FFDE").pack(pady=10)

        self.entry_buscar = tk.Entry(frame, width=40)
        self.entry_buscar.pack(pady=5, fill="x", expand=True)

        botones = tk.Frame(frame, bg="#E6FFDE")
        botones.pack(pady=5, fill="x", expand=True)

        tk.Button(botones, text="Buscar por nombre", command=self.buscar_nombre, bg="#3e9055", fg="white").grid(row=0, column=0, padx=10, sticky="ew")
        tk.Button(botones, text="Buscar por matrícula", command=self.buscar_matricula, bg="#3e9055", fg="white").grid(row=0, column=1, padx=10, sticky="ew")
        tk.Button(botones, text="Regresar", command=self.regresar, bg="#3e9055", fg="white").grid(row=0, column=2, padx=10, sticky="ew")

        # Tabla de resultados
        self.tree = ttk.Treeview(frame, columns=("matricula","nombre","apellidos","correo","carrera"), show="headings")
        self.tree.pack(pady=10, fill="both", expand=True)

        self.tree.heading("matricula", text="Matrícula")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("apellidos", text="Apellidos")
        self.tree.heading("correo", text="Correo")
        self.tree.heading("carrera", text="Carrera")

        # Doble clic en fila
        self.tree.bind("<Double-1>", self.abrir_resumen)

    def buscar_nombre(self):
        nombre = self.entry_buscar.get().strip()
        if not nombre:
            messagebox.showwarning("Aviso", "Escribe un nombre para buscar")
            return
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT matricula, nombre, apellido_paterno || ' ' || apellido_materno, correo, carrera
            FROM usuarios WHERE nombre LIKE ?
        """, ('%'+nombre+'%',))
        resultados = cursor.fetchall()
        conn.close()
        self.mostrar_resultados(resultados)

    def buscar_matricula(self):
        matricula = self.entry_buscar.get().strip()
        if not matricula:
            messagebox.showwarning("Aviso", "Escribe una matrícula para buscar")
            return
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT matricula, nombre, apellido_paterno || ' ' || apellido_materno, correo, carrera
            FROM usuarios WHERE matricula=?
        """, (matricula,))
        resultados = cursor.fetchall()
        conn.close()
        self.mostrar_resultados(resultados)

    def mostrar_resultados(self, resultados):
        # Limpiar tabla
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Insertar resultados
        for fila in resultados:
            self.tree.insert("", tk.END, values=fila)
        if not resultados:
            messagebox.showinfo("Sin resultados", "No se encontraron coincidencias")

    def abrir_resumen(self, event):
        seleccion = self.tree.focus()
        if not seleccion:
            return
        datos = self.tree.item(seleccion, "values")
        ResumenBuscado(tk.Toplevel(), datos)

    def regresar(self):
        self.root.destroy()
        ventanaInicial.deiconify()


class ResumenBuscado:
    def __init__(self, root, datos):
        self.root = root
        self.root.title("Datos del alumno")
        self.root.geometry("600x400")
        self.root.minsize(550,350)
        self.datos = datos

        frame = tk.Frame(self.root, bg="#E6FFDE")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(frame, text="Datos del alumno", font=("Arial",16,"bold"), bg="#E6FFDE").pack(pady=10)

        resumen_frame = tk.Frame(frame, bg="white", relief="solid", bd=1)
        resumen_frame.pack(fill="both", expand=True, padx=10, pady=10)

        datos_texto = f"""
Matrícula: {datos[0]}
Nombre: {datos[1]}
Apellidos: {datos[2]}
Correo: {datos[3]}
Carrera: {datos[4]}
        """
        tk.Label(resumen_frame, text=datos_texto, justify="left", bg="white", anchor="w").pack(padx=10, pady=10, fill="both")

        botones = tk.Frame(frame, bg="#F5F5F5")
        botones.pack(pady=10)

        tk.Button(botones, text="Descargar PDF", bg="green", fg="white", width=15, command=self.descargar_pdf).grid(row=0, column=0, padx=10)
        tk.Button(botones, text="Cerrar", bg="orange", fg="black", width=15, command=self.root.destroy).grid(row=0, column=1, padx=10)

    def descargar_pdf(self):
        from tkinter import filedialog
        from fpdf import FPDF
        from tkinter import messagebox

        # Pedir al usuario la ubicación y nombre del archivo
        nombre_archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            initialfile=f"Resumen_{self.datos[0]}"
        )
        if not nombre_archivo:
            return  # Si el usuario cancela, salir

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, f"Resumen del alumno:\n\nMatrícula: {self.datos[0]}\nNombre: {self.datos[1]}\nApellidos: {self.datos[2]}\nCorreo: {self.datos[3]}\nCarrera: {self.datos[4]}")
        pdf.output(nombre_archivo)
        messagebox.showinfo("PDF guardado", f"Archivo PDF guardado como: {nombre_archivo}")



# ------------------- Clase Resumen -------------------
class Resumen:
    def __init__(self, root, f1_ref, f2_ref, f3_ref):
        self.root = root
        self.f1 = f1_ref
        self.f2 = f2_ref
        self.f3 = f3_ref
        self.root.title("Resumen de datos")
        self.root.geometry("600x500")

        frame = tk.Frame(self.root, bg="#E6FFDE")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(frame, text="Resumen de datos", font=("Arial",16,"bold"), bg="#E6FFDE").pack(pady=10)

        resumen_frame = tk.Frame(frame, bg="white", relief="solid", bd=1)
        resumen_frame.pack(fill="both", expand=True, padx=10, pady=10)

        datos_texto = f"""
Nombre: {self.f1.nombre_var.get()} {self.f1.segnombre_var.get()} {self.f1.apellido_paterno_var.get()} {self.f1.apellido_materno_var.get()}
Fecha de nacimiento: {self.f1.fnac_var.get()}
Sexo: {self.f1.sexo_var.get()}
Estado civil: {self.f1.estado_civil_var.get()}
Teléfono: {self.f1.telefono_var.get()}
Correo: {self.f1.correo_var.get()}

Nacionalidad: {self.f2.nacionalidad_var.get()}
Código Postal: {self.f2.codigopostal_var.get()}
Estado: {self.f2.estado_var.get()}
Municipio: {self.f2.municipio_var.get()}
Localidad: {self.f2.localidad_var.get()}

Campus: {self.f3.escuela_var.get()}
Carrera: {self.f3.carrera_var.get()}
Año de ingreso: {self.f3.anio_var.get()}
        """

        tk.Label(resumen_frame, text=datos_texto, justify="left", bg="white", anchor="w").pack(padx=10, pady=10, fill="both")

        botones = tk.Frame(frame, bg="#F5F5F5")
        botones.pack(pady=10)

        tk.Button(botones, text="Confirmar", bg="green", fg="white", width=15, command=self.confirmar).grid(row=0, column=0, padx=10)
        tk.Button(botones, text="Editar", bg="orange", fg="black", width=15, command=self.editar).grid(row=0, column=1, padx=10)

    def confirmar(self):
        matricula = self.f3.generar_matricula()
        datos = (
            self.f1.nombre_var.get(),
            self.f1.segnombre_var.get(),
            self.f1.apellido_paterno_var.get(),
            self.f1.apellido_materno_var.get(),
            self.f1.correo_var.get(),
            self.f3.carrera_var.get(),
            self.f1.telefono_var.get(),
            self.f1.fnac_var.get(),
            self.f1.sexo_var.get(),
            self.f3.anio_var.get(),
            self.f2.estado_var.get(),
            self.f2.municipio_var.get(),
            self.f1.estado_civil_var.get(),
            matricula
        )
        insertar_usuario(datos)
        messagebox.showinfo("Éxito", f"Datos guardados correctamente.\nMatrícula generada: {matricula}")
        self.root.destroy()
        ventanaInicial.deiconify()

    def editar(self):
        self.root.destroy()
        self.f3.root.deiconify()


# ------------------- Ejecutar la aplicación -------------------
crear_tabla()

ventanaInicial = tk.Tk()
ventanaInicial.geometry("400x200")
ventanaInicial.title("Gestión de alumnos por matrícula")
ventanaInicial.configure(bg="#b3faa1")
ventanaInicial.grid_columnconfigure(0, weight=1)
ventanaInicial.grid_columnconfigure(1, weight=1)


tk.Label(ventanaInicial, text="Gestión de alumnos por matrícula", fg="#000000", bg="#79DA4F", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")
tk.Label(ventanaInicial, text="¿Qué desea hacer?", fg="#000000", bg="#A3E28F", font=("Arial", 10)).grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

# Crear formularios
form1 = tk.Toplevel(ventanaInicial)
form1.geometry("800x400")
form1.title("Formulario 1")
form1.withdraw()

form2 = tk.Toplevel(ventanaInicial)
form2.geometry("400x400")
form2.title("Formulario 2")
form2.withdraw()

form3 = tk.Toplevel(ventanaInicial)
form3.geometry("700x300")
form3.title("Formulario 3")
form3.withdraw()

f1 = Formulario1(form1, siguiente=form2)
f2 = Formulario2(form2, anterior=form1, siguiente=form3)
f3 = Formulario3(form3, anterior=form2)

# Botones en ventana inicial
bAgregar = tk.Button(ventanaInicial, text="Agregar", width=15, 
                     command=lambda: [ventanaInicial.withdraw(), form1.deiconify()])
bAgregar.grid(row=2,column=0,padx=10,pady=20)

# Aquí asignamos la acción de buscar
bBuscar = tk.Button(ventanaInicial, text="Buscar", width=15, 
                    command=lambda: [ventanaInicial.withdraw(), VentanaBuscar(tk.Toplevel())])
bBuscar.grid(row=2,column=1,padx=10,pady=20)


ventanaInicial.mainloop()

