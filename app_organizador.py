print("--- 1. INICIANDO SCRIPT COMPLETO ---")

try:
    import os
    import shutil
    import tkinter as tk
    from tkinter import messagebox
    import json
    import subprocess
except Exception as e:
    print(f"!!! ERROR IMPORTANDO LIBRERÍAS: {e}")
    input("Enter para salir...")
    exit()

# --- CONFIGURACIÓN ---
BASE_USER = os.path.expanduser('~')
CARPETA_ORIGEN = os.path.join(BASE_USER, 'Downloads')
NOMBRE_CONFIG = "reglas_revit.json"
RUTA_CONFIG = os.path.join(os.getcwd(), NOMBRE_CONFIG)

DEFAULT_REGLAS = {
    "Puertas": ["puerta", "door", "portón", "entrada", "gate"],
    "Ventanas": ["ventana", "window", "glass", "vidrio", "climalit"],
    "Mobiliario": ["mesa", "silla", "sofa", "table", "chair", "cama", "bed", "escritorio"],
    "Vegetacion": ["arbol", "tree", "planta", "plant", "rpc"],
    "Coches": ["coche", "car", "vehiculo", "parking"],
    "Iluminacion": ["luz", "foco", "lampara", "light", "lamp", "iluminacion", "led"],
    "Sanitarios": ["wc", "inodoro", "lavabo", "sink", "bath", "ducha", "bañera", "grifo"],
    "Proyectos_RVT": [".rvt"]
}

# --- FUNCIONES ---
def cargar_o_crear_config():
    if not os.path.exists(RUTA_CONFIG):
        try:
            with open(RUTA_CONFIG, 'w', encoding='utf-8') as f:
                json.dump(DEFAULT_REGLAS, f, indent=4, ensure_ascii=False)
            return DEFAULT_REGLAS
        except:
            return DEFAULT_REGLAS
    else:
        try:
            with open(RUTA_CONFIG, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return DEFAULT_REGLAS

def abrir_configuracion():
    cargar_o_crear_config()
    try:
        os.startfile(RUTA_CONFIG)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def ejecutar_limpieza():
    print(">>> Iniciando limpieza...")
    reglas_activas = cargar_o_crear_config()

    # Detección de escritorio
    posibles_rutas = [
        os.path.join(BASE_USER, 'OneDrive', 'Escritorio'),
        os.path.join(BASE_USER, 'OneDrive', 'Desktop'),
        os.path.join(BASE_USER, 'Escritorio'),
        os.path.join(BASE_USER, 'Desktop')
    ]
    ruta_escritorio = os.path.join(BASE_USER, 'Desktop')
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            ruta_escritorio = ruta
            break
            
    CARPETA_DESTINO_BASE = os.path.join(ruta_escritorio, 'RevitOrdenado')

    if not os.path.exists(CARPETA_ORIGEN):
        messagebox.showerror("Error", "No encuentro la carpeta Descargas")
        return

    btn_accion.config(text="Procesando...", state="disabled")
    ventana.update()

    archivos_movidos = 0
    errores = 0

    for archivo in os.listdir(CARPETA_ORIGEN):
        ruta_origen = os.path.join(CARPETA_ORIGEN, archivo)
        
        if os.path.isdir(ruta_origen): continue

        nombre_lower = archivo.lower()
        if not (nombre_lower.endswith('.rfa') or nombre_lower.endswith('.rvt')): continue

        movido = False
        
        # 1. Intentar mover por Reglas (JSON)
        for carpeta_cat, keywords in reglas_activas.items():
            if not isinstance(keywords, list): continue
            if any(k.lower() in nombre_lower for k in keywords):
                ruta_destino_final = os.path.join(CARPETA_DESTINO_BASE, carpeta_cat)
                if not os.path.exists(ruta_destino_final): os.makedirs(ruta_destino_final)
                try:
                    shutil.move(ruta_origen, os.path.join(ruta_destino_final, archivo))
                    archivos_movidos += 1
                    movido = True
                    print(f"✅ Clasificado: {archivo} -> {carpeta_cat}")
                    break 
                except Exception as e:
                    errores += 1
                    print(f"❌ Error: {e}")

        # 2. SI NO SE MOVIÓ POR REGLAS -> MOVER A "OTROS" (Aquí estaba el faltante)
        if not movido:
             ruta_otros = os.path.join(CARPETA_DESTINO_BASE, "Otros_Sin_Clasificar")
             if not os.path.exists(ruta_otros):
                 os.makedirs(ruta_otros)
             try:
                 shutil.move(ruta_origen, os.path.join(ruta_otros, archivo))
                 archivos_movidos += 1
                 print(f"📦 Sin regla: {archivo} -> Otros_Sin_Clasificar")
             except Exception as e:
                 errores += 1
                 print(f"❌ Error moviendo a Otros: {e}")

    btn_accion.config(text="ORDENAR AHORA", state="normal")
    
    mensaje = f"✅ Proceso terminado.\nMovidos: {archivos_movidos}"
    if errores > 0: mensaje += f"\n⚠️ Errores: {errores}"
    
    messagebox.showinfo("Reporte", mensaje)
    print(">>> Fin.")

# --- INTERFAZ ---
ventana = tk.Tk()
ventana.title("Organizador Revit Pro")
ventana.geometry("450x350")
ventana.config(bg="#f0f0f0")

try:
    ventana.iconbitmap("icono.ico")
except:
    pass 

lbl_titulo = tk.Label(ventana, text="Organizador de Librerías", font=("Segoe UI", 16, "bold"), bg="#f0f0f0")
lbl_titulo.pack(pady=15)

lbl_ruta = tk.Label(ventana, text=f"Destino: Escritorio/RevitOrdenado", font=("Consolas", 9), fg="blue", bg="#f0f0f0")
lbl_ruta.pack(pady=5)

btn_accion = tk.Button(ventana, text="ORDENAR AHORA", font=("Segoe UI", 11, "bold"), 
                       bg="#0078D7", fg="white", height=2, width=25,
                       command=ejecutar_limpieza)
btn_accion.pack(pady=15)

tk.Frame(ventana, height=1, bg="#ccc", width=300).pack(pady=10)

btn_config = tk.Button(ventana, text="⚙️ Editar Reglas", font=("Segoe UI", 9), 
                       bg="#e1e1e1", fg="black", command=abrir_configuracion)
btn_config.pack(pady=5)

lbl_footer = tk.Label(ventana, text="v3.1 - Con carpeta 'Otros'", font=("Segoe UI", 8), bg="#f0f0f0", fg="#999")
lbl_footer.pack(side="bottom", pady=10)

ventana.mainloop()